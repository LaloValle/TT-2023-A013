import { NavLink } from "react-router-dom"
import { useState } from "react"
import { TbSortAscendingLetters, TbSortDescendingLetters } from 'react-icons/tb'

import { CircularIcon } from "../../components"

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
      <span value={value} className='text-sm hidden md:inline ml-2'>{title}</span>
    </div>
  )
}

const GesturesBar = ({data, order, onClickFilter, onClickOrder}) => {
  return (
    <div className="w-full h-max my-2 z-40 fixed mt-[76px] md:relative md:mt-0">
      {/* Tabs */}
      <div className="border-b-2 border-b-gray-300 bg-white">
        {
          data.tabs.titles.map((title,i) => (
            <NavLink key={i} to={data.tabs.links[i]} className={({isActive}) => `${isActive ? 'border-b-2 border-b-gray-500' : ''} relative top-[2px] text-xs md:text-sm px-2 py-3 inline-block font-light`}>{title}</NavLink>
          ))
        }
      </div>

      {/* Filters */}
      <div className="w-full h-max flex flex-row-reverse justify-between pt-2 px-2">
        <div className="grow flex gap-x-2 justify-end pr-4 md:pr-0">
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
        <div className="flex h-full gap-x-3 items-center">
          <CircularIcon
            icon={(<TbSortAscendingLetters className="text-base md:text-lg"/>)}
            active={order == 'd'}
            activeStyle={'bg-gray-800 text-white'}
            hoverStyles={['bg-gray-300']}
            onClickHandler={onClickOrder}
            size={'sm'}
          />
          <CircularIcon
            icon={(<TbSortDescendingLetters className="text-base md:text-lg"/>)}
            active={order == 'a'}
            activeStyle={'bg-gray-800 text-white'}
            hoverStyles={['bg-gray-300']}
            onClickHandler={onClickOrder}
            size={'sm'}
          />
        </div>
      </div>
    </div>
  )
}

export default GesturesBar