import { languages } from "../../content"
import { createSlice } from "@reduxjs/toolkit"

const languageSlice =  createSlice({
    name: 'languages',
    initialState: languages[0].language,
    reducers: {
        changeLanguage: (state,action) =>{
            state = action.payload
            return action.payload
        }
    }
})

export const {changeLanguage} = languageSlice.actions
export default languageSlice.reducer