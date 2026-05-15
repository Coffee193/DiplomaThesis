import '../styling/ChatBox.css'
import { ArrowUpload, UploadFile, BlocksLoad, SpinnerLoad, NeuralNetwork, SparklesIcon, Key2Icon, XCloseIcon } from '../components/svgs/UtilIcons'
import { useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ChatBoxUpload } from './ChatBoxUpload'
import { ChatBoxModelPopUp } from './ChatBoxModelPopUp'
import { model_list } from './modelList'

export function ChatBox({ isloadingState, chatlist, chattype, convsetState, linkparams, isgeneratingState, isgeneratingsetState, convstreamgeneratingRef, ReadAnswerStream, chatnavsetState, modelState }){

    const cbtextareaRef = useRef()
    const cbarrowRef = useRef()
    const navigate = useNavigate()
    //const [cbuState, cbusetState] = useState({'visible': false, 'isloading': true})
    const [cbuState, cbusetState] = useState({'documents': []})
    const cbinputRef = useRef()
    const cbuploadRef = useRef()
    const cbloadRef = useRef()
    const cbaskquestion = useRef(false)
    const [cbmodelState, cbmodelsetState] = useState({'name': 'Llama3.1:7B - Agent', 'type': 'local', 'agent': 'json-agent', 'id': 1})
    const [cbmodelpopupactiveState, cbmodelpopupactivesetState] = useState(false)
    const [cbkeyboxvisibleState, cbkeyboxvisiblesetState] = useState(false)
    const cbkeyRef = useRef()

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
        let request = {"q": cbtextareaRef.current.value, "m": cbmodelState['id']}
        let body = null

        if(cbmodelState['type'] === 'cloud'){
            request['k'] = cbkeyRef.current.value
        }

        //if(cbinputRef.current.value !== ''){
        console.log(cbuState['documents'].length)
        console.log(cbuState['documents'])
        if(cbuState['documents'].length !== 0){
            body = new FormData()
            body.append('data', JSON.stringify(request))
            //body.append('document', JSON.stringify({'data': cbuState['data'], 'name': cbuState['name']}))
            //body.append('document', JSON.stringify({'data': cbuState['documents']['data'], 'name': cbuState['documents']['name']}))
            body.append('document', JSON.stringify(cbuState['documents'].map( ({data, name}) => ({data, name}) )))
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
        if(cbuState['documents'].length === 0 && cbtextareaRef.current.value.replace(/(\r\n|\n|\r)/gm, '').length === 0){
            return
        }
        if(linkparams === undefined){
            CreateChat()
            if(isgeneratingsetState !== undefined){
                isgeneratingsetState(true)
            }
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
        let askdoclist = []

        if(cbmodelState['type'] === 'cloud'){
            request['k'] = cbkeyRef.current.value
        }

        if(cbuState['documents'].length !== 0){
            body = new FormData()
            body.append('data', JSON.stringify(request))
            //body.append('document', JSON.stringify({'data': cbuState['data'], 'name': cbuState['name']}))
            body.append('document', JSON.stringify( cbuState['documents'].map(({name, data}) => ({name, data})) ))
            /*
            blob = new Blob(
                [atob(cbuState['data'].slice(29))],
                {
                    type: 'application/JSON'
                }
            )
            url = URL.createObjectURL(blob)*/

            askdoclist = cbuState['documents'].map(doc => {
                const blob = new Blob([atob(doc['data'].slice(29))], { type: 'application/JSON'})
                const url = URL.createObjectURL(blob)
                return {name: doc.name, type: doc.type, 'size': doc.size, 'hardpath': url, 'isloading': false}
            })
        }
        else{
            body = JSON.stringify(request)
        }

        convsetState(prevState => [
            <div className='cm_chatbox cb_answerload'>
                <BlocksLoad/>
            </div>,
            <div className='cm_chatuser'>
                {/*cbinputRef.current.value !== '' ? <ChatBoxUpload cbuState={{'visible': true, 'inchat': true, 'name': cbuState['name'], 'type': cbuState['type'], 'size': cbuState['size'], 'hardpath': url}}/> : ''*/}
                {cbuState['documents'].length !== 0 && <ChatBoxUpload cbuState={{'inchat': true, 'documents': askdoclist}}/>}
                {request['q'].replace(/(\r\n|\n|\r)/gm, '').length !== 0 && <div className='cm_chatbox cm_boxuser'> {request['q']} </div>}
            </div>,
            prevState
        ])
        if(cbuState['documents'].length !== 0){
            //cbusetState({'visible': false, 'isloading': true})
            cbusetState({'documents': []})
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
        //cbusetState({'visible': true, 'name': cbinputRef.current.files[0]['name'], 'size': (cbinputRef.current.files[0]['size']/1024).toFixed(1), 'type': cbinputRef.current.files[0]['type'].split('/')[1].toUpperCase()})
        let doc_id = Date.now()
        cbusetState(prevState => ({documents: [...prevState.documents, {'name': cbinputRef.current.files[0]['name'], 'size': (cbinputRef.current.files[0]['size']/1024).toFixed(1), 'type': cbinputRef.current.files[0]['type'].split('/')[1].toUpperCase(), 'isloading': true, 'id': doc_id}]}))
        let filereader = new FileReader();
        filereader.readAsDataURL(cbinputRef.current.files[0])
        filereader.onloadend = () => {
            //cbusetState(prevState => ({...prevState, 'isloading': false, 'data': filereader.result}))
            cbusetState(prevState => ({...prevState, documents: prevState.documents.map(doc => doc.id === doc_id ? {...doc, isloading: false, data: filereader.result} : doc)}))
            //UploadDeactive()
            ArrowActive()
            cbinputRef.current.value = ''
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

    function GetModelName(id_val){
        const item = model_list.find(obj => obj.id === id_val)
        return item ? item.name : null
    }

    return(
        <div className={chattype === 'body' ? 'cb_holder' : 'cb_holder_bottom'} style={chattype === 'main' && isloadingState === true ? {justifyContent: 'end'} : {justifyContent: 'space-between'}}>
            { isloadingState === false ? (
            <>
                <div>
                    <ChatBoxUpload cbuState={cbuState} cbusetState={cbusetState} cbinputRef={cbinputRef} UploadActive={UploadActive} EmptyTextArrowDeactive={EmptyTextArrowDeactive}/>
                    <textarea className='cb_textarea' placeholder='Ask Sapling' onChange={() => CheckQuestion()} ref={cbtextareaRef} onKeyDown={(event) => PressEnter(event)} autoFocus={true}/>
                </div>
                <div className='cb_infoholder' style={chattype === 'body' ? {justifyContent: 'space-between'} : {justifyContent: 'end'}}>
                    { isgeneratingState === false ? (
                    <>
                        { chattype === 'body' ? 
                        (
                        <>
                        <div className='cb_modelholder'>
                            <div className=/*'cb_utilthink '*/'cb_model' onClick={() => {cbmodelpopupactiveState === true ? cbmodelpopupactivesetState(false) : cbmodelpopupactivesetState(true)}}>
                                <NeuralNetwork/>
                                <span>{cbmodelState['name']}</span>
                            </div>
                            {cbmodelState['type'] === 'cloud' && 
                            <>
                                <div className='cb_key' onClick={() => cbkeyboxvisiblesetState(true ? cbkeyboxvisibleState === false : false)}><Key2Icon width={23} height={23}/></div>
                                <div className='cb_keybox' style={cbkeyboxvisibleState === false ? {display: 'none'} : {display: 'flex'}}>
                                    <div className='cb_keytop'>
                                        <div className='cb_keytitle'>Add Your API Key</div>
                                        <div className='cb_keyx' onClick={() => cbkeyboxvisiblesetState(false)}><XCloseIcon/></div>
                                    </div>
                                    <div className='cb_keymain'>
                                        <input className='cb_keyinput' ref={cbkeyRef}/>
                                    </div>
                                </div>
                            </>}
                        </div>
                        <ChatBoxModelPopUp current_model={cbmodelState} isactiveState={cbmodelpopupactiveState} isactivesetState={cbmodelpopupactivesetState} changemodelState={cbmodelsetState}/>
                        </>
                        ) : <></>
                        }
                        <div className='cb_utilsholder'>
                            <div className='cb_util'>{GetModelName(modelState)}</div>
                            <div className='cb_util cb_utilactive cb_upload' onClick={() => cbinputRef.current.click()} ref={cbuploadRef}>
                                <UploadFile/>
                                <div className={'cb_uploadtext ' + (chattype === 'main' ? 'cb_uploadmain' : 'cb_uploadbody')}>Upload File</div>
                                <input type='file' className='cb_input' ref={cbinputRef} accept='application/JSON' onChange={() => UploadDocument()}/>
                            </div>
                            <div className={'cb_util ' +  ( (cbtextareaRef.current === undefined || cbtextareaRef.current.value === '') ? 'cb_utildeactive' : 'cb_utilactive')} onClick={() => SubmitQuestion()} ref={cbarrowRef}><ArrowUpload/></div>
                        </div>
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