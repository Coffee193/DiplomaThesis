import '../styling/ChatMain.css'
import { useRef, useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ChatBox } from './ChatBox'

export function ChatMain({ chatlist }){

    const linkparams = useParams()
    const navigate = useNavigate()
    const [isloadingState, isloadingsetState] = useState(true)
    const [convState, convsetState] = useState()

    useEffect(() => {
        GetConversation()
    }, [linkparams.id])

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
            for(let i=0; i<response["c"].length; i++){
                conv_vals.push(
                <div className='cm_chatuser'>
                    <div className='cm_chatbox cm_boxuser'>
                        {response["c"][i]["q"]}
                    </div>
                </div>
                )
                conv_vals.push(
                    <div className='cm_chatbox'>
                        {response["c"][i]["a"]}
                    </div>
                )
            }
            convsetState(conv_vals)
            isloadingsetState(false)
        }
        else if(response_status === 401 || response_status === 403){
            navigate('/login', {state: {to: '/chat/' + linkparams.id, expired: true}})
        }

    }

    return(
        <div className='cm_holder'>
            <div className='cm_container'>
                <div className='cm_chat' style={isloadingState === false ? {paddingBottom: '200px'} : {paddingBottom: '0px'}}>
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
                <ChatBox chatlist={chatlist} isloadingState={isloadingState} chattype='main' convsetState={convsetState}/>
                <div className='cm_backwhite'/>
            </div>
        </div>
    )
}