import '../styling/ChatMain.css'
import { useRef, useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ChatBox } from './ChatBox'
import { ChatBoxUpload } from './ChatBoxUpload'

export function ChatMain({ chatlist, chatnavloadingState, linkparams }){

    const navigate = useNavigate()
    const [isloadingState, isloadingsetState] = useState(true)
    const [convState, convsetState] = useState()
    const cmchatRef = useRef()

    useEffect(() => {
        if(chatnavloadingState === false){
            GetConversation()
        }
    }, [linkparams.id, chatnavloadingState])

    async function GetConversation(){
        let response_status = null
        let response = await fetch(import.meta.env.VITE_URL + 'chats/getconversation/' + linkparams.id + '/', {
            method: 'GET',
            credentials: 'include',
        }).then(res => {
            response_status = res.status
            return res.json()
        }).then(data => data)
        .catch(() => {})

        if(response_status === 200){
            let conv_vals = []
            for(let i=response['c'].length - 1; i>=0; i--){
                conv_vals.push(
                    <>
                        <div className='cm_chatbox'>
                            {response["c"][i]["a"]}
                        </div>
                        <div className='cm_chatuser'>
                            {response["c"][i]["d"] !== undefined ? <ChatBoxUpload cbuState={{'visible': true, 'inchat': true, 'name': response["c"][i]["d"]["name"], 'type': response["c"][i]["d"]["name"].split('.')[1].toUpperCase(), 'size': response["c"][i]["d"]["size"]}}/> : null}
                            {response["c"][i]["q"] !== undefined ?
                            <div className='cm_chatbox cm_boxuser'>
                                {response["c"][i]["q"]}
                            </div> : null
                            }
                        </div>
                    </>
                )
            }
            // Remove this
            /*conv_vals.push(
            <>
                <div className='cm_chatuser'>
                        <ChatBoxUpload cbuState={{'visible': true, 'inchat': true, 'name': 'Habibi', 'type': 'XML', 'size': 800}}/>
                        <div className='cm_chatbox cm_boxuser'>
                            uihuihuihiouhiohdiojijdiosajdiosajdiosjdiosajdiosajaiodjsaiodjsaioihuisahduisahduisahduisahduisahiudsah
                        </div>
                </div>
            </>
            )*/
            //
            convsetState(conv_vals)
            isloadingsetState(false)
        }
        else if(response_status === 401 || response_status === 403){
            navigate('/login', {state: {to: '/chat/' + linkparams.id + '/', expired: true}})
        }

    }

    return(
        <div className='cm_holder'>
            <div className='cm_container'>
                <div className='cm_chat' style={isloadingState === false ? {paddingBottom: '200px'} : {paddingBottom: '0px'}} ref={cmchatRef}>
                    {isloadingState === true ? (
                        <>
                            <div className='cm_loadinguser'>
                                <div className='loading_box loading' style={{width: '75%'}}/>
                                <div className='loading_box loading' style={{width: '85%'}}/>
                            </div>
                            <div className='cm_loading'>
                                <div className='loading_box loading_blue' style={{width: '75%'}}/>
                                <div className='loading_box loading_blue' style={{width: '90%'}}/>
                                <div className='loading_box loading_blue' style={{width: '90%'}}/>
                            </div>
                            <div className='cm_loadinguser'>
                                <div className='loading_box loading' style={{width: '75%'}}/>
                            </div>
                            <div className='cm_loading'>
                                <div className='loading_box loading_blue' style={{width: '75%'}}/>
                                <div className='loading_box loading_blue' style={{width: '90%'}}/>
                            </div>
                        </>
                    ) : (convState)
                    }
                </div>
                <ChatBox chatlist={chatlist} isloadingState={isloadingState} chattype='main' convsetState={convsetState} linkparams={linkparams}/>
                <div className='cm_backwhite'/>
            </div>
        </div>
    )
}