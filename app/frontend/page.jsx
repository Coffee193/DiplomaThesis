import './styling/main.css'

import { Route, Routes } from 'react-router-dom'

import { Home } from './pages/Home'
import { ChatLobby } from './pages/ChatLobby'
import { TermsPolicies } from './pages/TermsPolicies'
import { Settings } from './pages/Settings'
import { Referal } from './pages/Referal'
import { NavBar } from './pages/NavBar'
import { useState } from 'react'
import { LoginRegister } from './pages/LoginRegister'

export function Main() {

    const [updatenavbarstate, updatenavbarsetState] = useState({'name': '', 'image': ''})

    return(
        <Routes>
            <Route path='/login' element={<LoginRegister lrtype={'l'}/>}/>
            <Route path='/register' element={<LoginRegister lrtype={'r'}/>}/>
            <Route element={<NavBar updatenavbarstate={updatenavbarstate}/>}>
                <Route path = '/' element = {<Home/>} />
                <Route path = '/chat'>
                    <Route index element={<ChatLobby/>}/>
                    <Route path=':id' element={<ChatLobby/>}/>
                </Route>
                <Route path = '/termspolicies' element = {<TermsPolicies/>}/>
                <Route path = '/settings' element = {<Settings updatenavbarsetState={updatenavbarsetState}/>}/>
                <Route path = '/referalcodes' element = {<Referal/>}/>
            </Route>
        </Routes>
    )
}