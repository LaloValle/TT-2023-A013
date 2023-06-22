import { useState } from "react"
import { BsFillMegaphoneFill } from "react-icons/bs"

import { cuerpoHorizontal } from "../assets"
import { CircularIcon } from '../components'
import { gestures } from "../content"

const GestureCard = ({data, index, activeIndex, onClickHandler=()=>''}) => {
    const [playingAudio, setPlayingAudio] = useState(false)
    const [showGif, setShowGif] = useState(false)

    //Event Handlers
    const clickAudio = () => {
        setPlayingAudio((current)=>!current)
    }

  return (
    <div
        className={`w-full h-max rounded-xl p-3 flex flex-col ${index == activeIndex ? 'bg-primary text-white' : 'bg-gray-200'}`}
        onMouseEnter={()=> setShowGif(true)}
        onMouseLeave={()=> setShowGif(false)}
    >
        {/* Video animation */}
        <div className='w-full aspect-4/3 relative'>
            {/* Image */}
            <img src={ data?.placeholder || cuerpoHorizontal} alt={`Gesto ${data.name}`} className="w-full aspect-4/3 cursor-pointer" onClick={()=>onClickHandler(index)}/>
            {showGif && data?.gif ? (
                <img src={data.gif} alt={`Gif gesto ${data.name}`} className="absolute top-0 left-0 w-full aspect-4/3 cursor-pointer" onClick={()=>onClickHandler(index)}/>
            ) : ('')}
            {/* <CircularIcon 
                icon={(<BsFillMegaphoneFill className='text-md text-white/50'/>)}
                hoverStyles={['bg-gray-800']}
                activeStyle={'bg-white !text-dark'}
                extraStyles={`absolute bg-gray-600 bottom-2 right-2 z-30`}
                onClickHandler={clickAudio}
                active={playingAudio}
            /> */}
        </div>

        {/* info */}
        <div className="w-full py-1 px-2 flex justify-between items-center">
            <span className={`text-2xl text-semibold ${index == activeIndex ? 'text-highlight' : 'text-primary'}`}>/{data.phoneme}/</span>
            <p className={`text-xl ${index == activeIndex ? 'text-white' : 'text-gray-400'}`}>{Array.from(data.spelling).join(', ')}</p>
        </div>
    </div>
  )
}

export default GestureCard