import '../styling/LoginRegister.css'
import { useState, useRef } from 'react'
import { useNavigate, Link, useLocation } from 'react-router-dom'
import { UsernamePhoneInput } from './UsernamePhoneInput'
import { ArrowDownIcon, BlocksLoad, XCloseIcon } from '../components/svgs/UtilIcons'
import { PasswordInput } from './PasswordInput'
import { ReferalInput } from './ReferalInput'
import { TermsPoliciesCheckbox } from './TermsPoliciesCheckbox'
import { KeepMeSignedIn } from './KeepMeSignedIn'


export function LoginRegister({ lrtype }){
    const [lrheaderbackstate, lrheaderbacksetState] = useState()
    const valuesRef = useRef([null, null, null, ['Field is empty', 'Password field is empty', 'Passwords do not match', 'Referal code must be 10 characters long', 'You must agree to our Terms and Policies'], null, false]) // emailphoneval, type (:e-> email, p->phone), password, warning -> [0: emailphonewarning, 1: passwordwarning, 2: passwordconfirmwarning, 3: referalwarning, 4: checkboxwarning], referal, keepmesignedin
    const [warningstate, warningsetState] = useState('')
    const lrinfoholderRef = useRef()
    const [warningsubmitstate, warningsubmitsetState] = useState('')
    const usernamephoneinputRef = useRef()
    const passwordinputRef = useRef()
    const confirmpasswordinputRef = useRef()
    const referalinputRef = useRef()
    const termspoliciesinputRef = useRef()
    const keepmesignedininputRef = useRef()
    const [nextbuttonState, nextbuttonsetState] = useState('Next')
    const [submitbuttonState, submitbuttonsetState] = useState(lrtype === 'l' ? ('Log In') : ('Sign Up'))
    const nextbuttonRef = useRef()
    const submitbuttonRef = useRef()
    const expiredRef = useRef()

    const navigate = useNavigate()
    const location = useLocation()

    async function LoginRegister_NextClick(){
        console.log(valuesRef.current)
        if(valuesRef.current[3][0] !== null){
            warningsetState(valuesRef.current[3][0])
            return
        }
        ClickButton(false, nextbuttonRef, nextbuttonsetState)
        let response_status = null
        let request = {"v": valuesRef.current[0], "t": valuesRef.current[1], "c": lrtype}
        let response = await fetch(import.meta.env.VITE_URL + '/loginregister/finduser/', {
            method: 'POST',
            body: JSON.stringify(request),
        }).then(res => {
            response_status = res.status
            return res.json()
        }).then(data => data).catch(() => warningsetState('Could not connect to the server'))
        ClickButton(true, nextbuttonRef, nextbuttonsetState)

        if(response_status === 404 || response_status === 409){
            warningsetState(response)
        }
        else if(response_status === 200){
            let headerval = valuesRef.current[0]
            if(headerval.length > 25){
                headerval = headerval.slice(0, 22) + '...'
            }
            warningsetState('')
            lrheaderbacksetState(headerval)
            ClickSlide('forward')
        }
    }

    function ClickSlide(move){
        if(move === 'forward'){
            lrinfoholderRef.current.style.left = '-425px'
            warningsetState('')
            setTimeout(function(){
                FocusElement('p')
            }, 200)
        }
        else if(move === 'back'){
            lrinfoholderRef.current.style.left = '0px'
            warningsubmitsetState('')
            setTimeout(function(){
                FocusElement('u')
            }, 200)
        }
    }

    function LoginRegister_SubmitClick(){
        if(lrtype === 'l'){
            SubmitLogIn()
        }
        else if(lrtype === 'r'){
            SubmitRegister()
        }
    }

    async function SubmitLogIn(){
        for(let i = 0; i < 2; i++){
            if(valuesRef.current[3][i] !== null){
                warningsubmitsetState(valuesRef.current[3][i])
                return
            }
        }
        ClickButton(false, submitbuttonRef, submitbuttonsetState)

        let response_status = null
        let request = {"v": valuesRef.current[0], "t": valuesRef.current[1], "p": valuesRef.current[2], "k": valuesRef.current[5]}
        let response = await fetch(import.meta.env.VITE_URL + 'loginregister/login/', {
            method: 'POST',
            body: JSON.stringify(request),
            credentials: 'include',
        }).then(res => {
            response_status = res.status
            return res.json()
        }).then(data => data).catch(() => warningsetState('Could not connect to the server'))
        ClickButton(true, submitbuttonRef, submitbuttonsetState)

        if(response_status === 401){
            warningsubmitsetState(response)
        }
        else if(response_status === 200){
            location.state !== null && location.state !== 'expired' ? (navigate(location.state)) : (navigate('/'))
        }
    }

    async function SubmitRegister(){
        for(let i = 1; i < valuesRef.current[3].length; i++){
            if(valuesRef.current[3][i] !== null){
                warningsubmitsetState(valuesRef.current[3][i])
                return
            }
        }
        ClickButton(false, submitbuttonRef, submitbuttonsetState)
        
        let response_status = null
        let request = {"v": valuesRef.current[0], "t": valuesRef.current[1], "p": valuesRef.current[2], "r": valuesRef.current[4]}
        let response = await fetch(import.meta.env.VITE_URL + '/loginregister/register/', {
            method: 'POST',
            body: JSON.stringify(request),
            credentials: 'include',
        }).then(res => {
            response_status = res.status
            return res.json()
        }).then(data => data).catch(() => warningsubmitsetState('Could not connect to the server'))
        ClickButton(true, submitbuttonRef, submitbuttonsetState)

        if(response_status === 409){
            warningsubmitsetState(response)
        }
        else if(response_status === 200){
            location.state !== null && location.state !== 'expired' ? (navigate(location.state)) : (navigate('/'))
        }
    }

    function RefreshValues(){
        FocusElement('u')
        usernamephoneinputRef.current.value = ''
        passwordinputRef.current.value = ''
        valuesRef.current = [null, null, null, ['Field is empty', 'Password field is empty', 'Passwords do not match', 'Referal code must be 10 characters long', 'You must agree to our Terms and Policies'], null, false]
        warningsetState('')
        warningsubmitsetState('')
    }

    function FocusElement(element){
        if(element === 'u' || element === 0){
            usernamephoneinputRef.current.focus()
        }
        else if(element === 'p' || element === 1){
            passwordinputRef.current.focus()
        }
        else if(element === 'cp' || element === 2){
            confirmpasswordinputRef.current.focus()
        }
        else if(element === 'r' || element === 3){
            referalinputRef.current.focus()
        }
        else if(element === 'tp' || element === 4){
            termspoliciesinputRef.current.focus()
        }
        else if(element === 'kms' || element === 5){
            keepmesignedininputRef.current.focus()
        }
    }

    function ClickButton(active, buttonref, buttonsetstate){
        if(active === false){
            buttonref.current.classList.remove('lr_clickbuttonactive')
            buttonsetstate(<BlocksLoad/>)
        }
        else{
            buttonref.current.classList.add('lr_clickbuttonactive')
            buttonsetstate('Next')
        }
    }

    return(
        <div className='lr_holderall'>

            <div className='lr_body'>
                {location.state === 'expired' ? (
                <div className='lr_expired' ref={expiredRef} onClick={() => expiredRef.current.style.display = 'none'}>
                    <span>Session Expired</span><div><XCloseIcon/></div>
                </div>) : (<></>)}
                <div className='lr_mainbox'>
                    <Link to='/' tabIndex="-1"><div className='lr_LogoHome'><img src='../components/images/MainLogo.png'/></div></Link>
                    <div className='lr_infoholder' ref={lrinfoholderRef}>
                        
                        <div className='lr_firststep'>
                            <div className='lr_inputnextholder'>
                                <div className='lr_header'>{lrtype === 'l' ? ('Log In') : ('Sign Up')}</div>
                                <div className='lr_maincontent'>
                                    <div className='lr_emailphone'>
                                        <div className='lr_firststep_label'>Email / Phone Number</div>
                                        <UsernamePhoneInput valuesRef={valuesRef} valueIndex={0} typeIndex={1} warningIndex={3} warningvalueIndex={0} alwaysPhone={false} alwaysEmail={false} ref={usernamephoneinputRef} autoFocus={true} onpressEnter={LoginRegister_NextClick} tabIndex="-1" classtype='lr'/>
                                    </div>
                                    <div className='lr_warningholder' onClick={() => warningsetState('')}>
                                        <div className='lr_warning'>{warningstate}</div>
                                    </div>
                                    <div className='lr_clickbutton lr_clickbuttonactive' onClick={() => LoginRegister_NextClick()} ref={nextbuttonRef}>{nextbuttonState}</div>
                                </div>
                            </div>
                            <div className='lr_loginregisterholder'>
                                <span>{lrtype === 'l' ? ("Don't have an account?") : ("Already have an account?")}</span>
                                <Link to={lrtype === 'l' ? ('/register'): ('/login')} onClick={() => RefreshValues()} tabIndex="-1" replace><div className='lr_loginregisterclick'>{lrtype === 'l' ? ('Sign Up') : ('Log In')}</div></Link>
                            </div>
                        </div>

                        <div className='lr_secondstep'>
                            <div className='lr_backbutton' onClick={() => ClickSlide('back')}><ArrowDownIcon className='lr_backbuttonsvg'/><span className='lr_backbuttonspan'>Back</span></div>
                            <div className='lr_backheader' onClick={() => ClickSlide('back')}><span className='lr_backheaderspan'>{lrheaderbackstate}</span></div>
                            <div className='lr_maincontent_second'>
                                <PasswordInput classtype={'lr'} placeholder={'Password'} valuesRef={valuesRef} passwordIndex={2} warningIndex={3} warningvalueIndex={1} isconfirmpassword={false} ref={passwordinputRef} tabIndex="-1" onpressTab={FocusElement} onpressTabValue={lrtype === 'r' ? ('cp') : ('kms')} onpressEnter={lrtype === 'r' ? (SubmitRegister) : (SubmitLogIn)}/>
                                {lrtype === 'r' ? (
                                <div className='lr_rholder'>
                                    <PasswordInput classtype={'lr'} placeholder={'Confirm Password'} valuesRef={valuesRef} passwordIndex={2} warningIndex={3} warningvalueIndex={2} isconfirmpassword={true} ref={confirmpasswordinputRef} tabIndex="-1" onpressTab={FocusElement} onpressTabValue={'r'} onpressEnter={SubmitRegister}/>
                                    <ReferalInput valuesRef={valuesRef} referalIndex={4} warningIndex={3} warningvalueIndex={3} tabIndex="-1" ref={referalinputRef} onpressTab={FocusElement} onpressTabValue={'tp'} onpressEnter={SubmitRegister}/>
                                    <TermsPoliciesCheckbox valuesRef={valuesRef} warningIndex={3} warningvalueIndex={4} ref={termspoliciesinputRef} tabIndex="-1" onpressTab={FocusElement} onpressTabValue={'p'} onpressEnter={'self'}/>
                                </div>
                                ) : (<></>)}
                                <div className='lr_warningholder' onClick={() => warningsubmitsetState('')}>
                                    <div className='lr_warning'>{warningsubmitstate}</div>
                                </div>
                                <div className='lr_clickbutton lr_clickbuttonactive' onClick={() => LoginRegister_SubmitClick()} ref={submitbuttonRef}>{submitbuttonState}</div>
                                {lrtype === 'l'? (
                                    <KeepMeSignedIn ref={keepmesignedininputRef} valuesRef={valuesRef} keepmesignedinIndex={5} tabIndex="-1" onpressTab={FocusElement} onpressTabValue={'p'} onpressEnter={'self'}/>
                                ) : (<></>)
                                }
                            </div>
                        </div>

                    </div>
                </div>
            </div>

        </div>
    )
}