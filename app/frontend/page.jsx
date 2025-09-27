import './styling/main.css'

import { Route, Routes } from 'react-router-dom'

import { Login } from './pages/Login'
import { Register } from './pages/Register'
import { HomeMain } from './pages/Home'
import { ChatLobby } from './pages/ChatLobby'
import { TermsPolicies } from './pages/TermsPolicies'
import { Settings } from './pages/Settings'

export function Home() {
    return(
        <Routes>
            <Route path = '/' element = {<><HomeMain/></>} />
            <Route path = '/login' element = {<><Login/></>} />
            <Route path = '/register' element = {<><Register/></>} />
            <Route path = '/chat'>
                <Route index element={<><ChatLobby/></>}/>
                <Route path=':id' element={<><ChatLobby/></>}/>
            </Route>
            <Route path = '/termspolicies' element = {<><TermsPolicies/></>}/>
            <Route path = '/settings' element = {<><Settings/></>}/>
        </Routes>
    )
}