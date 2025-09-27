import '../styling/NavBar.css'
import { Link, useNavigate } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { SideBar, UserIcon, Logout, Settings, DiagonalArrow } from '../components/svgs/UtilIcons'

export function NavBar(haslowborder = false){

    const [loginstate, loginsetState] = useState()
    const navigate = useNavigate()

    async function ClickLogout(){
        let cookie_var = document.cookie
        if(cookie_var.includes('user_name=') === false){
            return
        }
        console.log('yoyos')
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
                    console.log('chipii')
                    console.log(cookie_var[i].slice(0,10))
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
                    cookie_val = 'Info'
                }
                else{
                    cookie_val = 'Hello, ' + cookie_val
                }

                loginsetState(
                    <div className='nav_logged'>
                        <Link to = '/chat'><SideBar width={30} height={30} className='NavSidebar'/></Link>
                        <div className='nav_user_holder'>
                            <UserIcon width={30} height={30} className='nav_user'/>
                            <div className='nav_user_info'>
                                <div className='nav_user_name'>{cookie_val}</div>
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
                )
            }
        else{
            loginsetState(<Link to='/login'><div className='LoginButton'>Log In</div></Link>)
        }
    },[])

    return(
        <div className = 'nav_all_holder'>
            <Link to = '/'><div className = 'LogoNav'>Sapling<img src = '../components/images/MainLogo.png'/></div></Link>
            <div className='nav_info'>
                {loginstate}
            </div>
        </div>
    )
}