import { useState, useRef } from 'react'
import { useSelector } from 'react-redux'

import { getGestures, filters } from '../features'
import { gesturesDictionary } from '../content'
import { useLoaderData } from 'react-router-dom'
import { SearchingBar, DictionaryGestures, GesturesBar, ScreenGestures } from './sections'


// Loader for data
export const loaderGestures = async ({params}) => { 
  console.log('Parametros gestos >>',params)
  return [Object.values(await getGestures()), params?.query || ''] 
}

// Auxiliar functions
const orderComparisonGestures = (a,b) => {
  return (a.phoneme).localeCompare(b.phoneme)
}
const sortGestures = (gestures, order) => 
  order == 'd'
  ? gestures.sort(orderComparisonGestures)
  : gestures.sort(orderComparisonGestures).reverse()

const Gestures = () => {
  // Constants
  const language = useSelector(state => state.language)
  const data = gesturesDictionary[language] // UI Content
  const dataLoaded = useLoaderData() // 0 - phonemes list; 1 - Query
  const originalGestures = dataLoaded[0].reduce((array,gesture,i)=> array = array.concat({...gesture,...{index:i}}),[])

  const ref = useRef({
    resultsIndex: originalGestures.map((_,i)=>i), // Caché of the results index
    resultsLength: originalGestures.length,
    total1stFilters: gesturesDictionary['es'].bar.filters.values.reduce((count,{order}) => count += (order == 1 ? 1 : 0), 0),
    totalActive1stFilters: gesturesDictionary['es'].bar.filters.values.reduce((count,{order}) => count += (order == 1 ? 1 : 0), 0),
    phonemeIndex: originalGestures.reduce((dictionary, gesture, index) =>( {...dictionary, [gesture.phoneme] : index }), {})
  })

  // States
  const [order, setOrder] = useState('d') //Descendant
  const [activeIndex, setActiveIndex] = useState('')
  const [filtersApplied, setFiltersApplied] = useState([
    { order: 1, key: 'phoneme'},
    { order: 1, key: 'word'},
  ])

  const [resultsGestures, setResultsGestures] = useState([...originalGestures]) // Shown results before 1st order filters, acts as a caché for when this type of filters are added or removed
  const [gesturesShown, setGesturesShown] = useState(originalGestures.map((_,i) => i)) // Index of the resultsGestures state that are being shown

  // Asigning new gestures to show
  const newResultsGestures = (newGestures) => {
    setResultsGestures([...newGestures])
    setGesturesShown([...newGestures.reduce((acum,gesture)=> acum = acum.concat(gesture.index),[])])
  }
  
  // Click handlers
  const clickFilter = (active, filter) => {
    // When either a 1st order filter is added or removed the filters remaining must be applied to the shown gestures
    let apply1stOrder = []
    // Forces to make the filtering even when there are no filters of 1st order left. This is useful when the las 1st order filter is removed and no result must be show
    let applyFilters = filter.order == 1
    ref.current.totalActive1stFilters += filter.order == 1 
                                          ? active
                                            ? -1
                                            : 1
                                          : 0 

    if(active){ // Removing filters
      const auxGestures = filtersApplied.filter(({key}) => key != filter.key)
      setFiltersApplied([...auxGestures])
      if(filter.order == 1)
        apply1stOrder = auxGestures.filter((filter) => filter.order == 1)
    }else{ // Adding filters
      filtersApplied.push(filter)
      // When the new filter is of first order is applied inmediately
      if(filter.order == 1)
        apply1stOrder = filtersApplied.filter((filter) => filter.order == 1)
    }

    // Scape clause
    if(!applyFilters) return true
    // When a filter gets removed then the remaining filters are applied to the shown data, otherwise the original data is filtered
    let auxGestures = resultsGestures.reduce((acum,gesture)=>{
      for(const f in apply1stOrder){
        if(filters[apply1stOrder[f].key](gesture))
          return [...acum, gesture.index]
      }
      return acum
    },[])
    /* let auxGestures = ref.current.resultsIndex.map((_,i)=>i) // All the index available in results
      .filter((index) => {
        console.log('Evaluated >>',resultsGestures[index])
        for(const f in apply1stOrder){
          if(filters[apply1stOrder[f].key](resultsGestures[index]))
            return true
        }
        return false
      }) */
    setGesturesShown([...auxGestures])
  }
  const clickOrder = () => {
    setResultsGestures([...resultsGestures.reverse()])
    setGesturesShown([...gesturesShown.reverse()])
    setOrder((current)=> current === 'd' ? 'a' : 'd')
  }
  const clickGesture = (index) => {
    setActiveIndex(index)
    //Opens the screen with the gesture info
  }
  const closeScreenGesture = () => {
    setActiveIndex('')
  }

  return (
  <>
    <div className="w-full border-b-2 border-b-gray-200"> 
      <SearchingBar
        elements={originalGestures}
        properties={['phoneme','spelling','name']}
        setResults={newResultsGestures} 
        instaQuery={dataLoaded[1]}
      /> 
    </div>

    <section id='gestures' className='container px-4 pb-10'>
      <GesturesBar 
        data={data.bar}
        order={order}
        onClickFilter={clickFilter}
        onClickOrder={clickOrder} 
      />
      <DictionaryGestures
        gesturesShown={gesturesShown.map((g) => originalGestures[g])}
        activeIndex={activeIndex}
        onClickGesture={clickGesture}
        emptyResultsData={data.emptyResults}
        resultsCount={data.resultsCount}
      />
      <ScreenGestures
        gesture={activeIndex ? originalGestures[ref.current.phonemeIndex[activeIndex]] : {}}
        onCloseGesture={closeScreenGesture}
      />
    </section>
  </>
  )
}

export default Gestures