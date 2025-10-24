import '../styling/Settings.css'
import { useEffect, useState, useRef } from 'react'
import { UserIconThin, PencilIcon, XCloseIcon, EyeIcon, EyeCloseIcon, Tick } from '../components/svgs/UtilIcons'
import { useNavigate, Link } from 'react-router-dom'
import html2canvas from 'html2canvas'
import { SettingsBox } from './SettingsBox'
import { SettingsName } from './SettingsName'
import { SettingsPopUp } from './SettingsPopUp'

export function Settings({updatenavbarsetState}){
    
    const [simgState, simagesetState] = useState(<div className='s_img_dim s_loading'/>)
    const [snameholderState, snameholdersetState] = useState(<div className='s_loading_box s_loading'/>)

    const navigate = useNavigate()

    const skeletonRef = useRef()
    const loadedRef = useRef()

    const [semailState, semailsetState] = useState()
    const [sphoneState, sphonesetState] = useState()
    const [sadminState, sadminsetState] = useState()

    const [spopupState, spopupsetState] = useState({'visible': false, 'header': ''})

    useEffect(() => {
        GetUserInfo()
    }, [])

    async function GetUserInfo(){
        /*if(document.cookie.includes('userinfo=') === false){
            navigate('/login', {state: '/settings'})
        }

        let response_status = null
        let response = await fetch(import.meta.env.VITE_URL + '/loginregister/getuserinfo/', {
            method: 'GET',
            credentials: 'include',
        }).then(res => {
            response_status = res.status
            return res.json()
        }).then(data => data)*/
        //
        let response_status = 200
        let response = {"email": "test@test.test", "phone": null, "name": "Goku", "is_admin": true, "img": "237346999496364032"}
        //

        if(response_status === 200){
            SettingsBoxBuild(response)
        }
        else if(response_status === 401 || response_status === 403){
            navigate('/login', {state: '/settings'})
        }
    }

    function SettingsBoxBuild(response){
        simagesetState(<img className='s_img_dim s_loading' src={import.meta.env.VITE_IMG_PATH + response['img'] + '.JPEG'} onError={ImageNotFound}/>)
        snameholdersetState(<SettingsName value={response['name']}/>)
        semailsetState(response['email'])
        sphonesetState(response['phone'])
        sadminsetState(true)
        skeletonRef.current.style.display = 'none'
        loadedRef.current.style.display = 'flex'
    }

    function ImageNotFound(){
        simagesetState(<UserIconThin className='s_icon'/>)
    }

    return(
        <div className='s_allholder'>
            <SettingsPopUp popupState={spopupState} popupsetState={spopupsetState}/>
            <div className='s_mainholder'>
                <div className='s_box'>

                    <div className='s_img'>
                        <div className='s_imgholder'>
                            {simgState}
                        </div>
                        {snameholderState}
                    </div>

                    <div className='s_content' ref={skeletonRef}>
                        <div className='s_loading_box s_loading'/>
                        <div className='s_loading_box s_loading' style={{width: '75%'}}/>
                    </div>
                    <div className='s_content' style={{display: 'none'}} ref={loadedRef}>
                        <SettingsBox header='Email' value={semailState} valueempy='no email address provided' popupsetState={spopupsetState} popupvalue={{'visible': true, 'header': 'Change Email', 'classclose': 'sp_closeblue', 'inputtype': 'email', 'classbutton': 'sp_bgblue', 'placeholderfirst': 'Enter New Email Address', 'placeholdersecond': 'Enter Password'}}/>
                        <SettingsBox header='Phone' value={sphoneState} valueempty='no phone number provided' popupsetState={spopupsetState} popupvalue={{'visible': true, 'header': 'Change Phone', 'classclose': 'sp_closeblue', 'inputtype': 'phone', 'classbutton': 'sp_bgblue', 'placeholderfirst': 'Enter New Phone Number', 'placeholdersecond': 'Enter Password'}}/>
                        <SettingsBox header='Password' value='*****' popupsetState={spopupsetState} popupvalue={{'visible': true, 'header': 'Change Password', 'classclose': 'sp_closeblue', 'inputtype': 'password', 'classbutton': 'sp_bgblue', 'placeholderfirst': 'Enter New Password', 'placeholdersecond': 'Enter Password'}}/>
                        
                        <div className='s_line'/>

                        <div className='s_content'>
                            <div className='s_util'>DELETE ALL CHATS</div>
                            {sadminState === true ? (<div className='s_util'>DELETE ACCOUNT</div>) : (<div className='s_util'>DELETE ACCOUNT</div>)}
                            <div className='s_util s_blue'>LOGOUT</div>
                            {sadminState === true ? (<Link to='/referalcodes'><div className='s_referal'>REFERAL CODES</div></Link>): ('')}
                        </div>
                    </div>

                </div>
            </div>
        </div>
    )
}