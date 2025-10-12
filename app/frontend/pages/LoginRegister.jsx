import '../styling/LoginRegister.css'
import { useState, useRef } from 'react'
import { useNavigate, Link, useLocation } from 'react-router-dom'
import { UsernamePhoneInput } from './UsernamePhoneInput'
import { ArrowDownIcon } from '../components/svgs/UtilIcons'
import { PasswordInput } from './PasswordInput'
import { ReferalInput } from './ReferalInput'
import { TermsPoliciesCheckbox } from './TermsPoliciesCheckbox'


export function LoginRegister({ lrtype }){
    const lrsignedinexplainRef = useRef()
    const [lrsignedinstate, lrsignedinsetState] = useState(['rotate(0deg)', 'none'])
    const [lrheaderbackstate, lrheaderbacksetState] = useState()
    const valuesRef = useRef([null, null, null, ['Field is empty', 'Password field is empty', 'Passwords do not match', 'Referal code must be 10 characters long', 'You must agree to our Terms and Policies'], null]) // emailphoneval, type (:e-> email, p->phone), password, warning -> [0: emailphonewarning, 1: passwordwarning, 2: passwordconfirmwarning, 3: referalwarning, 4: checkboxwarning], referal
    const [warningstate, warningsetState] = useState('')
    const lrinfoholderRef = useRef()
    const lr_arrowsignedinRef = useRef()
    const [warningsubmitstate, warningsubmitsetState] = useState('')
    const usernamephoneinputRef = useRef()
    const passwordinputRef = useRef()
    const confirmpasswordinputRef = useRef()
    const referalinputRef = useRef()
    const termspoliciesinputRef = useRef()

    const navigate = useNavigate()
    const location = useLocation()

    async function LoginRegister_NextClick(){
        if(valuesRef.current[3][0] !== null){
            warningsetState(valuesRef.current[3][0])
            return
        }
        let response_status = null
        let request = {"v": valuesRef.current[0], "t": valuesRef.current[1], "c": lrtype}
        let response = await fetch(import.meta.env.VITE_URL + '/loginregister/finduser/', {
            method: 'POST',
            body: JSON.stringify(request),
        }).then(res => {
            response_status = res.status
            return res.json()
        }).then(data => data)

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
            setTimeout(function(){
                FocusElement('p')
            }, 200)
        }
    }

    function ClickSlide(move){
        if(move === 'forward'){
            lrinfoholderRef.current.style.left = '-425px'
            warningsetState('')
        }
        else if(move === 'back'){
            lrinfoholderRef.current.style.left = '0px'
            warningsubmitsetState('')
        }
    }

    function ClickArrowSignedIn(){
        let pos = lr_arrowsignedinRef.current.getAttribute('data-pos')
        if(pos === 'down'){
            lr_arrowsignedinRef.current.setAttribute('data-pos', 'up')
            lrsignedinsetState(['rotate(180deg)', 'block'])
        }
        else if(pos === 'up'){
            lr_arrowsignedinRef.current.setAttribute('data-pos', 'down')
            lrsignedinsetState(['rotate(0deg)', 'none'])
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
        if(valuesRef.current[3] === true){
            warningsubmitsetState(valuesRef.current[4])
            return
        }
        let response_status = null
        let request = {"v": valuesRef.current[0], "t": valuesRef.current[1], "p": valuesRef.current[2]}
        let response = await fetch(import.meta.env.VITE_URL + 'loginregister/login/', {
            method: 'POST',
            body: JSON.stringify(request),
            credentials: 'include',
        }).then(res => {
            response_status = res.status
            return res.json()
        }).then(data => data)
    }

    async function SubmitRegister(){
        for(let i = 1; i < valuesRef.current[3].length; i++){
            if(valuesRef.current[3][i] !== null){
                warningsubmitsetState(valuesRef.current[3][i])
                return
            }
        }
        
        let response_status = null
        let request = {"v": valuesRef.current[0], "t": valuesRef.current[1], "p": valuesRef.current[2], "r": valuesRef.current[4]}
        let response = await fetch(import.meta.env.VITE_URL + '/loginregister/register/', {
            method: 'POST',
            body: JSON.stringify(request),
            credentials: 'include',
        }).then(res => {
            response_status = res.status
            return res.json()
        }).then(data => data)

        if(response_status === 409){
            warningsubmitsetState(response)
        }
        else if(response_status === 200){
            /*location.state === null ? (navigate('/')) : navigate(location.state)*/
        }
    }

    function RefreshValues(){
        FocusElement('u')
        usernamephoneinputRef.current.value = ''
        passwordinputRef.current.value = ''
        valuesRef.current = [null, null, null, ['Field is empty', 'Password field is empty', 'Passwords do not match', 'Referal code must be 10 characters long', 'You must agree to our Terms and Policies'], null]
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
    }

    return(
        <div className='lr_holderall'>

            <div className='lr_body'>
                <div className='lr_mainbox'>
                    <Link to='/'><div className='lr_LogoHome'><img src='../components/images/MainLogo.png'/></div></Link>
                    <div className='lr_infoholder' ref={lrinfoholderRef}>
                        
                        <div className='lr_firststep'>
                            <div className='lr_inputnextholder'>
                                <div className='lr_header'>{lrtype === 'l' ? ('Log In') : ('Sign Up')}</div>
                                <div className='lr_maincontent'>
                                    <div className='lr_emailphone'>
                                        <div className='lr_firststep_label'>Email / Phone Number</div>
                                        <UsernamePhoneInput valuesRef={valuesRef} valueIndex={0} typeIndex={1} warningIndex={3} warningvalueIndex={0} alwaysPhone={false} alwaysEmail={false} ref={usernamephoneinputRef} autoFocus={true} onpressEnter={LoginRegister_NextClick}/>
                                    </div>
                                    <div className='lr_warningholder' onClick={() => warningsetState('')}>
                                        <div className='lr_warning'>{warningstate}</div>
                                    </div>
                                    <div className='lr_clickbutton' onClick={() => LoginRegister_NextClick()}>Next</div>
                                </div>
                            </div>
                            <div className='lr_loginregisterholder'>
                                <span>{lrtype === 'l' ? ("Don't have an account?") : ("Already have an account?")}</span>
                                <Link to={lrtype === 'l' ? ('/lrregister'): ('/lrlogin')} onClick={() => RefreshValues()} tabIndex="-1" replace><div className='lr_loginregisterclick'>{lrtype === 'l' ? ('Sign Up') : ('Log In')}</div></Link>
                            </div>
                        </div>

                        <div className='lr_secondstep'>
                            <div className='lr_backbutton' onClick={() => ClickSlide('back')}><ArrowDownIcon className='lr_backbuttonsvg'/><span className='lr_backbuttonspan'>Back</span></div>
                            <div className='lr_backheader' onClick={() => ClickSlide('back')}><span className='lr_backheaderspan'>{lrheaderbackstate}</span></div>
                            <div className='lr_maincontent_second'>
                                <PasswordInput classtype={'loginregister'} placeholder={'Password'} valuesRef={valuesRef} passwordIndex={2} warningIndex={3} warningvalueIndex={1} isconfirmpassword={false} ref={passwordinputRef} tabIndex="-1" onpressTab={FocusElement} onpressTabValue={'cp'}/>
                                {lrtype === 'r' ? (
                                <div className='lr_rholder'>
                                    <PasswordInput classtype={'loginregister'} placeholder={'Confirm Password'} valuesRef={valuesRef} passwordIndex={2} warningIndex={3} warningvalueIndex={2} isconfirmpassword={true} ref={confirmpasswordinputRef} tabIndex="-1" onpressTab={FocusElement} onpressTabValue={'r'}/>
                                    <ReferalInput valuesRef={valuesRef} referalIndex={4} warningIndex={3} warningvalueIndex={3} tabIndex="-1" ref={referalinputRef} onpressTab={FocusElement} onpressTabValue={'tp'}/>
                                    <TermsPoliciesCheckbox valuesRef={valuesRef} warningIndex={3} warningvalueIndex={4} ref={termspoliciesinputRef}/>
                                </div>
                                ) : (<></>)}
                                <div className='lr_warningholder' onClick={() => warningsubmitsetState('')}>
                                    <div className='lr_warning'>{warningsubmitstate}</div>
                                </div>
                                <div className='lr_clickbutton' onClick={() => LoginRegister_SubmitClick()}>{lrtype === 'l'? ('Log In') : ('Sign Up')}</div>
                                {lrtype === 'l'? (
                                    <>
                                    <div className='lr_signedinholder'>
                                        <input type='checkbox'/>
                                        <div className='lr_signedintext' onClick={() => ClickArrowSignedIn()}>
                                            <span>Keep me signed in</span>
                                            <ArrowDownIcon className='lr_signedinarrow' style={{transform: lrsignedinstate[0]}} ref={lr_arrowsignedinRef} data-pos='down'/>
                                        </div>
                                    </div>
                                    <div className='lr_signedinexplain' ref={lrsignedinexplainRef} style={{display: lrsignedinstate[1]}}>You'll be automatically signed in to your account when using this device</div>
                                    </>
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