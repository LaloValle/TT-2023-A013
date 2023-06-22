// Static content of the page
//  - Titles
//  - Lists of links
//  - Etc.

import { BsSoundwave,BsSegmentedNav } from 'react-icons/bs'
import { RxLetterCaseToggle } from 'react-icons/rx'
import { CgFormatText } from 'react-icons/cg'
import { GiOpenChest } from 'react-icons/gi'
import { phonemes } from './phonemes'

export const navLinks = [
    {
        path: '/gestos',
        title: {
            es: 'Gestos',
            en: 'Gestures'
        },
    },
    {
        path: '/fonemas',
        title: {
            es: 'Fonemas',
            en: 'Phonemes'
        },
    },
    {
        path: '/api_datos',
        title: {
            es: 'Conjunto datos',
            en: 'Dataset'
        }
    },
    {
        path: '/api_traduccion',
        title: {
            es: 'Traducción',
            en: 'Translate'
        }
    }
    // {
    //     path: '/aprender',
    //     title: {
    //         es: 'Aprender',
    //         en: 'Learn',
    //     },
    // },
    // {
    //     path: '/herramieta',
    //     title: {
    //         es: 'Herramienta',
    //         en: 'Tool',
    //     },
    // },
    // {
    //     path: '/clasificador',
    //     title: {
    //         es: 'Clasificador',
    //         en: 'Classifier'
    //     },
    // }
]

export const languages = [
    {
        language: 'es',
        code: 'MX'
    },
    {
        language: 'en',
        code: 'US'
    }
]

export const searchBar = {
    es:{
        placeholder: {
            phonemes: 'Busca letras asociadas y grafías "ɲ"',
            gestures: 'Busca letras, palabras y nombres',
        },
        buttons: {
            gestures: 'Gestos',
            phonemes: 'Fonemas',
        }
    },
    en:{
        placeholder: {
            phonemes: 'Search associated letters and graphys "ɲ"',
            gestures: 'Search letters, words and names',
        },
        buttons: {
            gestures: 'Gestures',
            phonemes: 'Phonemes',
        }
    }
}

export const rootContent = {
    hero: {
        es: {
            title: 'Simplificamos la comunicación verbal para pacientes con',
            affections: [ 'afasias.', 'disartrias.', 'apraxias.' ],
            subtitle: 'Conforma palabras utilizando gestos del brazo',
            search: {
                options: [{value: 'gestos', title:'Gestos'}, {value: 'fonemas', title: 'Fonemas'}, {value: 'traduccion', title: 'Traducción'}],
                placeholders: [
                    'Busca letras, símbolos o palabras',
                    'Busca grafias y letras asociadas',
                    'Ingresa una palabra',
                ],
                title: 'Diccionario',
                components: 'Fonemas, movimientos del brazo (gestos) y traducción de palabras',

            },
            action: '¡Descubre la herramienta!'
        },
        en: {
            message: 'Currently the tool works only for the Spanish language (Mexico)',
            title: 'Making the verbal communication simple for patients with',
            affections: [ 'aphasias.', 'dysarthrias.', 'apraxias.' ], 
            subtitle: 'Make up words with arm gestures',
            search: {
                options: [{value: 'gestos', title:'Gestures'}, {value: 'fonemas', title: 'Phonemes'}, {value: 'traduccion', title: 'Translate'}],
                placeholders: [
                    'Search letter, symbols and words',
                    'Search grahys y associated letters',
                    'Add a word',
                ],
                title: 'Dictionary',
                components: 'Phonemes, arm movements (gestures) and words translation'

            },
            action: '¡Discover the tool!'
        }
    },

    voice:{
        es: {
            title: 'Voz mediante IA',
            subtitle: 'Tan natural como tu voz',
            description: 'Los pacientes se enfocan en crear palabras con la asociación de sonidos correctos y la herramienta se encarga de reproducirlas mediante al habla.',
            liveTool: {
                field: {
                    name: 'Palabra',
                    value: 'Actuar',
                },
                phonemes: 'Fonemas',
                voiceSettings: 'Configuración de voz',
            }
        },
        en: {
            title: 'AI powered voice',
            subtitle: 'As natural as your voice',
            description: 'Patients are tasked with the word creation through correct sound association while the tool takes care of the speech reproduction.',
            liveTool: {
                field: {
                    name: 'Word',
                    value: 'Actuar'
                },
                phonemes: 'Phonemes',
                voiceSettings: 'Voice Settings'
            }
        }
    },

    phonemes:{
        es: {
            title: 'Fonemas no letras',
            subtitle: 'Practica el lenguaje hablado',
            description: 'Cada gesto se corresponde con un fonema en vez de una letra, de esta forma el paciente ejercita la composición del lenguaje hablado y no la ortografía de las palabras',
            liveTool: {
                cardsPhonemes: [ 
                    phonemes['k'],
                    phonemes['s'],
                    phonemes['i'],
                 ],
                tablePhonemes: [ 
                    phonemes['ɾ'],
                    phonemes['r']
                 ]
            },
            link: 'Visita la lista'
        },
        en: {
            title: 'Phonemes no words',
            subtitle: 'Practice spoken language',
            description: 'Each gesture is matched with a phoneme instead of a letter, thus the patient exercises the spoken language composition, not the words spelling',
            liveTool: {
                cardsPhonemes: [ 
                    phonemes['k'],
                    phonemes['s'],
                    phonemes['i'],
                 ],
                tablePhonemes: [ 
                    phonemes['ɾ'],
                    phonemes['r']
                 ]
            },
            link: 'Visit the list'
        }
    },

    gestures:{
        title: {
            es: 'Gestos de brazo',
            en: 'Arm gestures',
        },
        subtitle: {
            es: 'Movimientos sencillos de replicar',
            en: 'Easy to replicate movements'
        },
        description: {
            es: 'Los gestos son fáciles de reproducir y no involucra movimientos precisos y pequeños, esto abre la posibilidad a pacientes con limitaciones motrices para su adopción.',
            en: 'The gestures are easy to reproduce and do not involve small, precise movements, which opens the possibility for patients with motor limitations to adopt them.'
        },
        body: {
            involved: {
                es: [ 'Brazo completo', 'Hombro', 'Codo' ],
                en: [ 'Whole arm', 'Shoulder', 'Elbow' ]
            },
            avoided: {
                es: [ 'Muñeca', 'Dedos' ],
                en: [ 'Wrist', 'Fingers' ]
            }
        }
    }
}

