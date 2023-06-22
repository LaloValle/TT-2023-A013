import { useSelector, useDispatch } from 'react-redux'
import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { AiOutlineLogin, AiOutlineMenu, AiFillCloseCircle } from 'react-icons/ai'

import { changeLanguage } from '../../features'
import { logo } from "../../assets"
import { navLinks, languages as listLanguages } from "../../content"
 
const Navbar = () => {
  const language = useSelector(state => state.language)
  const dispatch = useDispatch()

  const [languageIndex, setLanguageIndex] = useState(0)
  const [showingMenu, setShowMenu] = useState(true)

  /* Preventing scrolling when menu open */
  useEffect(()=>{
    if(!showingMenu)
      document.body.style.overflow = "hidden";
    else
      document.body.style.overflow = "scroll";
  },[showingMenu])

  // Click handler
  const clickLanguage = () => {
    dispatch(changeLanguage(listLanguages[1-languageIndex].language))
    setLanguageIndex((current)=> 1-current) // Works only for binary settings
  }

  return (
    <nav className="container w-full flex py-2 px-4 md:py-4 md:px-6 gap-x-3">
        <Link to='/'> <img src={logo} alt="Logo" className=" h-5 md:h-7 mr-10" /> </Link>
        {/* Desktop */}
        <div className="hidden md:flex flex-1 gap-x-6">
          { navLinks.map(({ path, title }) => <Link key={title[language]} className='cursor-pointer align-middle' to={path} > {title[language]} </Link>) }
        </div>
        <div className="hidden md:flex gap-x-8 items-center">
          <span className="font-bold uppercase cursor-pointer text-lg" onClick={()=>clickLanguage()}>{listLanguages[languageIndex].language}</span> 
          <Link to='/login' > <AiOutlineLogin className='navbar-icon'/> </Link>
        </div>

        {/* Mobile */}
        <div className='flex md:hidden flex-1 justify-end'>
          { showingMenu
            ? (<AiOutlineMenu className='navbar-icon' onClick={() => setShowMenu((showing) => !showing )} />)
            : (
              <>
                <AiFillCloseCircle className='navbar-icon z-50' onClick={() => setShowMenu((showing) => !showing )} />
                
                <div className='fixed z-50 top-0 left-0 h-screen w-[90vw] bg-white shadow-lg flex flex-col gap-y-2 py-2 px-4'> 
                  <Link className=' mb-12' to='/'> <img src={logo} alt="Logo" className="h-5" /> </Link>         
                  { navLinks.map(({ path, title }) => <Link key={title[language]} className='cursor-pointer align-middle px-6 py-6 text-lg transition-colors hover:bg-secondary hover:text-white' to={path} > {title[language]} </Link>) }
                  <div className=' w-full self-end flex flex-end justify-end gap-x-8 grow items-end pb-6'>
                    <span className="font-bold uppercase cursor-pointer text-lg" onClick={()=>clickLanguage()}>{listLanguages[languageIndex].language}</span> 
                    <Link to='/login' > <AiOutlineLogin className='navbar-icon'/> </Link>
                  </div>
                </div>
              </>
            )
          }
          
          
        </div>
    </nav>
  )
}

export default Navbar