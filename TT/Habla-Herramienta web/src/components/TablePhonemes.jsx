import parse from 'html-react-parser'
import { useSelector } from 'react-redux'
import { toStyles } from '../content'
import { phonemes, headers } from "../content"

const RowPhoneme = ({data, index, activeIndex, columns, onClickHandler=()=>'', activeStyle='', hoverStyles=[], gridCols=''}) => {

    return (
        <div className={`col-span-full w-full grid ${gridCols ? gridCols : `grid-cols-${columns.length}` }  ${index%2 == 0 ? 'bg-gray-300' : 'bg-white'} ${index === activeIndex ? activeStyle : hoverStyles ? toStyles(hoverStyles, 'hover:') : ''} ${activeIndex >= 0 ? 'cursor-pointer' : ''}`} onClick={()=>onClickHandler(index)}>
            {columns.map((col) => (
                <p className={`text-sm px-4 py-3 w-full h-full align-middle text-center`}>
                    {
                        col === 'examples'
                        ? parse(data[col].reduce((cumulative,{word,phonemes}) => cumulative + ` ${word} / <span className='text-primary'>${phonemes}</span> /,`, '').slice(0, -1))
                        : typeof data[col] === 'string'
                            ? col === 'phoneme' ? `/ ${data[col]} /` : ''
                            : data[col].join(', ')
    
                    }
                </p>
            ))}
        </div>
    )
}

const TablePhonemes = ({phonemes: symbols, headers: columns, gridCols='', onClickHandler=()=>'', extraStyles='', hoverStyles=[], activeStyle='', activeIndex=-1}) => {
    const language = useSelector(state => state.language)
    const titles = headers[language]

  return (
    <div className={`w-full gap-y-1 grid ${gridCols ? gridCols : `grid-cols-${columns.length}` } auto-rows-max items-center justify-items-center ${extraStyles ? extraStyles : ''}`}>
        {
            /* Headers */
            columns.map((col) => (
                <h4 key={Math.random()} className="font-semibold w-full text-center text-sm row-start-1 px-2 py-2">{titles[col]}</h4>
            ))
        }

        {
            symbols.map((symbol,i) => {
                return <RowPhoneme 
                    data={symbol}
                    index={i}
                    activeIndex={activeIndex} // State
                    columns={columns}
                    onClickHandler={onClickHandler}
                    activeStyle={activeStyle}
                    hoverStyles={hoverStyles}
                    gridCols={gridCols}
                />
            } )
        }
    </div>
  )
}

export default TablePhonemes