export const phonemesDictionary = {
    es: {
        title: 'Diccionario de fonemas en el idioma Español',
        description: 'Utilizamos los símbolos del SFI(Sistema Fonético Internacional) para asignar una representación escrita a los fonemas y la pronunciación de una palabra',
        filters: {
            categories: ['Phonemas','Grafías','Orden'],
            values: ['phoneme','associated','order'],
            icons: [
                <BsSoundwave />,
                <RxLetterCaseToggle />,
                <BsSegmentedNav />
            ],
        },
        emptyResults: {
            icon: <GiOpenChest className=' text-9xl mx-auto pb-10'/>,
            header: 'Sin resultados por mostrar',
            message: 'Intenta con otra búsqueda o modifica los filtros activos'
        },
        animationButton: 'Visualizar',
        addButton: {
            active: 'En biblioteca',
            default: 'Aprender',
        }
    },
    en: {
        title: 'Phonemes dictionary in the Spanish language',
        description: 'We use the symbols of the IPS (International Phonetic System) to assign a written representation to the phonemes and pronunciation of a word',
        filters: {
            categories: ['Phonemes','Associated letters','Order'],
            values: ['phoneme','associated','order'],
            icons: [
                <BsSoundwave />,
                <RxLetterCaseToggle />,
                <BsSegmentedNav />
            ],
        },
        emptyResults: {
            icon: <GiOpenChest className=' text-9xl mx-auto pb-10'/>,
            header: 'Sin resultados por mostrar',
            message: 'Intenta con otra búsqueda o modifica los filtros activos'
        },
        animationButton: 'Visualize',
        addButton: {
            active: 'In Library',
            default: 'Learn',
        }
    }
}

export const gesturesDictionary = {
    es: {
        bar: {
            tabs: {
                titles: ['Gestos', 'Traducción'],
                links: ['/gestos', '/gestos/traductor']
            },
            filters: {
                categories: [
                    'Fonemas',
                    'Palabras',
                ],
                values: [
                    { order: 1, key: 'phoneme'},
                    { order: 1, key: 'word'},
                ],
                icons: [
                    // Requires:
                    //  import * as rx from 'react-icons/rx'
                    //  import * as cg from 'react-icons/cg'
                    <BsSoundwave />,
                    <CgFormatText />,
                ]
            },
        },
        emptyResults: {
            icon: <GiOpenChest className=' text-9xl mx-auto pb-10'/>,
            header: 'Sin resultados por mostrar',
            message: 'Intenta con otra búsqueda o modifica los filtros activos'
        },
        resultsCount: (count) => `Mostrando ${count} resultados`
    },
    en: {
        bar: {
            tabs: {
                titles: ['Gestures', 'Translate'],
                links: ['/gestos', '/gestos/traductor']
            },
            filters: {
                categories: [
                    'Phonemes',
                    'Words',
                ],
                values: [
                    { order: 1, key: 'phoneme'},
                    { order: 1, key: 'word'},
                ],
                icons: [
                    // Requires:
                    //  import * as rx from 'react-icons/rx'
                    //  import * as cg from 'react-icons/cg'
                    <BsSoundwave />,
                    <CgFormatText />,
                ]
            },
        },
        emptyResults: {
            icon: <GiOpenChest className=' text-9xl mx-auto pb-10'/>,
            header: 'No results to be shown',
            message: 'Try making a different search or changing the active filters'
        },
        resultsCount: (count) => `Showing ${count} results`
    }
}