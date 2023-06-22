import { filters } from "./ops"
import languageReducer, {changeLanguage} from "./languages/languagesSlices"
import { getPhonemes, getGestures } from "./data/dataRecovery"

export {
    filters,
    languageReducer, changeLanguage,
    getPhonemes, getGestures
}