import { useState, useEffect, useRef } from 'react'
import { useSelector } from 'react-redux'

import { GiFrog } from 'react-icons/gi'
import { MdWavingHand } from 'react-icons/md'
import { IoIosHelpBuoy } from 'react-icons/io'
import { BsArrowRepeat } from 'react-icons/bs'
import { RiUserVoiceFill } from 'react-icons/ri'
import { TbPlugConnectedX } from 'react-icons/tb'
import { SiMicrobit,SiGooglecloud } from 'react-icons/si'
import { FaRaspberryPi,FaPiedPiperPp } from 'react-icons/fa'

import { translate, translateStatus, gestures, styles } from '../content'
import { CircularIcon } from '../components'

import { io } from 'socket.io-client'

//
//  Auxiliar Components
//
const SpecialPhonemes = ({setFunction, size, hoverBackground}) => {
    const sizes = {
        sm : {
            dim : '8',
            pt : '2',
            pr : '8',
            gap : '3',
        },
        lg : {
            dim : '8',
            pt : '8',
            pr : '8',
            gap : '5',
        },
    }
    const styles = sizes[size]
    return (
        <div className={`absolute z-[80] w-min top-0 right-0 flex justify-end pt-${styles.pt} pr-${styles.pr} gap-${styles.gap}`}>
            <span 
                className={`text-${size} font-bold text-gray-600 w-${styles.dim} aspect-square flex justify-center items-center hover:${hoverBackground} cursor-pointer rounded-full transition-colors`}
                onClick={()=>{setFunction(value => value+'ʧ')}}
            >
                ʧ
            </span>
            <span 
                className={`text-${size} font-bold text-gray-600 w-${styles.dim} h-${styles.dim} flex justify-center items-center hover:${hoverBackground} cursor-pointer rounded-full transition-colors`}
                onClick={()=>{setFunction(value => value+'ɲ')}}
            >
                ɲ
            </span>
            <span 
                className={`text-${size} font-bold text-gray-600 w-${styles.dim} h-${styles.dim} flex justify-center items-center hover:${hoverBackground} cursor-pointer rounded-full transition-colors`}
                onClick={()=>{setFunction(value => value+'ɾ')}}
            >
                ɾ
            </span>
        </div>
    )
}
const SimplifiedGestureCard = ({data}) => {
  return (
    <div
        className={`w-full h-max rounded-xl p-3 flex flex-col`}
    >
        {/* Video animation */}
        <div className='w-full aspect-4/3 relative'>
            {/* Animation */}
            <video
                alt="Video alt"
                loop="True"
                autoPlay="True"
                src={data.animation}
                poster={data.animationPlaceholder}
                className="w-full aspect-4/3 shadow-md"
            ></video>
        </div>

        {/* info */}
        <div className="w-full py-1 px-2 flex justify-between items-center">
            <span className={`text-xl text-semibold text-primary`}>{data.name}</span>
            <div className='flex gap-3'>
                {[1,2,3].map((index) => (
                    <div className={`rounded-full w-3 h-3 ${data?.dificulty - index >= 0 ? 'bg-actions' : 'bg-gray-300'}`}></div>
                ))}
            </div>
        </div>
    </div>
  )
}
const PhonemeGesture = ({phoneme, index, actualIndex, clickHandler}) => {
    return (
        <div key={index} className={` text-8xl cursor-pointer ${index == actualIndex ? 'font-bold ' : 'font-normal'} ${index <= actualIndex ? 'text-primary' : 'text-gray-700'}`} onClick={()=>clickHandler(index)}>{phoneme}</div>
    )
}
const PhonemesGesture = ({phonemes, actualIndex, clickHandler}) => {
    return (
        <div className='flex justify-center items-center gap-2 w-full h-full'>
            {
                phonemes.map((phoneme,index) => (
                        <PhonemeGesture 
                            phoneme={phoneme}
                            index={index}
                            actualIndex={actualIndex}
                            clickHandler={clickHandler}
                        />
                ))
            }
        </div>
    )
}
const SpeakerOption = ({icon, index, actualIndex, clickHandler}) => {
    return (
        <div key={index} className={` w-14 h-14 flex justify-center items-center cursor-pointer rounded-none  ${index == actualIndex ? 'bg-primary' : 'bg-gray-100 hover:bg-gray-200'} ${index == 0 ? 'rounded-r rounded-xl ' : index == 2 ? 'rounded-l rounded-xl ' : ''}`} onClick={()=>clickHandler(index)}>{icon}</div>
    )
}

