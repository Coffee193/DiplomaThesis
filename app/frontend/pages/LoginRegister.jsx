import '../styling/LoginRegister.css'
import { useState, useEffect, useRef } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { UsernamePhoneInput } from './UsernamePhoneInput'
import { ArrowDownIcon } from '../components/svgs/UtilIcons'
import { PasswordInput } from './PasswordInput'


export function LoginRegister({ lrtype }){
    const lrsignedinexplainRef = useRef()
    const [lrsignedinstate, lrsignedinsetState] = useState(['rotate(0deg)', 'none'])
    const [lrheaderbackstate, lrheaderbacksetState] = useState()
    const valuesRef = useRef([null, null, null, true,'Field is empty']) // emailphonewarningval, type (:e-> email, p->phone, w->warning), password
    const [warningstate, warningsetState] = useState('')
    const lr_firststepRef = useRef()
    const lr_secondstepRef = useRef()
    const lr_arrowsignedinRef = useRef()
    const [warningsubmitstate, warningsubmitsetState] = useState('')

    const navigate = useNavigate()

    async function LoginRegister_NextClick(){
        if(valuesRef.current[3] === true){
            warningsetState(valuesRef.current[4])
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
            valuesRef.current[3] = true
            valuesRef.current[4] = 'Field is empty'
        }
    }

    function ClickSlide(move){
        if(move === 'forward'){
            lr_firststepRef.current.style.left = 'calc(-100% - 20px)'
            lr_firststepRef.current.style.right = 'calc(100% + 20px)'

            lr_secondstepRef.current.style.left = '20px'
            lr_secondstepRef.current.style.right = '20px'
        }
        else if(move === 'back'){
            console.log('back')
            lr_firststepRef.current.style.left = '20px'
            lr_firststepRef.current.style.right = '20px'

            lr_secondstepRef.current.style.left = 'calc(100% + 20px)'
            lr_secondstepRef.current.style.right = 'calc(-100% + 20px)'
        }
    }

    function GoBack(){
        ClickSlide('back')
        valuesRef.current[3] = false
        valuesRef.current[4] = ''
    }

    /* Maybe put the firststep and secondstep in a position relative div and move that parent div */

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
        console.log('SUUUU')
        let response_status = null
        let request = {"v": valuesRef.current[0], "t": valuesRef.current[1], "p": valuesRef.current[2]}
        let response = await fetch(import.meta.env.VITE_URL + 'loginregister/login/', {
            method: 'POST',
            body: JSON.stringify(request),
        }).then(res => {
            response_status = res.status
            return res.json()
        }).then(data => data)
    }

    async function SubmitRegister(){
        let response_status = null
        let response = await fetch(import.meta.env.VITE_URL + '/loginregister/register/', {

        })
    }

    return(
        <div className='lr_holderall'>

            <div className='lr_body'>
                <div className='lr_mainbox'>
                    <Link to='/'><div className='lr_LogoHome'><img src='../components/images/MainLogo.png'/></div></Link>
                    <div className='lr_infoholder'>
                        
                        <div className='lr_firststep' ref={lr_firststepRef}>
                            <div className='lr_inputnextholder'>
                                <div className='lr_header'>{lrtype === 'l' ? ('Log In') : ('Sign Up')}</div>
                                <div className='lr_maincontent'>
                                    <div className='lr_emailphone'>
                                        <div className='lr_firststep_label'>Email / Phone Number</div>
                                        <UsernamePhoneInput valuesRef={valuesRef} valueIndex={0} typeIndex={1} warningIndex={3} warningtextIndex={4}/>
                                    </div>
                                    <div className='lr_warningholder' onClick={() => warningsetState('')}>
                                        <div className='lr_warning'>{warningstate}</div>
                                    </div>
                                    <div className='lr_clickbutton' onClick={() => LoginRegister_NextClick()}>Next</div>
                                </div>
                            </div>
                            <div className='lr_loginregisterholder'>
                                <span>{lrtype === 'l' ? ("Don't have an account?") : ("Already have an account?")}</span>
                                <Link to={lrtype === 'l' ? ('/lrregister'): ('/lrlogin')} ><div className='lr_loginregisterclick'>{lrtype === 'l' ? ('Sign Up') : ('Log In')}</div></Link>
                            </div>
                        </div>

                        <div className='lr_secondstep' ref={lr_secondstepRef}>
                            <div className='lr_backbutton' onClick={() => GoBack()}><ArrowDownIcon className='lr_backbuttonsvg'/><span className='lr_backbuttonspan'>Back</span></div>
                            <div className='lr_backheader' onClick={() => GoBack()}><span className='lr_backheaderspan'>{lrheaderbackstate}</span></div>
                            <div className='lr_maincontent_second'>
                                <PasswordInput classtype={'loginregister'} placeholder={'Password'} valuesRef={valuesRef} passwordindex={2} warningIndex={3} warningtextIndex={4}/>
                                {lrtype === 'r' ? (
                                <PasswordInput classtype={'loginregister'} placeholder={'Confirm Password'} valuesRef={valuesRef} />
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