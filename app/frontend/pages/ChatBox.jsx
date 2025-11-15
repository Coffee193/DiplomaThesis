import '../styling/ChatBox.css'
import { ArrowUpload, UploadFile } from '../components/svgs/UtilIcons'
import { useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ChatBoxUpload } from './ChatBoxUpload'

export function ChatBox({ isloadingState, chatlist, chattype, convsetState, linkparams }){

    const cbtextareaRef = useRef()
    const cbarrowRef = useRef()
    const navigate = useNavigate()
    const [cbuState, cbusetState] = useState({'visible': false, 'isloading': true})
    const cbinputRef = useRef()
    const cbuploadRef = useRef()

    function CheckQuestion(){
        if(cbuploadRef.current.value === ''){
            if(cbtextareaRef.current.value.length === 0){
                ArrowDeactive()
            }
            else{
                ArrowActive()
            }
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
        if(linkparams === undefined){
            CreateChat()
        }
        else{
            AskQuestion()
        }
    }

    async function AskQuestion(){
        let response_status = null
        let request = {"q": cbtextareaRef.current.value, "id": linkparams.id}
        convsetState(prevState => [
            <div className='cm_chatuser'>
                <div className='cm_chatbox cm_boxuser'>
                    {request['q']}
                </div>
            </div>,
            prevState
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
            convsetState(prevState => [
                <div className='cm_chatbox'>
                    {response['a']}
                </div>,
                prevState
            ])
        }
        else if(response_status === 401 || response_status === 403){
            navigate('/login', {state: {to: '/chat/' + linkparams.id, expired: true}})
        }
    }

    function UploadDocument(){
        console.log('i was called')
        cbusetState({'visible': true, 'name': cbinputRef.current.files[0]['name'], 'size': (cbinputRef.current.files[0]['size']/1024).toFixed(1), 'type': cbinputRef.current.files[0]['type'].split('/')[1].toUpperCase()})
        let filereader = new FileReader();
        filereader.readAsDataURL(cbinputRef.current.files[0])
        filereader.onloadend = () => {
            cbusetState(prevState => ({...prevState, 'isloading': false, 'data': filereader.result}))
            UploadDeactive()
            ArrowActive()
        }
    }

    function ArrowActive(){
        cbarrowRef.current.classList.add('cb_utilactive')
        cbarrowRef.current.classList.remove('cb_utildeactive')
    }
    function ArrowDeactive(){
        cbarrowRef.current.classList.add('cb_utildeactive')
        cbarrowRef.current.classList.remove('cb_utilactive')
    }
    function UploadActive(){
        cbuploadRef.current.classList.remove('cb_utildeactive')
        cbuploadRef.current.classList.add('cb_utilactive', 'cb_upload')
    }
    function UploadDeactive(){
        cbuploadRef.current.classList.remove('cb_upload', 'cb_utilactive')
        cbuploadRef.current.classList.add('cb_utildeactive')
    }
    function EmptyTextArrowDeactive(){
        if(cbtextareaRef.current.value === ''){
            ArrowDeactive()
        }
    }

    async function AskQuestionWithDocument(){
        let response_status = null
        
    }

    return(
        <div className={chattype === 'body' ? 'cb_holder' : 'cb_holder_bottom'} style={chattype === 'main' && isloadingState === true ? {justifyContent: 'end'} : {justifyContent: 'space-between'}}>
            { isloadingState === false ? (
            <>
                <div>
                    <ChatBoxUpload cbuState={cbuState} cbusetState={cbusetState} cbinputRef={cbinputRef} UploadActive={UploadActive} EmptyTextArrowDeactive={EmptyTextArrowDeactive}/>
                    <textarea className='cb_textarea' placeholder='Ask Sapling' onChange={() => CheckQuestion()} ref={cbtextareaRef} onKeyDown={(event) => PressEnter(event)} autoFocus={true}/>
                </div>
                <div className='cb_infoholder'>
                    <div className='cb_util cb_utilactive cb_upload' onClick={() => cbinputRef.current.value === '' ? cbinputRef.current.click() : null} ref={cbuploadRef}>
                        <UploadFile/>
                        <div className={'cb_uploadtext ' + (chattype === 'main' ? 'cb_uploadmain' : 'cb_uploadbody')}>Upload File</div>
                        <input type='file' className='cb_input' ref={cbinputRef} accept='text/xml' onChange={() => UploadDocument()}/>
                    </div>
                    <div className='cb_util cb_utildeactive' onClick={() => SubmitQuestion()} ref={cbarrowRef}><ArrowUpload/></div>
                </div>
                <div className='cb_bg' onClick={() => cbtextareaRef.current.focus()}/>
                </>
            ) : (
                <div className='cb_loading'>
                    <div className='cb_utilload loading'/>
                </div>
            )
            }
        </div>
    )
}