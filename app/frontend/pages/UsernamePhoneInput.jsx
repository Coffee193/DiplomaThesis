import '../styling/UsernamePhoneInput.css'
import { useState, useRef } from 'react'
import { ArrowDownIcon } from '../components/svgs/UtilIcons'
import { AustraliaIcon } from '../components/svgs/CountriesIcons'

export function UsernamePhoneInput(){

    const [countrysvgstate, countrysvgsetState] = useState(<AustraliaIcon/>)
    const upi_countrycodeRef = useRef()
    const upi_usernamephoneRef = useRef()
    const upi_usernamephoneinputRef = useRef()

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
        }
        else{
            upi_usernamephoneRef.current.style.display = 'none'
        }
    }
    

    return(
        <div className='upi_allholder'>
            <div className='upi_usernamephone' ref={upi_usernamephoneRef}>
                <div className='upi_svgcountry'>{countrysvgstate}</div>
                <div className='upi_numberareacode'><div>+</div><input className='upi_numberinput' ref={upi_countrycodeRef} placeholder=''/></div>
                <div className='upi_arrow' onMouseEnter={() => Upi_ArrowEnterLeave('enter')} onMouseLeave={() => Upi_ArrowEnterLeave('leave')}><ArrowDownIcon width={15} height={15}/></div>
            </div>
            <input className='upi_usernamephoneinput' autoComplete='off' autoCapitalize='off' spellCheck='false' 
            onChange={() => CheckIsPhone()} ref={upi_usernamephoneinputRef}/>
        </div>
    )
}