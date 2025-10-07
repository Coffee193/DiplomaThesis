import '../styling/LoginRegister.css'
import { useState, useEffect, useRef } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { UsernamePhoneInput } from './UsernamePhoneInput'
import { ArrowDownIcon } from '../components/svgs/UtilIcons'
import { PasswordInput } from './PasswordInput'


export function LoginRegister(){
    const [lrheaderstate, lrheadersetState] = useState()
    const [lrlinkclickstate, lrlinkclicksetState] = useState([null , null])
    const [lrsubmitbuttonstate, lrsubmitbuttonsetState] = useState()
    const [lrextravalstate, lrextravalsetState] = useState({'lr_keepsignedin': null})
    const lrsignedinexplainRef = useRef()
    const [lrsignedinstate, lrsignedinsetState] = useState(['rotate(180deg)', 'none'])
    const [lrheaderbackstate, lrheaderbacksetState] = useState()

    const navigate = useNavigate()

    useEffect(() => {
        if(window.location.pathname === '/lrlogin'){
            lrheadersetState('Log In')
            lrlinkclicksetState(['Sign Up', '/lrregister'])
            lrsubmitbuttonsetState('Log In')
            lrextravalsetState({'lr_keepsignedin': 'display_block'})
        }
        else if(window.location.pathname === '/lrregister'){
            lrheadersetState('Sign Up')
            lrlinkclicksetState(['Log In', '/lrlogin'])
            lrsubmitbuttonsetState('Sign Up')
            lrextravalsetState({'lr_keepsignedin': 'display_none'})
        }
    },[window.location.pathname])

    return(
        <div className='lr_holderall'>


            <div className='lr_body'>
                <div className='lr_mainbox'>
                    <Link to='/'><div className='lr_LogoHome'><img src='../components/images/MainLogo.png'/></div></Link>
                    <div className='lr_infoholder'>
                        
                        <div className='lr_firststep'>
                            <div className='lr_inputnextholder'>
                                <div className='lr_header'>{lrheaderstate}</div>
                                <div className='lr_maincontent'>
                                    <div className='lr_emailphone'>
                                        <div className='lr_firststep_label'>Email / Phone Number</div>
                                        <UsernamePhoneInput/>
                                    </div>
                                    <div className='lr_clickbutton'>Next</div>
                                </div>
                            </div>
                            <div className='lr_loginregisterholder'>
                                <span>Don't have an account?</span>
                                <Link to={lrlinkclickstate[1]} ><div className='lr_loginregisterclick'>{lrlinkclickstate[0]}</div></Link>
                            </div>
                        </div>

                        <div className='lr_secondstep'>
                            <div className='lr_backbutton'><ArrowDownIcon className='lr_backbuttonsvg'/><span className='lr_backbuttonspan'>Back</span></div>
                            <div className='lr_backheader'><span className='lr_backheaderspan'>{lrheaderbackstate}</span></div>
                            <div className='lr_maincontent_second'>
                                <PasswordInput classtype={'loginregister'} placeholder={'Password'}/>
                                <div className='lr_clickbutton'>{lrsubmitbuttonstate}</div>
                                <div className={lrextravalstate['lr_keepsignedin']}>
                                    <div className='lr_signedinholder'>
                                        <input type='checkbox'/>
                                        <div className='lr_signedintext'>
                                            <span>Keep me signed in</span>
                                            <ArrowDownIcon className='lr_signedinarrow' style={{transform: lrsignedinstate[0]}}/>
                                        </div>
                                    </div>
                                    <div className='lr_signedinexplain' ref={lrsignedinexplainRef} style={{display: lrsignedinstate[1]}}>You'll be automatically signed in to your account when using this device</div>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>
            </div>

        </div>
    )
}