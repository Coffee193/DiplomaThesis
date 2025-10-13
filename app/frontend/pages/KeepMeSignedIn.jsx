import '../styling/KeepMeSignedIn.css'
import { useRef, useState, forwardRef } from "react"
import { ArrowDownIcon } from "../components/svgs/UtilIcons"
import { pressKey } from './pressKeyFunc'

export const KeepMeSignedIn = forwardRef(({valuesRef, keepmesignedinIndex, tabIndex, onpressEnter, onpressEnterValue, onpressTab, onpressTabValue}, keepmesignedinRef) => {

    const [kms_signedinState, kms_signedinsetState] = useState(['rotate(0deg)', 'none'])
    const kms_arrowsignedinRef = useRef()
    const kms_inputRef = useRef()

    function ClickArrowSignedIn(){
        let pos = kms_arrowsignedinRef.current.getAttribute('data-pos')
        if(pos === 'down'){
            kms_arrowsignedinRef.current.setAttribute('data-pos', 'up')
            kms_signedinsetState(['rotate(180deg)', 'block'])
        }
        else if(pos === 'up'){
            kms_arrowsignedinRef.current.setAttribute('data-pos', 'down')
            kms_signedinsetState(['rotate(0deg)', 'none'])
        }
    }

    function ClickCheckBox(){
        if(kms_inputRef.current.checked === false){
            kms_inputRef.current.checked = true
            valuesRef.current[keepmesignedinIndex] = true
        }
        else{
            kms_inputRef.current.checked = false
            valuesRef.current[keepmesignedinIndex] = false
        }
    }

    return(
        <>
        <div className='kms_signedinholder'>
            <input type='checkbox' ref={(element) => {kms_inputRef.current = element; keepmesignedinRef !== null ? (keepmesignedinRef.current = element) : ('')}} className='kms_input' onKeyDown={(event) => pressKey(event, onpressEnter === 'self' ? (ClickCheckBox) : (onpressEnter), onpressEnter !== 'self' ? (onpressEnterValue) : (undefined), onpressTab, onpressTabValue)} onClick={(event) => {event.target.checked === true ? (valuesRef.current[keepmesignedinIndex] = true): (valuesRef.current[keepmesignedinIndex] = false)}} tabIndex={tabIndex} onMouseDown={(event) => event.preventDefault()}/>
            <div className='kms_signedintext' onClick={() => ClickArrowSignedIn()}>
                <span>Keep me signed in</span>
                <ArrowDownIcon className='kms_signedinarrow' style={{transform: kms_signedinState[0]}} ref={kms_arrowsignedinRef} data-pos='down'/>
            </div>
        </div>
        <div className='kms_signedinexplain' style={{display: kms_signedinState[1]}}>You'll be automatically signed in to your account when using this device</div>
        </>
    )
})