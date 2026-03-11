import '../styling/ChatNav.css'
import { ChatBubble, DotsIcon } from '../components/svgs/UtilIcons'
import { useNavigate } from 'react-router-dom'
import { useState, useRef, useEffect } from 'react'
import { ChatNavUtils } from './ChatNavUtils'

export function ChatNav({convState, convsetState, chatlist, isloadingState, isloadingsetState, linkparams}){

    const navigate = useNavigate()
    const chatclickRef = useRef(null) /* id of chat to be renamed/deleted */
    const searchchatinputRef = useRef()
    const [cnpState, cnpsetState] = useState({'visible': false, 'id': null})
    /* Must update entire Conversations Nav because if I try to do it with Ref and removing/adding classes then there will be
    problems on the screen (the color will be cut off in the middle etc) */

    function ChatPopUp(element){
        if(chatclickRef.current === element.dataset.idval){
            cnpsetState({'visible': false, 'id': null})
            chatclickRef.current = null
            return
        }

        let navdim = parseInt(window.getComputedStyle(document.getElementsByClassName('n_allholder')[0]).getPropertyValue('--nav-height').slice(0, 2))
        
        let element_position_top_float = element.getBoundingClientRect().top.toFixed(1) - navdim - 185

        chatclickRef.current = element.dataset.idval
        cnpsetState({'visible': true, 'top': String(element_position_top_float) + 'px', 'name': element.dataset.name, 'id': element.dataset.idval, 'index': element.dataset.index})
    }

    useEffect(() => {
        if(chatlist.current === undefined){
            getOrders()
        }
        else{
            convsetState(createConversations(chatlist.current, false))
        }
    }, [linkparams])

    async function getOrders(){
        if(document.cookie.includes('userinfo=') === false){
            navigate('/login', {state: {to: '/chat'}})
            return
        }

        let response_status = null
        let response = await fetch(import.meta.env.VITE_URL + 'chats/getchats/', {
            method: 'GET',
            credentials: 'include',
        }).then(res => {
            response_status = res.status
            return res.json()}).then(data => data)
            .catch(() => {})

        if(response_status === 200){
            chatlist.current = response
            convsetState(createConversations(response))
            isloadingsetState(false)
        }
        else if(response_status === 401 || response_status === 403){
            navigate('/login', {state: {to: '/chat', expired: true}})
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
                        <div className='cn_info_chat_bg' onClick={() => isselected === false ? ClickChat(arr[i]['_id']) : ''}/>
                        <div className='cn_info_chat_title'>{arr[i]['name']}</div>
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


    function ClickChat(idval){
        if(idval !== null){
            navigate('/chat/' + idval + '/')
        }
        else{
            navigate('/chat')
        }
        convsetState(createConversations(chatlist.current, false))
        searchchatinputRef.current.value = ''
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
                <div onClick={()=> ClickChat(null)}>
                    <div className='cn_util_item'>
                        <ChatBubble width={25} height={25} strokeWidth={0.5} viewBox={'-1 -1 18 18'}/><span>New Chat</span>
                    </div>
                </div>
                <div>
                    <ChatNavUtils chatclickRef={chatclickRef} convsetState={convsetState} chatlist={chatlist} createConversations={createConversations} cnpState={cnpState} cnpsetState={cnpsetState} linkparams={linkparams} searchchatinputRef={searchchatinputRef}/>
                </div>
                </>
                )
                }
            </div>
            <div className='cn_info'>
                <div className='cn_info_text'>
                    <div>Chats</div>
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
        </div>
        </>
    )
}