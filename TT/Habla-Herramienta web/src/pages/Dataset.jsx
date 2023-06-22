import React, { useState, useEffect } from 'react'
import { useSelector } from 'react-redux'
import { useRef } from 'react'

import { MdOutlineConnectWithoutContact, MdWavingHand, MdOutlineWatch} from 'react-icons/md'
import { HiOutlineViewGridAdd } from 'react-icons/hi'
import { RiSendPlane2Fill } from 'react-icons/ri'
import { TbPlugConnectedX } from 'react-icons/tb'
import { BiPackage } from 'react-icons/bi'
import { GiFinishLine } from 'react-icons/gi'
import { TfiPanel } from 'react-icons/tfi'
import { FaHandSpock, FaTrash } from 'react-icons/fa'
import { SiMicrobit } from 'react-icons/si'

import { styles } from '../content'
import { CircularIcon } from '../components'
import { dataset, connectionStatus, gestures } from '../content'

import { io } from 'socket.io-client'

const Dataset = () => {
    const ref = useRef({
        socket: null,
        socketEndpoint:'ws://192.168.1.142:5690',
    })

    //
    //  Phases:
    //      - Disconnected
    //      - Refused
    //      - Connected
    //      - Finished
    //
    //  Connection States
    //  0 - Disconnected
    //  1 - Pending
    //  2 - Connected
    //  3 - Finished
    //
    const [connectionState, setConnectionState] = useState(0)
    const [phase, setPhase] = useState('disconnected')
    const [nameNewSet, setNameNewSet] = useState('')
    const [addName, setAddName] = useState(false)
    const [microbitConnected, setMicrobitConnected] = useState(false)
    // -1 -> failed
    // 0 -> idle
    // 1 -> correct
    const [datasetConfig, setDatasetConfig] = useState({})
    const [gestureSaved, setGestureSaved] = useState(0)
    const [gesturePhoneme, setGesturePhoneme] = useState('a')

    let idTimerRequest = 0
    useEffect(()=>{
        // While disconnected
        if(connectionState == 1){
            // Starting connection
            ref.current.socket = io(ref.current.socketEndpoint, {
                path: '/ws/socket.io'
            })

            ref.current.socket.on('connect', () => {
                if (idTimerRequest) {clearTimeout(idTimerRequest); idTimerRequest = 0}
                console.log('Web socket client connected ...')
                let request = {
                    // Creates a new dataset
                    'new' : addName ? nameNewSet : ''
                }
                ref.current.socket.emit('current-configuration',request)
            });

            ref.current.socket.on('receive-configuration',(configuration) =>{
                setDatasetConfig(configuration)
                setGesturePhoneme(configuration.phoneme)
                setConnectionState(2)
                setPhase('connected')
                setAddName(false)
                setNameNewSet('')
            })

            idTimerRequest = setTimeout(()=>{
                setMicrobitConnected(false)
                setConnectionState(0)
                setPhase('refused')
                setNameNewSet('')
                setAddName(false)
                ref.current.socket.disconnect()
                ref.current.socket = io()
            },10000)
        }
        // While connected
        if(connectionState == 2){
            ref.current.socket.on('receive-configuration',(configuration) =>{
                setDatasetConfig(configuration)
                setGesturePhoneme(configuration.phoneme)
                if(configuration.newSample){
                    if (idTimerRequest) {clearTimeout(idTimerRequest); idTimerRequest = 0}
                    setGestureSaved(1)
                    idTimerRequest = setTimeout(()=>{setGestureSaved(0)},1500)
                }
            })

            ref.current.socket.on('sampling-ended',()=>{
                ref.current.socket.disconnect()
                setMicrobitConnected(false)
                setConnectionState(3)
                setPhase('finished')
                setNameNewSet('')
                setAddName(false)
            })

            ref.current.socket.on('microbit-connected', ()=>{
                setMicrobitConnected(true)
            })
        }
    },[connectionState])

    const language = useSelector(state => state.language)
    const data = dataset[language][phase] // UI Content
    const status = connectionStatus[language]
    const gesture = gestures[language][gesturePhoneme]

    return (
    <div className='w-full screen_height_no_menu relative'>
        <div className='screen_height_no_menu flex flex-col justify-center items-center'>
            {
                phase == 'disconnected'
                ? (
                    <>
                        <h2 className=' text-4xl text-gray-700'>{data.title}</h2>
                        <p className='text-xl text-gray-500 mt-4'>{data.subtitle}</p>
                        <MdOutlineConnectWithoutContact
                            className='text-primary text-9xl my-10'
                        />
                        <div className='flex justify-center items-center gap-8'>
                            <div className={` cursor-pointer ${styles.outlinedWide(styles.palettes.dark)}`}
                                onClick={()=>{setConnectionState(1)}}
                            >
                                {data.actions.connect}
                            </div>
                            <HiOutlineViewGridAdd
                                title='Crear nuevo conjunto'
                                className={`text-4xl cursor-pointer ${addName ? 'text-gray-400' : 'text-dark'}`}
                                onClick={()=>{setAddName((value)=>!value)}}
                            />
                        </div>
                        
                        { addName
                            ? (
                                <>
                                    <div className=' max-w-max'>
                                        <div className=' h-8 w-full rounded-md bg-gray-200 md:h-12 mt-12 flex items-center flex-wrap'>
                                            <input type='text' placeholder={data.name.placeholder} className=' grow text-sm px-4 py-2' value={nameNewSet} onChange={(value)=>{setNameNewSet(value.target.value)}} />
                                            <div className='h-full aspect-square bg-actions text-white text-2xl flex justify-center items-center rounded-r-lg cursor-pointer'>
                                            <RiSendPlane2Fill 
                                                onClick={()=>{setConnectionState(1)}}
                                            />
                                            </div>
                                        </div>
    
                                        <p className='text-xs mt-2 text-gray-600 break-words max-w-[500px]'>{data.name.description}</p>
    
                                    </div>
                                </>
                            )
                            : ('')
                        }
                    </>
                )
                : phase == 'refused' 
                ? (
                    <>
                        <TbPlugConnectedX className='text-9xl mb-8' />
                        <h2 className=' text-4xl text-gray-700'>{data.error}</h2>
                        <p className='text-xl text-gray-500 mt-4'>{data.message}</p>

                        <div 
                            className={` cursor-pointer mt-10 ${styles.outlinedWide(styles.palettes.dark)}`}
                            onClick={()=>{
                                setConnectionState(0)
                                setPhase('disconnected')
                            }}
                        >{data.retry}</div>
                    </>
                )
                : phase == 'connected' 
                ? (
                    datasetConfig?.name
                    ? <>
                        <div className={`fixed z-[80] rounded-lg bg-red bottom-5 right-5 px-6 py-4 text-white ${ gestureSaved == -1 ? 'bg-red-500' : (gestureSaved == 0 ? 'bg-primary' : 'bg-teal-500')}`}>
                            <div className='flex justify-center items-center my-2'><MdWavingHand className='text-highlight text-4xl'/><span className='text-center flex-1 text-5xl px-3'><b>{datasetConfig.repetitions}</b> <i className='text-2xl not-italic align-middle'>de</i>{datasetConfig.totalRepetitions}</span></div>
                            <p className='text-sm text-center mt-4'>Gesto ({datasetConfig.gesture}/{datasetConfig.totalGestures})</p>
                        </div>


                        <div className='relative z-[70] rounded-lg  mx-5 py-8 px-8 max-w-7xl w-full bg-white shadow-lg'>
                            {/* HEADER */}
                            <div className='flex justify-between items-center mb-4 px-2'>
                                <h2 className='text-gray-700 tracking-wide font-bold uppercase text-2xl'>{gesture?.name}</h2>
                                <div className='flex items-center gap-3'>
                                    <span className=' text-secondary text-lg first-letter:uppercase'>{datasetConfig.name}</span>
                                    <BiPackage 
                                        className='text-xl'
                                    />
                                </div>
                            </div>

                            <div className='grid grid-cols-3 grid-rows-2 gap-2 relative'>
                                <div className='aspect-4/3 relative col-span-2 row-span-2'>
                                    {/* Animation */}
                                    {/* https://stackoverflow.com/questions/63890401/play-pause-video-onscroll-in-reactjs */}
                                    <video
                                        alt="Video alt"
                                        loop="True"
                                        autoPlay="True"
                                        src={gesture.animation}
                                        poster={gesture.animationPlaceholder}
                                        className="w-full aspect-4/3"
                                    ></video>
                                </div>

                                <div className='row-span-2 px-4 h-full max-h-full flex flex-col justify-evenly'>
                                    {/* Phoneme and pronunciation */}
                                    <div className=' py-14 relative'>
                                        <h3 className='text-7xl text-center'>/<span className='text-primary'>{gesture?.phoneme}</span>/</h3>
                                        <p className=' pt-6 text-4xl text-gray-500 text-center'>{gesture?.spelling.join(', ')}</p>
                                    </div>

                                    <p className="text-gray-400 text-justify">{gesture?.description}</p>


                                    {/* <TfiPanel 
                                        className={`items-end text-2xl absolute -bottom-3 -right-3 cursor-pointer text-${showOps ? 'primary' : 'gray-500'}`}
                                        onClick={()=>(setShowOps(ops => !ops))}
                                    /> */}
                                </div>
                            </div>
                        </div>
                    </>
                    : ''
                )
                : phase == 'finished'
                ? (
                    <>
                        <div className='fixed z-[80] rounded-lg bg-red bottom-5 right-5 px-6 py-4 text-gray-700 cursor-pointer bg-highlight'
                        onClick={()=>{
                            setPhase('disconnected')
                            setConnectionState(0)
                            setAddName(true)
                            setNameNewSet('')
                            setDatasetConfig({})
                        }}
                        >
                            <MdOutlineWatch
                                className='text-gray-700 text-5xl mx-auto mb-2'
                            />
                            <p className='text-xs text-gray-600'>{data.new}</p>
                        </div>

                        <div className='w-full h-screen bg-white flex flex-col justify-center items-center'>
                            <GiFinishLine 
                                className=' text-8xl text-primary'
                            />
                            <h2 className='text-secondary text-3xl mt-10'>{data.title}</h2>
                            <p className='mt-4'>{data.subtitle}</p>
                        </div>


                    </>
                )
                : (
                    <p>Otra fase</p>
                )
            }
        </div>

        {/* Connection status */}
        <div className='absolute top-4 left-6 flex gap-4 items-center z-10'>
            <div className={` w-4 aspect-square rounded-full ${status[connectionState].background}`}></div>
            {/* <p>{status[connectionState].status}</p> */}
            {microbitConnected ? ( <SiMicrobit className={`text-3xl text-primary`}/> ) : ('') }
        </div>
    </div>
    )
}

export default Dataset