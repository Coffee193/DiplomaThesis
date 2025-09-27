import '../styling/ChatNav.css'
import { ChatBubble, SearchIcon, XCloseIcon, DotsIcon, PencilIcon, TrashIcon } from '../components/svgs/UtilIcons'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { useState, useRef, useEffect } from 'react'

    /*export function createConversations(arr, conv_to_date = true){
        let monthyear = []
        let convfinalstate = []

        for(let i=arr.length - 1; i>=0; i--){
            if(conv_to_date === true){
                arr[i]['date_created'] = new Date(arr[i]['date_created'] * 1000)
            }
            let monthyearstr = getMonthYearString(arr[i]['date_created'])
            if(monthyear.includes(monthyearstr) === false){
                monthyear.push(monthyearstr)
                convfinalstate.push(<div className='cnav_info_date'>{monthyearstr}</div>)
            }
            convfinalstate.push(
                <div className='cnav_info_chat_holder'>
                    <div className='cnav_info_chat'>
                        <div className='cnav_info_chat_title'>{arr[i]['name']}</div>
                        <div className='cnav_info_chat_options' onClick={(e) => ChatOptionsPopUp(e.target)}><DotsIcon/></div>
                    </div>
                </div>)
        }

        return convfinalstate

        function getMonthYearString(response_date){
        let response_date_month = response_date.getMonth() + 1
        let append_val = ' '
        if(response_date_month < 9){
            append_val = ' 0'
        }
        return response_date.getFullYear().toString() + append_val + response_date_month.toString()
    }
    }*/

