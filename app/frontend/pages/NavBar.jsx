import '../styling/NavBar.css'
import { Link, useNavigate, Outlet } from 'react-router-dom'
import { useEffect, useRef, useState } from 'react'
import { SideBar, UserIcon, Logout, Settings, DiagonalArrow } from '../components/svgs/UtilIcons'

export function NavBar({updatenavbarstate}){

    
    const navigate = useNavigate()
    const loginRef = useRef()
    const userinfovals = GetUserInfoValues()
    const [namestate, namesetState] = useState(userinfovals[0] === 'None' ? ('Info') : ('Hello, ' + userinfovals[0]))
    const [imgstate, imgsetState] = useState(userinfovals[1] !== '' ? (<div className='nav_user nav_imgexist'><img className='nav_img' src={import.meta.env.VITE_IMG_PATH + userinfovals[1] + '.JPEG'} onError={InitImgNotFound}/></div>) : (<UserIcon width={30} height={30} className='nav_user'/>))

    async function ClickLogout(){
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


    function GetImg(){
        let cookievar = document.cookie.split('; ')
        for(let i = 0; i < cookievar.length; i++){
            if(cookievar[i].slice(0, 9) === 'userinfo='){
                cookievar = cookievar[i].slice(9)
                break
            }
        }
        return <div className='nav_user nav_imgexist'><img className='nav_img' src={import.meta.env.VITE_IMG_PATH + cookievar + '.JPEG'} onError={InitImgNotFound}/></div>
    }

    function InitImgNotFound(){
        imgsetState(<UserIcon width={30} height={30} className='nav_user'/>)
    }

    function GetUserInfoValues(){
        let cookievar = document.cookie.split('; ')
        for(let i = 0; i < cookievar.length; i++){
            if(cookievar[i].slice(0, 9) === 'userinfo='){
                return cookievar[i].slice(9).split('$')
            }
        }
        return ['None', '']
    }

    return(
        <>
        <div className='nav_all_holder' onClick={() => {GetImg();console.log(imgstate)}}>
            <Link to = '/' tabIndex="-1"><div className = 'nav_logo'>Sapling<img src = '../components/images/MainLogo.png'/></div></Link>
            <div className='nav_info'>
                {document.cookie.includes('userinfo=') === true ? (
                    <div className='nav_logged'>
                        <Link to = '/chat'><SideBar width={30} height={30} className='nav_linkchat'/></Link>
                        <div className='nav_user_holder'>
                            {updatenavbarstate['image'] === '' ? imgstate : (
                                updatenavbarstate['image'] === null ? (<UserIcon width={30} height={30} className='nav_user'/>) : (<div className='nav_user nav_imgexist'><img className='nav_img' src={updatenavbarstate['image']}/></div>)
                            )}
                            <div className='nav_user_info'>
                                <div className='nav_user_name'>
                                    {/*{namestate}*/}
                                    {updatenavbarstate['name'] === '' ? namestate : (
                                        updatenavbarstate['name'] === null ? ('Info') : ('Hello, ' + updatenavbarstate['name'])
                                    )}
                                </div>
                                <div className='nav_user_clicks'>
                                    <ul>
                                        <Link to='/settings'><Settings/>Settings</Link>
                                        <Link to='/termspolicies'><DiagonalArrow style={{transform: 'rotate(180deg)'}}/>Terms& Policies</Link>
                                    </ul>
                                    <div className='nav_logout_line'>
                                        <div className='nav_logout' onClick={() => ClickLogout()}><Logout width={25} height={25}/>Logout</div>
                                    </div>
                                </div>
                            </div>
                        </div>    
                    </div>
                ) : (
                    <Link to='/login' ref={loginRef} tabIndex="-1"><div className='nav_loginbutton'>Log In</div></Link>
                )}
            </div>
        </div>
        <Outlet/>
        </>
    )
}