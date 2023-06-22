import { Link } from 'react-router-dom'
import { GrUserAdd } from 'react-icons/gr'

import { styles, phonemesDictionary } from '../content'
import { cuerpoVertical } from "../assets"
import CircularIcon from './CircularIcon'
import { useSelector } from 'react-redux'

const SideAnimation = ({phoneme, stateAdd, onClickAdd}) => {
    const language = useSelector((state) => state.language)
    const dict = phonemesDictionary[language]

  return (
    <div className='w-full h-full p-4 bg-gray-300 rounded-xl flex flex-col'>
        <div className='relative'>
            <img src={cuerpoVertical} alt="Cuerpo 3:4" className="w-full aspect-3/4 bg-secondary relative"/>
            <span className='w-full absolute bottom-0 left-0 uppercase text-white bg-black/50 text-center py-1'>{phoneme}</span>
        </div>
        <div className="grow w-full flex justify-between items-end py-1 px-4">
            <Link to='/gestos' className={styles.outlinedWide(styles.palettes.white, true)}>{dict.animationButton}</Link>
            <CircularIcon 
                icon={(<GrUserAdd className='text-xl text-white' />)}
                activeStyle={'bg-white text-primary'}
                extraStyles={'text-white'}
                hoverStyles={['bg-gray-400','text-white']}
                active={stateAdd}
                onClickHandler={onClickAdd}
                /* help={Object.values(dict.addButton)} */
            />
        </div>
    </div>
  )
}

export default SideAnimation