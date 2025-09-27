import '../styling/LoginSignup.css'
import '../styling/RegisterExtra.css'

import { AreaCodePopUp } from './AreaCodePopUp'

import { AppleIcon } from '../components/svgs/CompaniesIcons'
import { GoogleIcon } from '../components/svgs/CompaniesIcons'
import { useEffect, useState } from 'react'
import { PhoneNumbers } from '../components/CountriesPhones'
import { ArrowDownIcon } from '../components/svgs/UtilIcons'
import { QuestionMarkIcon } from '../components/svgs/UtilIcons'
import { EyeIcon } from '../components/svgs/UtilIcons'
import { EyeCloseIcon } from '../components/svgs/UtilIcons'
import { Link, useNavigate } from 'react-router-dom'

/* For Password PopUp */
import { TickIcon } from '../components/svgs/UtilIcons'
import { TickOnlyCircleIcon } from '../components/svgs/UtilIcons'

export function Register(){

    const [warningstate, warningsetState] = useState('')
    const [emailphonestate, emailphonesetState] = useState('')
    const [passwordstate, passwordsetState] = useState('')
    const [re_passwordstate, re_passwordsetState] = useState('')
    const [checkboxstate, checkboxsetState] = useState('unchecked')
    const [country_svgstate, country_svgsetState] = useState([<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="M12.003 21q-1.866 0-3.51-.708q-1.643-.709-2.859-1.924q-1.216-1.214-1.925-2.856Q3 13.87 3 12.003q0-1.866.708-3.51q.709-1.643 1.924-2.859q1.214-1.216 2.856-1.925Q10.13 3 11.997 3q1.866 0 3.51.708q1.643.709 2.859 1.924q1.216 1.214 1.925 2.856Q21 10.13 21 11.997q0 1.866-.708 3.51q-.709 1.643-1.924 2.859q-1.214 1.216-2.856 1.925Q13.87 21 12.003 21Z"/></svg>])
    const [area_codestate, area_codesetstate] = useState('')
    const [eyeIconsvgstate, eyeIconsvgsetState] = useState(<EyeIcon/>)
    const [warning_submitstate, warning_submitsetState] = useState('')
    const [password_typestate, password_typesetState] = useState('password')
    const [password_eyeidstate, password_eyeidsetState] = useState('show')
    const [referal_codestate, referal_codesetState] = useState('')
    /* Password PopUp */
    const [password_popupstate, password_popupsetState] = useState([<TickOnlyCircleIcon/>,<TickOnlyCircleIcon/>,<TickOnlyCircleIcon/>,<TickOnlyCircleIcon/>])

    const reg_only_contains_numbers = new RegExp('^[0-9]+$');
    const reg_conatins_atLeast1_num = new RegExp('[0-9]');
    const reg_conatins_atLeast1_lowercase = new RegExp(['[a-z]']);
    const reg_conatins_atLeast1_uppercase = new RegExp(['[A-Z]']);
    let phone_value = false

    const navigate = useNavigate()
    
    function handleSignUp_Next(){
        console.log(country_svgstate)
        console.log(area_codestate)
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
        }
        else if(emailphonestate.search(reg_only_contains_numbers) === 0){
            if(emailphonestate.length<5){
                warningsetState('Please enter a valid phone number!')
                return
            }
            emailphonesetState('@+' + area_codestate + ' ' + emailphonestate)
        }
        warningsetState('')
        let First_SignUpStep_var = document.getElementsByClassName('FirstLoginStep')[0]
        let Second_SignUpStep_var = document.getElementsByClassName('SecondLoginStep')[0]

        First_SignUpStep_var.style.left = 'calc(-100% - 20px)'
        First_SignUpStep_var.style.right = 'calc(100% + 20px)'

        Second_SignUpStep_var.style.left = '20px'
        Second_SignUpStep_var.style.right = '20px'
    }

    function handleSignUp_Back(){
        console.log(country_svgstate)
        console.log(area_codestate)
        if(emailphonestate[0] === '@'){
            emailphonesetState(emailphonestate.split(' ')[1])
        }
        let First_SignUpStep_var = document.getElementsByClassName('FirstLoginStep')[0]
        let Second_SignUpStep_var = document.getElementsByClassName('SecondLoginStep')[0]

        First_SignUpStep_var.style.left = '20px'
        First_SignUpStep_var.style.right = '20px'

        Second_SignUpStep_var.style.left = 'calc(100% + 20px)'
        Second_SignUpStep_var.style.right = 'calc(-100% + 20px)'
    }

    useEffect(() =>{
        const country = Intl.DateTimeFormat().resolvedOptions().timeZone;
        country_svgsetState(PhoneNumbers[country]['svg'])
        area_codesetstate(PhoneNumbers[country]['n'])} ,[])

    useEffect(() => {
        /*const country = Intl.DateTimeFormat().resolvedOptions().timeZone;*/
        /* https://codepen.io/diego-fortes/pen/YzEPxYw */
        if( (emailphonestate.length >= 5) && (emailphonestate.search(reg_only_contains_numbers) === 0)){
            /*
            if(phone_value === false){
                if(country in PhoneNumbers){
                    country_svgsetState(PhoneNumbers[country]['svg'])
                    area_codesetStae(PhoneNumbers[country]['n'])
                }
                phone_value = true
            }*/
            document.getElementsByClassName('LoginPhoneNumber')[0].style.display = 'flex';
        }
        else{
            document.getElementsByClassName('LoginPhoneNumber')[0].style.display = 'none';
            phone_value = false
        }
    }, [emailphonestate])

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
            document.getElementById('Arrow_Referal').style.transform = 'rotate(180deg)'
            document.getElementById('referal_code').style.display = 'none'
        }
        else{
            e.target.id = 'down'
            document.getElementById('Arrow_Referal').style.transform = ''
            document.getElementById('referal_code').style.display = 'block'
        }
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

    /* Submit button */
    useEffect(() => {
        if( (passwordstate !== re_passwordstate) || (checkboxstate === 'unchecked') || (checkSubmit_password()) || (referal_codestate.length !== 10) ){
            document.getElementById('submit').classList.add('disable_submit')
            document.getElementById('submit_cursor').classList.add('cursor_not_allowed')
        }
        else{
            document.getElementById('submit').classList.remove('disable_submit')
            document.getElementById('submit_cursor').classList.remove('cursor_not_allowed')
        }
    },[passwordstate, checkboxstate, re_passwordstate, referal_codestate])
    
    function checkSubmit_password(){
        if(passwordstate.length < 8 || passwordstate.length > 30 || !(reg_conatins_atLeast1_num.test(passwordstate)) || !(reg_conatins_atLeast1_lowercase.test(passwordstate)) || !(reg_conatins_atLeast1_uppercase.test(passwordstate))){
            return true
        }
        return false
    }

    async function handleSignUp_Submit(){
        let response_status = null
        let request = null
        if(emailphonestate[0] === '@'){
            console.log(emailphonestate)
            request = {"e": null, "n": emailphonestate.slice(2), "p": passwordstate, "r": referal_codestate}
        }
        else{
            request = {"e": emailphonestate, "n": null, "p": passwordstate, "r": referal_codestate}
        }
        console.log(request)
        let response = await fetch('http://127.0.0.1:8000/loginregister/register/',{
            method: 'POST',
            body: JSON.stringify(request),
            credentials: 'include',
        }).then(res =>{
            response_status = res.status
            return res.json()
        }).then(data => data)
        if(response_status !== 200){
            warning_submitsetState(response)
        }
        else{
            warning_submitsetState('')
            navigate(-1)
            console.log(response)
        }

        //let response = await fetch('http://127.0.0.1:8000/loginregister/register/')
    }

    /* PopUp Password Requirements */
    useEffect(() => { Update_Password_Requirements() }, [passwordstate])

    function Update_Password_Requirements(){
        let len_0 = null
        let num_1 = null
        let low_2 = null
        let upp_3 = null
        if(passwordstate.length>=8 && passwordstate.length<=30){
            len_0 = <TickIcon/>
        }
        else {
            len_0 = <TickOnlyCircleIcon/>
        }

        if((reg_conatins_atLeast1_num.test(passwordstate))){
            num_1 = <TickIcon/>
        }
        else{
            num_1 = <TickOnlyCircleIcon/>
        }

        if((reg_conatins_atLeast1_lowercase.test(passwordstate))){
            low_2 = <TickIcon/>
        }
        else{
            low_2 = <TickOnlyCircleIcon/>
        }

        if((reg_conatins_atLeast1_uppercase.test(passwordstate))){
            upp_3 = <TickIcon/>
        }
        else{
            upp_3 = <TickOnlyCircleIcon/>
        }
        password_popupsetState([len_0, num_1, low_2, upp_3])
    }

    document.title = 'SignUp'

    return(
        <div className = 'registerAllView'>
        {/*<div className = 'empty_loginsingup_navbar'></div>*/}
        
        <AreaCodePopUp BlurClassName = 'LoginBody'
        setcountrysvg = {country_svgsetState} setareacode = {area_codesetstate}/>

        {/* PopUp See Password Requirements */}
        <div className='popUp_password_requirements light-theme'>
            <div className='popUp_password_bubble'>
                <div className ='popUp_password_item'>{password_popupstate[0]}<span>8-30 Characters</span></div>
                <div className ='popUp_password_item'>{password_popupstate[1]}<span>At least 1 Number</span></div>
                <div className ='popUp_password_item'>{password_popupstate[2]}<span>At least 1 Lowercase</span></div>
                <div className ='popUp_password_item'>{password_popupstate[3]}<span>At least 1 Uppercase</span></div>
            </div>
        </div>
        {/* ---end--- */}

        <div className = 'LoginBody light-theme'>
            <div className = 'Loginmainbox' id='Sign_Up'>
            <Link to = '/'><div className = 'LogoHome'><img src = '../components/images/MainLogo.png'/></div></Link>

                <div className = 'MainBox'>
                <div className = 'FirstLoginStep'>
                    <div className = 'LoginHeader'> Sign Up </div>
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
                                            <div>+{area_codestate}</div>
                                            <ArrowDownIcon width={12} height={12}/>
                                        </div>
                                    </div>
                                    
                                    <input type = 'text' id = 'emailphone' name = 'emailphone' autoComplete='off' autoCapitalize='off' spellCheck='false' className = 'LoginInputfield'
                                    onChange={(e) =>
                                        emailphonesetState(e.target.value)}/>
                                </div>
                                
                                <div className = 'LoginExtraField'>
                                    <div className = 'LoginWarningField'>{warningstate}</div>
                                </div>
                                <div className = 'LoginUpper_Nextbutton' onClick={() => handleSignUp_Next()}>Next</div>
                            </div>
                        
                        <div className = 'LoginORField'>
                            <div className = 'or_LoginLine'>
                                <div className = 'or_LoginLine_fill'></div>
                                <div className = 'or_LoginLine_orval'>or</div>
                                <div className = 'or_LoginLine_fill'></div>
                            </div>
                            <div className = 'LoginAlternative'>
                                <GoogleIcon width={18} height={18}/>
                                <span>SignUp With Google</span>
                            </div>
                            <div className = 'LoginAlternative'>
                                <AppleIcon/>
                                <span>SignUp With Apple</span>
                            </div>
                        </div>
                        <div className = 'SigUpHolder'><span>Already have an account?</span>
                            <Link to = '/login' replace><div className = 'SignUpClick'>Log In</div></Link>
                        </div>
                    </form>
                </div>
                
                <div className='SecondLoginStep'>
                    
                    <div className = 'SecondLoginStep_BackButton' onClick={() => handleSignUp_Back()}><ArrowDownIcon width={24} height={24} className = 'SecondLoginStep_BackButton_Svg'/><span className = 'SecondLoginStep_BackButton_span'>Back</span></div>
                    <div className = 'Email_Phone_Header_div' onClick={() => handleSignUp_Back()}><span className = 'Email_Phone_Header' >{Email_Phone_Header_returnHeader()}</span></div>
                    
                    <div className = 'second_step_signup_main_fields'>
                        <div className = 'second_step_signup_Password LoginInputfield cursorText Input_Div_OnFocusInner'>
                            <input type = {password_typestate} id = 'password_signup' name = 'password' autoComplete='off' autoCapitalize='off' spellCheck='false' className = 'Invisible_Input bigger_font_input' placeholder = 'Password' onChange={(e) => passwordsetState(e.target.value)}/>
                            <div className = 'SecondLoginStep_SvgsPassword'>
                                <QuestionMarkIcon className ='signup_password_questionmark' onMouseOver={() => {
                                    console.log(document.getElementsByClassName('popUp_password_requirements')[0])
                                    let pass_req = document.getElementsByClassName('popUp_password_requirements')[0]
                                    pass_req.style.bottom = '50px'
                                    pass_req.style.opacity = '1'}}

                                    onMouseOut={() => {
                                        let pass_req = document.getElementsByClassName('popUp_password_requirements')[0]
                                        pass_req.style.bottom = '-170px'
                                        pass_req.style.opacity = '0'
                                    }}/>
                                <div className = 'SecondLoginStep_SvgsPassword_EyeIcon' id={password_eyeidstate} onClick={()=> toggleEyeSvg()}>{eyeIconsvgstate}</div>
                            </div>
                        </div>
                    </div>
                    <input type = 'password' id = 're_password' name = 're_password' autoComplete='off' autoCapitalize='off' spellCheck='false' className = 'LoginInputfield bigger_font_input margin_top_input' placeholder = 'Re-enter Password' onChange={(e) => re_passwordsetState(e.target.value)}/>
                    <div className = 'Second_SignUpStep_errorMessage'></div>
                    <div className = 'Second_SignUpStep_RefferalCode  margin_top_input'>
                        <div className = 'Second_SignUpStep_header'><span>Referal Code</span><div className = 'Second_SignUpStep_header_SvgArrow' id = 'up' onClick = {(e) => toggleArrowReferalCodeSvg(e)}><ArrowDownIcon width={16} height = {16} id = 'Arrow_Referal'/></div></div>
                        <input type = 'text' id = 'referal_code' name = 'referal_code' maxLength = '10' autoComplete='off' autoCapitalize='off' spellCheck='false' className = 'LoginInputfield bigger_font_input margin_top_input_referal' placeholder = '' onChange={(e) => referal_codesetState(e.target.value)}/>
                    </div>
                    <div className = 'Second_SignUpStep_PrivacyPolicy'>
                        <div className = 'Second_SignUpStep_PrivacyPolicy_checkbox'>
                            <input type='checkbox' onClick={() => { (checkboxstate === 'unchecked')? checkboxsetState('checked'): checkboxsetState('unchecked')}}/>
                        </div>
                        <div className = 'Second_SignUpStep_PrivacyPolicy_text margin_top_input'>
                            By Signing up you agree to our <span className = 'Second_SignUpStep_PrivacyPolicy_text_Link' id='Terms_of_use'>Terms of Use</span>, our <span className = 'Second_SignUpStep_PrivacyPolicy_text_Link' id = 'Privacy_policy'>Privacy Policy</span> and our <span className = 'Second_SignUpStep_PrivacyPolicy_text_Link' id = 'Cookies_policy'>Cookies Policy</span>
                        </div>
                    </div>
                    <div className = 'warning_submit' onClick={() => warning_submitsetState('')}>{warning_submitstate}</div>
                    <div id='submit_cursor'>
                        <div className = 'LoginUpper_Nextbutton margin_top_submit' id='submit' onClick={async () => await handleSignUp_Submit()}>Submit</div>
                    </div>
                </div>
                </div>
            </div>
        </div>
        </div>
    )
}