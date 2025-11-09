import '../styling/ChatBody.css'
import { useNavigate } from 'react-router-dom'
import { ChatBox } from './ChatBox'

export function ChatBody({ chatlist , setnewconv, isloadingState}){

    const navigate = useNavigate()

    function CheckQuestion(){
        if(textareaRef.current.value.length === 0){
            arrowuploadRef.current.classList.add('cbody_chat_info_deactive')
            arrowuploadRef.current.classList.remove('cbody_chat_info_active')
        }
        else{
            arrowuploadRef.current.classList.add('cbody_chat_info_active')
            arrowuploadRef.current.classList.remove('cbody_chat_info_deactive')
        }
    }

    async function AskQuestion(){
        console.log(arrowuploadRef.current.classList.contains('cbody_chat_info_active'))
        if(arrowuploadRef.current.classList.contains('cbody_chat_info_active') === true){
            let response_status = null
            let request = {"q": textareaRef.current.value, "model": modelselectedState}
            let response = await fetch('http://127.0.0.1:8000/chats/createchats/', {
                method: 'POST',
                body: JSON.stringify(request),
                credentials: 'include',
            }).then(res => {
                response_status = res.status
                return res.json()}).then(data => data)
            .catch(() => {response_status = 'failed'})

            if(response_status === 200){
                response['date_created'] = new Date(response['date_created'] * 1000)
                chatlist.current.push(response)
                setnewconv(response)
                navigate('/chat/' + response['_id'].toString())
            }
            else if(response_status === 401 || response_status === 403){
                navigate('/login')
            }
            else{
                navigate('/error400')
            }
        }
    }

    return(
        <div className = 'cbd_holder'>
            <div className='cbd_inner'>
                <div className='cbd_upper'>
                    <div className='cbd_image_holder'><img src='../components/images/MainLogo.png'/></div>
                    <div className='cbd_image_text'>How can I assist you?</div>
                </div>
                <ChatBox isloadingState={isloadingState}/>
            </div>
        </div>
)
}