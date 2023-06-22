import { rootContent as content } from "../../content"
import { Link } from 'react-router-dom'
import { GrOverview } from 'react-icons/gr'
import { TablePhonemes, PhonemeCard } from "../../components"
import { useSelector } from "react-redux"

const MainPhonemes = () => {
    const language = useSelector(state => state.language)
    const phonemes = content.phonemes[language]

  return (
    <section id='phonemes' className='container main-section light right grid-rows-[repeat(3,max-content)_minmax(160px,1fr)_max-content]'>
        <div className='relative row-start-4 mt-4 md:mt-0 md:col-start-1 md:row-start-1 md:row-span-5 w-full min-h-[450px] h-[40vh] overflow-hidden'>
          {
            phonemes.liveTool.cardsPhonemes.map((symbol,i) => (
              <div key={i} className='phoneme-card max-w-[300px] pb-10 h-full w-full absolute bottom-0 left-1/2 -translate-x-1/2'>
                <PhonemeCard
                  phoneme={symbol}
                  layoutSimple={true}
                />
              </div>
            ))
          }
          
        </div>

        <h2 className="title">{phonemes.title}</h2>
        <h3 className="subtitle">{phonemes.subtitle}</h3>
        <p className="description">{phonemes.description}</p>
        
        <div className="w-full h-full py-2 md:py-4 flex items-center">
          <TablePhonemes 
            phonemes={phonemes.liveTool.tablePhonemes}
            headers={['phoneme','associated','examples']}
            gridCols='grid-cols-[max-content_max-content_1fr]'
          />  
        </div>
        
        <Link to='fonemas' className="plain-icon-button inactive ml-auto my-4 md:my-6 bg-gray-100">{phonemes.link} <GrOverview className="text-lg ml-2" /> </Link>
    </section>
  )
}

export default MainPhonemes