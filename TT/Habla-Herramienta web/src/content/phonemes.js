const headers = {
    es: {
        phoneme: 'Fonema',
        associated: 'Grafías',
        letters: 'Grafías asociadas',
        examples: 'Ejemplos',
        order: 'Orden'
    },
    en: {
        phoneme: 'Phoneme',
        associated: 'Graphys',
        letters: 'Associated graphys',
        examples: 'Examples',
        order: 'Order',
    }
}

const phonemes = {
    a: {
        phoneme: 'a',
        order: 'Vocal',
        associated: ['a'],
        examples: [
            { word: 'casa', phonemes: 'kása', highlight:[1,3] },
            { word: 'árbol', phonemes: 'áɾbol', highlight:[0] },
            { word: 'ancla', phonemes: 'ánkla', highlight: [0,4] }
        ]
    },
    e:{
        phoneme: 'e',
        order: 'Vocal',
        associated: ['e'],
        examples: [
            { word: 'mesa', phonemes: 'mésa', highlight:[1] },
            { word: 'ensenada', phonemes: 'ensenáda', highlight:[0,3] },
            { word: 'erupción', phonemes: 'eɾupsión', highlight: [0] }
        ]
    },
    i:{
        phoneme: 'i',
        order: 'Vocal',
        associated: ['i','y'],
        examples: [
            { word: 'pino', phonemes: 'píno', highlight:[1] },
            { word: 'Uruguay', phonemes: 'Uɾuguái', highlight:[6] },
            { word: 'hoy', phonemes: 'ói', highlight: [1] }
        ]
    },
    o:{
        phoneme: 'o',
        order: 'Vocal',
        associated: ['o'],
        examples: [
            { word: 'copa', phonemes: 'kópa', highlight:[1] },
            { word: 'orador', phonemes: 'oɾadoɾ', highlight:[0,4] },
            { word: 'osadía', phonemes: 'osadía', highlight: [0] }
        ]
    },
    u:{
        phoneme: 'u',
        order: 'Vocal',
        associated: ['u'],
        examples: [
            { word: 'cuna', phonemes: 'kúna', highlight:[1] },
            { word: 'zumbido', phonemes: 'sumbído', highlight:[1] },
            { word: 'urraca', phonemes: 'uráka', highlight: [0] }
        ]
    },
    p:{
        phoneme: 'p',
        order: 'Consonante oclusiva',
        associated: ['p'],
        examples: [
            { word: 'perdón', phonemes: 'peɾdón', highlight:[0] },
            { word: 'patata', phonemes: 'patáta', highlight:[0] },
            { word: 'comprar', phonemes: 'kompɾaɾ', highlight: [3] }
        ]
    },
    b:{
        phoneme: 'b',
        order: 'Consonante Oclusiva',
        associated: ['b','v'],
        examples: [
            { word: 'boca', phonemes: 'bóka', highlight:[0] },
            { word: 'vaca', phonemes: 'báka', highlight:[0] },
            { word: 'vibrante', phonemes: 'bibɾánte', highlight: [0,2] }
        ]
    },
    t:{
        phoneme: 't',
        order: 'Consonante Oclusiva',
        associated: ['t'],
        examples: [
            { word: 'toro', phonemes: 'tóɾo', highlight:[0] },
            { word: 'cartílago', phonemes: 'kaɾtílago', highlight:[3] },
            { word: 'tardío', phonemes: 'taɾdío', highlight: [0] }
        ]
    },
    d:{
        phoneme: 'd',
        order: 'Consonante Oclusiva',
        associated: ['d'],
        examples: [
            { word: 'danzón', phonemes: 'dansón', highlight:[0] },
            { word: 'dama', phonemes: 'dáma', highlight:[0] },
            { word: 'dadivoso', phonemes: 'dadibóso', highlight: [0,2] }
        ]
    },
    k:{
        phoneme: 'k',
        order: 'Consonante Oclusiva',
        associated: ['c', 'qu', 'k'],
        examples: [
            { word: 'capa', phonemes: 'kápa', highlight:[0] },
            { word: 'queso', phonemes: 'késo', highlight:[0] },
            { word: 'kiwi', phonemes: 'kiui', highlight: [0] }
        ]
    },
    g:{
        phoneme: 'g',
        order: 'Consonante Oclusiva',
        associated: ['g','gu'],
        examples: [
            { word: 'garra', phonemes: 'gára', highlight:[0] },
            { word: 'guerra', phonemes: 'géra', highlight:[0] },
            { word: 'canguro', phonemes: 'kanguɾo', highlight: [3] }
        ]
    },
    ʧ:{
        phoneme: 'ʧ',
        order: 'Consonante Africada',
        associated: ['ch'],
        examples: [
            // 2 positions for the highlight are added for the web takes the symbol 'ʧ' as 2 characters
            { word: 'chico', phonemes: 'ʧíko', highlight:[0,1] },
            { word: 'chamizal', phonemes: 'ʧamisál', highlight:[0,1] },
            { word: 'cacharro', phonemes: 'kaʧaro', highlight: [2,3] }
        ]
    },
    f:{
        phoneme: 'f',
        order: 'Consonante Fricativa',
        associated: ['f'],
        examples: [
            { word: 'foca', phonemes: 'fóka', highlight:[0] },
            { word: 'alfalfa', phonemes: 'alfálfa', highlight:[2,5] },
            { word: 'café', phonemes: 'kafé', highlight: [2] }
        ]
    },
    s:{
        phoneme: 's',
        order: 'Consonante Fricativa',
        associated: ['s','c(e,i)','sc(e,i)','z'],
        examples: [
            { word: 'saco', phonemes: 'sáko', highlight:[0] },
            { word: 'cena', phonemes: 'séna', highlight:[0] },
            { word: 'escena', phonemes: 'eséna', highlight: [1] },
            { word: 'azul', phonemes: 'asúl', highlight: [1] }
        ]
    },
    x:{
        phoneme: 'x',
        order: 'Consonante Fricativa',
        associated: ['j','g(e,i)','x'],
        examples: [
            { word: 'jota', phonemes: 'xóta', highlight:[0] },
            { word: 'gente', phonemes: 'xénte', highlight:[0] },
            { word: 'mexicajo', phonemes: 'mexikáno', highlight: [2] }
        ]
    },
    j:{
        phoneme: 'j',
        order: 'Consonante Fricativa',
        associated: ['y','ll'],
        examples: [
            { word: 'yeso', phonemes: 'jéso', highlight:[0] },
            { word: 'llano', phonemes: 'jáno', highlight:[0] },
            { word: 'yema', phonemes: 'jéma', highlight: [0] }
        ]
    },
    m:{
        phoneme: 'm',
        order: 'Consonante Nasales',
        associated: ['m'],
        examples: [
            { word: 'mes', phonemes: 'més', highlight:[0] },
            { word: 'cormorán', phonemes: 'koɾmoɾán', highlight:[3] },
            { word: 'manzanilla', phonemes: 'mansaníja', highlight: [0] }
        ]
    },
    n:{
        phoneme: 'n',
        order: 'Consonante Nasal',
        associated: ['n'],
        examples: [
            { word: 'nada', phonemes: 'náda', highlight:[1,3] },
            { word: 'sanción', phonemes: 'sansión', highlight:[2,6] },
            { word: 'introducción', phonemes: 'intɾoduksión', highlight: [1,11] }
        ]
    },
    ɲ:{
        phoneme: 'ɲ',
        order: 'Consonante Nasal',
        associated: ['ñ'],
        examples: [
            { word: 'año', phonemes: 'áɲo', highlight:[1] },
            { word: 'cañaveral', phonemes: 'kaɲabeɾal', highlight:[2] },
            { word: 'carroñero', phonemes: 'karóɲa', highlight: [4] }
        ]
    },
    l:{
        phoneme: 'l',
        order: 'Consonante Lateral',
        associated: ['l'],
        examples: [
            { word: 'loco', phonemes: 'lóko', highlight:[0] },
            { word: 'calamidad', phonemes: 'kalamidád', highlight:[2] },
            { word: 'calzada', phonemes: 'kalsáda', highlight: [2] }
        ]
    },
    ɾ:{
        phoneme: 'ɾ',
        order: 'Consonante Vibrante',
        associated: ['r'],
        examples: [
            { word: 'coro', phonemes: 'kóɾo', highlight:[2] },
            { word: 'sorfeo', phonemes: 'soɾféo', highlight:[2] },
            { word: 'farsa', phonemes: 'fáɾsa', highlight: [2] }
        ]
    },
    r:{
        phoneme: 'r',
        order: 'Consonante Vibrante',
        associated: ['r','rr'],
        examples: [
            { word: 'corral', phonemes: 'korál', highlight:[2] },
            { word: 'rosa', phonemes: 'rósa', highlight:[0] },
            { word: 'honra', phonemes: 'ónra', highlight: [2] }
        ]
    }
}

export { phonemes, headers }