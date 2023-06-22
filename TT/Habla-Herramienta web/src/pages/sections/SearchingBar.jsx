import { useState, useEffect } from 'react'
import { useSelector } from 'react-redux'
import { FaSearch } from 'react-icons/fa'
import { MdWavingHand } from 'react-icons/md'
import { BsSoundwave } from 'react-icons/bs'
import { BiLoaderAlt } from 'react-icons/bi'
import { Form, NavLink } from 'react-router-dom'

import { filters } from '../../features'
import { searchBar } from '../../content'

const makeSearch = async (query,elements,properties,noGraphys,abort) => {
  return new Promise((resolve, reject) => {
    if(abort)
      reject('Aborted')
    if(!abort)
      resolve(
        elements.filter(element => filters.search(element,query,properties,noGraphys))
      )
  })
}

const useDebounceValue = (value, time=800) => {
  const [debounceValue, setDebounceValue] = useState(value)

  useEffect(()=>{
    const timeout = setTimeout(()=>{
      setDebounceValue(value)
    },time)

    return ()=>{ clearTimeout(timeout) }
  },[value,time])

  return debounceValue
}

const SearchingBar = ({elements, properties, setResults, noGraphys=false, instaQuery=''}) => {
  const language = useSelector(state => state.language)

  const [searching,setSearching] = useState(false)
  const [query,setQuery] = useState(instaQuery)
  const debounceQuery = useDebounceValue(query)

  const data = searchBar[language]

  useEffect(() => {
    let abort = false;
    (async () => {
      if(query.length > 0)
        setSearching(true)
      else
        setResults([...elements])
      
      if(debounceQuery.length > 0){
        const found = await makeSearch(debounceQuery.toLowerCase().split(' '), elements, properties, noGraphys, abort)
        if(!abort){
          setResults([...found])
          setSearching(false)
        }
      }
    })()

    return () => { 
      abort = true
      setSearching(false) 
    }
  }, [query,debounceQuery])
  

  return (
    <div className='flex p-2 container fixed mt-[36px] md:relative md:mt-0 bg-white z-40'>
        <Form className='text-sm md:text-base bg-gray-200 rounded-md pl-3 grow h-9 max-w-[600px] flex'>
          <input type='search' placeholder={data.placeholder.gestures} className='grow text-xs md:text-sm text-gray-700 align-middle' value={query} onChange={(e)=>setQuery(e.target.value)}/>
          <button className=' bg-actions rounded-r-md cursor-pointer h-full px-3 align-middle'> 
            {
              searching
              ? <BiLoaderAlt className='text-white text-base md:text-lg loading' />
              : <FaSearch className='text-white text-base md:text-lg' />
            }
          </button>
        </Form>

        <div className='grow flex justify-end gap-x-1 md:gap-x-3 h-full'>
          <NavLink to='/fonemas' className={({isActive}) => `${isActive ? 'active' : 'inactive'} plain-icon-button`}> <BsSoundwave className='inline text-base md:text-lg md:mr-2' /> <span className='hidden md:inline'>{` ${data.buttons.phonemes}`}</span> </NavLink>
          <NavLink to='/gestos' className={({isActive}) => `${isActive ? 'active' : 'inactive'} plain-icon-button`}> <MdWavingHand className='inline text-base md:text-lg md:mr-2' /> <span className='hidden md:inline'>{` ${data.buttons.gestures}`}</span> </NavLink>
        </div>
    </div>
  )
}

export default SearchingBar