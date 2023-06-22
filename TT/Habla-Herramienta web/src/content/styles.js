const styles = {
    palettes: {
        white: { bg:'white', color:'gray-300'},
        dark: { bg:'dark', color:'white'},
        primary: { bg:'primary', color:'white'},
        actions: { bg:'actions', color:'white'},
    },
    outlined: (palette=styles.palettes.white , hover=false) => `px-3 py-2 rounded-lg border-[1px] border-${palette.color} text-${palette.color} bg-${palette.bg} ${hover ? `hover:bg-${palette.color} hover:text-${palette.bg} hover:border-${palette.bg}` : ''}`,
    outlinedLg: (palette=styles.palettes.white , hover=false) => `px-6 py-4 rounded-lg border-[1px] border-${palette.color} text-${palette.color} bg-${palette.bg} ${hover ? `hover:bg-${palette.color} hover:text-${palette.bg} hover:border-${palette.bg}` : ''}`,
    outlinedWide: (palette=styles.palettes.white , hover=false) => `px-12 py-2 rounded-lg border-[1px] border-${palette.color} text-${palette.color} bg-${palette.bg} ${hover ? `hover:bg-${palette.color} hover:border-${palette.bg}` : ''}`,
}

const toStyles = (listStyles, add='') => listStyles.reduce((joined, current) => `${joined} ${add}${current}`,'')

export { styles, toStyles };