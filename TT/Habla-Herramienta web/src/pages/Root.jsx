import { Outlet } from "react-router-dom"

import { Footer, Navbar } from "../pages/sections"

const Root = () => {
  return (
    <>
      <div className="w-full bg-gray-200 fixed md:relative z-50"> <Navbar /> </div>
      <div className="w-full"> <Outlet /> </div>
      <div className="w-full bg-black"> <Footer /> </div>
    </>
  )
}

export default Root