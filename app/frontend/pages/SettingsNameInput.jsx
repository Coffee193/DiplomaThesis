import '../styling/SettingsNameInput.css'
import { pressKey } from './pressKeyFunc'
import { forwardRef, useRef } from 'react'

export const SettingsNameInput = forwardRef(({ placeholder, autoFocus, onpressTab, onpressTabValue, onpressEnter, onpressEnterValue, valuesRef, typeIndex, nameIndex, warningIndex, warningvalueIndex }, nameinputRef) => {

    const sni_inputRef = useRef()

    function CheckValues(){
        let warning = null
        let checkval = sni_inputRef.current.value
        if(checkval.length > 7){
            warning = 'Name cannot exceed 7 characters'
        }
        valuesRef.current[nameIndex] = checkval
        valuesRef.current[warningIndex][warningvalueIndex] = warning
        valuesRef.current[typeIndex] = 'name'
    }

    return(
        <div className='sni'>
            <input className='upi_s_border upi_s_height upi_s_padding sni_input' placeholder={placeholder} autoFocus={autoFocus} onKeyDown={(event) => pressKey(event, onpressEnter, onpressEnterValue, onpressTab, onpressTabValue)} ref={(element) => {sni_inputRef.current = element; nameinputRef !== null ? nameinputRef.current = element : ''}} onChange={() => CheckValues()}/>
        </div>
    )
})