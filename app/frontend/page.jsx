import './styling/main.css'

import { Route, Routes } from 'react-router-dom'

import { Login } from './pages/Login'
import { Register } from './pages/Register'
import { HomeMain } from './pages/Home'
import { ChatLobby } from './pages/ChatLobby'
import { TermsPolicies } from './pages/TermsPolicies'
import { Settings } from './pages/Settings'
import { Referal } from './pages/Referal'
import { NavBar } from './pages/NavBar'

export function Home() {
    return(
        <Routes>
            <Route path='/login' element={<Login/>}/>
            <Route path='/register' element={<Register/>}/>
            <Route element={<NavBar/>}>
                <Route path = '/' element = {<HomeMain/>} />
                <Route path = '/chat'>
                    <Route index element={<ChatLobby/>}/>
                    <Route path=':id' element={<ChatLobby/>}/>
                </Route>
                <Route path = '/termspolicies' element = {<TermsPolicies/>}/>
                <Route path = '/settings' element = {<Settings/>}/>
                <Route path = '/referalcodes' element = {<Referal/>}/>
            </Route>
        </Routes>
    )
}