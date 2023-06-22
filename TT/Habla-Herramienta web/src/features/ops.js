// Searching filters
export const filters = {
    /*
        First order filters
        -------------------
            Used to make subsets of the resulted gestures
    */
    //Filters for Phonemes
    phoneme: (gesture) => ['Fonema','Phoneme'].includes(gesture.nature) ,
    // Filters for Words
    word: (gesture) => ['Palabra','Word'].includes(gesture.nature),
    /*
        Second order filters
        --------------------
            Results of a search task
    */
    //Associated letters
    //  The query must have to be already preprocesed and passed as a list of letters of words
    /* associated: (element, query) => {
        if(element?.nature){ //Only for gestures
            if(element?.nature === 'word')
                return false
        }
        // Spelling for gestures and associated with phonemes
        let compareSet = element?.spelling ? element.spelling : element.associated
        for(let q in query){
            if(q in compareSet)
            return true
        }
        return false
    }, */

    /**
     * Searches for a match given the queries in the passed arguments in the provided element.
     * Search is inclusive as returns true when the first match appears
     * 
     * @param {Object} element - Object to be evaluated
     * @param {Array} query - Array of strings to be searched
     * @param {Array} properties - (Optional) Array of object properties where the queries are to be searched
     * @returns {Boolean} matches - true if there is a match in any of the properties with the passed queries
     */
    search: (element, query, properties=['phoneme','name','associated','spelling'], noGraphys=false) => {
        // Gestures: phoneme,name
        // Phonemes: phoneme
        if(noGraphys) properties = properties.slice(0,-2)

        const memo = {} //Used for properties that are arrays

        for(let indexQ in query){
            const q = query[indexQ]
            for(let indexP in properties){
                const p = properties[indexP]
                if(element?.[p]){
                    // Verifies if the property is an array
                    if(typeof element[p] != 'string')
                        memo[p] = Array.from(element[p]).join(' ').toLowerCase()
                    // When is already in memo
                    if(memo?.[p]){
                        if(memo[p].includes(q))
                            return true
                    }
                    // When the propert
                    else if(element[p].toLowerCase().includes(q))
                        return true
                }
            }
        }
        return false
    }
}