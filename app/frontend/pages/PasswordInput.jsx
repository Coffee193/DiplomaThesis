import '../styling/PasswordInput.css'
import { useState, useRef, forwardRef } from 'react'
import { EyeIcon, EyeCloseIcon } from '../components/svgs/UtilIcons'
import { pressKey } from './pressKeyFunc'

export const PasswordInput = forwardRef(({classtype, placeholder, valuesRef, passwordIndex, warningIndex, warningvalueIndex, isconfirmpassword, tabIndex, onpressEnter, onpressEnterValue, onpressTab, onpressTabValue, autoFocus}, passwordinputRef) => {

    const [pi_eyestate, pi_eyesetState] = useState(['password', <EyeIcon/>])
    const pi_inputRef = useRef()
    const [pi_classState, pi_classsetState] = useState()

    const reg_contains_at_least_1_num = new RegExp('[0-9]')
    const reg_contains_at_least_1_lowercase = new RegExp('[a-z]')
    const reg_contains_at_least_1_uppercase = new RegExp('[A-Z]')

    function ClickEye(){
        if(pi_eyestate[0] === 'password'){
            pi_eyesetState(['text', <EyeCloseIcon/>])
        }
        else if(pi_eyestate[0] === 'text'){
            pi_eyesetState(['password', <EyeIcon/>])
        }
    }

    function CheckValues(){
        let warning = null
        let checkval = pi_inputRef.current.value
        if(checkval === ''){
            warning = 'Field is empty'
        }
        else if( checkval.length < 8 ){
            warning = 'Password must be at least 8 characters'
        }
        else if(checkval.length > 30){
            warning = 'Password cannot exceed 30 characters'
        }
        else if( (reg_contains_at_least_1_num.test(checkval)) === false ){
            warning = 'Password must contain at least 1 number'
        }
        else if( (reg_contains_at_least_1_lowercase.test(checkval)) === false ){
            warning = 'Password must contain at least 1 lowercase letter'
        }
        else if( (reg_contains_at_least_1_uppercase.test(checkval)) === false){
            warning = 'Pssword must contain at least 1 uppercase letter'
        }
        valuesRef.current[passwordIndex] = checkval
        valuesRef.current[warningIndex][warningvalueIndex] = warning
    }

    function CheckPasswordsEqual(){
        if(pi_inputRef.current.value !== valuesRef.current[passwordIndex]){
            valuesRef.current[warningIndex][warningvalueIndex] = 'Passwords do not match'
        }
        else{
            valuesRef.current[warningIndex][warningvalueIndex] = null
        }
    }

    function ClassType(){
        if(classtype === 'lr'){
            return ['lr_password', 'lr_passwordinput', 'lr_passwordsvgholder', 'lr_passwordsvgeye']
        }
        else if(classtype === 's'){
            return ['sp_box', 'sp_input', 'lr_passwordsvgholder', 'sp_inputsvg']
        }
    }

    return(
        <div className={ClassType()[0]}>
            <input type={pi_eyestate[0]} autoComplete='off' autoCapitalize='off' spellcheck='false' className={ClassType()[1]} placeholder={placeholder} ref={(element) => {pi_inputRef.current = element; passwordinputRef !== null ? (passwordinputRef.current = element): ('')}} onChange={() => {isconfirmpassword === true ? (CheckPasswordsEqual()) : (CheckValues())}} tabIndex={tabIndex} onKeyDown={(event) => pressKey(event, onpressEnter, onpressEnterValue, onpressTab, onpressTabValue )} autoFocus={autoFocus}/>
            <div className={ClassType()[2]}>
                <div className={ClassType()[3]} onClick={() => ClickEye()}>{pi_eyestate[1]}</div>
            </div>
        </div>
    )
})