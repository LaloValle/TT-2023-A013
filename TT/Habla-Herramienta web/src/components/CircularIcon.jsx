import { toStyles } from "../content"

const CircularIcon = ({ 
    icon, size='md',
    onClickHandler=()=>'',
    extraStyles='', hoverStyles=[''], activeStyle='', active=false
  }) => {
    
    const sizes = {
        xsm: '1',
        sm: '2',
        md: '4',
        lg: '6',
        xl: '8',
        '2xl': '10'
    }

  return (
    <div className={`flex justify-center items-center h-max aspect-square rounded-full cursor-pointer transition-colors p-${sizes[size]} ${active ? activeStyle : toStyles(hoverStyles,'hover:')} ${extraStyles}`} onClick={()=> onClickHandler()}>
      {icon}
    </div>
  )
}

export default CircularIcon