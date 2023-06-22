import { useRef } from "react"
import { useSelector } from "react-redux"
import { Translation } from "../../components"
import { rootContent as content } from "../../content"

const Voice = () => {
    const language = useSelector(state => state.language)
    const voice = content.voice[language]

  return (
    <section id='voice' className='container main-section grid-rows-[repeat(3,max-content)_minmax(max-content,300px)] md:grid-cols-2'>
        <h2 className="title">{voice.title}</h2>
        <h3 className="subtitle">{voice.subtitle}</h3>
        <p className="description">{voice.description}</p>
        <div className="md:col-span-2 md:col-start-1 md:h-full w-full mt-8 md:mt-14 p-4">
          <Translation />
        </div>
    </section>
  )
}

export default Voice