import '../styling/ChatBox.css'
import { ArrowUpload } from '../components/svgs/UtilIcons'
import { useRef } from 'react'
import { useNavigate, useParams } from 'react-router-dom'

export function ChatBox({ isloadingState, chatlist, chattype, convsetState }){

    const cbtextareaRef = useRef()
    const cbarrowRef = useRef()
    const navigate = useNavigate()
    const linkparams = useParams()

    function CheckQuestion(){
        if(cbtextareaRef.current.value.length === 0){
            cbarrowRef.current.classList.add('cb_arrowdeactive')
            cbarrowRef.current.classList.remove('cb_arrowactive')
        }
        else{
            cbarrowRef.current.classList.add('cb_arrowactive')
            cbarrowRef.current.classList.remove('cb_arrowdeactive')
        }
    }

    async function CreateChat(){
        if(cbtextareaRef.current.value.length > 0){
            let response_status = null
            let request = {"q": cbtextareaRef.current.value}
            let response = await fetch(import.meta.env.VITE_URL + 'chats/createchat/', {
                method: 'POST',
                body: JSON.stringify(request),
                credentials: 'include',
            }).then(res => {
                response_status = res.status
                return res.json()}).then(data => data)
            .catch(() => {})

            if(response_status === 200){
                response['date_created'] = new Date(response['date_created'] * 1000)
                chatlist.current.push(response)
                navigate('/chat/' + response['_id'].toString() + '/')
            }
            else if(response_status === 401 || response_status === 403){
                navigate('/login', {state: {to: '/chat', expired: true}})
            }
        }
    }

    function PressEnter(event){
        if(cbtextareaRef.current.value.length === 0 && event.key === 'Enter' && event.shiftKey === false){
            event.preventDefault()
            return
        }
        if(event.key === 'Enter'){
            if(event.shiftKey === false){
                event.preventDefault()
                SubmitQuestion()
            }
        }
    }

    function SubmitQuestion(){
        if(linkparams.id === undefined){
            CreateChat()
        }
        else{
            AskQuestion()
        }
    }

    async function AskQuestion(){
        let response_status = null
        let request = {"q": cbtextareaRef.current.value, "id": linkparams.id}
        convsetState(prevState => [prevState,
            <div className='cm_chatuser'>
                <div className='cm_chatbox cm_boxuser'>
                    {request['q']}
                </div>
            </div>
        ])
        cbtextareaRef.current.value = ''
        let response = await fetch(import.meta.env.VITE_URL + 'chats/askquestion/', {
            method: 'POST',
            body: JSON.stringify(request),
            credentials: 'include',
        }).then(res => {
            response_status = res.status
            return res.json()
        }).then(data => data)
        .catch(() => {})

        if(response_status === 200){
            convsetState(prevState => [prevState,
                <div className='cm_chatbox'>
                    {response['a']}
                </div>
            ])
        }
        else if(response_status === 401 || response_status === 403){
            navigate('/login', {state: {to: '/chat/' + linkparams.id, expired: true}})
        }
    }

    return(
        <div className={chattype === 'body' ? 'cb_holder' : 'cb_holder_bottom'} style={chattype === 'main' && isloadingState === true ? {justifyContent: 'end'} : {justifyContent: 'space-between'}}>
            { isloadingState === false ? (
            <>
                <textarea className='cb_textarea' placeholder='Ask Sapling' onChange={() => CheckQuestion()} ref={cbtextareaRef} onKeyDown={(event) => PressEnter(event)} autoFocus={true}/>
                <div className='cb_infoholder'>
                    <div className='cb_arrow cb_arrowdeactive' onClick={() => SubmitQuestion()} ref={cbarrowRef}><ArrowUpload/></div>
                </div>
                <div className='cb_bg' onClick={() => cbtextareaRef.current.focus()}/>
                </>
            ) : (
                <div className='cb_loading'>
                    <div className='cb_arrowload loading'/>
                </div>
            )
            }
        </div>
    )
}