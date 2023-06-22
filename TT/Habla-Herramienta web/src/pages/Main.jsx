import { Hero, Voice } from "./sections"
import MainPhonemes from "./sections/MainPhonemes"

const Main = () => {

  return (
    <>
      <Hero />
      <div className="w-full bg-gray-100"> <MainPhonemes /> </div>
      <div className="w-full bg-secondary"> <Voice /> </div>
    </>
  )
}

export default Main