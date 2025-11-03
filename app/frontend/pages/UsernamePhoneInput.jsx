import '../styling/UsernamePhoneInput.css'
import { useState, useRef, forwardRef, useImperativeHandle } from 'react'
import { ArrowDownIcon } from '../components/svgs/UtilIcons'
import { AreaCode } from './AreaCode'
import { pressKey } from './pressKeyFunc'
import { country_list_full } from '../components/CountriesList'

export const UsernamePhoneInput = forwardRef(({ valuesRef, valueIndex, typeIndex, warningIndex, warningvalueIndex, alwaysEmail, alwaysPhone, autoFocus, onpressEnter, onpressEnterValue, onpressTab, onpressTabValue, tabIndex, classtype, placeholder, existnavbar, allowEmpty}, usernamephoneinputRef) => {
    
    console.log('i got rerendered')
    const country_list_keys = Object.keys(country_list_full)

    const [upi_areacodesvgState, upi_areacodesvgsetState] = useState(() => InitAreaCode()[0])
    const [upi_areacodenumberState, upi_areacodenumbersetState] = useState(() => InitAreaCode()[1])
    const upi_countrycodeinputRef = useRef()
    const upi_usernamephoneRef = useRef()
    const upi_usernamephoneinputRef = useRef()
    const upi_valtype = useRef(alwaysPhone === true ? ('phone') : ('email'))
    const [areacodevisibleState, areacodevisiblesetState] = useState(false)

    const reg_only_contains_numbers = new RegExp('^[0-9]+$')

    useImperativeHandle(usernamephoneinputRef, () => {
        return{
            focusInput: () => FocusUsernamePhoneInput(),
            focusAreaCode: () => FocusAreaCodeInput()
        }
    })
    

    function Upi_ArrowEnterLeave(val){
        if(val === 'enter'){
            upi_usernamephoneRef.current.classList.add('upi_hover')
        }
        else if(val === 'leave'){
            upi_usernamephoneRef.current.classList.remove('upi_hover')
        }
    }

    function CheckIsPhone(){
        if(alwaysEmail === false && alwaysPhone === false){
            let checkval = upi_usernamephoneinputRef.current.value
            if((checkval.length >= 5) && (reg_only_contains_numbers.test(checkval) === true)){
                upi_usernamephoneRef.current.style.display = 'flex'
                upi_valtype.current = 'phone'
            }
            else{
                upi_usernamephoneRef.current.style.display = 'none'
                upi_valtype.current = 'email'
            }
        }
        CheckValues()
    }

    function CheckValues(){
        let warning = null
        let checkval = upi_usernamephoneinputRef.current.value
        if(checkval === ''){
            checkval = null
            if(alwaysEmail === true || alwaysPhone === true){
                if(allowEmpty != true){
                    warning = 'Field is empty'
                }
                else{
                    if(alwaysPhone === true){
                        let areacodeval = upi_countrycodeinputRef.current.value

                        if(areacodeval !== ''){
                            warning = 'Area Code must be empty Or both fields must have a value'
                        }
                    }
                }
            }
            else{
                warning = 'Field is empty'
            }
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
            let areacodeval = upi_countrycodeinputRef.current.value
            if(areacodeval === ''){
                warning = 'Enter an area code'
            }
            if(areacodeval.length + checkval.length > 23){
                warning = 'Phone number cannot exceed 25 characters'
            }
            if(checkval.length < 5){
                warning = 'Phone number must be at least 5 characters (without Area Code)'
            }
        }

        valuesRef.current[warningIndex][warningvalueIndex] = warning
        if(upi_valtype.current === 'email'){
            //valuesRef.current[valueIndex] = upi_usernamephoneinputRef.current.value
            valuesRef.current[valueIndex] = checkval
            valuesRef.current[typeIndex] = 'email'
        }
        else if(upi_valtype.current === 'phone'){
            //valuesRef.current[valueIndex] = '+' + upi_countrycodeinputRef.current.value + ' ' + upi_usernamephoneinputRef.current.value
            valuesRef.current[valueIndex] = checkval === null ? null : '+' + upi_countrycodeinputRef.current.value + ' ' + upi_usernamephoneinputRef.current.value
            valuesRef.current[typeIndex] = 'phone'
        }
    }

    function InitAreaCode(){
        console.log('I was called')
        console.log('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        let country = Intl.DateTimeFormat().resolvedOptions().timeZone;
        for(let i = 0; i < country_list_keys.length; i++){
            if(country_list_full[country_list_keys[i]]['tz'] === country){
                if(alwaysPhone === true && allowEmpty == true){
                    valuesRef.current[warningIndex][warningvalueIndex] = 'Area Code must be empty Or both fields must have a value'
                }
                return [country_list_full[country_list_keys[i]]['svg'], country_list_full[country_list_keys[i]]['ac'].slice(1)]
            }
        }
        return [<div className='upi_countryempty'/>, '']
    }

    function ChangeAreaCodeCheckSvg(event){
        /*if(reg_only_contains_numbers.test(event.target.value) === false && event.target.value !== ''){
            upi_countrycodeinputRef.current.value = event.target.value.slice()
            return
        }*/
        let changesvgval = null
        for(let i=0; i < country_list_keys.length; i++){
            if(country_list_full[country_list_keys[i]]['ac'].slice(1) === event.target.value){
                changesvgval = country_list_full[country_list_keys[i]]['svg']
                break
            }
        }
        if(changesvgval === null){
            changesvgval = <div className='upi_countryempty'/>
        }
        upi_areacodesvgsetState(changesvgval)
    }

    function FocusUsernamePhoneInput(){
        upi_usernamephoneinputRef.current.focus()
    }
    function FocusAreaCodeInput(){
        upi_countrycodeinputRef.current.focus()
    }
    function PressEnterOnAreaCodeInput(){
        areacodevisiblesetState(true)
        upi_countrycodeinputRef.current.blur()
    }

    function ClassType(){
        if(classtype === 'lr'){
            return(
                ['upi_lr_border', 'upi_lr_height', 'upi_lr_padding']
            )
        }
        else if(classtype === 's'){
            return(
                ['upi_s_border', 'upi_s_height', 'upi_s_padding']
            )
        }
    }

    function CheckOnlyNumbers(event, inputRef){
        if(reg_only_contains_numbers.test(event.target.value) === false && event.target.value !== ''){
            inputRef.current.value = event.target.value.slice(0, -1)
            return false
        }
        return true
    }

    return(
        <>
        <AreaCode areacodesvgsetState={upi_areacodesvgsetState} areacodeinputRef={upi_countrycodeinputRef} areacodevisibleState={areacodevisibleState} areacodevisiblesetState={areacodevisiblesetState} country_list_full={country_list_full} country_list_keys={country_list_keys} valuesRef={valuesRef} warningIndex={warningIndex} warningvalueIndex={warningvalueIndex} valueIndex={valueIndex} existnavbar={existnavbar}/>
        <div className='upi_allholder'>
            <div className={'upi_usernamephone ' + ClassType()[0] + ' ' + ClassType()[2]} ref={upi_usernamephoneRef} style={alwaysPhone === true ? ({display: 'flex'}) : ({display: 'none'})}>
                <div className='upi_svgcountry'>{upi_areacodesvgState}</div>
                <div className='upi_numberareacode'><div>+</div><input className='upi_numberinput' ref={upi_countrycodeinputRef} placeholder='' defaultValue={upi_areacodenumberState} onChange={(event) => {CheckOnlyNumbers(event, upi_countrycodeinputRef) === true ? (ChangeAreaCodeCheckSvg(event), CheckValues()) : ''/*ChangeAreaCodeCheckSvg(event); (reg_only_contains_numbers.test(event.target.value) === true || event.target.value === '') ? (CheckValues()) : ('')*/}} onKeyDown={(event) => pressKey(event, PressEnterOnAreaCodeInput, undefined, FocusUsernamePhoneInput, undefined)} onFocus={() => Upi_ArrowEnterLeave('enter')} onBlur={() => Upi_ArrowEnterLeave('leave')} tabIndex={tabIndex} maxLength="5"/></div>
                <div className='upi_arrow' onMouseEnter={() => Upi_ArrowEnterLeave('enter')} onMouseLeave={() => Upi_ArrowEnterLeave('leave')} onClick={() => areacodevisiblesetState(true)}><ArrowDownIcon width={15} height={15}/></div>
            </div>
            <input className={'upi_usernamephoneinput ' + ClassType()[0] + ' ' + ClassType()[1] + ' ' + ClassType()[2]} autoComplete='off' autoCapitalize='off' spellCheck='false' placeholder={placeholder}
            onChange={(event) => {alwaysPhone === true && CheckOnlyNumbers(event, upi_usernamephoneinputRef) === false ? '' : CheckIsPhone()}} ref={ (el) => {upi_usernamephoneinputRef.current = el; usernamephoneinputRef !== null ? (usernamephoneinputRef.current = el) : ('')}} autoFocus={autoFocus} onKeyDown={(event) => pressKey(event, onpressEnter, onpressEnterValue, onpressTab !== undefined ? (onpressTab) : (FocusAreaCodeInput), onpressTabValue)} tabIndex={tabIndex}/>
        </div>
        </>
    )
})