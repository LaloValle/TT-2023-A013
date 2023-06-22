import parse from 'html-react-parser'
import { BsFillMegaphoneFill } from "react-icons/bs"
import { GiPsychicWaves } from 'react-icons/gi'
import { useSelector } from 'react-redux'
import { headers } from "../content"
import CircularIcon from './CircularIcon'

const PhonemeCard = ({
    phoneme:data,
    layoutSimple=false,
    stateAnimation,
    onClickAnimation,
    stateAudio,
    onClickAudio
}) => {
    const language = useSelector(state => state.language)
    const titles = headers[language]

    const borderStyle = 'border-b-2 border-b-gray-300'

    const highlightAt = (text, index) => {
        if(typeof text === 'string') text = text.split('')
        text[index] = `<span className="text-primary font-semibold">${text[index]}</span>`
        return text
    }

  return (
    <div className={`grid items-center auto-rows-max grid-cols-2 ${layoutSimple ? `grid-rows-2 bg-white` : 'grid-rows-[1.25fr_max-content_1fr]'} shadow-xl filter-none rounded-2xl bg-gray-100 w-full h-full p-5 text-sm md:text-base`}>

        {data
            ? (<>
                <div className='col-span-2 w-full relative h-full flex items-center justify-center'>
                    <h2 className="text-6xl md:text-8xl bg-gray font-semibold text-secondary text-center col-span-2">/ <span className="text-primary">{data.phoneme}</span> /</h2>
                    
                    {
                        !layoutSimple
                        ? 
                            <CircularIcon 
                                icon={(<GiPsychicWaves className='text-base md:text-xl text-white'/>)}
                                hoverStyles={['bg-secondary']}
                                activeStyle={'bg-primary'}
                                extraStyles={'absolute top-1/2 bg-gray-400 left-2 my-2 z-30'}
                                onClickHandler={onClickAnimation}
                                active={stateAnimation}
                            />
                            
                        : ''
                    }
                    <CircularIcon 
                        icon={(<BsFillMegaphoneFill className='text-base md:text-xl text-white'/>)}
                        hoverStyles={['bg-secondary']}
                        activeStyle={'bg-primary'}
                        extraStyles={`absolute  bg-gray-400 ${layoutSimple ? 'right-2 translate-y-1/2 bottom-0' : 'left-2 my-2 bottom-1/2'} z-30`}
                        onClickHandler={onClickAudio}
                        active={stateAudio}
                    />
                </div>

                {
                    !layoutSimple
                    ? (
                        <div className={`w-full col-span-2 flex justify-between py-4 ${borderStyle}`}>
                            <h5 className='text-sm md:text-base font-semibold'>{titles.order}</h5>
                            <p className='text-sm md:text-base text-gray-500'>{data.order}</p>
                        </div>
                    ) : ''
                }

                <div className={`col-span-2 relative h-full flex flex-col ${borderStyle}`}>
                    {
                        !layoutSimple
                        ? <h5 className='text-sm md:text-base font-semibold py-3'>{titles.letters}</h5>
                        : ''
                    }
                    <h3 className="text-4xl pb-4 text-gray-700 justify-self-center flex items-center justify-center grow">{data.associated.join(', ')}</h3>
                </div>
                
                {
                    !layoutSimple
                    ? <h5 className='text-sm md:text-base font-semibold py-3'>{titles.examples}</h5>
                    : ''
                }

                {data.examples.map(({word, phonemes:symbol, highlight},i) => (
                    <div className='text-sm md:text-base w-full col-span-2 grid grid-cols-2 text-gray-400 border-b-gray-300 border-b-2 py-2 text-center'>
                        <p className='text-base md:text-lg'>{word}</p>
                        <p className='text-base md:text-lg'>
                            / { parse(
                                ((word,index) => { 
                                    let arrayWord = word.split('')
                                    index.map((i) => arrayWord = highlightAt(arrayWord, i))
                                    return arrayWord.join('')
                                })(symbol, highlight)
                            )} /
                        </p>
                    </div>
                ))}
            </>) : 
                ''
        }
    </div>
  )
}

export default PhonemeCard