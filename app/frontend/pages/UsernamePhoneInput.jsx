import '../styling/UsernamePhoneInput.css'
import { useState, useRef, useEffect } from 'react'
import { ArrowDownIcon } from '../components/svgs/UtilIcons'
import { AustraliaIcon } from '../components/svgs/CountriesIcons'
import { AreaCode } from './AreaCode'

export function UsernamePhoneInput({ valuesRef, valueIndex, typeIndex, warningIndex, warningvalueIndex }){

    const [countrysvgstate, countrysvgsetState] = useState(<AustraliaIcon/>)
    const [upi_inputvalstate, upi_inputvalsetState] = useState('')
    const upi_countrycodeRef = useRef()
    const upi_usernamephoneRef = useRef()
    const upi_usernamephoneinputRef = useRef()
    const upi_valtype = useRef('email')

    const [areacodevisibilitystate, areacodevisibilitysetState] = useState(0)

    const reg_only_contains_numbers = new RegExp('^[0-9]+$')

    function Upi_ArrowEnterLeave(val){
        if(val === 'enter'){
            upi_usernamephoneRef.current.classList.add('upi_hover')
        }
        else if(val === 'leave'){
            upi_usernamephoneRef.current.classList.remove('upi_hover')
        }
    }

    function CheckIsPhone(){
        let checkval = upi_usernamephoneinputRef.current.value
        if((checkval.length > 5) && (checkval.search(reg_only_contains_numbers) === 0)){
            upi_usernamephoneRef.current.style.display = 'flex'
            upi_valtype.current = 'phone'
        }
        else{
            upi_usernamephoneRef.current.style.display = 'none'
            upi_valtype.current = 'email'
        }
        CheckValues()
    }

    function AreaCodeOpen(){
        areacodevisibilitysetState(oldvalue => oldvalue + 1)
    }

    function CheckValues(){
        let warning = null
        let checkval = upi_usernamephoneinputRef.current.value
        if(checkval === ''){
            warning = 'Field is empty'
        }
        else if(upi_valtype.current === 'email'){
            let contains_a = checkval.indexOf('@')
            let contains_dot = checkval.indexOf('.')
            let count_a = checkval.split('@').length - 1
            let count_dot = checkval.split('.').length - 1
            if( (contains_a === -1) || (contains_dot === -1) || (contains_a + 1 >= contains_dot) || (checkval.length < 5) || (contains_a === 0) || (contains_dot === checkval.length - 1) || (count_a !== 1) || (count_dot !== 1) || (checkval.length > 255)){
                warning = 'Enter a valid email address'
            }
        }
        else if(upi_valtype.current === 'phone'){
            if(upi_inputvalstate === ''){
                warning = 'Enter an area code'
            }
            if(upi_inputvalstate.length + checkval.length > 24){
                warning = 'Phone number cannot exceed 24 characters'
            }
        }

        valuesRef.current[warningIndex][warningvalueIndex] = warning
        if(upi_valtype.current === 'email'){
            valuesRef.current[valueIndex] = upi_usernamephoneinputRef.current.value
            valuesRef.current[typeIndex] = 'email'
        }
        else if(upi_valtype.current === 'phone'){
            valuesRef.current[valueIndex] = '+' + upi_inputvalstate + ' ' + upi_usernamephoneinputRef.current.value
            valuesRef.current[typeIndex] = 'phone'
        }
    }
    

    return(
        <>
        <AreaCode areacodevisibility={areacodevisibilitystate} areacodeinputsetState={upi_inputvalsetState} areacodecountrysetState={countrysvgsetState}/>
        <div className='upi_allholder'>
            <div className='upi_usernamephone' ref={upi_usernamephoneRef}>
                <div className='upi_svgcountry'>{countrysvgstate}</div>
                <div className='upi_numberareacode'><div>+</div><input className='upi_numberinput' ref={upi_countrycodeRef} placeholder='' value={upi_inputvalstate} onChange={(e) => upi_inputvalsetState(e.target.value)}/></div>
                <div className='upi_arrow' onMouseEnter={() => Upi_ArrowEnterLeave('enter')} onMouseLeave={() => Upi_ArrowEnterLeave('leave')} onClick={() => AreaCodeOpen()}><ArrowDownIcon width={15} height={15}/></div>
            </div>
            <input className='upi_usernamephoneinput' autoComplete='off' autoCapitalize='off' spellCheck='false' 
            onChange={() => CheckIsPhone()} ref={upi_usernamephoneinputRef}/>
        </div>
        </>
    )
}