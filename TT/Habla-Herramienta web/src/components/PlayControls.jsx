import { useState, useEffect } from "react"
import { MdOutlineReplay, MdOutlinePause, MdPlayArrow, MdOutlineSpeaker } from "react-icons/md"

import CircularIcon from "./CircularIcon"

const PlayControls = () => {

    const [muteSound, setMuteSound] = useState(false)

  return (
    <div className='w-full h-full flex'>
        <div className="grow flex justify-center items-end gap-x-1">
            <CircularIcon 
                icon={(<MdOutlinePause className='text-xl'/>)}
                /* onClickHandler={paintNextPhoneme} */
                hoverStyles={['bg-secondary']}
                /* activeStyle={'bg-pink-400'}
                active={sex == 'f'} */
            />
            <CircularIcon 
                icon={(<MdPlayArrow className='text-xl'/>)}
                /* onClickHandler={paintNextPhoneme} */
                hoverStyles={['bg-secondary']}
                /* activeStyle={'bg-pink-400'}
                active={sex == 'f'} */
            />
            <CircularIcon 
                icon={(<MdOutlineReplay className='text-xl'/>)}
                /* onClickHandler={paintNextPhoneme} */
                hoverStyles={['bg-secondary']}
                /* activeStyle={'bg-pink-400'}
                active={sex == 'f'} */
            />
        </div>
        <div className='relative flex items-top justify-center'>
            <CircularIcon 
                icon={(<MdOutlineSpeaker className='text-lg'/>)}
                onClickHandler={() => setMuteSound((current) => !current)}
                hoverStyles={['bg-secondary']}
                activeStyle={'bg-white text-dark'}
                active={muteSound}
                size='sm'
            />
        </div>
    </div>
  )
}

export default PlayControls