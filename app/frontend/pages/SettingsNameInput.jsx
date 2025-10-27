import '../styling/SettingsNameInput.css'
import { pressKey } from './pressKeyFunc'
import { forwardRef } from 'react'

export const SettingsNameInput = forwardRef(({ placeholder, autoFocus, onpressTab, onpressTabValue, onpressEnter, onpressEnterValue }, nameinputRef) => {
    return(
        <div className='sni'>
            <input className='upi_s_border upi_s_height upi_s_padding sni_input' placeholder={placeholder} autoFocus={autoFocus} onKeyDown={(event) => pressKey(event, onpressEnter, onpressEnterValue, onpressTab, onpressTabValue)} ref={nameinputRef}/>
        </div>
    )
})