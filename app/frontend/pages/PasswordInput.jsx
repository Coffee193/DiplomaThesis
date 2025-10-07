import '../styling/PasswordInput.css'
import { useState, useEffect } from 'react'
import { EyeIcon, EyeCloseIcon } from '../components/svgs/UtilIcons'

export function PasswordInput({classtype, placeholder}){

    const [pi_classstate, pi_classsetState] = useState([null, null])
    const [pi_eyestate, pi_eyesetState] = useState(['password', <EyeIcon/>])

    useEffect(() => {
        if(classtype === 'loginregister'){
            pi_classsetState(['lr_password', 'lr_passwordinput', 'lr_passwordsvgholder', 'lr_passwordsvgeye'])
        }
    },[])

    return(
        <div className={pi_classstate[0]}>
            <input type={pi_eyestate[0]} autoComplete='off' autoCapitalize='off' spellcheck='false' className={pi_classstate[1]} placeholder={placeholder}/>
            <div className={pi_classstate[2]}>
                <div className={pi_classstate[3]}>{pi_eyestate[1]}</div>
            </div>
        </div>
    )
}