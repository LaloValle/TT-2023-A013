import json
import time
import random
import joblib
import resampy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import svm
from functools import reduce

from LLibraries.DTW import DTW
from LLibraries.SAX import to_SAX_dataset, SAX
from LLibraries.DTWWindowOptimizer import minimum_warping_window
from LLibraries.DTWFeatures import compute_3_axis_representatives, SAX_DTWF_SVC, DTW_features_dataset
from LLibraries.Tools import stratified_sampling, merge_measurements, merge_measurements_list, save_representatives, accuracy, recover_presentatives

#----------------------
# Funciones auxiliares
#----------------------
def padding_NaNs(path:str='', measurements:list=[], min_max:bool=False, new_path:str='', returns_path:bool=False):
    """Dada la ruta de un archivo csv con series de tiempo de longitud variable
    como elementos, se rellenan los espacios en blanco con 'Nan's de manera que
    todos los elementos se forman del mismo número de mediciones que la serie de
    tiempo mayor con más mediciones.
    Se guarda el resultado como un archivo tsv en la misma ruta y se añade el
    postfijo '_NaNs'

    Parameters
    ==========
    ruta : str
        Ruta del archivo csv
    min_max : bool(opcional)
        Retorna el número de mediciones para la serie de tiempo más corta y más larga

    Return
    ======
    extremos_mediciones : tuple
        El mínimo y máximo de las mediciones de las series de tiempo en el archivo
    """
    if path:
        with open(path) as x:
            measurements = list(map(lambda x: x.split(','), x.readlines()))
        for i in range(len(measurements)): measurements[i][-1] = measurements[i][-1].replace('\n','') #Elimina el salto de línea en el último elemento

    # Obtiene la longitud de cada una de las medidas
    lengths = reduce(
        lambda acc,x: acc + [len(x)],
        measurements,
        []
    )
    maximum_length = max(lengths) #Identifica la longitud máxima entre todas las medidas

    # Agrega los Nans faltantes de manera que todas las medidas tengan el mismo número de elementos según la medición con mayor número
    measurements_Nans = reduce(
        lambda acc,x: acc + [x + (['NaN']*(maximum_length-len(x)))],
        measurements,
        []
    )
    
    try:
        if path[-4:] == '.csv': path = path[:-4] # Se recorta la extensión .csv
        if new_path : path = new_path + path[path.rfind('/'):] # Se añade el nombre del archivo a la ruta nueva
        path += '_NaNs.tsv'
        # Cuando no se agrega una ruta se proveé un arreglo desde memoria
        if not path: path = new_path
        # Se convierte a un DataFrame para ser grabado en un archivo .tsv
        pd.DataFrame(measurements_Nans).to_csv(path, sep='\t', header=False, index=False)
        print(f'<--- File succesfully generated "{path}_NaNs.tsv" --->\n')

        returns = []
        if min_max: returns.append({'minimo' : min(lengths), 'maximo' : maximum_length})
        if returns_path: returns.append(path)
        return returns
    except:
        print(f'ERROR >> While saving in {path}\n')

def recover_measurements_array(path):
    """Obtiene las mediciones de un conjunto de datos que cumple con ciertas restricciones:
        1. El archivo deberá ser un .tsv
        2. Todas las filas deben de tener el mismo número de elementos rellenando con 'NaN' los elementos restantes para completar con la medición más grande
    
    Parameters
    ----------
    ruta : str
        Ruta donde se localiza el conjunto de datos

    Returns
    -------
    mediciones : numpy.array
        Arreglo con las mediciones
    """
    print('Recovering path >>',path)
    measurements = []
    with open(path) as file:
        measurements = list(map(lambda row: list(map(lambda element: np.NaN if 'NaN' in element else int(element), row.split('\t'))), file.readlines()))
    return np.array(measurements,dtype=np.float16)

