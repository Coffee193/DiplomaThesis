import '../styling/PasswordInput.css'
import { useState, useEffect, useRef } from 'react'
import { EyeIcon, EyeCloseIcon } from '../components/svgs/UtilIcons'

export function PasswordInput({classtype, placeholder, valuesRef}){

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

        if(warning === null){
            valuesRef.current[2] = checkval
        }
        else{
            valuesRef.current[3] = true
            valuesRef.current[4] = warning
        }

    }

    return(
        <div className={pi_classstate[0]}>
            <input type={pi_eyestate[0]} autoComplete='off' autoCapitalize='off' spellcheck='false' className={pi_classstate[1]} placeholder={placeholder} ref={pi_inputRef} onChange={() => CheckValues()}/>
            <div className={pi_classstate[2]}>
                <div className={pi_classstate[3]} onClick={() => ClickEye()}>{pi_eyestate[1]}</div>
            </div>
        </div>
    )
}