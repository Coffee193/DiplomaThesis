import '../styling/SettingsName.css'

export function SettingsName({ value, popupvalue, popupsetState, valuesRef, typeIndex, warningIndex, warningvalueIndex }){
    
    //const [nameState, namesetState] = useState(SetName(value))

    function SetName(name){
        return name === null ? ('Welcome, Back!'): ('Welcome, ' + name)
    }
    
    return(
        <div className='sn' onClick={() => {popupsetState(popupvalue); valuesRef.current[typeIndex] = popupvalue['inputtype']; popupvalue['allowEmpty'] === true ? valuesRef.current[warningIndex][warningvalueIndex] = null : ''}}>
            {SetName(value)}
        </div>
    )
}