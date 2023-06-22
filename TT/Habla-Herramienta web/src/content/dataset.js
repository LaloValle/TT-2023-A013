const connectionStatus = {
    es: [
        {
            status: 'Desconectado',
            background: 'bg-gray-400'
        },
        {
            status: 'Pendiente',
            background: 'bg-highlight'
        },
        {
            status: 'Conectado',
            background: 'bg-actions'
        },
        {
            status: 'Finalizado',
            background: 'bg-gray-400'
        },
    ],
    en: [
        {
            status: 'Disconnected',
            background: 'bg-gray-300'
        },
        {
            status: 'Pending',
            background: 'bg-highlight'
        },
        {
            status: 'Connected',
            background: 'bg-actions'
        },
        {
            status: 'Finished',
            background: 'bg-gray-400'
        },
    ]
}

const dataset = {
    es: {
        disconnected: {
            title: 'API de Conjunto de datos',
            subtitle: 'Configurar y monitorear el proceso de creación de un nuevo conjunto de datos',
            actions: {
                connect: 'Conectar',
                create: 'Crear nuevo'
            },
            name: {
                placeholder: 'Mediciones_Luis',
                description: 'Nombre del nuevo conjunto de datos y archivos csv para cada eje'
            }
        },
        refused: {
            error: 'Falló la conexión',
            message: 'Ocurrió un problema con la conexión con la API de datos',
            retry: 'Reintentar'
        },
        finished : {
            title: '¡Gracias por tu colaboración!',
            subtitle : 'La recopilación de los gestos ha terminado',
            new : 'Iniciar nuevo conjunto'
        }
    },
    en: {
        disconnected: {
            title: 'Dataset API',
            subtitle: 'Configure and track the new dataset creation process',
            actions: {
                connect: 'Connect',
                create: 'Create new'
            },
            name: {
                placeholder: 'Measurements_Alondra',
                description: 'Name asigned to the new dataset and that\'ll be used to named each axis csv file generated'
            }
        },
        refused: {
            error: 'Connection failed !',
            message: 'An error happened while connecting with the Dataset API',
            retry: 'Retry'
        },
        finished : {
            title: '¡Thank you for your help!',
            subtitle : 'The gesture\'s compilation has ended',
            new : 'Start new dataset'
        }
    }
}

export { dataset, connectionStatus }