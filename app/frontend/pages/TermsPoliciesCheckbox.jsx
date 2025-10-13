import '../styling/termsPoliciesCheckbox.css'
import { Link } from 'react-router-dom'
import { forwardRef, useRef } from 'react'
import { pressKey } from './pressKeyFunc'

export const TermsPoliciesCheckbox = forwardRef(({ valuesRef, warningIndex, warningvalueIndex, tabIndex, onpressEnter, onpressEnterValue, onpressTab, onpressTabValue}, termspoliciesRef) => {
    
    const tpc_inputRef = useRef()

    function ClickCheckBox(){
        if(tpc_inputRef.current.checked === false){
            tpc_inputRef.current.checked = true
            valuesRef.current[warningIndex][warningvalueIndex] = null
        }
        else{
            tpc_inputRef.current.checked = false
            valuesRef.current[warningIndex][warningvalueIndex] = 'You must agree to our Terms and Policies'
        }
    }

    return(
        <div className='tpc_termsholder'>
            <div className='tpc_termscheckbox'>
                <input type='checkbox' onClick={(event) => {event.target.checked === true ? (valuesRef.current[warningIndex][warningvalueIndex] = null) : (valuesRef.current[warningIndex][warningvalueIndex] = 'You must agree to our Terms and Policies')}} ref={(element) => {tpc_inputRef.current = element;termspoliciesRef !== null ? (termspoliciesRef.current = element) : ('')}} className='tpc_input' tabIndex={tabIndex} onKeyDown={(event) => pressKey(event, onpressEnter === 'self' ? (ClickCheckBox) : (onpressEnter), onpressEnter !== 'self' ? (onpressEnterValue) : (undefined), onpressTab, onpressTabValue)} onMouseDown={(event) => event.preventDefault()}/>
            </div>
            <div>
                By Signing Up you agree to our <Link className='tpc_termslink' to='/termspolicies'>Terms of Use</Link> and our <Link className='tpc_termslink' to='/termspolicies'>Privacy Policy</Link>
            </div>
        </div>
    )
})