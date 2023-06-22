// Defining a default error page
//  React routes catches the errors when loading data, while rendering, or performing data mutations

import React from 'react'
import { useRouteError } from 'react-router-dom'
const ErrorPage = () => {
    const error = useRouteError()
    console.error(error)

    return(
        <div className='w-full h-screen flex-col justify-center items-center text-center'>
            <h1 className='font-bold text-gray-800 text-6xl'>Oops!</h1>
            <p className='text-gray-600 text-4xl'>Sorry, an unexpected error has occurred.</p>
            <p className='text-xl mt-6 text-red-500 font-semibold'>
                <i>{error.statusText || error.message}</i>
            </p>
        </div>
    )
}

export default ErrorPage