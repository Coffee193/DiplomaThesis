import '../styling/PasswordInput.css'
import { useState, useEffect, useRef, forwardRef } from 'react'
import { EyeIcon, EyeCloseIcon } from '../components/svgs/UtilIcons'
import { pressKey } from './pressKeyFunc'

export const PasswordInput = forwardRef(({classtype, placeholder, valuesRef, passwordIndex, warningIndex, warningvalueIndex, isconfirmpassword, tabIndex, onpressEnter, onpressEnterValue, onpressTab, onpressTabValue}, passwordinputRef) => {

    const [pi_classstate, pi_classsetState] = useState([null, null, null, null])
    const [pi_eyestate, pi_eyesetState] = useState(['password', <EyeIcon/>])
    const pi_inputRef = useRef()

    const reg_contains_at_least_1_num = new RegExp('[0-9]')
    const reg_contains_at_least_1_lowercase = new RegExp('[a-z]')
    const reg_contains_at_least_1_uppercase = new RegExp('[A-Z]')

    useEffect(() => {
        if(classtype === 'loginregister'){
            pi_classsetState(['lr_password', 'lr_passwordinput', 'lr_passwordsvgholder', 'lr_passwordsvgeye'])
        }
    },[])

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

    return(
        <div className={pi_classstate[0]}>
            <input type={pi_eyestate[0]} autoComplete='off' autoCapitalize='off' spellcheck='false' className={pi_classstate[1]} placeholder={placeholder} ref={(element) => {pi_inputRef.current = element; passwordinputRef !== null ? (passwordinputRef.current = element): ('')}} onChange={() => {isconfirmpassword === true ? (CheckPasswordsEqual()) : (CheckValues())}} tabIndex={tabIndex} onKeyDown={(event) => pressKey(event, onpressEnter, onpressEnterValue, onpressTab, onpressTabValue )}/>
            <div className={pi_classstate[2]}>
                <div className={pi_classstate[3]} onClick={() => ClickEye()}>{pi_eyestate[1]}</div>
            </div>
        </div>
    )
})