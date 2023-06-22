import { configureStore } from '@reduxjs/toolkit'
import { languageReducer } from '../features'

const store = configureStore({
    reducer: {
        language: languageReducer
    }
})

export default store