import '../styling/NavBar.css'
import { Link, useNavigate, Outlet } from 'react-router-dom'
import { useEffect, useRef, useState } from 'react'
import { SideBar, UserIcon, Logout, Settings, DiagonalArrow } from '../components/svgs/UtilIcons'

export function NavBar(){

    const navigate = useNavigate()
    const navloggedRef = useRef()
    const loginRef = useRef()
    const [namestate, namesetState] = useState()
    const [userimgstate, userimgsetState] = useState()

    async function ClickLogout(){
        let cookie_var = document.cookie
        if(cookie_var.includes('user_name=') === false){
            return
        }
        let response_status = null
        let response =  await fetch('http://127.0.0.1:8000/loginregister/logout/', {
                                    method:'DELETE',
                                    credentials: 'include',
                                }).then(res => {
                                    response_status = res.status
                                    return res.json()}).then(data => data)
            if(response_status === 200){
                navigate('/')
                window.location.reload()
            }
    }

    useEffect(() => {
        let cookie_var = document.cookie

        if(cookie_var.includes('user_name=') === true){
                let cookie_val = null
                cookie_var = cookie_var.split(';')
                for(let i=0;i<cookie_var.length;i++){
                    if(cookie_var[i][0] === ' '){
                        cookie_var[i] = cookie_var[i].slice(1)
                    }

                    if(cookie_var[i].slice(0,10) === 'user_name='){
                        cookie_val = cookie_var[i].slice(10)
                        break
                    }
                    else{
                        continue
                    }
                }

                if(cookie_val === 'None'){
                    namesetState('Info')
                }
                else{
                    namesetState('Hello, ' + cookie_val)
                }

                loginRef.current.classList.add('display_none')
                navloggedRef.current.classList.remove('display_none')
                navloggedRef.current.classList.add('flex')
                console.log('rerednerd*********')
                GetUserImg()
            }    
    },[])

    async function GetUserImg(){
        let response_status = null
        let response = await fetch('http://127.0.0.1:8000/loginregister/getuserimg/',{
            method: 'GET',
            credentials: 'include',
        }).then(res => {
            response_status = res.status
            return res.json()
        }).then(data => data)

        if(response_status === 401 || response_status === 403){
            navigate('/login')
            return
        }
        else if(response_status === 200){
            if(response === false){
                userimgsetState(<UserIcon width={30} height={30} className='nav_user'/>)
            }
            else{
                let img_path = import.meta.env.VITE_IMG_PATH + response + '.JPEG'
                userimgsetState(<div className='nav_user flex justify-center align-center h-30px overflow-hidden'><img className='contain h-100 w-100' src={img_path}/></div>)
            }

        }

    }

    return(
        <>
        <div className = 'nav_all_holder'>
            <Link to = '/'><div className = 'LogoNav'>Sapling<img src = '../components/images/MainLogo.png'/></div></Link>
            <div className='nav_info'>
                <div className='nav_logged display_none' ref={navloggedRef}>
                    <Link to = '/chat'><SideBar width={30} height={30} className='NavSidebar'/></Link>
                    <div className='nav_user_holder'>
                        {userimgstate}
                        <div className='nav_user_info'>
                            <div className='nav_user_name'>{namestate}</div>
                            <div className='nav_user_clicks'>
                                <ul>
                                    <Link to = '/settings'><Settings/>Settings</Link>
                                    <Link to = '/termspolicies'><DiagonalArrow style={{transform: 'rotate(180deg)'}}/>Terms& Policies</Link>
                                </ul>
                                <div className='nav_logout_line'>
                                    <div className='nav_logout' onClick={() => ClickLogout()}><Logout width={25} height={25}/>Logout</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <Link to='/login' ref={loginRef}><div className='LoginButton'>Log In</div></Link>
            </div>
        </div>
        <Outlet/>
        </>
    )
}