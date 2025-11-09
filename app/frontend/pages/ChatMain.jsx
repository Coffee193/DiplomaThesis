import '../styling/ChatMain.css'
import { NeuralNetwork, UploadFile, ArrowUpload } from '../components/svgs/UtilIcons'
import { useRef, useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'

export function ChatMain(){

    const textareaRef = useRef()
    const arrowuploadRef = useRef()
    const conv_id = useParams()
    const navigate = useNavigate()
    const [convState, convsetState] = useState('')
    const [modelState, modelsetState] = useState('')

    function CheckQuestion(){
        if(textareaRef.current.value.length === 0){
            arrowuploadRef.current.classList.add('chatmain_deactive')
            arrowuploadRef.current.classList.remove('chatmain_active')
        }
        else{
            arrowuploadRef.current.classList.add('chatmain_active')
            arrowuploadRef.current.classList.remove('chatmain_deactive')
        }
    }

    useEffect(() => {
        //getChatConversations()
    }, [conv_id.id])

    async function getChatConversations(){
        let response_status = null
        let response = await fetch('http://127.0.0.1:8000/chats/getchatconversation/' + conv_id.id + '/', {
            method: 'GET',
            credentials: 'include',
        }).then(res => {
            response_status = res.status
            return res.json()
        }).then(data => data)

        if(response_status === 200){
            let conv_vals = []
            for(let i=0; i<response["c"].length; i++){
                conv_vals.push(
                <div className='chatmain_chatbox_user'>
                    <div className='chatmain_chatbox chatmain_user'>
                        {response["c"][i]["q"]}
                    </div>
                </div>
                )
                conv_vals.push(
                    <div className='chatmain_chatbox chatmain_ai'>
                        {response["c"][i]["a"]}
                    </div>
                )
            }
            convsetState(conv_vals)
            modelsetState(response["m"])
        }
        else if(response_status === 401 || response_status === 403){
            navigate('/login')
        }

    }

    async function AskQuestion(){
        if(arrowuploadRef.current.classList.contains('chatmain_active') === true){
            let response_status = null
            let request = {"q": textareaRef.current.value, "c": conv_id.id}
            convsetState(prevState => [prevState,
                <div className='chatmain_chatbox_user'>
                    <div className='chatmain_chatbox chatmain_user'>
                        {request['q']}
                    </div>
                </div>
            ])
            textareaRef.current.value = ''
            let response = await fetch('http://127.0.0.1:8000/chats/askquestion/', {
                method: 'POST',
                body: JSON.stringify(request),
                credentials: 'include',
            }).then(res => {
                response_status = res.status
                return res.json()
            }).then(data => data)
            .catch(() => {response_status = 'failed'})

            if(response_status === 200){
                convsetState(prevState => [prevState,
                    <div className='chatmain_chatbox chatmain_ai'>
                        {response['a']}
                    </div>
                ])
            }
            else if(response_status === 401 || response_status === 403){
                navigate('/login')
            }
        }
    }

    function ShortcutAskQuestion(event){
        if(event.keyCode === 13 && event.shiftKey === false && textareaRef.current.value.length > 0){
            event.preventDefault()
            AskQuestion()
        }
    }

    return(
        <div className='cm_holder'>
            <div className='cm_container'>
                <div className='cm_chat'>
                    {convState}
                </div>
                <div className='chatmain_ask'>
                    <textarea className='chatmain_textarea' placeholder='Ask Sapling' ref={textareaRef} onChange={() => CheckQuestion()} onKeyDown={(event) => ShortcutAskQuestion(event)}/>
                    <div className='chatmain_infoholder'>
                        <div className='chatmain_info_left'>
                            <NeuralNetwork/><span>{modelState}</span>
                        </div>
                        <div className='chatmain_info_right'>
                            <div className='chatmain_info_uploadfile chatmain_active'>
                                <UploadFile/>
                                <div className='chatmain_info_uploadfile_text'>Upload PDF</div>
                            </div>
                            <div className='chatmain_info_arrowupload chatmain_deactive' ref={arrowuploadRef} onClick={() => AskQuestion()}><ArrowUpload/></div>
                        </div>
                    </div>
                    <div className='chatmain_ask_backclick' onClick={() => textareaRef.current.focus()}/>
                </div>
                <div className='chatmain_ask_backwhite'/>
            </div>
        </div>
    )
}