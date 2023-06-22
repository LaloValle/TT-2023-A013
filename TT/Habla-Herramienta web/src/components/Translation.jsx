import { useState } from "react"
import { IoMale, IoFemale } from 'react-icons/io5'
import CircularIcon from "./CircularIcon"
import PlayControls from "./PlayControls"

import { hola } from "../assets"
import { styles, rootContent as content } from "../content"
import { useSelector } from "react-redux"

const toPhonemes = (word) => 'actuar'

const Translation = () => {
    const language = useSelector(state => state.language)
    const settings = content.voice[language].liveTool
    
    const [wordPhonemes, setWordPhonemes] = useState(toPhonemes(settings.field.value))
    const [paintedPhonemes, setPaintedPhonemes] = useState('/')
    const [sex, setSex] = useState('m')

    /* Painted Phonemes functions */
    const paintNextPhoneme = () => {
        let aux_str = '/'
        aux_str += wordPhonemes.substring(0, paintedPhonemes.length)
        /* console.log('painted >',paintedPhonemes.length, '  word > ',wordPhonemes.length) */
        if(paintedPhonemes.length === (wordPhonemes.length+1)) aux_str += '/' // Las character added
        else if(paintedPhonemes.length > wordPhonemes.length) return false // Al ready printed whole
        setPaintedPhonemes(aux_str)
    }
    const resetNextPhoneme = () => setPaintedPhonemes('/')

    /* Word */
    const newWordPhonemes = (word) => {
        // Stop the reproduction of the animation
        // Translates to phonemes
        //  Should be used the function to translate
        setWordPhonemes(word)
        // Verifies if the already painted string is a subset of the new word
        /* console.log(paintedPhonemes,`/${word}`,`/${word}`.match(paintedPhonemes)) */
        if(`/${word}`.match(paintedPhonemes)) return true // No change needed
        else resetNextPhoneme()
    }

    // Events handlers
    const clickMale = () => {
        setSex('m')
    }
    const clickFemale = () => {
        setSex('f')
        paintNextPhoneme()
    }

  return (
    <div className='flex flex-col-reverse md:flex-row text-white items-center md:bg-dark rounded-lg md:mx-auto md:w-full h-max md:h-full text-sm md:text-base md:px-8 md:py-4'>
        
        {/* Settings section */}
        <div className="grid grid-cols-2 grid-rows-grid-rows-[max-content_1fr_max_content_repeat(2,1fr)] gap-y-4 min-w-[350px] md:w-1/2 md:h-full">
            <label htmlFor='translate_word' className="text-sm text-gray-400">{settings.field.name}</label>
            <p className="text-xs md:text-sm text-gray-400 justify-self-center">{settings.phonemes}</p>

            <input id='translate_word' type='text' className={`${styles.outlined(styles.palettes.dark)} col-start-1`} defaultValue={settings.field.value} 
                onChange={(e) => newWordPhonemes(e.target.value.toLowerCase())}
            />
            <div className="col-start-2 relative w-max mx-auto">
                <span className="text-2xl md:text-3xl text-gray-400 w-full inline-block text-center align-middle tracking-wider" >{`/${wordPhonemes}/`}</span>
                <span className="absolute top-0 left-0 text-2xl md:text-3xl text-left text-highlight w-full inline-block align-middle tracking-wider" > {paintedPhonemes}</span>
            </div>

            <hr className='h-1 text-white col-span-2 col-start-1' />

            <h4 className="text-semibold text-highlight col-start-1 col-span-2">{settings.voiceSettings}</h4>

            <div className="col-start-1 flex justify-evenly items-center row-span-2 h-full w-full">
                <CircularIcon 
                    icon={(<IoMale className='text-2xl md:text-3xl lg:text-4xl'/>)}
                    hoverStyles={['bg-secondary']}
                    activeStyle={'bg-primary'}
                    onClickHandler={clickMale}
                    active={sex == 'm'}
                    size='lg'
                    />
                <CircularIcon 
                    icon={(<IoFemale className='text-2xl md:text-3xl lg:text-4xl'/>)}
                    onClickHandler={clickFemale}
                    hoverStyles={['bg-secondary']}
                    activeStyle={'bg-pink-400'}
                    active={sex == 'f'}
                    size='lg'
                />
            </div>

            <select name="voiceName" className={`col-start-2 ${styles.outlined(styles.palettes.dark)}`}>
                <option>Dummy</option>
            </select>
            <select name="voiceAge" className={`col-start-2 ${styles.outlined(styles.palettes.dark)}`}>
                <option>Young</option>
            </select>
        </div>

        {/* Animation and controls section */}
        <div className="flex flex-col w-full min-w-[350px] md:h-full md:min-w-0 md:w-1/2">

            {/* Animation div */}
            <div className='w-full h-full relative'>
                <img src={hola} alt="Saludo" className='w-full max-w-[400px] md:max-w-max aspect-auto relative mx-auto md:mx-0 md:absolute md:left-0 md:bottom-0'/>
                <div className='w-full h-full absolute top-0 left-0 z-20 bg-gradient-to-t md:from-dark from-secondary'></div>
            </div>

            <div>
                <PlayControls />
            </div>
        </div>
    </div>
  )
}

export default Translation