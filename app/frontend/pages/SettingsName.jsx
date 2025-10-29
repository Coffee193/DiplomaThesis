import '../styling/SettingsName.css'

export function SettingsName({ value, popupvalue, popupsetState }){
    
    //const [nameState, namesetState] = useState(SetName(value))

    function SetName(name){
        return name === null ? ('Welcome, Back!'): ('Welcome, ' + name)
    }
    
    return(
        <div className='sn' onClick={() => popupsetState(popupvalue)}>
            {SetName(value)}
        </div>
    )
}