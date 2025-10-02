import '../styling/Settings.css'
import { NavBar } from './NavBar'
import { useEffect, useState, useRef } from 'react'
import { UserIconThin, PencilIcon, XCloseIcon, EyeIcon, EyeCloseIcon, Tick } from '../components/svgs/UtilIcons'
import { useNavigate, Link } from 'react-router-dom'
import html2canvas from 'html2canvas'

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
    const [newpasswordclassstate, newpasswordclasssetState] = useState('settingschange_valbox_extra settingschange_valbox_extra_passwordadd')
    const [changeinputplaceholderstate, changeinputplaceholdersetState] = useState('')
    const changeimgholderRef = useRef()
    const [changeimgstate, changeimgsetState] = useState(null)
    const changeimgvalRef = useRef()
    const [changeimguploadstate, changeimguploadsetState] = useState('UPLAOD IMAGE')
    const changeimgpicRef = useRef()
    const changeimgpressRef = useRef()
    const changeimgdarkRef = useRef()
    const changeimgpopupRef = useRef()
    const [imgpreviewstate, imgpreviewsetState] = useState()
    const imgmoveposRef = useRef()
    const imgcanmoveRef = useRef()
    const imgpreviewRef = useRef()
    const screenshotRef = useRef()
    const changeimgprevvalRef = useRef([null, false])
    const [popupbuttonstate, popupbuttonsetState] = useState('Submit')
    const [popuppasswordstate, popuppasswordsetState] = useState('Enter Password')
    const deleteinfoRef = useRef(false)
    const settingsxcloseRef = useRef()
    const [settingsnotificationstate, settingsnotificationsetState] = useState('Successfully Deleted')
    const settingsnotificationRef = useRef()

    const reg_contains_only_num = new RegExp('^[0-9]+$')
    const reg_contains_atleast1_num = new RegExp(['[0-9]'])
    const reg_contains_atleast1_lowercase = new RegExp(['[a-z]'])
    const reg_contains_atleast1_uppercase = new RegExp(['[A-Z]'])
    
    useEffect(() => {
        GetUserInfo()
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

            if(response['img'] === false){
                iconsetState(<UserIconThin className='settingsicon' onClick={() => PopUpOpenClose('open', 'Change Image', '', 'image')}/>)
                changeimguploadsetState('UPLOAD IMAGE')
                changeimgvalRef.current.classList.add('settingschange_img_inactive')
                changeimgpicRef.current.classList.add('settingschange_img_inactive')
            }
            else{
                let img_path = import.meta.env.VITE_IMG_PATH + response['img'] + '.JPEG'
                iconsetState(<img src={img_path} className='settingsicon' onClick={() => PopUpOpenClose('open', 'Change Image', '', 'image')}/>)
                changeimguploadsetState('CHANGE IMAGE')
                changeimgsetState(img_path)
                changeimgpicRef.current.classList.add('settingschange_img_active')
                changeimgvalRef.current.classList.add('settingschange_img_active')
            }

            if(response['name'] === null){
                namesetState('Welcome, Back!')
            }
            else{
                namesetState('Welcome, ' + response['name'])
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
                adminsetState(<Link to='/referalcodes'><div className='settingscontent_referal'>REFERAL CODES</div></Link>)
            }
            
        }
        else if(response_status === 401 || response_status === 403){
            navigate('/login')
        }
    }

    function PopUpOpenClose(action='open', header = '', text = '', changetype = '', deleteinfo = false, keepimgval = false){
        if(action === 'open'){
            deleteinfoRef.current = deleteinfo
            popupRef.current.style.pointerEvents = 'all'
            popupRef.current.style.opacity = '1'
            popupRef.current.style.transform = 'scale(1)'
            popupRef.current.style.zIndex = 3
            darkenRef.current.style.opacity = '1'
            darkenRef.current.style.pointerEvents = 'all'

            changevaltypeRef.current = changetype
            
            if(deleteinfoRef.current === false){
                changeheadersetState(<div>{header}</div>)
                settingsxcloseRef.current.classList.remove('settingsclose_red')
                settingsxcloseRef.current.classList.add('settingsclose_blue')
            }
            else{
                changeheadersetState(<div className='settingsheader_red'>{header}</div>)
                settingsxcloseRef.current.classList.remove('settingsclose_blue')
                settingsxcloseRef.current.classList.add('settingsclose_red')
            }
            
            if(deleteinfo === false){
                popuppasswordsetState('Enter Password')
                popupbuttonsetState('Submit')
                changebuttonRef.current.classList.remove('settingschange_red')
                changebuttonRef.current.classList.add('settingschange_blue')
            }
            else{
                popuppasswordsetState('Confirm Password')
                popupbuttonsetState('Delete')
                changebuttonRef.current.classList.remove('settingschange_blue')
                changebuttonRef.current.classList.add('settingschange_red')
            }

            if(changetype === 'password'){
                newpasswordclasssetState('settingschange_valbox_extra settingschange_valbox_extra_passwordadd')
                newpasswordeyesetState([<EyeIcon/>, true, 'password'])
            }
            else{
                newpasswordclasssetState('settingschange_valbox_extra settingschange_valbox_extra_passwordremove')
                newpasswordeyesetState([<EyeCloseIcon/>, false, 'text'])
            }

            if(changetype !== 'image'){
                changeinputplaceholdersetState(text)
                {/*AHA*/}
                changeboxRef.current.classList.remove('settingschange_valbox_remove')
                changeboxRef.current.classList.add('settingschange_valbox_add')
                changeimgholderRef.current.classList.remove('settingschange_img_active')
            }
            else{
                changeboxRef.current.classList.remove('settingschange_valbox_add')
                changeboxRef.current.classList.add('settingschange_valbox_remove')
                changeimgholderRef.current.classList.add('settingschange_img_active')
            }

        }
        else if(action === 'close'){
            popupRef.current.style.pointerEvents = 'none'
            popupRef.current.style.opacity = '0'
            popupRef.current.style.transform = 'scale(0.8)'
            popupRef.current.style.zIndex = -1
            darkenRef.current.style.opacity = '0'
            darkenRef.current.style.pointerEvents = 'none'
            changewarningsetState('')
            changeinputRef.current.value = ''
            changepasswordRef.current.value = ''
            SettingsInputChange()
            changesubmitactiveRef.current = [false, 'Fields are empty']
            newpasswordeyesetState([<EyeIcon/>, true, 'password'])
            if(keepimgval === false){
                if(changeimgprevvalRef.current[1] === true){
                    changeimgsetState(changeimgprevvalRef.current[0])
                    if(changeimgprevvalRef.current[0] === null){
                        ChangeImgVisible(false)
                        changeimgpressRef.current.value = ''
                        changeimguploadsetState('UPLOAD IMAGE')
                        changeimgprevvalRef.current[0] = null
                    }
                    changeimgprevvalRef.current[1] = false
                }
            }
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

        let inp_val = changeinputRef.current.value
        if(changevaltypeRef.current === 'email'){
            if(inp_val.length !== 0){
                let contains_a = inp_val.indexOf('@')
                let contains_dot = inp_val.indexOf('.')
                if( (contains_a <= 0) || (contains_dot === -1) || (contains_a + 1 >= contains_dot) || (inp_val.length < 5) || (contains_dot === inp_val.length - 1)){
                    ChangeSettingsSetSubmitAcive(false, 'Enter a valid Email Address')
                    return
                }
            }
        }
        else if(changevaltypeRef.current === 'phone'){
            if(inp_val.length !== 0){
                if(inp_val.length <5 || !reg_contains_only_num.test(inp_val.slice(1)) || inp_val[0] !== '+'){
                    ChangeSettingsSetSubmitAcive(false, 'Enter a valid phone number')
                    return
                }
            }
        }
        else if(changevaltypeRef.current === 'password'){
            let passwordtext = 'New Password'
            if(deleteinfoRef.current !== false){
                passwordtext = 'Password'
            }
            if(inp_val.length === 0){
                ChangeSettingsSetSubmitAcive(false, passwordtext + ' field is empty')
                return
            }
            else if(inp_val.length < 8){
                ChangeSettingsSetSubmitAcive(false, passwordtext + ' is too short')
                return
            }
            else if(inp_val.length > 30){
                ChangeSettingsSetSubmitAcive(false, passwordtext + ' is too long')
                return
            }
            else if(!reg_contains_atleast1_num.test(inp_val)){
                ChangeSettingsSetSubmitAcive(false, passwordtext + ' must contain at least 1 number')
                return
            }
            else if(!reg_contains_atleast1_lowercase.test(inp_val)){
                ChangeSettingsSetSubmitAcive(false, passwordtext + ' must contain at least 1 lowercase')
                return
            }
            else if(!reg_contains_atleast1_uppercase.test(inp_val)){
                ChangeSettingsSetSubmitAcive(false, passwordtext + ' must contain at least 1 uppercase')
                return
            }
            
            if(deleteinfoRef.current !== false){
                if(inp_val !== passwordval){
                    ChangeSettingsSetSubmitAcive(false, 'Confirm Password must match Password')
                    return
                }
            }
        }
        else if(changevaltypeRef.current === 'image'){
            if(changeimgprevvalRef.current[1] === false){
                ChangeSettingsSetSubmitAcive(false, 'You did not change your image')
                return
            }
        }
        else if(changevaltypeRef.current === 'name'){
            if(inp_val.length > 7){
                ChangeSettingsSetSubmitAcive(false, 'Name is too big')
                return
            }
        }

        if(deleteinfoRef.current === false){
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
        }

        ChangeSettingsSetSubmitAcive(true)
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

    function SettingsChangePressButton(){
        if(changesubmitactiveRef.current[0] === false){
            changewarningsetState(changesubmitactiveRef.current[1])
        }
        else{
            if(deleteinfoRef.current === false){
                if(changevaltypeRef.current === 'image'){
                    SettingsUpdateImg()
                }
                else{
                    SettingsUpdateValue()
                }
            }
            else if(deleteinfoRef.current === 'chats'){
                DeleteAllChats()
            }
            else if(deleteinfoRef.current === 'account'){
                console.log('del account')
            }
        }
    }

    async function SettingsUpdateValue(){
        let response_status = null
        let request = {"k": changevaltypeRef.current, "v": changeinputRef.current.value, "p": changepasswordRef.current.value}
        let response = await fetch('http://127.0.0.1:8000/loginregister/updatevalue/', {
            method: 'POST',
            body: JSON.stringify(request),
            credentials: 'include',
        }).then(res => { response_status = res.status
            return res.json()}).then(data => data)
        if(response_status === 403 || response_status === 401){
            navigate('/login')
            return
        }
        else if(response_status === 409){
            changewarningsetState(response)
        }
        else if(response_status === 200){
            if(changevaltypeRef.current === 'email'){
                if(changeinputRef.current.value === ''){
                    emailsetState(<div className='settingscontent_infoval vallight'>no email provided</div>)
                }
                else{
                    emailsetState(<div className='settingscontent_infoval'>{changeinputRef.current.value}</div>)
                }
            }
            else if(changevaltypeRef.current === 'phone'){
                if(changeinputRef.current.value === ''){
                    phonesetState(<div className='settingscontent_infoval vallight'>no phone number provided</div>)
                }
                else{
                    phonesetState(<div className='settingscontent_infoval'>{changeinputRef.current.value}</div>)
                }
            }
            else if(changevaltypeRef.current === 'name'){
                if(changeinputRef.current.value === ''){
                    namesetState('Welcome, Back!')
                }
                else{
                    namesetState('Welcome, ' + changeinputRef.current.value)
                }
            }
            else if(changevaltypeRef.current === 'password'){
                settingsnotificationsetState('Password Updated!')
                settingsnotificationRef.current.style.bottom = '35px'
            }
            PopUpOpenClose('close')
        }
    }

    async function SettingsUpdateImg(){
        let response_status = null
        let request = {"p": changepasswordRef.current.value}
        let formdata = new FormData()
        formdata.append("data", JSON.stringify(request))
        formdata.append("img", changeimgstate)
        let response = await fetch('http://127.0.0.1:8000/loginregister/updateimage/', {
            method: 'POST',
            credentials: 'include',
            body: formdata,
        }).then(res => {
            response_status = res.status
            return res.json()
        }).then(data => data)

        if(response_status === 403 || response_status === 401){
            navigate('/login')
            return
        }
        else if(response_status === 415){
            changewarningsetState('Image msut be of type JPEG, JPG, PNG or AVIF')
            return
        }
        else if(response_status === 413){
            changewarningsetState(response)
        }
        else if(response_status === 200){
            if(response === 'Image successfully deleted'){
                changeimguploadsetState('UPLOAD IMAGE')
                ChangeImgVisible()
                PopUpOpenClose('close')
                iconsetState(<UserIconThin className='settingsicon' onClick={() => PopUpOpenClose('open', 'Change Image', '', 'image')}/>)
                return
            }
            iconsetState(<img src={imgpreviewstate} className='settingsicon' onClick={() => PopUpOpenClose('open', 'Change Image', '', 'image')}/>)
            changeimguploadsetState('CHANGE IMAGE')
            ChangeImgVisible(true)
            PopUpOpenClose('close', '', '', '', false, true)
        }

    }

    async function DeleteAllChats(){
        let response_status = null
        let request = {"p": changeinputRef.current.value, "vp": changepasswordRef.current.value}
        let response = await fetch('http://127.0.0.1:8000/chats/deleteallchats/', {
            method: 'DELETE',
            credentials: 'include',
            body: JSON.stringify(request),
        }).then(res => {
            response_status = res.status
            return res.json()
        }).then(data => data)

        if(response_status === 403 || response_status === 401){
            navigate('/login')
            return
        }
        else if(response_status === 200){
            settingsnotificationsetState('All Chats Successfully Deleted! (' + response + ')')
            settingsnotificationRef.current.style.bottom = '35px'
            PopUpOpenClose('close')
        }
    }

    function ClickSelectImg(){
        changeimgpressRef.current.click()
    }

    function ImgSelectChange(){
        changeimgdarkRef.current.style.display = 'block'
        changeimgpopupRef.current.style.display = 'block'
        changeimgdarkRef.current.style.pointerEvents = 'all'
        changeimgpopupRef.current.style.pointerEvents = 'all'
        let imgreader = new FileReader();
        imgreader.readAsDataURL(changeimgpressRef.current.files[0])
        imgreader.onloadend = () => {
            imgpreviewsetState(imgreader.result)
        }
    }

    function ImgConfirmClose(remove = false){
        changeimgdarkRef.current.style.display = 'none'
        changeimgpopupRef.current.style.display = 'none'
        changeimgdarkRef.current.style.pointerEvents = 'none'
        changeimgpopupRef.current.style.pointerEvents = 'none'
        if(remove === true){
            changeimgpressRef.current.value = ''
        }
    }

    function handleImgMouseDown(e){
        imgcanmoveRef.current = true
        imgmoveposRef.current = e.sclientX
    }
    function handleImgMouseUp(){
        imgcanmoveRef.current = false
    }
    function handleImgMouseMove(e){
        if(imgcanmoveRef.current === true){
            let pos = imgmoveposRef.current - e.clientX
            imgmoveposRef.current = e.clientX
            imgpreviewRef.current.style.left = (imgpreviewRef.current.offsetLeft - pos) + 'px'
        }
    }
    
    function SaveScreenshot(){
        html2canvas(screenshotRef.current, {scale: 2}).then((canvas) => {
            let img = canvas.toDataURL('image/jpeg')
            if(changeimgprevvalRef.current[1] === false){
                changeimgprevvalRef.current = [changeimgstate, true]
            }
            changeimgsetState(img)
            NewImgSubmit()
        })
    }

    function NewImgSubmit(){
        ChangeImgVisible(true)
        ImgConfirmClose()
        changeimguploadsetState('CHANGE IMAGE')
        ChangeValuesSubmitButton()
    }

    function ChangeImgVisible(visible = false){
        if(visible === false){
            changeimgvalRef.current.classList.remove('settingschange_img_active')
            changeimgpicRef.current.classList.remove('settingschange_img_active')
            changeimgvalRef.current.classList.add('settingschange_img_inactive')
            changeimgpicRef.current.classList.add('settingschange_img_inactive')
        }
        else{
            changeimgvalRef.current.classList.remove('settingschange_img_inactive')
            changeimgpicRef.current.classList.remove('settingschange_img_inactive')
            changeimgvalRef.current.classList.add('settingschange_img_active')
            changeimgpicRef.current.classList.add('settingschange_img_active')
        }
    }

    function DeleteImg(){
        if(changeimgprevvalRef.current[1] === false){
            changeimgprevvalRef.current = [changeimgstate, true]
        }
        ChangeImgVisible()
        changeimguploadsetState('UPLOAD IMAGE')
        changeimgpressRef.current.value = ''
        ChangeValuesSubmitButton()
    }

    async function Logout(){
        let response_status = null
        let response = await fetch('http://127.0.0.1:8000/loginregister/logout/', {
            method: 'DELETE',
            credentials: 'include',
        }).then(res => {
            response_status = res.status
            return res.json()
        }).then(data => data)

        if(response_status === 200){
            navigate('/')
            window.location.reload()
        }

    }

    function CloseNotification(){
        settingsnotificationRef.current.classList.add('settingsnotification_close')
        setTimeout(NotificationInitBottom, 700)
        setTimeout(NotificationInitPosition, 1500)
    }

    function NotificationInitBottom(){
        settingsnotificationRef.current.style.bottom = '-35px'
    }

    function NotificationInitPosition(){
        settingsnotificationRef.current.classList.remove('settingsnotification_close')
    }

    return(
        <div className='settings_allholder'>
            <NavBar/>
            <div className='settingschange_img_confirm' ref={changeimgpopupRef}>
                <div className='settingschange_img_confirmbox'>
                    <div className='settingschange_img_confirmcircle'>
                        <div className='settingschange_img_screenshot' ref={screenshotRef}>
                            <div className='settingschange_img_preview' onMouseDown={(e) => handleImgMouseDown(e)} onMouseUp={() => handleImgMouseUp()} onMouseMove={(e) => handleImgMouseMove(e)} ref={imgpreviewRef}>
                                <img src={imgpreviewstate} className='settingschange_img_upload'/>
                                <div className='settingschange_img_blackbg'/>
                            </div>
                        </div>
                    </div>
                </div>
                <div className='settingschange_img_confirmbuttons'>
                    <div className='settingschange_img_confirmbuttonval settingschange_img_confirmcancel' onClick={() => ImgConfirmClose(true)}><XCloseIcon/></div>
                    <div className='settingschange_img_confirmbuttonval settingschange_img_confirmaccept' onClick={() => SaveScreenshot()}><Tick width={24} height={24}/></div>
                </div>
            </div>
            <div className='settingschange_img_darkenall' ref={changeimgdarkRef} onClick={() => ImgConfirmClose(true)}/>
            <div className='settingschangeval' ref = {popupRef}>
                <div className='settingschange_header'>
                    {changeheaderstate}
                    <XCloseIcon className = 'settingschange_headerclose' onClick={() => PopUpOpenClose('close')} ref={settingsxcloseRef}/>
                </div>
                <div className='settingschange_val'>
                    <div className='settingschange_img' ref={changeimgholderRef}>
                        <div className='settingschange_img_imgholder' ref={changeimgpicRef}>
                            <img src={changeimgstate} className='settingschange_img_pic'/>
                        </div>
                        <div className='settingschange_img_val'>
                            <div className='settingschange_img_val_box settingschange_blue' onClick={() => ClickSelectImg()}>
                                {changeimguploadstate}
                            </div>
                            <input type='file' className='settingschange_img_inpimg' ref={changeimgpressRef} accept='image/*' onChange={() => ImgSelectChange()}/>
                            <div className='settingschange_img_val_box settingschange_red' ref={changeimgvalRef} onClick={() => DeleteImg()}>
                                DLEETE IMAGE
                            </div>
                        </div>
                    </div>
                    <div className='settingschange_valbox' ref={changeboxRef}>
                        <input placeholder={changeinputplaceholderstate} className='settingschange_valinput' onFocus={() => changeboxRef.current.classList.add('settingschange_focus')} onBlur={() => changeboxRef.current.classList.remove('settingschange_focus')} ref={changeinputRef} type={newpasswordeyestate[2]} onChange={() => {SettingsInputChange()
                            ChangeValuesSubmitButton()
                        }}/>
                        <div className='settingschange_valbox_extra' ref={changeinputsvgRef} onClick={() => {changeinputRef.current.value = ''
                            SettingsInputChange()
                            ChangeValuesSubmitButton()
                        }}>
                            <XCloseIcon/>
                        </div>
                        <div className={newpasswordclassstate} onClick={() => NewPasswordVisibility()}>
                            {newpasswordeyestate[0]}
                        </div>
                    {/*AHA */}
                    </div>
                    <div className='settingschange_valbox' ref={changeboxpasswordRef}>
                        <input placeholder={popuppasswordstate} className='settingschange_valinput' ref={changepasswordRef} type={passwordeyestate[2]} onChange={() => ChangeValuesSubmitButton()} onFocus={() => changeboxpasswordRef.current.classList.add('settingschange_focus')} onBlur={() => changeboxpasswordRef.current.classList.remove('settingschange_focus')}/>
                        <div className='settingschange_valbox_extra settingschange_valbox_extra_visible' onClick={() => PasswordVisibility()}>
                            {passwordeyestate[0]}
                        </div>
                    </div>
                    <div className='settingschange_warning'>{changewarningstate}</div>
                </div>
                <div className='settingschange_submit'>
                    <div className='settingschange_button settingschange_inactive settingschange_blue' ref={changebuttonRef} onClick={() => SettingsChangePressButton()}>
                        {popupbuttonstate}
                    </div>
                </div>
            </div>
            <div className='settingsdarken' ref = {darkenRef} onClick={() => PopUpOpenClose('close')}/>
            {/*<div className='settingsnotification'>
                <div>{settingsnotificationstate}</div>
                <div><Tick height={24} width={24} className='settingsnotification_tick'/></div>
            </div>*/}
            <div className='settings_mainholder'>
                <div className='settingsbox'>
                    <div className='settingscontent_img'>
                        <div className='settings_imgholder'>
                            {iconstate}
                        </div>
                        <div className='settings_greetings' onClick={() => PopUpOpenClose('open', 'Change Name', 'Enter New Name', 'name')}>
                            {namestate}
                        </div>
                    </div>

                    <div className='settingscontent'>
                        <div className='settingscontent_info' onClick={() => PopUpOpenClose('open', 'Change Email', 'Enter New Email Address', 'email')}>
                            <span className='settingscontent_infoheader'>Email</span>
                            <div className='settingscontent_infomain'>
                                {emailstate}
                                <div className='settingscontent_infochange'><PencilIcon stroke-width={1}/></div>
                            </div>
                        </div>
                    
                        <div className='settingscontent_info' onClick={() => PopUpOpenClose('open', 'Change Phone', 'Enter New Phone Number', 'phone')}>
                            <span className='settingscontent_infoheader'>Phone</span>
                            <div className='settingscontent_infomain'>
                                {phonestate}
                                <div className='settingscontent_infochange'><PencilIcon stroke-width={1}/></div>
                            </div>
                        </div>

                        <div className='settingscontent_info' onClick={() => PopUpOpenClose('open', 'Change Password', 'Enter New Password', 'password')}>
                            <span className='settingscontent_infoheader'>Password</span>
                            <div className='settingscontent_infomain'>
                                <div className='settingscontent_infoval'>*****</div>
                                <div className='settingscontent_infochange'><PencilIcon stroke-width={1}/></div>
                            </div>
                        </div>
                    </div>

                    <div className='settings_line'/>

                    <div className='settingscontent'>
                        <div className='settingscontent_infomajor' onClick={() => PopUpOpenClose('open', 'DELETE ALL CHATS', 'Enter Password', 'password', 'chats')}>
                            DELETE ALL CHATS
                        </div>
                        <div className='settingscontent_infomajor' onClick={() => PopUpOpenClose('open', 'PERMANENTLY DELETE ACCOUNT', 'Enter Password', 'password', 'account')}>
                            DELETE ACCOUNT
                        </div>
                        <div className='settingscontent_infomajor settingsmajor_blue' onClick={() => Logout()}>
                            LOGOUT
                        </div>
                    </div>

                    {adminstate}

                </div>
                <div className='settingsnotification' ref={settingsnotificationRef}>
                    <div><Tick className='settingsnotification_tick'/></div>
                    <div>{settingsnotificationstate}</div>
                    <div><XCloseIcon className='settingsnotification_x' onClick={() => CloseNotification()}/></div>
                </div>
            </div>
        </div>
    )

}