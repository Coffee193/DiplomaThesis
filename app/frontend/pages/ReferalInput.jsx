import '../styling/ReferalInput.css'
import { ArrowDownIcon } from '../components/svgs/UtilIcons'
import { useState, useRef, forwardRef } from 'react'
import { pressKey } from './pressKeyFunc'

export const ReferalInput = forwardRef(({ valuesRef, referalIndex, warningIndex, warningvalueIndex, tabIndex, onpressEnter, onpressEnterValue, onpressTab, onpressTabValue}, referalinputRef) => {

    const [riclickstate, riclicksetState] = useState(['d', 'rotate(0deg)', '1', 'all'])
    const riinputRef = useRef()

    function CheckValue(){
        let warning = null
        let checkval = riinputRef.current.value
        if(checkval.length !== 10){
            warning = 'Referal code must be 10 characters long'
        }

        valuesRef.current[referalIndex] = checkval
        valuesRef.current[warningIndex][warningvalueIndex] = warning
    }

    return(
        <div className='ri_referal'>
            <div className='ri_referalheader'>
                <span>Referal Code</span><div className='ri_referalsvg' onClick={() => {riclickstate[0] === 'd' ? (riclicksetState(['u', 'rotate(180deg)', '0', 'none'])) : (riclicksetState(['d', 'rotate(0deg)', '1', 'all']))}}><ArrowDownIcon style={{transform: riclickstate[1]}}/></div>
            </div>
            <input className='ri_referalinput' maxLength='10' autoComplete='off' autocapitalize='off' spellCheck='false' style={{opacity: riclickstate[2], pointerEvents: riclickstate[3]}} onChange={() => CheckValue()} ref={(element) => {riinputRef.current = element; referalinputRef !== null ? (referalinputRef.current = element) : ('')}} tabIndex={tabIndex} onKeyDown={(event) => pressKey(event, onpressEnter, onpressEnterValue, onpressTab, onpressTabValue)}/>
        </div>
    )
})