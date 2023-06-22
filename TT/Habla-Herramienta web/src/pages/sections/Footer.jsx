import { AiFillHeart } from "react-icons/ai"

const Footer = () => {
  return (
    <div className='flex flex-col justify-center gap-3 pt-8 pb-4 px-4'>
      <div className="text-white flex gap-3 justify-center mb-5">
        <p>Sistema embebido como herramienta de apoyo a la comunicación para pacientes con afecciones del habla</p>
        <span>(</span>
        <i className="text-highlight">TT 2023-A013</i>
        <span>)</span>
      </div>
      <div className="text-sm text-gray-400 flex justify-center gap-1">
        <span>Desarrollado con </span>
        <AiFillHeart className="text-red-500 text-lg"/>
        <span>por Luis Valle</span>
      </div>
    </div>
  )
}

export default Footer