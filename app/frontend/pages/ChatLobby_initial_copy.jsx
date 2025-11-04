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
    const [mainbodyState, mainbodysetState] = useState()

    function ConversationSelect(){
        if(conv_id.id === undefined){
            mainbodysetState(<ChatBody chatlist={chatslist} setnewconv={newconvsetState}/>)
        }
        else{
            mainbodysetState(<ChatMain/>)
        }
    }
    useEffect(() => ConversationSelect(), [conv_id])

    return(
        <div className='all_holder_clobby'>
            <div className='clobby'>
                <div className='clobby_all'>
                    <ChatNav convState={conversationsState} convsetState={conversationssetState} chatlist={chatslist} newconv={newconvState}/>
                    
                    {/*<ChatBody chatlist={chatslist} setnewconv={newconvsetState}/>*/}
                    {mainbodyState}
                </div>
            </div>
        </div>
    )
}