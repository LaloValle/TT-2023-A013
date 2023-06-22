const translateStatus = {
    es: [
        {
            status: 'Rechazado',
            color: 'bg-red-500'
        },
        {
            status: 'Pendiente',
            color: 'bg-highlight'
        },
        {
            status: 'Esperando',
            color: 'text-gray-400'
        },
        {
            status: 'Conectado',
            color: 'text-primary'
        },
    ],
    en: [
        {
            status: 'Refused',
            color: 'bg-red-500'
        },
        {
            status: 'Pending',
            color: 'bg-highlight'
        },
        {
            status: 'Waiting',
            color: 'text-gray-400'
        },
        {
            status: 'Connected',
            color: 'text-primary'
        },
    ]
}

const translate = {
    es: {
        name : 'Fonemas a gestos',
        placeholder : 'konbeɾtiɾ',
        error: 'Falló la conexión',
        errorMessage: 'Ocurrió un problema con la conexión con la API de datos',
        retry: 'Reintentar'
    },
}

export { translateStatus, translate }