import { useSelector } from 'react-redux'
import { GestureCard } from '../../components'

const DictionaryGestures = ({gesturesShown, activeIndex, emptyResultsData, resultsCount=()=>'', onClickGesture=()=>''}) => {
  const language = useSelector(state => state.language)

  return (
    <div className='pt-48 md:pt-4'>
      <div className='w-full gap-y-8 grid justify-evenly items-left grid-cols-[repeat(auto-fit,minmax(250px,300px))]'>
        {
          gesturesShown.length > 0
          ? gesturesShown.map((gesture) => (
              <GestureCard 
                data={gesture}
                index={gesture.phoneme}
                activeIndex={activeIndex}
                onClickHandler={onClickGesture}
              />
            ))
          : (
            <div className='py-20 col-span-full'>
              {emptyResultsData.icon}
              <span className='text-2xl md:text-3xl block text-center pb-4'>{emptyResultsData.header}</span>
              <p className='text-base md:text-lg text-gray-500 text-center px-10 mx-auto'>{emptyResultsData.message}</p>
            </div>
          )
        }
      </div>
      <span className='border-t-2 border-t-gray-200 mt-4 w-full block py-4 text-sm text-right'>{resultsCount(gesturesShown.length)}</span>
    </div>
  )
}

export default DictionaryGestures