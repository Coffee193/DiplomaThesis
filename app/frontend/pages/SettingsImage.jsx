import '../styling/SettingsImage.css'
import { useState } from 'react'

export function SettingsImage({ existimage }){

    const [siboxState, siboxsetState] = useState(existimage)
    const [siimageState, siimagesetState] = useState()

    return(
        <div className='si_box'>
            { siboxState === true ? (
            <>
                <div className='si_holder'>
                    {siimageState}
                </div>
                <div className='si_utilholder'>
                    <div className='si_util si_utilblue'>CHANGE IMAGE</div>
                    <div className='si_util si_utilred'>DELETE IMAGE</div>
                </div>
            </>
            ) : (
                <div className='si_utilholder'>
                    <div className='si_util si_utilblue'>UPLOAD IMAGE</div>
                </div>
            )}
            <input type='file' className='si_input' accept='image/*'/>
        </div>
    )
}