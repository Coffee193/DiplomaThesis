import '../styling/ChatLobby.css'
import { ChatNav } from './ChatNav'
import { ChatBody } from './ChatBody'
import { useState, useRef, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { ChatMain } from './ChatMain'

export function ChatLobby(){

    const [conversationsState, conversationssetState] = useState()
    const chatslist = useRef()
    const linkparams = useParams()
    const [isloadingState, isloadingsetState] = useState(true)
    

    return(
        <div className='cl_holder'>
            <div className='cl_box'>
                <div className='cl_main'>
                    <ChatNav convState={conversationsState} convsetState={conversationssetState} chatlist={chatslist} isloadingState={isloadingState} isloadingsetState={isloadingsetState} linkparams={linkparams}/>
                    {linkparams.id === undefined ? (
                        <ChatBody chatlist={chatslist} isloadingState={isloadingState} chatnavsetState={conversationssetState}/>
                    ) : (
                        <ChatMain chatnavloadingState={isloadingState} linkparams={linkparams} chatnavsetState={conversationssetState} chatlist={chatslist}/>
                    )}
                </div>
            </div>
        </div>
    )
}