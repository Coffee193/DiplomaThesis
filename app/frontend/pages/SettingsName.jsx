import '../styling/SettingsName.css'
import { useState } from 'react'

export function SettingsName({ value }){
    
    const [nameState, namesetState] = useState(SetName(value))

    function SetName(name){
        return name === null ? ('Welcome, Back!'): ('Welcome, ' + name)
    }
    
    return(
        <div className='sn'>
            {nameState}
        </div>
    )
}