def ready_dataset(paths:dict, number_words:int, alphabet_size:int, instances_per_class:float=np.inf, numeric_alphabet:bool=True, as_array:bool=False,resample_to:int=0):
    """Permite recuperar y preparar las mediciones a través de preprocesar los datos de manera que los conjuntos se encuentren en representación SAX.
    Variables como el número de palabras, tamaño del alfabeto utilizado y si el alfabeto es numérico se toman de los valores globales
    """
    gestures = dict()
    for axis,path in paths.items():
        aux_gestures = recover_measurements_array(path)
        stratified_gestures = stratified_sampling(aux_gestures, max_possible_instances=instances_per_class == np.inf,instances_per_class=instances_per_class, shuffle=False)

        # Agrega las mediciones faltantes como el valor promedio de 2 puntos en un índice
        if resample_to:
            def extend(series,final_measurements):
                index = random.sample(range(1,len(series)-1), final_measurements-(series.shape[0]-1))
                for i in index: series = np.insert(series,i+1,(series[i]+series[i+1])//2)
                return series
            # Se toma en cuenta que la primer medicion es la clase del gesto por lo que se resta de la longitud total
            stratified_gestures = list(map(lambda series: series if series.shape[0]-1 >= resample_to else extend(series,resample_to), stratified_gestures))
        
        gestures[axis] = to_SAX_dataset(stratified_gestures, number_words, alphabet_size, numeric_alphabet)
        if as_array: gestures[axis] = np.array(gestures[axis])
    return gestures



#---------------------------
# Clase del método SAX-DTW F
#---------------------------
class SAXDTWF():

    def __init__(self, config_file):
        """Is taken as a path the value of the 'config_file' parameter when is a string type, otherwise should be a dict structure with the configuration data.
        The file might include the next fields(the fields with * are optional or only taken into count when combined with flag fields added):
            
        Method parameters
        -----------------
            - number_words(int) : Number of measurements taken by gesture
            - alphabet_size(int) : Number of symbols in the SAX discretization
            - numeric_alphabet(bool) : Flag that indicates if the discretized alphabet is managed as numbers of alphabetic characters
            - window_size(int)* : DTW window's size
            - paths(dict)* : Each axis-taken time series files paths dictionary. The keys are the axis in lowercase and the value the path's string

        Existing model recovering
        -------------------------
            - representatives(str)* : Each class representatives time series dictionary
            - classifier(str)* : Persisted model file's path

        Execution parameters
        --------------------
            - window_epoch(int)* : Times the minimum window process is executed
            - window_iterations(int)* : Times the minimum window is computed by epoch
            - upper_bound(int)* : Upper range limit used for computing the minimum window size
            - lower_bound(int)* : Lower range limit used for computing the minimum window size
            - measurements_base_path(str)* : New path used to save the tsv files after the csv-recovered measurements have been filled up with NaNs
            - methods_path(str)* : Path where the class representatives and post-training model will be saved
            - training_instances(int)* : Number of instances used for the training for each class
            - complete_to(int)* : Total number of measurements each time series must have, if there are time series with less measurements they are resampled
        
        Flags
        -----
            - add_NaNs : When active, the paths field is required, the files are supposed to be csv and the measurements aren't equally large as the longest element. If added, the execution parameter 'measurements_base_path' is used to point the path where the tsv-generated files are loaded, otherwise each csv file path is used insted.
            - compute_window : Executes the method to compute the minimum window size. When included, the 'window_epoch' and 'upper_bound' parameters are applied, only when the values are positive and bigger than zero
            - train_model : The model gets trained, and when added the execution parameter 'training_instances' is taken into acount. As result the class representatives and the trained SVC model is returned.
            - test_model : After being trained, a small test is perfomed over the model. For this flag to work the 'training_instances' parameters must be provided and the value must be at least 1 unit smaller than the total number of instances for the class with less instances
            - predict : Using the trained model the labels of the recovered gestures are predicted
            - hide_prediction_table : Prevents the printing of the table comparing the real labels and the predicted label
            - save_gestures : Saves only the merged gestures
            - save_model : Saves only the representatives and the classifier
            - save_config : When active, a configuration file with the actions perfomed is generated and the gestures and method results are saved
            - already_in_sax : Indicates that the measurements of the dataset that are loaded from the path are are already in SAX representation

        """
        if type(config_file) == str:
            # Se recupera la configuración JSON
            with open(config_file) as file: self.config = json.load(file)
        elif type(config_file) == dict:
            self.config = config_file

    def autoconfigure(self):
        ## Parametros modelo obligatorios
        self.number_words = self.config.get('number_words')
        self.alphabet_size = self.config.get('alphabet_size')
        self.numeric_alphabet = self.config.get('numeric_alphabet')

        ## Parametros modelo opcionales
        self.window_size = self.config.get('window_size',0)
        self.paths = self.config.get('paths',{'x':'','y':'','z':'','gestures':''})

        ## Recuperación de banderas
        self.add_NaNs = self.config.get('add_NaNs',False)
        self.compute_window = self.config.get('compute_window',False)
        self.train_model = self.config.get('train_model',False)
        self.test_model = self.config.get('test_model',False)
        self.predict = self.config.get('predict',False)
        self.hide_prediction_table = self.config.get('hide_prediction_table',True)
        self.save_gestures = self.config.get('save_gestures',False)
        self.save_model = self.config.get('save_model',False)
        self.save_config = self.config.get('save_config',False)
        self.already_in_sax = self.config.get('already_in_sax',False)

        ## Parámetros de ejecución
        self.measurements_base_path = self.config.get('measurements_base_path','')
        self.upper_bound = self.config.get('upper_bound',0)
        self.lower_bound = self.config.get('lower_bound',0)
        self.window_epoch = self.config.get('window_epoch',0)
        self.window_iterations = self.config.get('window_iterations',0)
        self.training_instances = self.config.get('training_instances',0)
        self.methods_path = self.config.get('methods_path','')
        self.complete_to = self.config.get('complete_to',0)

        ## Resultados del método
        self.min_max = dict()
        self.representatives = self.config.get('representatives',dict())
        self.classifier = self.config.get('classifier','')
        if type(self.representatives) == str: self.representatives = recover_presentatives(self.representatives)
        if self.classifier: self.classifier = joblib.load(self.classifier)

        ##
        ## Ejecución con banderas activas
        ##
        # Rellenado de series con NaNs
        if self.add_NaNs:
            # Se ejecuta la función para cada ruta
            for axis,path in self.paths.items():
                self.min_max,self.paths[axis] = padding_NaNs(path,min_max=True,new_path=self.measurements_base_path, returns_path=True)

        # Se recuperan como arreglos las mediciones
        self.sax_gestures = []
        if ''.join(list(self.paths.values())):
            self.labels, self.instances_per_class = self.__ready_measurements(self.already_in_sax,self.complete_to)
            self.sax_gestures = self.sax_gestures.astype(int)
            print(f'\n<--- The total number of instances per class : {self.instances_per_class} --->')
        else:
            print('<!!! As no paths for the measurements where added the "compute_window", "train_model", "test_model" and "predict" flags are ignored if active !!!>')
            self.compute_window = False
            self.train_model = False
            self.test_model = False
            self.predict = False

        # Se calcula el valor mínimo de ventana
        if self.compute_window:
            self.minimum_window_size(self.upper_bound if self.upper_bound > 0 else 10, self.lower_bound if self.lower_bound > 0 else 2, self.window_epoch if self.window_epoch > 0 else 1)

        # Previo al entrenamiento se realiza la partición del conjunto de datos para el entrenamiento y prueba
        training_dataset = testing_dataset = []
        if self.test_model and self.train_model: training_dataset,testing_dataset = self.__split_training_testing_dataset()
        # Entrenamiento del modelo
        if self.train_model:
            # Si se va a evaluar el modelo se realiza la partición del conjunto de datos
            self.train_classifier(training_dataset)

        # Prueba o predicción con el modelo
        if self.test_model or self.predict:
            self.predict_label(testing_dataset,self.hide_prediction_table)

        # Guardado
        if self.save_gestures: self.__save_gestures()
        if self.save_model: self.__save_model()
        if self.save_config: self.__save_config()

    def __ready_measurements(self,already_in_sax:bool=False,resample_to:int=0):
        if 'gestures' in self.paths:
            self.sax_gestures = recover_measurements_array(self.paths['gestures']) if already_in_sax else ready_dataset(self.paths, number_words=self.number_words, alphabet_size=self.alphabet_size, numeric_alphabet=self.numeric_alphabet,as_array=True)['gestures']
        else:
            dict_gestures = ready_dataset(self.paths, number_words=self.number_words, alphabet_size=self.alphabet_size, numeric_alphabet=self.numeric_alphabet,resample_to=resample_to)
            sax_aux_x, sax_aux_y, sax_aux_z = [dict_gestures['x'], dict_gestures['y'], dict_gestures['z']]
            if len(self.representatives) == 0: 
                self.representatives = compute_3_axis_representatives(sax_aux_x, sax_aux_y, sax_aux_z)
            # Se combinan los conjuntos de datos de los 3 ejes
            self.sax_gestures = merge_measurements(sax_aux_x, sax_aux_y, sax_aux_z, has_label=True)
        # Total number of instances for class(all classes have the same as it had been stratified)
        labels = np.unique(self.sax_gestures[:,0])
        instances_per_class = len(self.sax_gestures[self.sax_gestures[:,0] == labels[0]])
        return [labels, instances_per_class]
    def __split_training_testing_dataset(self):
        # Esta forma de generar los índices solo funciona cuando:
        #   1. Las etiquetas asignadas de origen son numéricas
        #   2. La mediciones se encuentran ordenadas por sus etiquetas de clase
        training_index = np.array([np.random.choice(np.arange(start=(label-1)*self.instances_per_class, stop=label*self.instances_per_class), self.training_instances, replace=False) for label in self.labels]).flatten().astype(int)

        testing_gestures = self.sax_gestures[training_index]
        training_gestures = np.delete(self.sax_gestures, training_index, axis=0)

        np.random.shuffle(testing_gestures)
        np.random.shuffle(training_gestures)
        return [testing_gestures, training_gestures]
    def __save_gestures(self):
        current_path = '.'

        gestures_path = f'{self.methods_path if self.methods_path else current_path}/gestures.tsv'
        np.savetxt(gestures_path, self.sax_gestures, delimiter='\t', fmt='%1.i')
        self.paths['gestures'] = gestures_path
        print(f'<--- Gestures saved "{gestures_path}" --->')
        try:
            pass
        except:
            print('ERROR >> While saving merged gestures')
    def __save_model(self, only_representatives:bool=False, only_classifier:bool=False):
        current_path = '.'

        if type(self.representatives) != str and not only_classifier:
            # Se guardan los representantes en un archivo y se proveé la ruta
            representatives_paths = f'{self.methods_path if self.methods_path else current_path}/Representatives.csv'
            try:
                if save_representatives(self.representatives,representatives_paths):
                    self.config['representatives'] = representatives_paths
            except:
                print('ERROR >> While saving representatives')

        if type(self.classifier) != str and not only_representatives:
            # Se guarda el modelo entrenado y se proveé la ruta
            classifiers_path = f'{self.methods_path if self.methods_path else current_path}/Classifier.joblib'
            try:
                with open(classifiers_path,'wb') as classifier_file:
                    joblib.dump(self.classifier, classifier_file)
                self.config['classifier'] = classifiers_path
                print(f'<--- Classifier persisted "{classifiers_path}" --->')
            except:
                print('ERROR >> When persisting the model as a joblib file')
    def __save_config(self):
        # Parámetros del método
        config = {
            'number_words' : self.number_words,
            'alphabet_size' : self.alphabet_size,
            'numeric_alphabet' : self.numeric_alphabet
        }
        if self.window_size > 0: config['window_size'] = self.window_size
        if ''.join(self.paths.values()): config['paths'] = self.paths

        # Banderas
        if self.add_NaNs: config['add_NaNs'] = self.add_NaNs
        if self.compute_window: config['compute_window'] = self.compute_window
        if self.train_model: config['train_model'] = self.train_model
        # Parámetros de ejecución
        if self.measurements_base_path: config['measurements_base_path'] = self.measurements_base_path
        if self.upper_bound: config['upper_bound'] = self.upper_bound
        if self.window_epoch: config['window_epoch'] = self.window_epoch
        if self.training_instances: config['training_instances'] = self.training_instances
        if self.methods_path: config['methods_path'] = self.methods_path

        # Resultados
        current_path = '.'
        if len(self.sax_gestures) and 'paths' not in self.paths.keys():
            self.__save_gestures()
        if sum(self.min_max.values()): config['min_max'] = self.min_max
        if self.representatives:
            if type(self.representatives) == str: config['representatives'] = self.representatives
            else:
                self.__save_model(only_representatives=True)
                config['representatives'] = self.config['representatives']
        if self.classifier:
            if type(self.classifier) == str: config['classifier'] = self.classifier
            else:
                self.__save_model(only_classifier=True)
                config['classifier'] = self.config['classifier']
        config['save_gestures'] = True
        config['save_model'] = True
        config['save_config'] = True

        # Se almacena la configuración en un archivo
        files_path = f'{self.methods_path if self.methods_path else current_path }/Configuration.json'
        with open(files_path,'w') as config_file:
            json.dump(config, config_file, default=int)
        print(f"\n<--- Method's configuration saved '{files_path}' --->")

    def minimum_window_size(self, upper_bound:int=10, lower_bound:int=2, epochs:int=1):
        windows = dict()
        for epoch in range(epochs):
            print(f'<--- Minimum window size in epoch #{epoch+1} --->')
            new_window = minimum_warping_window(self.sax_gestures,SAX_DTWF_SVC, alphabet_size=self.alphabet_size,upper_bound_window=upper_bound, lower_bound_window=lower_bound, representatives=self.representatives,convert_int=True,verbose=True,number_iterations=self.window_iterations if self.window_iterations > 0 else 10)
            # Se contabiliza la veces de ocurrencia de un valor de ventana
            if new_window in windows.keys(): windows[new_window] += 1
            else: windows[new_window] = 1
        # Se escoge el tamaño de ventana mínimo con el mayor número de ocurrencias
        #   Se opera pensando en que múltiples tamaños de ventana pueden tener el mismo número máximo de ocurrencias
        maximum_ocurrences = max(windows.values())
        windows_candidates = dict(filter(lambda par: par[1] == maximum_ocurrences, windows.items()))
        self.window_size = min(windows_candidates.keys())

    def train_classifier(self,training_dataset=[]):
        vectors, labels, representatives_aux = DTW_features_dataset(training_dataset if len(training_dataset) else self.sax_gestures, window_size=self.window_size, representatives=self.representatives)
        if len(list(self.representatives.values())) == 0: self.representatives = representatives_aux

        self.classifier = svm.SVC(C=1, gamma='scale', degree=3, kernel='poly')
        print('\n<--- Training SVC model --->')
        starting_time = time.time()
        self.classifier.fit(vectors,labels)
        ending_time = time.time() - starting_time
        print('<--- Finalización de entrenamiento: {} seg --->\n'.format(ending_time))

    def predict_label(self,prediction_dataset=[],hide_prediction_table:bool=True,has_label:bool=True,verbose:bool=True):
        vectors, labels, _ = DTW_features_dataset(prediction_dataset if len(prediction_dataset) else self.sax_gestures, self.representatives, window_size=self.window_size,has_label=has_label)

        if verbose : print('<--- Starting prediction --->')
        starting_time = time.time()
        predictions = self.classifier.predict(vectors)
        tiempo_fin_p = time.time() - starting_time
        if verbose:
            acc = accuracy(labels,predictions)
            print('Accuracy >> ', acc)
            print('<--- Prediction ended, Accuracy:{:.2f}% , {:.2f} sec --->'.format(acc*100, tiempo_fin_p))

        if not hide_prediction_table:
            results = pd.DataFrame({
            'Real_labels' : labels,
            'Predictions' : predictions
            })
            results["Predicted"] = results.apply(lambda row: "Yes" if row["Real_labels"] == row["Predictions"] else "No", axis=1)
            print('\n',results)

        return predictions

    def ready_time_series(self, time_series:dict):
        len_time_series = len(time_series['x'])
        if len_time_series < self.number_words:
            print(f'<--- Resampling time series from {len_time_series} to {self.number_words}  measurements --->')
            index = random.sample([i for i in range(len_time_series-1)], self.number_words-len_time_series)
            for i in index:
                time_series['x'].insert(i+1, (time_series['x'][i]+time_series['x'][i+1])//2)
                time_series['y'].insert(i+1, (time_series['y'][i]+time_series['y'][i+1])//2)
                time_series['z'].insert(i+1, (time_series['z'][i]+time_series['z'][i+1])//2)
            print(f'--- Time series final length: {len(time_series["x"])} ---')

        return merge_measurements_list(
            [
                [SAX(series,number_words=self.number_words,alphabet_size=self.alphabet_size,numeric_alphabet=self.numeric_alphabet, array_style=True)] 
                for series in time_series.values()
            ]
        )