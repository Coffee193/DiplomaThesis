import '../styling/ChatNavRenameDelete.css'
import { XCloseIcon, BlocksLoad } from '../components/svgs/UtilIcons'
import { pressKey } from './pressKeyFunc'
import { useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'

export function ChatNavRenameDelete({ cnrdState, cnrdsetState, convsetState, searchchatinputRef, SearchChat, chatlist, createConversations, linkparams }){

    const cnrdinputRef = useRef()
    const [cnrdwarningState, cnrdwarningsetState] = useState()
    const canclickbuttonRef = useRef()
    const cnrdbuttonRef = useRef()
    const navigate = useNavigate()

    function ClickButton(active){
        if(active === false){
            canclickbuttonRef.current = false
            cnrdbuttonRef.current.style.pointerEvents = 'none'
            cnrdsetState(prevState => ({...prevState, 'textbuttoninit': prevState['textbutton'], 'textbutton': <BlocksLoad/>}))
        }
        else if(active === true){
            canclickbuttonRef.current = true
            cnrdbuttonRef.current.style.pointerEvents = 'all'
            cnrdsetState(prevState => ({...prevState, 'textbutton': prevState['textbuttoninit']}))
        }
    }

    function SubmitRequest(){
        if(canclickbuttonRef.current === false){
            return
        }
        if(cnrdState['extrainfo'] === 'rename'){
            if(cnrdinputRef.current.value.length < 5){
                cnrdwarningsetState('Name must be at leat 5 characters long')
                return
            }
        }

        ClickButton(false)
        if(cnrdState['extrainfo'] === 'delete'){
            DeleteChat()
        }
        else if(cnrdState['extrainfo'] === 'rename'){
            RenameChat()
        }
    }

    async function RenameChat(){
        let request = {"id": cnrdState['id'], "v": cnrdinputRef.current.value}

        let response_status = null
        await fetch(import.meta.env.VITE_URL + 'chats/renamechat/', {
            method: 'POST',
            body: JSON.stringify(request),
            credentials: 'include',
        }).then(res => {
            response_status = res.status
            return res.json()
        }).then(data => data)
        .catch(()=> cnrdwarningsetState('Could not connect to the server'))

        ClickButton(true)
        if(response_status === 200){
            ClosePopUp()
            chatlist.current[cnrdState['index']]["name"] = request["v"]
            if(searchchatinputRef.current.value.length === 0){
                convsetState(createConversations(chatlist.current, false))
            }
            else{
                SearchChat(searchchatinputRef.current.value)
            }
        }
        else if(response_status === 401 || response_status === 403){
            navigate('/login', {state: {to: '/chat'}})
        }

    }

    async function DeleteChat(){
        let response_status = null
        let request = {"id": cnrdState['id']}
        await fetch(import.meta.env.VITE_URL + 'chats/deletechat/', {
            method: 'DELETE',
            body: JSON.stringify(request),
            credentials: 'include',
        }).then(res => {
            response_status = res.status
            return res.json()
        }).then(data => data)
        .catch(() => cnrdwarningsetState('Could not connect to the server'))

        ClickButton(true)
        if(response_status === 200){
            ClosePopUp()
            chatlist.current.splice(parseInt(cnrdState['index']), 1)
            if(searchchatinputRef.current.value.length === 0){
                convsetState(createConversations(chatlist.current, false))
            }
            else{
                SearchChat(searchchatinputRef.current.value)
            }
            if(cnrdState['id'] === linkparams.id){
                navigate('/chat')
            }
        }
        else if(response_status === 401 || response_status === 403){
            navigate('/login', {state: {to: '/chat'}})
        }
    }

    function ClosePopUp(){
        cnrdsetState({'visible': false})
        cnrdwarningsetState('')
    }

    return(
        <>
        <div className='cnrd_holder' style={cnrdState['visible'] === false ? {opacity: '0', pointerEvents: 'none', transform: 'scale(0.8)'} : {opacity: '1',pointerEvents: 'all', transform: 'scale(1)'}}>
            <div className='cnrd_header'>
                <div className={'cnrd_xclose ' + cnrdState['closeclass']} onClick={() => ClosePopUp()}><XCloseIcon/></div>
                <div className={cnrdState['titleclass']}>{cnrdState['title']}</div>
            </div>
            <div className='cnrd_body'>
                <div className='cnrd_text'>{cnrdState['text']}
                    <span>{cnrdState['convname']}</span>
                </div>
                {cnrdState['extrainfo'] === 'rename' ? (
                    <input className='cnrd_input' maxLength='50' autoFocus={true} onKeyDown={(event) => pressKey(event, SubmitRequest, undefined, undefined, undefined)} ref={cnrdinputRef}/>
                ): ('')}
                <div className='cnrd_warning' onClick={() => cnrdwarningsetState('')}>{cnrdwarningState}</div>
            </div>
            <div className='cnrd_utilholder'>
                <div className='buttonactive cnrd_util cnrd_cancel' onClick={() => ClosePopUp()}>Cancel</div>
                <div className={'cnrd_util ' + cnrdState['buttonclass']} onClick={() => SubmitRequest()} ref={cnrdbuttonRef} style={cnrdState['visible'] === false ? {pointerEvents: 'none'} : {pointerEvents: 'all'}}>{cnrdState['textbutton']}</div>
            </div>
        </div>
        <div className='cnrd_bg' style={cnrdState['visible'] === false ? {opacity: '0', pointerEvents: 'none'} : {opacity: '1', pointerEvents: 'all'}} onClick={() => ClosePopUp()}/>
        </>
    )
}