import '../styling/ChatLobby.css'
import { ChatNav } from './ChatNav'
import { ChatBody } from './ChatBody'
import { useState, useRef, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { ChatMain } from './ChatMain'

export function ChatLobby(){

    const [conversationsState, conversationssetState] = useState()
    const chatslist = useRef()
    const [newconvState, newconvsetState] = useState()
    const conv_id = useParams()

    const [isloadingState, isloadingsetState] = useState(true)

    return(
        <div className='cl_holder'>
            <div className='cl_box'>
                <div className='cl_main'>
                    <ChatNav convState={conversationsState} convsetState={conversationssetState} chatlist={chatslist} newconv={newconvState} isloadingState={isloadingState} isloadingsetState={isloadingsetState}/>
                    {conv_id.id === undefined ? (
                        <ChatBody chatlist={chatslist} setnewconv={newconvsetState} isloadingState={isloadingState}/>
                    ) : (
                        <ChatMain isloadingState={isloadingState} isloadingsetState={isloadingsetState}/>
                    )}
                </div>
            </div>
        </div>
    )
}