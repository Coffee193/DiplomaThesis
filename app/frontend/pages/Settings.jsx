import '../styling/Settings.css'
import { NavBar } from './NavBar'
import { useEffect, useState, useRef } from 'react'
import { UserIconThin, PencilIcon, XCloseIcon, EyeIcon, EyeCloseIcon } from '../components/svgs/UtilIcons'
import { useNavigate } from 'react-router-dom'

export function Settings(){

    const [iconstate, iconsetState] = useState()
    const [namestate, namesetState] = useState()
    const [emailstate, emailsetState] = useState()
    const [phonestate, phonesetState] = useState()
    const [adminstate, adminsetState] = useState()
    const navigate = useNavigate()
    const popupRef = useRef()
    const darkenRef = useRef()
    const [changeheaderstate, changeheadersetState] = useState()
    const [changevalstate, changevalsetState] = useState()
    const changeboxRef = useRef()
    const changeinputRef = useRef()
    const changeinputsvgRef = useRef()
    const changepasswordRef = useRef()
    const [passwordeyestate, passwordeyesetState] = useState([<EyeIcon/>, true, 'password'])
    const changebuttonRef = useRef()
    const changeboxpasswordRef = useRef()
    const [changewarningstate, changewarningsetState] = useState('')
    const changevaltypeRef = useRef()
    const changesubmitactiveRef = useRef([false, 'Fields are empty'])
    const [newpasswordeyestate, newpasswordeyesetState] = useState([<EyeIcon/>, true, 'password'])
    const [newpasswordsvgstate, newpasswordsvgsetState] = useState()

    const reg_contains_only_num = new RegExp('^[0-9]+$')
    const reg_contains_atleast1_num = new RegExp(['[0-9]'])
    const reg_contains_atleast1_lowercase = new RegExp(['[a-z]'])
    const reg_contains_atleast1_uppercase = new RegExp(['[A-Z]'])
    
    useEffect(() => {
        GetUserInfo()
        {/*if(1 === ''){
            ojh
        }
        else{
            iconsetState(<UserIconThin className='settingsicon'/>)
        }

        if(1 === ''){

        }
        else{
            namesetState('Welcome, Back!')
        }
        
        if(1 === ''){
            emailsetState(<div className='settingscontent_infoval vallight'>no email provided</div>)
        }
        else{
            let emailval = 'chrisioasdhiosadioasdiojsaio9ioasjdiosd@gmail.com'
            if(emailval.length > 39){
                emailval = emailval.slice(0, 37) + '...'
            }
            emailsetState(<div className='settingscontent_infoval'>{emailval}</div>)
        }

        if(1 === 1){
            phonesetState(<div className='settingscontent_infoval vallight'>no phone number provided</div>)
        }
        else{

        }

        if(1 === 1){
            adminsetState(
                <div className='settingscontent_referal'>REFERAL CODES</div>
            )
        }
        else{

        }*/}
    }, [])

    async function GetUserInfo(){
        let response_status = null
        let response = await fetch('http://127.0.0.1:8000/loginregister/getuserinfo/', {
            method: 'GET',
            credentials: 'include',
        }).then(res => {
            response_status = res.status
            return res.json()
        }).then(data => data)

        if(response_status === 200){

            if(response['img_path'] === null){
                iconsetState(<UserIconThin className='settingsicon' onClick={() => PopUpOpenClose('open', 'Change Image', '', false, 'image')}/>)
            }
            else{

            }

            if(response['name'] === null){
                namesetState('Welcome, Back!')
            }
            else{
                
            }

            if(response['email'] === null){
                emailsetState(<div className='settingscontent_infoval vallight'>no email provided</div>)
            }
            else{
                let emailval = response['email']
                if(emailval.length > 39){
                    emailval = emailval.slice(0, 37) + '...'
                }
                emailsetState(<div className='settingscontent_infoval'>{emailval}</div>)
            }

            if(response['phone'] === null){
                phonesetState(<div className='settingscontent_infoval vallight'>no phone number provided</div>)
            }
            else{
                phonesetState(<div className='settingscontent_infoval'>{response['phone']}</div>)
            }
            
            if(response['is_admin'] === true){
                adminsetState(<div className='settingscontent_referal'>REFERAL CODES</div>)
            }
            
        }
        else if(response_status === 401 || response_status === 403){
            navigate('/login')
        }
    }

    function PopUpOpenClose(action='open', header = '', text = '', changetype = ''){
        if(action === 'open'){
            popupRef.current.style.pointerEvents = 'all'
            popupRef.current.style.opacity = '1'
            popupRef.current.style.transform = 'scale(1)'
            darkenRef.current.style.opacity = '1'
            darkenRef.current.style.pointerEvents = 'all'

            changevaltypeRef.current = changetype
            
            changeheadersetState(header)
            if(changetype !== 'image'){
                console.log('&&&')
                if(changetype === 'password'){
                    newpasswordeyesetState([<EyeIcon/>, true, 'password'])
                    newpasswordsvgsetState(<div className='settingschange_valbox_extra settingschange_valbox_extra_visible' onClick={() => NewPasswordVisibility()}>
                        {newpasswordeyestate[0]}
                    </div>)
                }
                else{
                    newpasswordeyesetState([<EyeCloseIcon/>, false, 'text'])
                    newpasswordsvgsetState(<></>)
                }
                changevalsetState(
                    <div className='settingschange_valbox' ref={changeboxRef}>
                        <input placeholder={text} className='settingschange_valinput' onFocus={() => changeboxRef.current.classList.add('settingschange_focus')} onBlur={() => changeboxRef.current.classList.remove('settingschange_focus')} ref={changeinputRef} type={newpasswordeyestate[2]} onChange={() => {SettingsInputChange()
                            ChangeValuesSubmitButton()}
                        }/>
                        {newpasswordsvgstate}
                        <div className='settingschange_valbox_extra' ref={changeinputsvgRef} onClick={() => {changeinputRef.current.value = ''
                            SettingsInputChange()}
                        }>
                            <XCloseIcon/>
                        </div>
                    </div>
                )
            }
            else{

            }

        }
        else if(action === 'close'){
            popupRef.current.style.pointerEvents = 'none'
            popupRef.current.style.opacity = '0'
            popupRef.current.style.transform = 'scale(0.8)'
            darkenRef.current.style.opacity = '0'
            darkenRef.current.style.pointerEvents = 'none'
            changewarningsetState('')
            changeinputRef.current.value = ''
            changepasswordRef.current.value = ''
            SettingsInputChange()
            changesubmitactiveRef.current = [false, 'Fields are empty']
        }
    }

    function SettingsInputChange(){
        if(changeinputRef.current.value.length > 0){
            changeinputsvgRef.current.style.opacity = 1
            changeinputsvgRef.current.style.pointerEvents = 'all'
        }
        else{
            changeinputsvgRef.current.style.opacity = 0
            changeinputsvgRef.current.style.pointerEvents = 'none'
        }
    }

    function PasswordVisibility(){
        if(passwordeyestate[1] === true){
            passwordeyesetState([<EyeCloseIcon/>, false, 'text'])
        }
        else{
            passwordeyesetState([<EyeIcon/>, true, 'password'])
        }
    }
    function NewPasswordVisibility(){
        if(newpasswordeyestate[1] === true){
            newpasswordeyesetState([<EyeCloseIcon/>, false, 'text'])
        }
        else{
            newpasswordeyesetState([<EyeIcon/>, true, 'password'])
        }
    }

    function ChangeValuesSubmitButton(){
        let passwordval = changepasswordRef.current.value
        if(passwordval.length <= 8){
            ChangeSettingsSetSubmitAcive(false, 'Password is too short')
            return
        }
        else if(passwordval.length > 30){
            ChangeSettingsSetSubmitAcive(false, 'Password is too long')
            return
        }
        else if(!reg_contains_atleast1_num.test(passwordval)){
            ChangeSettingsSetSubmitAcive(false, 'Password must contain at least 1 number')
            return
        }
        else if(!reg_contains_atleast1_lowercase.test(passwordval)){
            ChangeSettingsSetSubmitAcive(false, 'Password must contain at least 1 lowercase')
            return
        }
        else if(!reg_contains_atleast1_uppercase.test(passwordval)){
            ChangeSettingsSetSubmitAcive(false, 'Password must contain at least 1 uppercase')
            return
        }

        let inp_val = changeinputRef.current.value
        if(changevaltypeRef.current === 'email'){
            if(inp_val.length === 0){
                ChangeSettingsSetSubmitAcive(false, 'Email field is empty')
                return
            }
            else{
                let contains_a = inp_val.indexOf('@')
                let contains_dot = inp_val.indexOf('.')
                if( (contains_a <= 0) || (contains_dot === -1) || (contains_a + 1 >= contains_dot) || (inp_val.length < 5) || (contains_dot = inp_val.length - 1)){
                    ChangeSettingsSetSubmitAcive(false, 'Enter a valid Email Address')
                    return
                }
                ChangeSettingsSetSubmitAcive(true)
                return
            }
        }
        else if(changevaltypeRef.current === 'phone'){
            if(inp_val.length === 0){
                ChangeSettingsSetSubmitAcive(false, 'Phone field is empty')
                return
            }
            else{
                if(inp_val.length <5 || inp_val.slice(1).search(reg_contains_only_num) === 0 || inp_val[0] !== '+'){
                    ChangeSettingsSetSubmitAcive(false, 'Enter a valid phone number')
                    return
                }
                ChangeSettingsSetSubmitAcive(true)
                return
            }
        }
        else if(changevaltypeRef.current === 'password'){
            if(inp_val.length === 0){
                ChangeSettingsSetSubmitAcive(false, 'New password field is empty')
                return
            }
            else if(inp_val.length < 8){
                ChangeSettingsSetSubmitAcive(false, 'New password is too short')
                return
            }
            else if(inp_val.length > 30){
                ChangeSettingsSetSubmitAcive(false, 'New password is too long')
                return
            }
            else if(!reg_contains_atleast1_num.test(inp_val)){
                ChangeSettingsSetSubmitAcive(false, 'New password must contain at least 1 number')
                return
            }
            else if(!reg_contains_atleast1_lowercase.test(inp_val)){
                ChangeSettingsSetSubmitAcive(false, 'New password must contain at least 1 lowercase')
                return
            }
            else if(!reg_contains_atleast1_uppercase.test(inp_val)){
                ChangeSettingsSetSubmitAcive(false, 'New password must contain at least 1 uppercase')
                return
            }
        }
    }

    function ChangeSettingsSetSubmitAcive(active = false, description = ''){
        if(active === false){
            changebuttonRef.current.classList.add('settingschange_inactive')
            changebuttonRef.current.classList.remove('settingschange_active')
            changesubmitactiveRef.current = [false, description]
        }
        else{
            changebuttonRef.current.classList.add('settingschange_active')
            changebuttonRef.current.classList.remove('settingschange_inactive')
            changesubmitactiveRef.current = [true, '']
        }
    }

    function SettingsChangePressSubmit(){
        if(changesubmitactiveRef.current[0] === false){
            changewarningsetState(changesubmitactiveRef.current[1])
        }
    }

    return(
        <div className='settings_allholder'>
            <NavBar/>
            <div className='settingschangeval' ref = {popupRef}>
                <div className='settingschange_header'>
                    {changeheaderstate}
                    <XCloseIcon className = 'settingschange_headerclose' onClick={() => PopUpOpenClose('close')}/>
                </div>
                <div className='settingschange_val'>
                    {changevalstate}
                    <div className='settingschange_valbox' ref={changeboxpasswordRef}>
                        <input placeholder='Enter Password' className='settingschange_valinput' ref={changepasswordRef} type={passwordeyestate[2]} onChange={() => ChangeValuesSubmitButton()} onFocus={() => changeboxpasswordRef.current.classList.add('settingschange_focus')} onBlur={() => changeboxpasswordRef.current.classList.remove('settingschange_focus')}/>
                        <div className='settingschange_valbox_extra settingschange_valbox_extra_visible' onClick={() => PasswordVisibility()}>
                            {passwordeyestate[0]}
                        </div>
                    </div>
                    <div className='settingschange_warning'>{changewarningstate}</div>
                </div>
                <div className='settingschange_submit'>
                    <div className='settingschange_button settingschange_inactive' ref={changebuttonRef} onClick={() => SettingsChangePressSubmit()}>
                        Submit
                    </div>
                </div>
            </div>
            <div className='settingsdarken' ref = {darkenRef} onClick={() => PopUpOpenClose('close')}/>
            <div className='settings_mainholder'>
                <div className='settingsbox'>
                    <div className='settingscontent_img'>
                        <div className='settings_imgholder'>
                            {iconstate}
                        </div>
                        <div className='settings_greetings' onClick={() => PopUpOpenClose('open', 'Change Name', 'Enter New Name', false, 'name')}>
                            {namestate}
                        </div>
                    </div>

                    <div className='settingscontent'>
                        <div className='settingscontent_info' onClick={() => PopUpOpenClose('open', 'Change Email', 'Enter New Email Address', false, 'email')}>
                            <span className='settingscontent_infoheader'>Email</span>
                            <div className='settingscontent_infomain'>
                                {emailstate}
                                <div className='settingscontent_infochange'><PencilIcon stroke-width={1}/></div>
                            </div>
                        </div>
                    
                        <div className='settingscontent_info' onClick={() => PopUpOpenClose('open', 'Change Phone', 'Enter New Phone Number', false, 'phone')}>
                            <span className='settingscontent_infoheader'>Phone</span>
                            <div className='settingscontent_infomain'>
                                {phonestate}
                                <div className='settingscontent_infochange'><PencilIcon stroke-width={1}/></div>
                            </div>
                        </div>

                        <div className='settingscontent_info' onClick={() => PopUpOpenClose('open', 'Change Password', 'Enter New Password', false, 'password')}>
                            <span className='settingscontent_infoheader'>Password</span>
                            <div className='settingscontent_infomain'>
                                <div className='settingscontent_infoval'>*****</div>
                                <div className='settingscontent_infochange'><PencilIcon stroke-width={1}/></div>
                            </div>
                        </div>
                    </div>

                    <div className='settings_line'/>

                    <div className='settingscontent'>
                        <div className='settingscontent_infomajor'>
                            DELETE ALL CHATS
                        </div>
                        <div className='settingscontent_infomajor'>
                            DELETE ACCOUNT
                        </div>
                        <div className='settingscontent_infomajor settingsmajor_blue'>
                            LOGOUT
                        </div>
                    </div>

                    {adminstate}

                </div>
            </div>
        </div>
    )

}