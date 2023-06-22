import Typed from 'react-typed'
import { useSelector } from 'react-redux'
import { useState, useRef } from 'react'
import { Link } from 'react-router-dom'
import { FaSearch} from 'react-icons/fa'
import { CgSmileMouthOpen } from 'react-icons/cg'
import { GiSandsOfTime, GiMagicHat } from 'react-icons/gi'
import { BiHide } from 'react-icons/bi'

import { rootContent as content } from '../../content'

const Hero = () => {
  const language = useSelector(state => state.language)
  const hero = content.hero[language]
  const refLinks = useRef([
    // Gestures
    (query) => `/gestos/${query}`,
    // Fonemas
    (query) => `/fonemas/${query}`,
    // Traducción
    (query) => `/`,
  ])
  
  const [searchOption, setSearchOption] = useState(0)
  const [searchQuery, setSearchQuery] = useState('')

  return (
    <div className='px-4 pt-24 pb-14 container text-center md:pt-28 md:pb-20 md:px-8 relative'>
        
        {/* Messages */}
        {hero?.message && (
          <>
            <input type="checkbox" name="messageCheckbox" id="messageCheckbox" className='absolute hidden'/>
            <label className='flex top-0 justify-between cursor-pointer bg-highlight shadow-xl p-3 absolute  left-[50%] translate-x-[-50%] w-full opacity-100 transition-all md:rounded-md md:top-2' htmlFor='messageCheckbox' onClick={(e) => setTimeout(() => { e.target.style.display = 'none' }, 300)} >
              <GiSandsOfTime className='text-lg font-bold text-gray-600 aspect-auto inline md:text-2xl'/>
              <p className='text-sm text-gray-700 inline md:text-base'>{hero.message}</p>
              <BiHide className='font-bold text-black text-lg self-center'/>
            </label>
          </>
        )}

        {/* Title */}
        <CgSmileMouthOpen className='text-5xl text-primary inline mr-3 font-bold md:text-6xl pb-3'/>
        <h1 className='text-3xl inline font-bold md:text-4xl'>{hero.title}</h1>
        <Typed 
            className='text-3xl inline ml-2 font-bold md:text-4xl text-primary'
            strings={hero.affections}
            fadeOut={true}
            showCursor={false}
            typeSpeed={150}
            loop
        />
        <h2 className='text-lg font-medium text-gray-600 md:text-xl mt-3'>{hero.subtitle}</h2>

        {/* Search bar */}
        <div className=' h-12 w-max-[725px] rounded-md bg-gray-200 md:h-16 mt-12 flex items-center flex-wrap'>
          <select name="search_type" className='text-sm px-2 rounded-l-md h-full cursor-pointer border-r-2 border-r-gray-300 bg-gray-200 md:text-base md:pl-3 md:pr-5' id='searchSelect' onChange={(e) => setSearchOption(e.target.selectedIndex)}>
            {hero.search.options.map(({value, title}) => <option key={value} value={value}>{title}</option>)}
          </select>
          <input type='search' placeholder={hero.search.placeholders[searchOption]} className='text-sm grow text-gray-700 align-middle pl-3 h-full md:text-base' defaultValue={searchQuery} onChange={(e)=>setSearchQuery(e.target.value)}/>
          <Link to={refLinks.current[searchOption](searchQuery)} className='py-2 w-full mt-3 md:mt-0 md:w-max md:py-0 bg-actions rounded-md md:rounded-none md:rounded-r-md cursor-pointer md:h-full md:aspect-square align-middle flex justify-center items-center'>
            <span className='inline text-white font-bold text-sm md:text-base pr-3 md:hidden'>Search</span>
            <FaSearch className='text-sm text-white md:text-lg' />
          </Link>
        </div>
        <b className='hidden md:inline text-sm mt-6'>{hero.search.title}: </b>
        <p className='hidden md:inline text-sm'>{hero.search.components}</p>

        {/* Action Button */}
        <div className='flex flex-col gap-x-8  items-center justify-end mt-32 group bg-red-500 relative w-max mx-auto'>
          <Link to='#voice' className=' text-gray-700 py-4 border-b-4 h-14 px-6 relative z-20 bg-white border-b-actions'>
            <div className='h-0 group-hover:h-full w-full bg-actions absolute rounded-t-md z-20 bottom-0 left-0 transition-all'></div>
            <span className='relative z-30 group-hover:text-white'>{hero.action}</span>
          </Link>
          <GiMagicHat className='absolute top-0 left-[50%] translate-x-[-50%] z-10 text-secondary text-5xl grow items-end group-hover:translate-y-[-110%] transition-transform delay-150' />
        </div>
      </div>
  )
}

export default Hero