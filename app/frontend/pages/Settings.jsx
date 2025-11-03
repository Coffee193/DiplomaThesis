import '../styling/Settings.css'
import { useEffect, useState, useRef } from 'react'
import { UserIconThin } from '../components/svgs/UtilIcons'
import { useNavigate, Link } from 'react-router-dom'
import { SettingsBox } from './SettingsBox'
import { SettingsName } from './SettingsName'
import { SettingsPopUp } from './SettingsPopUp'

export function Settings({updatenavbarsetState}){
    
    const [simgState, simagesetState] = useState(<div className='s_img_dim loading'/>)

    const navigate = useNavigate()

    const skeletonRef = useRef()
    const loadedRef = useRef()

    const nameskeletonRef = useRef()
    const nameloadedRef = useRef()

    const [semailState, semailsetState] = useState()
    const [sphoneState, sphonesetState] = useState()
    const [sadminState, sadminsetState] = useState()
    const [snameState, snamesetState] = useState()

    const [spopupState, spopupsetState] = useState({'visible': false, 'header': ''})
    const [snotificationState, snotificationsetState] = useState({'text': '', 'svg': null, 'visible': false, 'class': null})

    const valuesRef = useRef([null, null, null, ['Field is empty', 'Password field is empty', 'Passwords do not match']]) // value, type (e -> email, p -> phone, n -> name, i -> img), password, warning [1: valuewarning, 2:passwordwarning, 3:passwordconfirmwarning]

    useEffect(() => {
        GetUserInfo()
    }, [])

    async function GetUserInfo(){
        if(document.cookie.includes('userinfo=') === false){
            navigate('/login', {state: '/settings'})
        }

        let response_status = null
        let response = await fetch(import.meta.env.VITE_URL + '/loginregister/getuserinfo/', {
            method: 'GET',
            credentials: 'include',
        }).then(res => {
            response_status = res.status
            return res.json()
        }).then(data => data)

        //response_status = 200
        //let response = {"name": null, "img": null, "email": "t@t.t", "phone": null, "isadmin": true}

        if(response_status === 200){
            SettingsBoxBuild(response)
        }
        else if(response_status === 401 || response_status === 403){
            navigate('/login', {state: '/settings'})
        }
    }

    function SettingsBoxBuild(response){
        CreateImage(response['img'])
        snamesetState(response['name'])
        semailsetState(response['email'])
        sphonesetState(response['phone'])
        sadminsetState(response['is_admin'])
        skeletonRef.current.style.display = 'none'
        loadedRef.current.style.display = 'flex'
        nameskeletonRef.current.style.display = 'none'
        nameloadedRef.current.style.display = 'block'
    }

    function ImageNotFound(){
        simagesetState(<UserIconThin className='s_icon' onClick={() => {spopupsetState({'visible': true, 'header': 'Change Image', 'classclose': 'sp_closeblue', 'inputtype': 'image', 'classbutton': 'sp_bgblue', 'placeholdersecond': 'Enter Password', 'textbutton': 'Submit', 'setState': CreateImage}); valuesRef.current[3][0] = 'Image was not changed'; valuesRef.current[1] = 'image'}}/>)
    }

    async function CreateImage(soft_src = null, hard_src = null){
        let img_src = null
        if(hard_src === null){
            if(soft_src != null){
                let imgdata = await fetch(import.meta.env.VITE_IMG_PATH + soft_src + '.JPEG')
                .then(response => response.arrayBuffer())
                img_src ='data:image/jpeg;base64,' + btoa(String.fromCharCode(...new Uint8Array(imgdata)));
            }
            else{
                img_src = 'a'
            }
        }
        else{
            img_src = hard_src
        }

        simagesetState(<img className='s_icon' src={img_src} onError={ImageNotFound} onClick={() => {spopupsetState({'visible': true, 'header': 'Change Image', 'classclose': 'sp_closeblue', 'inputtype': 'image', 'classbutton': 'sp_bgblue', 'placeholdersecond': 'Enter Password', 'textbutton': 'Submit', 'imageval': img_src, 'setState': CreateImage}); valuesRef.current[3][0] = 'Image was not changed'; valuesRef.current[1] = 'image'}}/>)
    }

    async function Logout(){
        let response_status = null
        await fetch(import.meta.env.VITE_URL + '/loginregister/logout/', {
            method:'DELETE',
            credentials: 'include',
        }).then(res => {
            response_status = res.status
            return res.json()}).then(data => data)
            
        if(response_status === 200){
            navigate('/')
            window.location.reload()
        }
        else{
            navigate('/login', {state: 'expired'})
        }
    }

    return(
        <div className='s_allholder'>
            <SettingsPopUp popupState={spopupState} popupsetState={spopupsetState} valuesRef={valuesRef} notificationsetState={snotificationsetState} updatenavbarsetState={updatenavbarsetState}/>
            <div className='s_mainholder'>
                <div className='s_box'>

                    <div className='s_img'>
                        <div className='s_imgholder'>
                            {simgState}
                        </div>
                        <div className='loading_box loading' ref={nameskeletonRef}/>
                        <div ref={nameloadedRef} style={{display: 'none'}}>
                            <SettingsName value={snameState} popupsetState={spopupsetState} popupvalue={{'visible': true, 'header': 'Change Name', 'classclose': 'sp_closeblue', 'inputtype': 'name', 'classbutton': 'sp_bgblue', 'placeholderfirst': 'Enter New Name', 'placeholdersecond': 'Enter Password', 'textbutton': 'Submit', 'setState': snamesetState, 'allowEmpty': true}} valuesRef={valuesRef} typeIndex={1} warningIndex={3} warningvalueIndex={0}/>
                        </div>
                    </div>

                    <div className='s_content' ref={skeletonRef}>
                        <div className='loading_box loading'/>
                        <div className='loading_box loading' style={{width: '75%'}}/>
                    </div>
                    <div className='s_content' style={{display: 'none'}} ref={loadedRef}>
                        <SettingsBox header='Email' value={semailState} valueempty='no email address provided' popupsetState={spopupsetState} popupvalue={{'visible': true, 'header': 'Change Email', 'classclose': 'sp_closeblue', 'inputtype': 'email', 'classbutton': 'sp_bgblue', 'placeholderfirst': 'Enter New Email Address', 'placeholdersecond': 'Enter Password', 'textbutton': 'Submit', 'setState': semailsetState, 'allowEmpty': true}} valuesRef={valuesRef} typeIndex={1} warningIndex={3} warningvalueIndex={0}/>
                        <SettingsBox header='Phone' value={sphoneState} valueempty='no phone number provided' popupsetState={spopupsetState} popupvalue={{'visible': true, 'header': 'Change Phone', 'classclose': 'sp_closeblue', 'inputtype': 'phone', 'classbutton': 'sp_bgblue', 'placeholderfirst': 'Enter New Phone Number', 'placeholdersecond': 'Enter Password', 'textbutton': 'Submit', 'setState': sphonesetState, 'allowEmpty': true}} valuesRef={valuesRef} typeIndex={1} warningIndex={3} warningvalueIndex={0}/>
                        <SettingsBox header='Password' value='*****' popupsetState={spopupsetState} popupvalue={{'visible': true, 'header': 'Change Password', 'classclose': 'sp_closeblue', 'inputtype': 'password', 'classbutton': 'sp_bgblue', 'placeholderfirst': 'Enter New Password', 'placeholdersecond': 'Enter Password', 'textbutton': 'Submit'}} valuesRef={valuesRef} typeIndex={1}/>
                        
                        <div className='s_line' onClick={() => console.log(valuesRef.current)}/>

                        <div className='s_content'>
                            <div className='s_util' onClick={() => {spopupsetState({'visible': true, 'header': 'DELETE ALL CHATS', 'classclose': 'sp_closered', 'inputtype': 'password', 'classbutton': 'sp_bgred', 'placeholderfirst': 'Enter Password', 'placeholdersecond': 'Confirm Password', 'textbutton': 'Delete', 'headerred': true, 'extrainfo': 'deletechats'}); valuesRef.current[1] = 'password'}}>DELETE ALL CHATS</div>
                            <div className='s_util' onClick={() => {spopupsetState({'visible': true, 'header': 'DELETE ACCOUNT', 'classclose': 'sp_closered', 'inputtype': 'password', 'classbutton': 'sp_bgred', 'placeholderfirst': 'Enter Password', 'placeholdersecond': 'Confirm Password', 'textbutton': 'Delete', 'headerred': true, 'isadmin': sadminState, 'extrainfo': 'deleteaccount'}); valuesRef.current[1] = 'password'}}>DELETE ACCOUNT</div>
                            <div className='s_util s_blue' onClick={() => Logout()}>LOGOUT</div>
                            {sadminState === true ? (<Link to='/referalcodes' tabIndex="-1"><div className='s_referal'>REFERAL CODES</div></Link>): ('')}
                        </div>
                    </div>

                </div>
            </div>
            <div className='s_notificationholder' style={snotificationState['visible'] === true ? ({opacity: '1', transform: 'scale(1)', pointerEvents: 'all'}) : ({opacity: '0', transform: 'scale(0.8)', pointerEvents: 'none'})}>
                <div className='s_notification'>
                    <div>{snotificationState['text']}</div>
                    <div className={'s_notificationsvg ' + snotificationState['class']} onClick={() => snotificationsetState(prevState => ({...prevState, 'visible': false}))}>{snotificationState['svg']}</div>
                </div>
            </div>
        </div>
    )
}