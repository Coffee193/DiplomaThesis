import '../styling/NavBar.css'
import { Link, useNavigate, Outlet, useLocation } from 'react-router-dom'
import { useRef, useState } from 'react'
import { SideBar, UserIcon, Logout, Settings, DiagonalArrow } from '../components/svgs/UtilIcons'

export function NavBar({updatenavbarstate}){

    
    const navigate = useNavigate()
    const location = useLocation()
    const loginRef = useRef()
    const userinfovals = GetUserInfoValues()
    const [namestate, namesetState] = useState(userinfovals[0] === 'None' ? ('Info') : ('Hello, ' + userinfovals[0]))
    const [imgState, imgsetState] = useState(<img src={import.meta.env.VITE_IMG_PATH + userinfovals[1] + '.JPEG'} onError={InitImgNotFound}/>)

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
        imgsetState(<UserIcon width={30} height={30}/>)
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
        <div className='n_allholder' /*onClick={() => {GetImg();console.log(imgstate)}}*/ style={location.pathname === '/' ? {position: 'absolute', backgroundColor: 'transparent'} : null}>
            <Link to = '/' tabIndex="-1"><div className = 'n_logo'>Sapling<img src = '../components/images/MainLogo.png'/></div></Link>
            <div className='n_info'>
                {document.cookie.includes('userinfo=') === true ? (
                    <div className='n_logged'>
                        <Link to = '/chat'><SideBar width={30} height={30} className={'n_util ' + (location.pathname === '/' ? 'n_utilwhite' : 'n_utildefault')}/></Link>
                        <div className='n_userholder'>
                            <div className={'n_user n_util ' + (location.pathname === '/' ? 'n_userwhite' : 'n_userdefault')}>
                                {updatenavbarstate['image'] === '' ? imgState : (
                                    updatenavbarstate['image'] === null ? (<UserIcon width={30} height={30}/>) : (<img src={updatenavbarstate['image']}/>)
                                )}
                            </div>
                            <div className='n_userbox'>
                                <div className='n_userinfo'>
                                    <div className='n_username'>
                                        {updatenavbarstate['name'] === '' ? namestate : (
                                            updatenavbarstate['name'] === null ? ('Info') : ('Hello, ' + updatenavbarstate['name'])
                                        )}
                                    </div>
                                    <div className='n_userutils'>
                                        <ul>
                                            <Link to='/settings'><Settings/>Settings</Link>
                                            <Link to='/termspolicies'><DiagonalArrow style={{transform: 'rotate(180deg)'}}/>Terms& Policies</Link>
                                        </ul>
                                        <div className='n_logoutline'>
                                            <div className='n_logout' onClick={() => ClickLogout()}><Logout width={25} height={25}/>Logout</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>    
                    </div>
                ) : (
                    <Link to='/login' ref={loginRef} tabIndex="-1"><div className='n_login'>Log In</div></Link>
                )}
            </div>
        </div>
        <Outlet/>
        </>
    )
}