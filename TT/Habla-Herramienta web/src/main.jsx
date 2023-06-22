import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'

import { Provider } from 'react-redux'
import { RouterProvider, createBrowserRouter } from "react-router-dom"
import { Dataset, ErrorPage, Gestures, Phonemes, Root, Translate } from "./pages"
import Main from './pages/Main'
import { store } from './app'


//Loaders
import { loaderPhonemes, loaderGestures } from './pages'

// Router construction
const router = createBrowserRouter([
  {
    path:'/',
    element: <Root />,
    errorElement: <ErrorPage />,
    children: [
      {
        index: true,
        element: <Main />
      },
      {
        path: 'gestos',
        element: <Gestures />,
        loader: loaderGestures,
      },
      {
        path: 'gestos/:query',
        element: <Gestures />,
        loader: loaderGestures,
      },
      {
        path: '/fonemas',
        element: <Phonemes />,
        loader: loaderPhonemes,
      },
      {
        path: '/fonemas/:query',
        element: <Phonemes />,
        loader: loaderPhonemes,
      },
      {
        path: '/api_datos',
        element: <Dataset />
      },
      {
        path: '/api_traduccion',
        element: <Translate />
      }
    ]
  }
])

ReactDOM.createRoot(document.getElementById('root')).render(
  // <React.StrictMode>
    <Provider store={store}>
      <RouterProvider router={router} />
    </Provider>
  // </React.StrictMode>,
)