const Translate = () => {
    const ref = useRef({
        socket: null,
        timeoutPhonemes : 0,
        socketEndpoint:'ws://192.168.1.74:6614',
        // socketEndpoint:'ws://192.168.1.64:6614',
        speakers: ['gcp','piper','coqui']
    })

    const language = useSelector(state => state.language)
    const data = translate[language] // UI Content
    const gesturesList = gestures[language]
    const phonemes = Object.keys(gesturesList).filter(phoneme => phoneme.length == 1)

    const [connectionStatus,setConnectionStatus] = useState(-1)
    const [configPath, setConfigPath] = useState('./Traductor/Modelo/Configuracion.json')
    const [phonemesString,setPhonemesString] = useState('exemplo')
    const [phonemesWord, setPhonemesWord] = useState('Ejemplo')
    const [correctWord,setCorrectWord] = useState(true)
    const [translateString,setTranslateString] = useState('')
    const [translateList,setTranslateList] = useState([])
    const [translateIndex,setTranslateIndex] = useState(-1)
    const [translateGesture, setTranslateGesture] = useState('')
    const [translateToGestures, setTranslateToGestures] = useState(true)
    const [raspberryConnected, setRaspberryConnected] = useState(false)
    const [playingBackVoice, setPlayingBackVoice] = useState(false)
    const [speaker, setSpeaker] = useState(1)
    const [isPhoneme, setIsPhoneme] = useState(true)

    const status = translateStatus[language][connectionStatus >= 0 ? connectionStatus : 0] // Just to avoid problems with the initial status value

    // Auxiliar functions
    const is_phoneme = character =>  phonemes.includes(character)

    // Event handlers
    const clickTranslate = (index) => {
        if(translateList.length > 0){
            setTranslateIndex(index)
            setTranslateGesture(gesturesList[translateList[index]])
        }
    }
    const clickPlaybackVoice = () => {
        if(! playingBackVoice){
            setPlayingBackVoice(true)
            ref.current.socket.emit('playback-voice',{phonemes : phonemesString.split('')})
        }
    }
    const changeInputPhonemes = (event) => {
        let value = String(event.target.value)
        // First evaluates if add special characters
        let lastPhoneme = value[value.length-1]
        if(lastPhoneme == 'r'){
            // 'r'
            if(value.length > 1 && value[value.length-2] == 'ɾ') value = value.slice(0,-2)+'r'
            // 'ɾ'
            else value = value.slice(0,-1) + 'ɾ'
            lastPhoneme = 'r'
        }
        if(lastPhoneme == 'ñ'){
            // 'ɲ'
            value = value.slice(0,-1) + 'ɲ'
            lastPhoneme = 'ɲ'
        }
        if(lastPhoneme == 'h'){
            // 'ʧ'
            value = value.slice(0,-1) + 'ʧ'
            lastPhoneme = 'ʧ'
        }
        // Normal phonemes
        if(is_phoneme(lastPhoneme) || value == '') setPhonemesString(value)
        // Correct word
        if(ref.current.timeoutPhonemes) clearTimeout(ref.current.timeoutPhonemes)
        ref.current.timeoutPhonemes = setTimeout(() => ref.current.socket.emit('phonemes-word',{phonemes:value.split('')}), 1500)
    }

    let idTimerRequest = 0
    useEffect(()=>{
        if(translateList.length > 0 && translateIndex == -1) clickTranslate(0)
        if(ref.current.socket) ref.current.socket.emit('set-speaker',{'speaker':ref.current.speakers[speaker]})
        if(ref.current.socket) ref.current.socket.emit('set-translating-type',{'translating': isPhoneme ? 'phoneme' : 'word'})
        
        //
        // Socket
        //
        // While pending
        if(connectionStatus == 1){
            idTimerRequest = setTimeout(()=>{
                setConnectionStatus(0)
                ref.current.socket.disconnect()
                ref.current.socket = io()
            },10000)
            console.log(`Timer >> ${idTimerRequest}`)

            // Starting connection
            ref.current.socket = io(ref.current.socketEndpoint, {
                path: '/ws/socket.io'
            })

            ref.current.socket.on('connect', () => {
                if (idTimerRequest) {clearTimeout(idTimerRequest); idTimerRequest = 0; console.log('Timer resolved')}
                const request = { path : configPath ? configPath : 'd', speaker : ref.current.speakers[speaker] }
                ref.current.socket.emit('current-configuration',request)
            });

            ref.current.socket.on('configured', () => {
                setConnectionStatus(2)
            })
        }
        // While waiting
        if(connectionStatus == 2){
            ref.current.socket.on('microbit-connected',()=>{
                setConnectionStatus(3)
                setPhonemesString('')
            })

            ref.current.socket.on('raspberry-connected',()=>{
                setRaspberryConnected(true)
            })

            ref.current.socket.on('playback-finished',()=>{
                setPlayingBackVoice(false)
            })

            ref.current.socket.on('correct-word',(correction) => {
                setPhonemesWord(correction.word)
                setCorrectWord(correction.correct)
            })
        }
        // While connected
        if(connectionStatus == 3){
            ref.current.socket.on('raspberry-connected',()=>{
                setRaspberryConnected(true)
            })
            
            ref.current.socket.on('predicted-phonemes',received =>{
                const {phonemes,word} = received
                setPhonemesString(phonemes)
                if (received?.word) setPhonemesWord(word)
                // Guided help
                if(translateList.length > 0 && phonemes.length < translateList.length){
                    let sliced = translateList.slice(0,phonemes.length).join('')
                    if(sliced == phonemes)
                        clickTranslate(phonemes.length)
                }
            })

            ref.current.socket.on('microbit-disconnected', ()=>{
                setConnectionStatus(2)
                setPhonemesString('exemplo')
                setPhonemesWord('Ejemplo')
            })

            ref.current.socket.on('playback-finished',()=>{
                setPlayingBackVoice(false)
            })

            ref.current.socket.on('correct-word',(correction) => {
                setPhonemesWord(correction.word)
                setCorrectWord(correction.correct)
            })
        }

    },[connectionStatus, translateList, speaker, isPhoneme])


    return (
        <div className='w-screen screen_height_no_menu relative'>
            
            {
                // Refused
                connectionStatus == 0
                ? (
                    <div className='screen_height_no_menu flex flex-col justify-center items-center'>
                        <TbPlugConnectedX className='text-9xl mb-8' />
                        <h2 className=' text-4xl text-gray-700'>{data.error}</h2>
                        <p className='text-xl text-gray-500 mt-4'>{data.errorMessage}</p>

                        <div 
                            className={`cursor-pointer mt-10 ${styles.outlinedWide(styles.palettes.dark)}`}
                            onClick={()=>{
                                setConnectionStatus(1)
                            }}
                        >{data.retry}</div>
                    </div>
                )
                // Pending, waiting micro:bit, connected micro:bit
                : connectionStatus >= 1 || connectionStatus == -1
                ? (
                    <div className='w-full screen_height_no_menu relative flex flex-col'>
                        {/* 
                            Connection modal window
                        */}
                        {
                            // Before connection
                            connectionStatus == -1
                            ? (
                                <div className='w-full screen_height_no_menu absolute top-0 left-0 bg-black/30 z-[100] flex justify-center items-center'>

                                    <div className='px-12 pt-10 py-16 w-min relative rounded-md shadow-lg bg-white flex flex-col justify-center items-center'>
                                        <p className='text-xl pb-6 '>Ingresa la ruta de la configuración</p>

                                        <div className='flex justify-center items-center'>
                                            <input type='text' className='px-3 py-2 w-96 bg-gray-200 rounded-l-md' placeholder="Configuración por defecto 'd'" value={configPath} onChange={event => setConfigPath(event.target.value)}></input>
                                            <div className='bg-highlight h-full px-4 py-2 cursor-pointer rounded-r-md' onClick={()=>(setConnectionStatus(1))}>
                                                <TbPlugConnectedX className='text-gray-700 text-2xl'/>
                                            </div>
                                        </div>

                                        <div className='bg-highlight rounded-b-md absolute bottom-0 left-0 h-6 w-full'></div>
                                    </div>
                                </div>
                            )
                            : (
                                ''
                            )
                        }

                        {/* 
                            Phonemes String
                        */}
                        <div className='w-full relative flex flex-col flex-grow'>
                            {/* Input phonemes */}
                            <input className='absolute top-0 left-0 w-full h-full z-50 opacity-0 cursor-default' type='text' value={phonemesString} readOnly={connectionStatus != 2 ? true : false} onChange={event => changeInputPhonemes(event)}></input>

                            {
                                connectionStatus == 3
                                ? (
                                    <>
                                        <div className='w-full mt-10 flex justify-center items-center relative z-50 cursor-pointer'>
                                            <span className={`px-5 py-3 rounded-r rounded-xl text-sm ${isPhoneme ? 'bg-actions text-white' : 'bg-gray-300'}`} onClick={() => setIsPhoneme(value => !value)}>Fonema</span>
                                            <span className={`px-5 py-3 rounded-l rounded-xl text-sm ${!isPhoneme ? 'bg-actions text-white' : 'bg-gray-300'}`} onClick={() => setIsPhoneme(value => !value)}>Palabra</span>
                                        </div>
                                        <div className='flex absolute top-10 right-10 z-50'>
                                            {/* GCP */}
                                            <SpeakerOption
                                                icon={(<SiGooglecloud className={`text-2xl cursor-pointer ${speaker == 0 ? 'text-white' : 'text-gray-500'}`}/>)}
                                                index={0}
                                                actualIndex={speaker}
                                                clickHandler={setSpeaker}
                                            />
                                            {/* Piper */}
                                            <SpeakerOption
                                                icon={(<FaPiedPiperPp className={`text-2xl ${speaker == 1 ? 'text-white' : 'text-gray-500'}`}/>)}
                                                index={1}
                                                actualIndex={speaker}
                                                clickHandler={setSpeaker}
                                            />
                                            {/* Coqui TTS */}
                                            <SpeakerOption
                                                icon={(<GiFrog className={`text-2xl ${speaker == 2 ? 'text-white' : 'text-gray-500'}`}/>)}
                                                index={2}
                                                actualIndex={speaker}
                                                clickHandler={setSpeaker}
                                            />
                                        </div>
                                    </>
                                )
                                : (
                                    ''
                                )
                            }

                            <div className='flex flex-col relative z-10 justify-center gap-20 flex-grow'>
                                {
                                    isPhoneme
                                    ? (
                                        <>
                                            <div className='relative flex justify-center items-center gap-5'>
                                                <span className='bg-white text-secondary text-9xl'>/</span>
                                                <span className='bg-whiteinline-block text-9xl font-bold text-primary'>{phonemesString}</span>
                                                <span className='bg-white text-secondary text-9xl'>/</span>
                                            </div>
                                            <div className='text-center'>
                                                <span className={`inline-block pt-9 text-4xl border-t-gray-200 border-t-2 ${correctWord ? 'text-gray-400' : 'text-red-300'}`}>{phonemesWord}</span>
                                            </div>
                                        </>
                                    )
                                    : (
                                        <div className='relative flex justify-center items-center gap-5'>
                                            <span className='bg-whiteinline-block text-9xl font-bold text-primary'>{phonemesString}</span>
                                        </div>

                                    )
                                }
                            </div>

                            {/* Actions options */}
                            <div className='w-max h-max absolute bottom-0 left-8 z-[80]'>
                                <CircularIcon
                                    icon={(<RiUserVoiceFill className={`text-xl ${playingBackVoice ? 'text-white' : 'text-gray-700'}`}/>)}
                                    hoverStyles={['bg-gray-200']}
                                    active={playingBackVoice}
                                    activeStyle={'bg-primary'}
                                    onClickHandler={clickPlaybackVoice}
                                />
                                {
                                    connectionStatus == 3 
                                    ? (
                                        <CircularIcon
                                            icon={(<BsArrowRepeat className='text-xl text-gray-700'/>)}
                                            hoverStyles={['bg-gray-200']}
                                        />
                                    )
                                    : ('')
                                }
                                <div className={`rounded-t-full p-4 text-3xl text-gray-700 cursor-pointer ${translateToGestures ? 'bg-gray-200' : 'bg-white'}`}
                                    onClick={()=>{setTranslateToGestures(value => !value)}}
                                >
                                    <MdWavingHand />
                                </div>
                            </div>
                        </div>

                        {/* 
                            Phonemes to gestures
                        */}
                        <div className='col-span-2'>
                            {
                                translateToGestures 
                                ? (
                                    // <div className='bg-gray-200 mx-8 mb-4 rounded-lg relative'>
                                    //     {/* Special characters phonems */}
                                    //     <div className='absolute z-[80] top-0 right-0 flex justify-end pt-4 pr-8 gap-3'>
                                    //         <span 
                                    //             className='text-sm font-bold text-gray-600 w-8 h-8 flex justify-center items-center hover:bg-gray-300 cursor-pointer rounded-full transition-colors'
                                    //             onClick={()=>{setTranslateString(value => value+'ʧ')}}
                                    //         >
                                    //             ʧ
                                    //         </span>
                                    //         <span 
                                    //             className='text-sm font-bold text-gray-600 w-8 h-8 flex justify-center items-center hover:bg-gray-300 cursor-pointer rounded-full transition-colors'
                                    //             onClick={()=>{setTranslateString(value => value+'ɲ')}}
                                    //         >
                                    //             ɲ
                                    //         </span>
                                    //         <span 
                                    //             className='text-sm font-bold text-gray-600 w-8 h-8 flex justify-center items-center hover:bg-gray-300 cursor-pointer rounded-full transition-colors'
                                    //             onClick={()=>{setTranslateString(value => value+'ɾ')}}
                                    //         >
                                    //             ɾ
                                    //         </span>
                                    //     </div>

                                    //     <div className='pt-12 pb-6 px-3 flex justify-center items-center'>
                                    //         {/* Input */}
                                    //         <div className='relative w-full max-w-3xl'>
                                    //             <span className='absolute -top-7 left-3'>{data.name}</span>
                                                
                                    //             <input type='text' className='px-6 py-2 w-full bg-gray-100 text-gray-800 rounded-l-md' placeholder={data.placeholder} value={translateString} onChange={(event)=>{{if(is_phoneme(event.target.value[event.target.value.length-1]) || event.target.value == '') setTranslateString(event.target.value)}}}></input>
                                    //         </div>
                                    //         <div className='bg-highlight h-full px-4 py-2 cursor-pointer rounded-r-md'><IoIosHelpBuoy className='text-gray-700 text-2xl'/></div>
                                    //     </div>

                                    //     {/* List of gestures */}
                                    //     <div className='max-w-full overflow-x-auto px-10 pb-4 flex gap-5'>
                                    //         {
                                    //             translateString.split('').map(phoneme => (
                                    //                 <div className=' w-60 aspect-4/3 flex-shrink-0'>
                                    //                     <SimplifiedGestureCard data={gesturesList[phoneme]}/>
                                    //                 </div>
                                    //             ))
                                    //         }
                                    //     </div>  
                                    // </div>
                                    <div className='bg-gray-200 mx-8 mb-4 rounded-b-lg rounded-r-lg'>
                                        <div className='grid grid-cols-[1fr_minmax(250px,400px)] relative max-w-7xl mx-auto pt-4'>
                                            <div className='flex flex-col'>
                                                <div className='pt-12 pb-6 px-3 flex justify-center items-center relative'>
                                                    {/* Special characters phonems */}
                                                    <SpecialPhonemes setFunction={setTranslateString} size={'sm'} hoverBackground={'bg-gray-300'}/>

                                                    {/* Input */}
                                                    <div className='relative w-full max-w-3xl'>
                                                        <span className='absolute -top-7 left-3'>{data.name}</span>
                                                        <input type='text' className='px-6 py-2 w-full bg-gray-100 text-gray-800 rounded-l-md' placeholder={data.placeholder} value={translateString} onChange={(event)=>{{if(is_phoneme(event.target.value[event.target.value.length-1]) || event.target.value == '') setTranslateString(event.target.value)}}}></input>
                                                    </div>
                                                    <div className='bg-highlight h-full px-4 py-2 cursor-pointer rounded-r-md'
                                                        onClick={()=>{
                                                            // Clean
                                                            setTranslateIndex(-1)
                                                            setTranslateList([])
                                                            if(translateString){
                                                                setTranslateList(translateString.split(''))
                                                                clickTranslate(0)
                                                            }
                                                        }}
                                                    >
                                                        <IoIosHelpBuoy className='text-gray-700 text-2xl'/>
                                                    </div>

                                                </div>
                                                {/* Phonemes - gestures */}
                                                {
                                                    translateList.length > 0
                                                    ? (
                                                        <div className='flex-grow'>
                                                            <PhonemesGesture 
                                                                phonemes={translateList}
                                                                actualIndex={translateIndex}
                                                                clickHandler={clickTranslate}
                                                            />
                                                        </div>
                                                    )
                                                    : (
                                                        ''
                                                    )
                                                }
                                                
                                            </div>

                                            {

                                                translateList.length > 0 
                                                ? (
                                                    <div className=' w-full aspect-4/3 flex-shrink-0'>
                                                        <SimplifiedGestureCard data={translateGesture}/>
                                                    </div>
                                                )
                                                : (
                                                    ''
                                                )
                                            }
                                        </div>
                                    </div>
                                )
                                : (
                                    ''
                                )
                            }
                        </div>
                    </div>
                )
                : (
                    ''
                )
            }

            
            <div className='absolute top-12 left-12 flex items-center gap-2'>
                {connectionStatus <= 1 
                    ?( <div className={`w-3 h-3 rounded-full inline-block ${status.color}`}></div> )
                    : ( 
                        <>
                            <SiMicrobit className={`text-3xl ${status.color}`}/>
                            <FaRaspberryPi className={`text-3xl ${raspberryConnected ? 'text-[#e30b5d]' : 'text-gray-400'}`}/>
                        </>
                    )
                }
                {/* <span>{status.status}</span> */}
            </div>
        </div>
    )
}

export default Translate