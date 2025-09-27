import '../styling/ChatBody.css'
import { ArrowUpload, UploadFile, NeuralNetwork } from '../components/svgs/UtilIcons'
import { useRef, useState } from 'react'
import { ModelSelectPopUp } from './ModelselectPopUp'
import { useNavigate } from 'react-router-dom'


export function ChatBody({ chatlist , setnewconv }){

    const textareaRef = useRef()
    const [modelpopupState, modelpopupsetState] = useState(0)
    const [modelselectedState, modelselectedsetState] = useState('Llama 3.0')
    const arrowuploadRef = useRef()
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
        <div className = 'cbody_holder'>
            <ModelSelectPopUp BlurClassName={'cbody_inner'} modelpopupclicked={modelpopupState} changemodel={modelselectedsetState}/>
            <div className='cbody_inner'>
                <div className='cbody_upper'>
                    <div className='cbody_image_holder'><img src='../components/images/MainLogo.png'/></div>
                    <div className='cbody_image_text'>How can I assist you?</div>
                </div>
                <div className='cbody_lower'>
                    <textarea className='cbody_textarea' placeholder='Ask Sapling' ref={textareaRef} onChange={() => CheckQuestion()}/>
                    <div className='cbody_chat_info_holder'>
                        <div className='cbody_chat_info_left'>
                            <div onClick={() => modelpopupsetState((prevstate) => prevstate + 1)}>
                                <NeuralNetwork/><span>{modelselectedState}</span>
                            </div>
                        </div>
                        <div className='cbody_chat_info_right'>
                            <div className='cbody_chat_uploadpdf cbody_chat_info_active'>
                                <UploadFile/>
                                <div className='cbody_chat_uploadpdf_text' style={{color:'#fff'}}>Upload PDF</div>
                            </div>
                            <div className='cbody_chat_arrowupload cbody_chat_info_deactive' ref={arrowuploadRef} onClick={() => AskQuestion()}><ArrowUpload/></div>
                        </div>
                    </div>
                    <div className='cbody_lower_backclick' onClick={() => textareaRef.current.focus()}/>
                </div>
            </div>
        </div>
)
}