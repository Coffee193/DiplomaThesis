import '../styling/ChatNav.css'
import { ChatBubble, SearchIcon, XCloseIcon, DotsIcon, PencilIcon, TrashIcon } from '../components/svgs/UtilIcons'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { useState, useRef, useEffect } from 'react'
import { ChatNavPopUp } from './ChatNavPopUp'
import { ChatNavSearch } from './ChatNavSearch'
import { ChatNavRenameDelete } from './ChatNavRenameDelete'

export function ChatNav({convState, convsetState, chatlist, newconv, isloadingState, isloadingsetState}){

    const navigate = useNavigate()
    const chatlistidRef = useRef([null, null])
    const renameRef = useRef()
    const deleteRef = useRef()
    const chatoptionsbackRef = useRef()
    const renameinputRef = useRef()
    const renameclickRef = useRef()
    const searchchatinputRef = useRef()
    const linkparams = useParams()
    const [cnpState, cnpsetState] = useState({'visible': false})
    const [cnrdState, cnrdsetState] = useState({'visible': false})
    /* Must update entire Conversations Nav because if I try to do it with Ref and removing/adding classes then there will be
    problems on the screen (the color will be cut off in the middle etc) */

    function ChatPopUp(element){
        if(chatlistidRef.current[0] === element.dataset.idval){
            cnpsetState({'visible': false})
            chatlistidRef.current = [null, null]
            return
        }

        //let popupdim = parseInt(window.getComputedStyle(document.getElementsByClassName('cnp')[0]).getPropertyValue('--chatnav-dim-popup').slice(0, 2))
        let navdim = parseInt(window.getComputedStyle(document.getElementsByClassName('nav_all_holder')[0]).getPropertyValue('--nav-height').slice(0, 2))
        
        let element_position_top_float = element.getBoundingClientRect().top.toFixed(1) - navdim - 185

        chatlistidRef.current = [element.dataset.idval, element.dataset.name]
        cnpsetState({'visible': true, 'top': String(element_position_top_float) + 'px', 'name': element.dataset.name})
    }

    useEffect(() => {
        getOrders()
    }, [])

    /*useEffect(() => {
        if(newconv !== undefined){
            let convfinalstate = createConversations(chatlist.current, false)
            convsetState(convfinalstate)
        }
    }, [newconv])*/

    async function getOrders(){
        let response_status = null
        let response = await fetch(import.meta.env.VITE_URL + 'chats/getchats/', {
            method: 'GET',
            credentials: 'include',
        }).then(res => {
            response_status = res.status
            return res.json()}).then(data => data)
            .catch(() => {})

        if(response_status === 200){
            console.log(response)
            chatlist.current = response
            convsetState(createConversations(response))
            isloadingsetState(false)
        }
        else if(response_status === 401 || response_status === 403){
            navigate('/login', {state: '/chat'})
        }
    }

    function createConversations(arr, conv_to_date = true, indexset = null){
        let monthyear = []
        let convfinalstate = []
        let indexval = null

        for(let i=arr.length - 1; i>=0; i--){
            if(conv_to_date === true){
                arr[i]['date_created'] = new Date(arr[i]['date_created'] * 1000)
            }
            let monthyearstr = getMonthYearString(arr[i]['date_created'])
            if(monthyear.includes(monthyearstr) === false){
                monthyear.push(monthyearstr)
                convfinalstate.push(<div className='cn_info_date'>{monthyearstr}</div>)
            }
            if(indexset === null){
                indexval = i
            }
            else{
                indexval = indexset[i]
            }
            
            let isselected = arr[i]['_id'] === linkparams.id

            convfinalstate.push(
                <div className='cn_info_chat_holder'>
                    <div className={'cn_info_chat ' + (isselected === true ? 'cn_info_chat_select' : 'cn_info_chat_notselect')} id={'cnav_chat_' + i}>
                        <div className='cn_info_chat_title' onClick={() => isselected === false ? ClickChat(arr[i]['_id']) : ''}>{arr[i]['name']}</div>
                        <div className='cn_info_chat_options' onClick={(e) => ChatPopUp(e.target)} data-idval={arr[i]['_id']} data-name={arr[i]['name']} data-index={indexval}><DotsIcon/></div>
                    </div>
                </div>)
        }

        return convfinalstate
    }

    function getMonthYearString(response_date){
        let response_date_month = response_date.getMonth() + 1
        let append_val = ' '
        if(response_date_month < 9){
            append_val = ' 0'
        }
        return response_date.getFullYear().toString() + append_val + response_date_month.toString()
    }
    
    function ChatOptionAppearClose(popup, value){
        /* popup = 'rename' or 'delete' 
           value = 'show' or 'hide'*/
        if(popup === 'rename'){
            if(value === 'show'){
                renameRef.current.style.opacity = '1'
                chatoptionsbackRef.current.style.opacity = '1'
                renameRef.current.style.pointerEvents = 'all'
                chatoptionsbackRef.current.style.pointerEvents = 'all'
                renameRef.current.style.transform = 'scale(1, 1)'
            }
            else if(value === 'hide'){
                renameRef.current.style.opacity = '0'
                chatoptionsbackRef.current.style.opacity = '0'
                renameRef.current.style.pointerEvents = 'none'
                chatoptionsbackRef.current.style.pointerEvents = 'none'
                renameRef.current.style.transform = 'scale(0.8, 0.8)'
            }
        }
        else if(popup === 'delete'){
            if(value === 'show'){
                deleteRef.current.style.opacity = '1'
                chatoptionsbackRef.current.style.opacity = '1'
                deleteRef.current.style.pointerEvents = 'all'
                chatoptionsbackRef.current.style.pointerEvents = 'all'
                deleteRef.current.style.transform = 'scale(1, 1)'
            }
            else if(value === 'hide'){
                deleteRef.current.style.opacity = '0'
                chatoptionsbackRef.current.style.opacity = '0'
                deleteRef.current.style.pointerEvents = 'none'
                chatoptionsbackRef.current.style.pointerEvents = 'none'
                deleteRef.current.style.transform = 'scale(0.8, 0.8)'
            }
        }
    }

    async function DeleteChat(){
        let response_status = null
        let request = {"_id": chatoptionsidRef.current[0]}
        let response = await fetch('http://127.0.0.1:8000/chats/deletechats/', {
            method: 'DELETE',
            body: JSON.stringify(request),
            credentials: 'include',
        }).then(res => {
            response_status = res.status
            return res.json()
        }).then(data => data)
        .catch(() => {response_status = 'failed'})

        if(response_status === 200){
            ChatOptionAppearClose('delete', 'hide')
            chatlist.current.splice(parseInt(chatoptionsidRef.current[1]), 1)
            if(searchchatinputRef.current.value.length === 0){
                let convfinalstate = createConversations(chatlist.current, false)
                convsetState(convfinalstate)
            }
            else{
                SearchChat(searchchatinputRef.current.value)
            }
        }
        else if(response_status === 401 || response_status === 403){
            navigate('/login')
        }
    }

    async function RenameChat(){
        if(renameinputRef.current.value.length <= 5){
            return
        }
        let request = {"_id": chatoptionsidRef.current[0], "rename": renameinputRef.current.value}
        console.timeLog(request)
        let response_status = null
        let response = await fetch('http://127.0.0.1:8000/chats/renamechats/', {
            method: 'POST',
            body: JSON.stringify(request),
            credentials: 'include',
        }).then(res => {
            response_status = res.status
            return res.json()
        }).then(data => data)
        .catch(()=> {response_status = 'failed'})

        if(response_status === 200){
            ChatOptionAppearClose('rename', 'hide')
            renameinputRef.current.value = ''
            chatlist.current[chatoptionsidRef.current[1]]["name"] = request["rename"]
            if(searchchatinputRef.current.value.length === 0){
                let convfinalstate = createConversations(chatlist.current, false)
                convsetState(convfinalstate)
            }
            else{
                SearchChat(searchchatinputRef.current.value)
            }
        }
        else if(response_status === 401 || response_status === 403){
            navigate('/login')
        }

    }

    function ChangeRename(){
        if(renameinputRef.current.value.length > 5){
            renameclickRef.current.classList.remove('rename_block')
        }
        else{
            renameclickRef.current.classList.add('rename_block')
        }
    }

    function SearchChat(value){
        if(value.length !== 0){
            let templist = []
            let indexlist = []
            for(let i=0; i<chatlist.current.length; i++){
                if(chatlist.current[i]["name"].toLowerCase().includes(value.toLowerCase())){
                    templist.push(chatlist.current[i])
                    indexlist.push(i)
                }
            }
            let convfinalstate = createConversations(templist, false, indexlist)
            convsetState(convfinalstate)
        }
        else{
            let convfinalstate = createConversations(chatlist.current, false)
            convsetState(convfinalstate)
        }
    }

    function ClickChat(idval){
        if(chatclickidRef.current !== idval){
            chatclickidRef.current = idval
        }
        else{
            return
        }
        let convfinalstate = createConversations(chatlist.current, false)
        convsetState(convfinalstate)
        if(idval !== null){
            navigate('/chat/' + idval + '/')
        }
        else{
            navigate('/chat')
        }
    }

    return(
        <>
        <div className='cn_holder'>
            <div className='cn_utils'>
                {isloadingState === true ? (
                    <>
                        <div className='loading_box loading_blue' style={{width: '75%', height: '42px'}}/>
                        <div className='loading_box loading_blue' style={{width: '50%', height: '32px'}}/>
                    </>
                ) : (
                <>
                <div onClick={()=>{console.log('i was clicked'); ClickChat(null)}}>
                    <div className='cn_util_item'>
                        <ChatBubble width={25} height={25} strokeWidth={0.5} viewBox={'-1 -1 18 18'}/><span>New Chat</span>
                    </div>
                </div>
                <div>
                    <ChatNavSearch convsetState={convsetState} chatlist={chatlist} createConversations={createConversations}/>
                </div>
                </>
                )
                }
            </div>
            <div className='cn_info'>
                <div className='cn_info_text'>
                    <div onClick={() => console.log(chatlist.current)}>Chats</div>
                </div>
                <div className='cn_info_container'>
                    {isloadingState === true ? (
                        <>
                            <div className='loading_box loading_blue'/>
                            <div className='loading_box loading_blue'/>
                            <div className='loading_box loading_blue' style={{width: '80%'}}/>
                        </>
                        ) : (convState) }
                </div>
            </div>
        <ChatNavPopUp cnpState={cnpState} cnpsetState={cnpsetState}/>
        </div>
        <ChatNavRenameDelete cnrdState={cnrdState} cnrdsetState={cnrdsetState}/>
        </>
    )
}