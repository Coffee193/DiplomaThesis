import '../styling/LoginRegister.css'
import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { UsernamePhoneInput } from './UsernamePhoneInput'

export function LoginRegister(){
    const [lrheaderstate, lrheadersetState] = useState()

    const nvigate = useNavigate()

    useEffect(() => {
        if(window.location.pathname === '/lrlogin'){
            lrheadersetState('Log In')
        }
        else if(window.location.pathname === '/lrregister'){
            lrheadersetState('Sign Up')
        }
    },[])

    return(
        <div className='lr_holderall'>


            <div className='lr_body'>
                <div className='lr_mainbox'>
                    <Link to='/'><div className='LogoHome'><img src='../components/images/MainLogo.png'/></div></Link>
                    <div style={{position: 'relative'}}>
                        <div className='lr_firststep'>
                            <div className='lr_header'>{lrheaderstate}</div>
                            <div className='lr_maincontent'>
                                <div className='lr_emailphone'>
                                    <div className='lr_firststep_label'>Email / Phone Number</div>
                                    <UsernamePhoneInput/>
                                </div>
                                <div className='lr_nextbutton'>Next</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    )
}