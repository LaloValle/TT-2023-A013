import { useRef, useState } from 'react'

import { PhonemesBar, SearchingBar } from './sections'
import { scribble } from '../assets'
import { TablePhonemes, SideAnimation, PhonemeCard } from '../components'
import { useSelector } from 'react-redux'

import { getPhonemes } from '../features'
import { phonemesDictionary as dict } from '../content'
import { useLoaderData } from 'react-router-dom'


// Loader for data
export const loaderPhonemes = async ({params}) => { 
  console.log('Parametros fonemas >>',params)
  return [Object.values(await getPhonemes()), params?.query || ''] 
}


const Phonemes = () => {
  const language = useSelector(state => state.language)
  const content = dict[language]
  const dataLoaded = useLoaderData() // 0 - phonemes list; 1 - Query
  const ref = useRef(dataLoaded[0])
  
  const [showingPhonemes,setShowingPhonemes] = useState(dataLoaded[0])  
  const [filters,setFilters] = useState(['phoneme','associated','order'])
  const [activeIndex, setActiveIndex] = useState(0)
  const [showAnimation, setShowAnimation] = useState(false)
  const [playingAudio, setPlayingAudio] = useState(false)
  const [alreadyAdded, setAlreadyAdded] = useState(false)
  
  // Event Handlers
  const clickRowTable = (index) => setActiveIndex(index)
  const clickAnimation = () => {
    // Recovers animation
    setShowAnimation((current) => !current)
  }
  const clickAudio = () => {
    // Recovers audio
    setPlayingAudio((current) => !current)
  }
  const clickAdd = () => {
    if(alreadyAdded) console.log('Gets deleted')
    else console.log('Gets added')
    setAlreadyAdded((current) => !current)
  }
  const clickFilter = (active,filter) => {
    if(active)
      setFilters([...filters.filter((element)=> element!=filter)])
    else 
      setFilters([...filters,filter])
  }

  return (
    <>
      <div className="w-full border-b-2 border-b-gray-200"> 
        <SearchingBar 
          elements={ref.current}
          properties={filters}
          setResults={setShowingPhonemes}
          instaQuery={dataLoaded[1]}
        />
      </div>

      <div className='container mt-[76px] z-40 fixed md:relative md:mt-0'>
        <PhonemesBar 
          onClickFilter={clickFilter}
        />
      </div>
      
      <div id='fonemas' className='container px-5 pt-32 pb-20 md:p-20'>
        <h1 className='font-bold text-center text-2xl md:text-3xl relative'>
          <img src={scribble}  className=' scale-75 absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/4'/>
          <span className='relative z-10'>{content.title}</span>
        </h1>

        <p className='w-full text-center my-10 text-base md:text-xl font-medium'>{content.description}</p>

        {
          showingPhonemes.length > 0
          ? (
            <div id='container-phonemes' className='w-full md:min-h-[520px] md:max-h-[570px] relative flex flex-col-reverse md:flex-row justify-between'>
              <div className='mt-8 md:mt-0 w-full md:w-1/2 max-h-[550px] overflow-y-scroll'>
                    <TablePhonemes 
                      phonemes={showingPhonemes}
                      headers={['phoneme','associated']}
                      activeStyle={'text-white bg-primary'}
                      hoverStyles={['bg-gray-400', 'text-white']}
                      activeIndex={activeIndex}
                      onClickHandler={clickRowTable}
                    />
              </div>
              <div className={`w-full max-w-[320px] md:w-1/2 self-center md:max-w-[360px] mx-auto relative`}>
                <div className={`h-full aspect-5/7 absolute z-40 top-40 md:top-0 -right-2 md:right-full ${showAnimation ? 'block' : 'hidden'}`}>
                  <SideAnimation
                    phoneme={'Gesto'}
                    stateAdd={alreadyAdded}
                    onClickAdd={clickAdd}
                  />
                </div>
                  <PhonemeCard
                    phoneme={showingPhonemes[activeIndex]}
                    stateAudio={playingAudio}
                    stateAnimation={showAnimation}
                    onClickAnimation={clickAnimation}
                    onClickAudio={clickAudio}
                  />
              </div>
            </div>
          )
          : (
              // Empty
            <div id='container-phonemes' className='w-full min-h-[520px] max-h-[570px] flex justify-center items-center'>
              <div>
                {content.emptyResults.icon}
                <span className='text-3xl block text-center pb-4'>{content.emptyResults.header}</span>
                <p className='text-lg text-gray-500 text-center px-10 mx-auto'>{content.emptyResults.message}</p>
              </div>
            </div>
          )
        }
      </div>
    </>
  )
}

export default Phonemes