import { useState } from 'react'
import { useSelector } from 'react-redux'

import { CircularIcon } from '../../components'
import { phonemesDictionary } from '../../content'

const Filter = ({value, title, icon, onClickHandler=()=>'', activeStyles=''}) => {
    const [active, setActive] = useState(true)
  
    return (
      <div className={`p-1 w-max h-max cursor-pointer flex items-center ${active ? activeStyles : ''}`}
        onClick={() => {
          onClickHandler(active,value)
          setActive((current) => !current)
        }}
      >
        <CircularIcon 
          icon={icon}
          active={active}
          activeStyle={'bg-primary text-white'}
          extraStyles={'text-gray-700'}
          size={'xsm'}
        />
        <span value={value} className='hidden md:inline text-sm ml-2'>{title}</span>
      </div>
    )
  }

const PhonemesBar = ({onClickFilter}) => {
    const language = useSelector(state => state.language)

    const data = phonemesDictionary[language]

  return (
    <div className="w-full h-max flex flex-row-reverse justify-between pt-2 px-2">
        <div className="grow flex gap-x-1 md:gap-x-2 justify-end">
        {
            data.filters.categories.map((cat,i) => (
            <Filter 
                title={cat}
                defaultState={true}
                value={data.filters.values[i]}
                icon={data.filters.icons[i]}
                onClickHandler={onClickFilter}
            />
            ))
        }
        </div>
    </div>
  )
}

export default PhonemesBar