export function ChatNav({convState, convsetState, chatlist, newconv}){

    const [searchState, searchsetState] = useState('')
    const XCloseRef = useRef()
    const SearchIconRef = useRef()
    const [chatoptionsstate, chatoptionssetState] = useState('0')
    const ChatOptionsRef = useRef()
    const RemovePopUpRef = useRef()
    const navigate = useNavigate()
    const [chatoptionsnameState, chatoptionsnamesetState] = useState()
    const chatoptionsidRef = useRef()
    const renameRef = useRef()
    const deleteRef = useRef()
    const chatoptionsbackRef = useRef()
    const renameinputRef = useRef()
    const renameclickRef = useRef()
    const searchchatinputRef = useRef()
    const chatclickidRef = useRef(null)
    const linkparams = useParams()
    /* [prev_selected, curr_selected] */

    function SearchValueChange(value){
        searchsetState(value)
        if(value !== ''){
            XCloseRef.current.style.opacity = '1'
            XCloseRef.current.style.pointerEvents = 'all'
        }
        else{
            XCloseRef.current.style.opacity = '0'
            XCloseRef.current.style.pointerEvents = 'none'
        }
        SearchChat(value)
    }

    function ChatOptionsPopUp(element){
        /*console.log(element.id)*/
        let element_position_top_float = element.getBoundingClientRect().top.toFixed(1) - 39
        if(element_position_top_float + ChatOptionsRef.current.offsetHeight + document.getElementsByClassName('nav_all_holder')[0].offsetHeight >= window.innerHeight){
            element_position_top_float = (element_position_top_float - ChatOptionsRef.current.offsetHeight - 39).toFixed(1)
        }
        let element_position_top = String(element_position_top_float) + 'px'
        if( (element_position_top === chatoptionsstate) && (ChatOptionsRef.current.style.opacity === '1')){
            ChatPopUpAppearance(false)
            return
        }
        ChatPopUpAppearance(true)
        chatoptionssetState(String(element_position_top))
    }

    function ChatPopUpAppearance(show){
        if(show === false){
            ChatOptionsRef.current.style.opacity = '0'
            ChatOptionsRef.current.style.pointerEvents = 'none'
            ChatOptionsRef.current.style.transform = 'scale(0.8, 0.8)'
            RemovePopUpRef.current.style.pointerEvents = 'none'
        }
        else if(show === true){
            ChatOptionsRef.current.style.opacity = '1'
            ChatOptionsRef.current.style.pointerEvents = 'all'
            ChatOptionsRef.current.style.transform = 'scale(1, 1)'
            RemovePopUpRef.current.style.pointerEvents = 'all'
        }
    }

    useEffect(() => {
        getOrders()
    }, [])

    useEffect(() => {
        if(newconv !== undefined){
            let convfinalstate = createConversations(chatlist.current, false)
            convsetState(convfinalstate)
        }
    }, [newconv])

    async function getOrders(){
        if(linkparams.id !== undefined){
            chatclickidRef.current = linkparams.id
        }
        let response_status = null
        let response = await fetch('http://127.0.0.1:8000/chats/getchats/', {
            method: 'GET',
            credentials: 'include',
        }).then(res => {
            response_status = res.status
            return res.json()}).then(data => data)
            .catch(() => {response_status = 'failed'})

        if(response_status === 200){
            console.log(response)
            let convfinalstate = createConversations(response)

            chatlist.current = response
            convsetState(convfinalstate)
        }
        else if(response_status === 401 || response_status === 403){
            navigate('/login')
        }
    }

    function createConversations(arr, conv_to_date = true, indexset = null){
        let monthyear = []
        let convfinalstate = []
        let indexval = null
        let chatselectval = null

        for(let i=arr.length - 1; i>=0; i--){
            if(conv_to_date === true){
                arr[i]['date_created'] = new Date(arr[i]['date_created'] * 1000)
            }
            let monthyearstr = getMonthYearString(arr[i]['date_created'])
            if(monthyear.includes(monthyearstr) === false){
                monthyear.push(monthyearstr)
                convfinalstate.push(<div className='cnav_info_date'>{monthyearstr}</div>)
            }
            if(indexset === null){
                indexval = i
            }
            else{
                indexval = indexset[i]
            }
            
            if(arr[i]['_id'] === chatclickidRef.current){
                chatselectval = 'cnav_info_chat_select'
            }
            else{
                chatselectval = 'cnav_info_chat_notselect'
            }
            convfinalstate.push(
                <div className='cnav_info_chat_holder'>
                    <div className={'cnav_info_chat ' + chatselectval} id={'cnav_chat_' + i}>
                        <div className='cnav_info_chat_title' onClick={() => ClickChat(arr[i]['_id'])}>{arr[i]['name']}</div>
                        <div className='cnav_info_chat_options' onClick={(e) => {ChatOptionsPopUp(e.target)
                                                                                 chatoptionsidRef.current = [e.target.dataset.idval, e.target.dataset.index]
                                                                                 chatoptionsnamesetState(e.target.dataset.name)
                        }} data-idval={arr[i]['_id']} data-name={arr[i]['name']} data-index={indexval}><DotsIcon/></div>
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
        <div className='cnav_holder'>
            
            <div className='cnav_remove_popup' onClick={()=>{ChatPopUpAppearance(false)}} ref={RemovePopUpRef}/>
            <div className='cnav_utils'>
                    <div onClick={()=>{ClickChat(null)}}>
                        <div className='cnav_util_item'>
                            <ChatBubble width={25} height={25} strokeWidth={0.5} viewBox={'-1 -1 18 18'}/><span>New Chat</span>
                        </div>
                    </div>
                <div>
                    <div className='cnav_util_search_holder'>
                        <div ref={SearchIconRef} className='transition_add'><SearchIcon/></div>
                        <input placeholder='Search Chat' onChange={(e) => SearchValueChange(e.target.value)} onFocus={() => SearchIconRef.current.classList.add('color_blue_hover_evenmore')} onBlur={() => SearchIconRef.current.classList.remove('color_blue_hover_evenmore')} value={searchState} ref={searchchatinputRef}/>
                        <div className='cnav_util_xclose' ref={XCloseRef} onClick={() => SearchValueChange('')}><XCloseIcon/></div>
                    </div>
                </div>
            </div>
            <div className='cnav_info'>
                <div className='cnav_info_text'>
                    <div onClick={() => console.log(chatlist.current)}>Chats</div>
                    {/*<div className='cnav_info_backline'/>*/}
                    {/*<div className='cnav_info_sortby'>

                    </div>*/}
                </div>
                <div className='cnav_info_container'>
                    {convState}
                </div>
            </div>
            <div className='cnav_info_chat_options_popup' id='chat_options_popup' ref={ChatOptionsRef} style={{top: chatoptionsstate}}>
                <div onClick={() => {ChatOptionAppearClose('rename', 'show')
                                     ChatPopUpAppearance(false)
                }}><PencilIcon width={24} height={24}/><span>Rename</span></div>
                <div onClick={() => {ChatOptionAppearClose('delete', 'show')
                                     ChatPopUpAppearance(false)
                }}><TrashIcon width={24} height={24}/><span>Delete</span></div>
            </div>
            
            
            
        </div>

        <div className='cnav_info_chat_options_main' ref={renameRef}>
            <div className='cnav_info_chat_options_header'>
                <div className='cnav_info_chat_options_close close_rename' onClick={() => ChatOptionAppearClose('rename', 'hide')}><XCloseIcon/></div>
                <div className='cnav_info_chat_options_title title_rename'>Rename Chat</div>
            </div>
            <div className='cnav_info_chat_options_body'>
                <div className='cnav_info_chat_options_text'>This will rename
                    <span className='cnav_info_chat_options_text_bold'> {chatoptionsnameState}</span>
                </div>
                <input className='cnav_info_chat_options_input' maxlength="50" ref={renameinputRef} onChange={() => ChangeRename()}/>
            </div>
            <div className='cnav_info_chat_options_click_holder'>
                <div className='cnav_info_chat_options_click cnav_info_cancel' onClick={() => {ChatOptionAppearClose('rename', 'hide')
                    renameinputRef.current.value = ''
                }}>Cancel</div>
                <div className='cnav_info_chat_options_click cnav_info_rename rename_block' onClick={() => RenameChat()} ref={renameclickRef}>Rename</div>
            </div>
        </div>
        <div className='cnav_info_chat_options_main' ref={deleteRef}>
            <div className='cnav_info_chat_options_header'>
                <div className='cnav_info_chat_options_close close_delete' onClick={() => ChatOptionAppearClose('delete', 'hide')}><XCloseIcon/></div>
                <div className='cnav_info_chat_options_title title_delete'>Delete Chat</div>
            </div>
            <div className='cnav_info_chat_options_body'>
                <div className='cnav_info_chat_options_text'>This will delete
                    <span className='cnav_info_chat_options_text_bold'> {chatoptionsnameState}</span>
                </div>
            </div>
            <div className='cnav_info_chat_options_click_holder'>
                <div className='cnav_info_chat_options_click cnav_info_cancel' onClick={() => ChatOptionAppearClose('delete', 'hide')}>Cancel</div>
                <div className='cnav_info_chat_options_click cnav_info_delete' onClick={() => DeleteChat()}>Delete</div>
            </div>
        </div>
        
        <div className='cnav_info_chat_options_back' ref={chatoptionsbackRef}
        onClick={() => {
            ChatOptionAppearClose('rename', 'hide')
            ChatOptionAppearClose('delete', 'hide')
        }}/>

        </>
    )
}