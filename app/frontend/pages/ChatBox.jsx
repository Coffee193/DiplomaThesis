import '../styling/ChatBox.css'
import { ArrowUpload, UploadFile, BlocksLoad, SpinnerLoad } from '../components/svgs/UtilIcons'
import { useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ChatBoxUpload } from './ChatBoxUpload'

export function ChatBox({ isloadingState, chatlist, chattype, convsetState, linkparams, isgeneratingState, isgeneratingsetState, convstreamgeneratingRef, ReadAnswerStream, chatnavsetState }){

    const cbtextareaRef = useRef()
    const cbarrowRef = useRef()
    const navigate = useNavigate()
    const [cbuState, cbusetState] = useState({'visible': false, 'isloading': true})
    const cbinputRef = useRef()
    const cbuploadRef = useRef()
    const cbloadRef = useRef()
    const cbaskquestion = useRef(false)

    function CheckQuestion(){
        if(cbinputRef.current.value === ''){
            if(cbtextareaRef.current.value.replace(/(\r\n|\n|\r)/gm, '').length === 0){
                ArrowDeactive()
            }
            else{
                ArrowActive()
            }
        }
    }

    async function CreateChat(){
        let response_status = null
        let request = {"q": cbtextareaRef.current.value}
        let body = null

        if(cbinputRef.current.value !== ''){
            body = new FormData()
            body.append('data', JSON.stringify(request))
            body.append('document', JSON.stringify({'data': cbuState['data'], 'name': cbuState['name']}))
        }
        else{
            body = JSON.stringify(request)
        }

        let response = await fetch(import.meta.env.VITE_URL + 'chats/createchat/', {
            method: 'POST',
            body: body,
            credentials: 'include',
        }).then(res => {
            response_status = res.status
            return res.json()}).then(data => data)
        .catch(() => {})

        if(response_status === 200){
            response['index'] = chatlist.current.length
            chatlist.current.push(response)
            chatnavsetState(chatlist.current)
            navigate('/chat/' + response['_id'].toString() + '/')
        }
        else if(response_status === 401 || response_status === 403){
            navigate('/login', {state: {to: '/chat', expired: true}})
        }
    }

    function PressEnter(event){
        if(event.key === 'Enter'){
            if(event.shiftKey === false){
                event.preventDefault()
                if(cbaskquestion.current === false){
                    SubmitQuestion()
                }
            }
        }
    }

    function SubmitQuestion(){
        if(cbinputRef.current.value === '' && cbtextareaRef.current.value.replace(/(\r\n|\n|\r)/gm, '').length === 0){
            return
        }
        if(linkparams === undefined){
            CreateChat()
            console.log('iiiiiiii')
            isgeneratingsetState(true)
            console.log('uuuuuuuuuuu')
        }
        else{
            AskQuestion()
            isgeneratingsetState(true)
        }
        ArrowDeactive()
    }

    async function AskQuestion(){
        let response_status = null
        let request = {"q": cbtextareaRef.current.value, "id": linkparams.id}
        
        let blob = null
        let url = null
        
        let body = null
        if(cbinputRef.current.value !== ''){
            body = new FormData()
            body.append('data', JSON.stringify(request))
            body.append('document', JSON.stringify({'data': cbuState['data'], 'name': cbuState['name']}))

            blob = new Blob(
                [atob(cbuState['data'].slice(21))],
                {
                    type: 'application/JSON'
                }
            )
            url = URL.createObjectURL(blob)
        }
        else{
            body = JSON.stringify(request)
        }

        convsetState(prevState => [
            <div className='cm_chatbox cb_answerload'>
                <BlocksLoad/>
            </div>,
            <div className='cm_chatuser'>
                {cbinputRef.current.value !== '' ? <ChatBoxUpload cbuState={{'visible': true, 'inchat': true, 'name': cbuState['name'], 'type': cbuState['type'], 'size': cbuState['size'], 'hardpath': url}}/> : ''}
                {cbinputRef.current.value !== '' && cbtextareaRef.current.value.replace(/(\r\n|\n|\r)/gm, '').length === 0 ? '' :
                <div className='cm_chatbox cm_boxuser'>
                    {request['q']}
                </div>}
            </div>,
            prevState
        ])
        if(cbinputRef.current.value !== ''){
            cbusetState({'visible': false, 'isloading': true})
            UploadActive()
            ArrowDeactive()
            cbinputRef.current.value = ''
        }
        
        cbtextareaRef.current.value = ''
        let response = await fetch(import.meta.env.VITE_URL + 'chats/askquestion/', {
            method: 'POST',
            body: body,
            credentials: 'include',
        }).then(res => {
            response_status = res.status
            return res.body
        }).then(body => {
            return body.getReader()
        })
        .catch(() => {})

        if(response_status === 200){
            convstreamgeneratingRef.current.add(linkparams.id)
            ReadAnswerStream(response, linkparams, convsetState, isgeneratingsetState, convstreamgeneratingRef)
        }
        else if(response_status === 401 || response_status === 403){
            navigate('/login', {state: {to: '/chat/' + linkparams.id, expired: true}})
        }
    }

    function UploadDocument(){
        cbusetState({'visible': true, 'name': cbinputRef.current.files[0]['name'], 'size': (cbinputRef.current.files[0]['size']/1024).toFixed(1), 'type': cbinputRef.current.files[0]['type'].split('/')[1].toUpperCase()})
        let filereader = new FileReader();
        filereader.readAsDataURL(cbinputRef.current.files[0])
        filereader.onloadend = () => {
            console.log(filereader.result)
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

    return(
        <div className={chattype === 'body' ? 'cb_holder' : 'cb_holder_bottom'} style={chattype === 'main' && isloadingState === true ? {justifyContent: 'end'} : {justifyContent: 'space-between'}}>
            { isloadingState === false ? (
            <>
                <div>
                    <ChatBoxUpload cbuState={cbuState} cbusetState={cbusetState} cbinputRef={cbinputRef} UploadActive={UploadActive} EmptyTextArrowDeactive={EmptyTextArrowDeactive}/>
                    <textarea className='cb_textarea' placeholder='Ask Sapling' onChange={() => CheckQuestion()} ref={cbtextareaRef} onKeyDown={(event) => PressEnter(event)} autoFocus={true}/>
                </div>
                <div className='cb_infoholder'>
                    { isgeneratingState === false ? (
                    <>
                        <div className='cb_util cb_utilactive cb_upload' onClick={() => cbinputRef.current.value === '' ? cbinputRef.current.click() : null} ref={cbuploadRef}>
                            <UploadFile/>
                            <div className={'cb_uploadtext ' + (chattype === 'main' ? 'cb_uploadmain' : 'cb_uploadbody')}>Upload File</div>
                            <input type='file' className='cb_input' ref={cbinputRef} accept='application/JSON' onChange={() => UploadDocument()}/>
                        </div>
                        <div className={'cb_util ' +  ( (cbtextareaRef.current === undefined || cbtextareaRef.current.value === '') ? 'cb_utildeactive' : 'cb_utilactive')} onClick={() => SubmitQuestion()} ref={cbarrowRef}><ArrowUpload/></div>
                    </>
                    ) : (
                    <div className='cb_util cb_utilaskload' ref={cbloadRef}><SpinnerLoad/></div>
                    )
                    }
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