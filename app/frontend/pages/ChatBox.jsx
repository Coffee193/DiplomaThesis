import '../styling/ChatBox.css'
import { ArrowUpload } from '../components/svgs/UtilIcons'
import { useRef } from 'react'
import { useNavigate } from 'react-router-dom'

export function ChatBox({ isloadingState, chatlist, chattype }){

    const cbtextareaRef = useRef()
    const cbarrowRef = useRef()
    const navigate = useNavigate()

    function CheckQuestion(){
        console.log('aaaaaaaa')
        console.log(cbtextareaRef.current.value.length)
        if(cbtextareaRef.current.value.length === 0){
            cbarrowRef.current.classList.add('cb_arrowdeactive')
            cbarrowRef.current.classList.remove('cb_arrowactive')
        }
        else{
            cbarrowRef.current.classList.add('cb_arrowactive')
            cbarrowRef.current.classList.remove('cb_arrowdeactive')
        }
    }

    async function AskQuestion(){
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
                AskQuestion()
            }
        }
    }

    return(
        <div className={chattype === 'body' ? 'cb_holder' : 'cb_holder_bottom'}>
            { isloadingState === false ? (
            <>
                <textarea className='cb_textarea' placeholder='Ask Sapling' onChange={() => CheckQuestion()} ref={cbtextareaRef} onKeyDown={(event) => PressEnter(event)}/>
                <div className='cb_infoholder'>
                    <div className='cb_arrow cb_arrowdeactive' onClick={() => AskQuestion()} ref={cbarrowRef}><ArrowUpload/></div>
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