import '../styling/LoginSignup.css'

import { AreaCodePopUp } from './AreaCodePopUp'
import { ArrowDownIcon } from '../components/svgs/UtilIcons'

import { PhoneNumbers } from '../components/CountriesPhones'

import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { GoogleIcon } from '../components/svgs/CompaniesIcons'
import { AppleIcon } from '../components/svgs/CompaniesIcons'
import { EyeIcon } from '../components/svgs/UtilIcons'
import { EyeCloseIcon } from '../components/svgs/UtilIcons'

export function Login(){

    const [emailphonestate, emailphonesetState] = useState('')
    const [country_svgstate, country_svgsetState] = useState([<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="M12.003 21q-1.866 0-3.51-.708q-1.643-.709-2.859-1.924q-1.216-1.214-1.925-2.856Q3 13.87 3 12.003q0-1.866.708-3.51q.709-1.643 1.924-2.859q1.214-1.216 2.856-1.925Q10.13 3 11.997 3q1.866 0 3.51.708q1.643.709 2.859 1.924q1.216 1.214 1.925 2.856Q21 10.13 21 11.997q0 1.866-.708 3.51q-.709 1.643-1.924 2.859q-1.214 1.216-2.856 1.925Q13.87 21 12.003 21Z"/></svg>])
    const [area_codeState, area_codesetState] = useState('')
    const [warningstate, warningsetState] = useState('')

    const [eyeIconsvgstate, eyeIconsvgsetState] = useState(<EyeIcon/>)
    const [warning_submitstate, warning_submitsetState] = useState('')

    const [password_eyeidstate, password_eyeidsetState] = useState('show')
    const [password_typestate, password_typesetState] = useState('password')
    const [passwordstate, passwordsetState] = useState('')
    const [remembermestate, remembermesetState] = useState(false)


    const reg_only_contains_numbers = new RegExp('^[0-9]+$');
    let phone_value = false
    let i = ''

    const navigate = useNavigate()

    async function handleLogIn_Next(){
        let request = null
        let num = false
        console.log(country_svgstate)
        console.log(area_codeState)
        if(emailphonestate === ''){
            warningsetState('Please enter a valid email or Phone number')
            return
        }
        /*(emailphonestate.search(reg_only_contains_numbers) === 0) || (emailphonestate.slice(-10) !== '@gmail.com' && emailphonestate.slice(-13) !== '@hotmail.com' && emailphonestate.slice(-10) !== '@yahoo.com' )) */
        /*
        else if( !((emailphonestate.search(reg_only_contains_numbers) === 0) || (emailphonestate.slice(-10) === '@gmail.com' || emailphonestate.slice(-12) === '@hotmail.com' || emailphonestate.slice(-10) === '@yahoo.com' ))){
            warningsetState('Please enter a valid email address')
            return
        }*/

        /* The exactly above was switched for the lower one because in the above you can pass @gmail.com with nothing in front and all will be
        ok*/
        
        else if( !((emailphonestate.search(reg_only_contains_numbers) === 0)) ){
            let contains_a = emailphonestate.indexOf('@')
            let contains_dot = emailphonestate.indexOf('.')
            if( (contains_a === -1) || (contains_dot === -1) || (contains_a + 1 >= contains_dot) || (emailphonestate.length < 5) || (contains_a === 0) || (contains_dot === emailphonestate.length - 1)){
                warningsetState('Please enter a valid email address!')
                return
            }
            request = {"e": emailphonestate, "n": null, "p": ""}
        }
        else if(emailphonestate.search(reg_only_contains_numbers) === 0){
            if(emailphonestate.length<5){
                warningsetState('Please enter a valid phone number!')
                return
            }
            request = {"e": null, "n": area_codeState + ' ' + emailphonestate, "p":""}
            num = true
        }
        
        console.log(request)
        let response = await fetch('http://127.0.0.1:8000/loginregister/finduser/',{
            method: 'POST',
            body: JSON.stringify(request)
        }).then(res => res.json()).then(data => data)
        console.log(response)
        if(response === 'User not Found'){
            warningsetState(response)
            return
        }
        
        //response = JSON.parse(response)
        //i = response["i"]
        
        warningsetState('')
        if(num === true){
            emailphonesetState('@+' + area_codeState + ' ' + emailphonestate)
        }
        let First_SignUpStep_var = document.getElementsByClassName('FirstLoginStep')[0]
        let Second_SignUpStep_var = document.getElementsByClassName('SecondLoginStep')[0]

        First_SignUpStep_var.style.left = 'calc(-100% - 20px)'
        First_SignUpStep_var.style.right = 'calc(100% + 20px)'

        Second_SignUpStep_var.style.left = '20px'
        Second_SignUpStep_var.style.right = '20px'
    }

    async function handleLogIn_Submit(){
        let request = null
        if(emailphonestate[0] === '@'){
            request = {"e": null, "n": emailphonestate.slice(2), "p": passwordstate, "r": remembermestate}
        }
        else{
            request = {"e": emailphonestate, "n": null, "p": passwordstate, "r": remembermestate}
        }
        console.log(request)
        let response_status = null
        let response = await fetch('http://127.0.0.1:8000/loginregister/login/',{
            method: 'POST',
            body: JSON.stringify(request),
            credentials: 'include',
        }).then(res => {
            response_status = res.status
            return res.json()}).then(data => data)

        console.log(response_status)
        if(response_status !== 200){
            warning_submitsetState(response)
        }
        else{
            warning_submitsetState('')
            {/* LOCALHOST test stage set cookie */}
            
            {/* */}
            navigate(-1)
        }

        //let response = await fetch('http://127.0.0.1:8000/loginregister/register/')
    }

    useEffect(() =>{
        
        const country = Intl.DateTimeFormat().resolvedOptions().timeZone;
        country_svgsetState(PhoneNumbers[country]['svg'])
        area_codesetState(PhoneNumbers[country]['n'])} ,[])

    useEffect(() => {
        /*const country = Intl.DateTimeFormat().resolvedOptions().timeZone;*/
        /* https://codepen.io/diego-fortes/pen/YzEPxYw */
        if( (emailphonestate.length >= 5) && (emailphonestate.search(reg_only_contains_numbers) === 0)){
            document.getElementsByClassName('LoginPhoneNumber')[0].style.display = 'flex';
        }
        else{
            document.getElementsByClassName('LoginPhoneNumber')[0].style.display = 'none';
            phone_value = false
        }
    }, [emailphonestate])

    function handleSignUp_Back(){
        if(emailphonestate[0] === '@'){
            emailphonesetState(emailphonestate.split(' ')[1])
        }
        let First_SignUpStep_var = document.getElementsByClassName('FirstLoginStep')[0]
        let Second_SignUpStep_var = document.getElementsByClassName('SecondLoginStep')[0]

        First_SignUpStep_var.style.left = '20px'
        First_SignUpStep_var.style.right = '20px'

        Second_SignUpStep_var.style.left = 'calc(100% + 20px)'
        Second_SignUpStep_var.style.right = 'calc(-100% + 20px)'

        i = null
    }

    function Email_Phone_Header_returnHeader(){
        let header_var = null
        if(emailphonestate[0] === '@'){
            header_var = emailphonestate.slice(1)
        }
        else{
            header_var = emailphonestate
        }
        if(header_var.length <25){
            console.log(header_var.length)
            return header_var
        }
        else{
            console.log( (header_var.slice(0, 22) + '...').length )
            return header_var.slice(0,22) + '...'
        }
    }

    function toggleEyeSvg(){
        
        if(password_eyeidstate === 'show'){
            password_eyeidsetState('hide')
            eyeIconsvgsetState(<EyeCloseIcon/>)
            //document.getElementById('password_signup').type = 'text'
            password_typesetState('text')
        }
        else{
            password_eyeidsetState('show')
            eyeIconsvgsetState(<EyeIcon/>)
            //document.getElementById('password_signup').type = 'password'
            password_typesetState('password')
        }
        console.log(e.target.id)
    }

    function toggleArrowReferalCodeSvg(e){
        if(e.target.id === 'down'){
            e.target.id = 'up'
            document.getElementsByClassName('Arrow_KeepmeSignedIn')[0].style.transform = 'rotate(180deg)'
            document.getElementById('KeepmeSignedInDown').style.display = 'none'
        }
        else{
            e.target.id = 'down'
            document.getElementsByClassName('Arrow_KeepmeSignedIn')[0].style.transform = ''
            document.getElementById('KeepmeSignedInDown').style.display = 'block'
        }
    }

    return(
        <>

            <AreaCodePopUp BlurClassName = 'LoginBody'
            setcountrysvg = {country_svgsetState} setareacode = {area_codesetState}/>
            
            <div className = 'LoginBody'>
                <div className = 'Loginmainbox'>
                    <Link to = '/'><div className = 'LogoHome'><img src = '../components/images/MainLogo.png'/></div></Link>
                    <div className = 'MainBox'>
                        <div className = 'FirstLoginStep'>
                            <div className = 'LoginHeader'> Log In </div>
                            <form action = '#' className = 'LoginForm'>
                                <div className = 'LoginUpperLabel'>Email / Phone Number</div>
                                <div className = 'LoginUpper'>
                                    <div className = 'LoginInitialField'>
                                        <div className = 'LoginPhoneNumber' onClick={() => {
                                                                                document.getElementsByClassName('LoginBody')[0].id = 'blurPage'
                                                                                document.getElementsByClassName('AreaCode_login_popUp')[0].classList.add('active')
                                                                                document.getElementsByClassName('Pop_up_darken_all')[0].style.display = 'block'
                                                                                }}>
                                                                                {country_svgstate}
                                                                                <div>
                                                                                    <div>+{area_codeState}</div>
                                                                                    <ArrowDownIcon width={12} height={12}/>
                                                                                </div>
                                                                            </div>
                                        <input type = 'text' id = 'username' name = 'username' autoComplete='off' autoCapitalize='off' spellCheck='false' className = 'LoginInputfield'
                                        onChange={(e) =>
                                            emailphonesetState(e.target.value)}/>
                                    </div>
                                    <div className = 'LoginExtraField'>
                                        <div className = 'LoginWarningField'>{warningstate}</div>
                                    <div className = 'LoginForgotPassword_orUserName'>Forgot Username</div>
                                    </div>
                                    <div className = 'LoginUpper_Nextbutton' onClick={async () => await handleLogIn_Next()}>Next</div>
                                </div>
                                <div className = 'LoginORField'>
                                    <div className = 'or_LoginLine'>
                                        <div className = 'or_LoginLine_fill'></div>
                                        <div className = 'or_LoginLine_orval'>or</div>
                                        <div className = 'or_LoginLine_fill'></div>
                                    </div>
                                    <div className = 'LoginAlternative'>
                                        <GoogleIcon width={18} height={18}/>
                                        <span>Login With Google</span>
                                    </div>
                                    <div className = 'LoginAlternative'>
                                        <AppleIcon/>
                                        <span>Login With Apple</span>
                                    </div>
                                </div>
                                <div className = 'SigUpHolder'><span>Don't have an account?</span>
                                    <Link to = '/register' replace><div className = 'SignUpClick'>Sign Up</div></Link>
                                </div>
                            </form>
                        </div>
                        <div className = 'SecondLoginStep'>
                            <div className = 'SecondLoginStep_BackButton' onClick={() => handleSignUp_Back()}><ArrowDownIcon width={24} height={24} className = 'SecondLoginStep_BackButton_Svg'/><span className = 'SecondLoginStep_BackButton_span'>Back</span></div>
                            <div className = 'Email_Phone_Header_div' onClick={() => handleSignUp_Back()}><span className = 'Email_Phone_Header' >{Email_Phone_Header_returnHeader()}</span></div>
                            
                            <div className = 'second_step_signup_main_fields'>
                                <div className = 'second_step_signup_Password LoginInputfield cursorText Input_Div_OnFocusInner'>
                                    <input type = {password_typestate} id = 'password_signup' name = 'password' autoComplete='off' autoCapitalize='off' spellCheck='false' className = 'PasswordLoginInput' placeholder = 'Password' onChange={(e) => passwordsetState(e.target.value)}/>
                                    <div className = 'SecondLoginStep_SvgsPassword'>
                                        <div className = 'SecondLoginStep_SvgsPassword_EyeIcon' id={password_eyeidstate} onClick={(e)=> toggleEyeSvg(e)}>{eyeIconsvgstate}</div>
                                    </div>
                                </div>
                            </div>
                            <div className = 'LoginExtraField margin_top_ForgotPassword'>
                                    <div className = 'LoginWarningField'>{warning_submitstate}</div>
                                    <div className = 'LoginForgotPassword_orUserName'>Forgot Password</div>
                            </div>
                            <div id='submit_cursor'>
                                <div className = 'LoginUpper_Nextbutton margin_top_ForgotPassword' id='submit' onClick={async () => await handleLogIn_Submit()}>Log In</div>
                            </div>
                            <div className = 'Login_keep_me_signed_in'>
                                <input type='checkbox' onClick={() => { (remembermestate === false)? remembermesetState(true): remembermesetState(false)}}/>
                                <div className='keep_me_signed_in_textsvg'>
                                    <span>Keep me signed in</span><ArrowDownIcon width={16} height = {16} id='up' className='Arrow_KeepmeSignedIn' style={{transform: 'rotate(180deg)'}} onClick = {(e) => toggleArrowReferalCodeSvg(e)} />
                                </div>
                            </div>
                            <div id='KeepmeSignedInDown'>
                                    You'll be automatically signed in to your account when using this device.<br/>

                            </div>
                        </div>
                    </div>
                    
                </div>                
            </div>

            
        </>
    )
}