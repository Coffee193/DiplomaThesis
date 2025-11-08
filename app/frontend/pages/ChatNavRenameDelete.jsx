import '../styling/ChatNavRenameDelete.css'
import { XCloseIcon } from '../components/svgs/UtilIcons'
import { pressKey } from './pressKeyFunc'
import { useRef, useState } from 'react'

export function ChatNavRenameDelete({ cnrdState, cnrdsetState }){

    const cnrdinputRef = useRef()
    const [cnrdwarningState, cnrdwarningsetState] = useState()

    async function RenameChat(){
        if(renameinputRef.current.value.length <= 5){
            cnrdwarningsetState('Name must be at leat 5 characters long')
            return
        }
        let request = {"id": cnrdState['id'], "v": cnrdinputRef.current.value}

        let response_status = null
        await fetch(import.meta.env.VITE_URL + 'chats/renamechats/', {
            method: 'POST',
            body: JSON.stringify(request),
            credentials: 'include',
        }).then(res => {
            response_status = res.status
            return res.json()
        }).then(data => data)
        .catch(()=> cnrdwarningsetState('Could not connect to the server'))

        if(response_status === 200){
            ChatOptionAppearClose('rename', 'hide')
            cnrdsetState({'visible': false})
            chatlist.current[cnrdState['index']]["name"] = request["v"]
            if(searchchatinputRef.current.value.length === 0){
                let convfinalstate = createConversations(chatlist.current, false)
                convsetState(convfinalstate)
            }
            else{
                SearchChat(searchchatinputRef.current.value)
            }
        }
        else if(response_status === 401 || response_status === 403){
            navigate('/login', {state: {to: '/chat'}})
        }

    }

    return(
        <>
        <div className='cnrd_holder' style={cnrdState['visible'] === false ? {opacity: '0', pointerEvents: 'none', transform: 'scale(0.8)'} : {opacity: '1',pointerEvents: 'all', transform: 'scale(1)'}}>
            <div className='cnrd_header'>
                <div className={'cnrd_xclose ' + cnrdState['closeclass']} onClick={() => cnrdsetState({'visible': false})}><XCloseIcon/></div>
                <div className={cnrdState['titleclass']}>{cnrdState['title']}</div>
            </div>
            <div className='cnrd_body'>
                <div className='cnrd_text'>{cnrdState['text']}
                    <span>{cnrdState['convname']}</span>
                </div>
                {cnrdState['visible'] === false ? ('') : (
                    <input className='cnrd_input' maxLength='50' autoFocus={true} onKeyDown={(event) => pressKey(event, )} ref={cnrdinputRef}/>
                )}
                <div className='cnrd_warning'>{cnrdwarningState}</div>
            </div>
            <div className='cnrd_utilholder'>
                <div className='cnrd_util cnrd_cancel' onClick={() => cnrdsetState({'visible': false})}>Cancel</div>
                <div className={'cnrd_util ' + cnrdState['buttonclass']}>{cnrdState['buttontext']}</div>
            </div>
        </div>
        <div className='cnrd_bg' style={cnrdState['visible'] === false ? {opacity: '0', pointerEvents: 'none'} : {opacity: '1', pointerEvents: 'all'}} onClick={() => cnrdsetState({'visible': false})}/>
        </>
    )
}