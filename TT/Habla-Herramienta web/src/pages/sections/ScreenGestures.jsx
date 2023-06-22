import React, { useState, useEffect } from 'react'
import { FaHandSpock } from 'react-icons/fa'

const ScreenGestures = ({gesture, onCloseGesture = ()=>''}) => {
    const [isShown, setIsShown] = useState(false)
    const spelling = gesture?.spelling ? gesture.spelling.join(', ') : ''

    useEffect(()=>{
        if(gesture?.phoneme)
            setIsShown(true)
    },[gesture])

    return (
        <div 
            className={`fixed top-0 left-0 w-full bg-black/50 h-screen z-[60] flex justify-center items-center px-4 py-7 ${isShown ? 'block' : 'hidden'}`}
        >
            <div className='absolute top-0 left-0 w-full h-full z-[60] ' onClick={() => {
                setIsShown(false)
                onCloseGesture()
            }}></div>

            <div className='relative z-[70] rounded-lg bg-white py-8 px-8 max-w-5xl w-full'>
                {/* HEADER */}
                <div className='flex justify-between items-center mb-4 px-4'>
                    <h2 className='text-gray-700 tracking-wide font-bold uppercase text-2xl'>{gesture?.name}</h2>
                    <div className='flex items-center'>
                        <span className=' text-primary first-letter:uppercase'>{gesture?.nature}</span>
                        <div className='ml-2 text-xs bg-primary text-white w-6 h-6 rounded-full flex justify-center items-center'>{gesture?.category}</div>
                    </div>
                </div>

                <div className='grid grid-cols-3 grid-rows-2 gap-2'>
                    <div className='aspect-4/3 relative col-span-2 row-span-2'>
                        {/* Animation */}
                        {/* https://stackoverflow.com/questions/63890401/play-pause-video-onscroll-in-reactjs */}
                        <video
                            alt="Video alt"
                            loop="True"
                            autoPlay="True"
                            src={gesture.animation}
                            poster={gesture.animationPlaceholder}
                            className="w-full aspect-4/3 cursor-pointer"
                        ></video>
                    </div>

                    <div className='row-span-2 px-4 h-full max-h-full'>
                        {/* Phoneme and pronuntiation */}
                        <div className=' py-14 relative'>
                            <h3 className='text-7xl text-center'>/<span className='text-primary'>{gesture?.phoneme}</span>/</h3>
                            <p className=' pt-6 text-4xl text-gray-500 text-center'>{spelling}</p>
                        </div>

                        <div className='flex justify-between items-center'>
                            <FaHandSpock
                                className=' text-3xl text-gray-400'
                            />

                            <div className='flex gap-6'>
                                {[1,2,3].map((index) => (
                                    <div className={`rounded-full w-6 h-6 ${gesture?.dificulty - index >= 0 ? 'bg-actions' : 'bg-gray-300'}`}></div>
                                ))}
                            </div>
                        </div>

                        <hr className='h-[1px] w-full bg-gray-500 my-6'/>

                        <p className="text-gray-400 text-justify">{gesture?.description}</p>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default ScreenGestures