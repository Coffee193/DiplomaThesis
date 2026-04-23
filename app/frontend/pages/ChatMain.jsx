import '../styling/ChatMain.css'
import { useRef, useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ChatBox } from './ChatBox'
import { ChatBoxUpload } from './ChatBoxUpload'
import { BlocksLoad, DotIcon, ArrowDownIcon, DotsIcon } from '../components/svgs/UtilIcons'

export function ChatMain({ chatlist, chatnavloadingState, linkparams, chatnavsetState }){

    const navigate = useNavigate()
    const [isloadingState, isloadingsetState] = useState(true)
    const [convState, convsetState] = useState()
    const cmchatRef = useRef()
    const [isgeneratingState, isgeneratingsetState] = useState(false)
    const convstreamgeneratingRef = useRef(new Set([]))
    const [thinkState, thinksetState] = useState(false)

    useEffect(() => {
        if(chatnavloadingState === false){
            GetConversation()
        }
    }, [linkparams.id, chatnavloadingState])


    async function GetConversation(){
        let generateTitle = null
        let response_status = null
        let response = await fetch(import.meta.env.VITE_URL + 'chats/getconversation/' + linkparams.id + '/', {
            method: 'GET',
            credentials: 'include',
        }).then(res => {
            response_status = res.status
            return res.json()
        }).then(data => data)
        .catch(() => {})
        
        if(response['c'].length === 0){
            generateTitle = chatlist.current.map((e) => e["_id"]).indexOf(linkparams.id)
        }

        if(response_status === 200){
            let conv_vals = []

            if('g' in response){
                isgeneratingsetState(true)
                conv_vals.push(
                        <div className='cm_chatbox cb_answerload'>
                            <BlocksLoad/>
                        </div>,
                        <div className='cm_chatuser'>
                            {response["g"]["u"] !== undefined ? <ChatBoxUpload cbuState={{'visible': true, 'inchat': true, 'name': response["g"]["u"]["name"], 'type': response["g"]["u"]["name"].split('.')[1].toUpperCase(), 'size': response["g"]["u"]["size"], 'link': linkparams.id, 'id': response["g"]["u"]["id"]}}/> : null}
                            {response["g"]["q"] !== "" ?
                            <div className='cm_chatbox cm_boxuser'>
                                {response["g"]["q"]}
                            </div> : null
                            }
                        </div>
                )
            }

            for(let i=response['c'].length - 1; i>=0; i--){
                conv_vals.push(
                    <>
                        <div className='cm_chatbox'>
                            {CreateInfoBlock(AddStreamBold(response["c"][i]["a"]), response["c"][i]["i"], response["c"][i]["s"])}
                        </div>
                        <div className='cm_chatuser'>
                            {response["c"][i]["d"] !== undefined ? <ChatBoxUpload cbuState={{'visible': true, 'inchat': true, 'name': response["c"][i]["d"]["name"], 'type': response["c"][i]["d"]["name"].split('.')[1].toUpperCase(), 'size': response["c"][i]["d"]["size"], 'id': response["c"][i]["d"]["id"], 'link': linkparams.id}}/> : null}
                            {response["c"][i]["q"] !== undefined ?
                            <div className='cm_chatbox cm_boxuser'>
                                {response["c"][i]["q"]}
                            </div> : null
                            }
                        </div>
                    </>
                )
            }
            
            convsetState(conv_vals)
            isloadingsetState(false)
            thinksetState(response['t'])

            if('g' in response){
                if(convstreamgeneratingRef.current.has(linkparams.id) === false){
                    ResumeAnswerStream(generateTitle)
                }
            }
            else{
                isgeneratingsetState(false)
            }
        }
        else if(response_status === 401 || response_status === 403){
            navigate('/login', {state: {to: '/chat/' + linkparams.id + '/', expired: true}})
        }

    }

    function CreateInfoBlock(data, info, search){
        if(info !== undefined){
            if(data.length === 1){
                data = data[0].split(/(\(DATA\))/)
            }
            for(let i=1; i<data.length; i++){
                if(data[i] === "(DATA)"){
                    data[i] =
                    <div className='cm_infoboxholder'>
                        <div className = {Object.keys(info[0]).length > 2 && (search === 'jobs' || search === 'tasksuitableresources') ? 'cm_infobox cm_infoboxgap': 'cm_infobox'}>
                            {CreateBlock(info, search)}
                        </div>
                    </div> 
                }
            }
        }
        return data
    }

    function CreateBlock(info, search){
        if(search == 'jobs'){
            return CreateJobBlock(info)
        }
        else if(search === 'tasks'){
            return CreateTasksBlock(info)
        }
        else if(search === 'tasksuitableresources'){
            return CreateTasksuitableresourceBlock(info)
        }
        else if(search === 'tasksprecedenceconstraints'){
            return CreateTaskprecedenceconstraintBlock(info)
        }
        else if(search === 'resources'){
            return CreateResourceBlock(info)
        }
    }

    function CreateTasksBlock(info){
        let list_out = []
        for(let i=0; i<info.length; i++){
            if(info[i]['name'] === undefined){
                list_out.push(
                <div className='cm_infoblock'>
                    <div className = 'cm_infotask'>ID: {info[i]['id']}</div>
                </div>)
            }
            else{
                list_out.push(
                <div className='cm_infoblock'>
                    <div className = 'cm_infoflex'>
                        <DotIcon/> ID: {info[i]['id']}
                        <div className='cm_infobg'>
                            ({info[i]['name']})
                        </div>
                    </div>
                </div>)
            }
        }
        return list_out
    }

    function NumberToShortMonthName(num){
        const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

        return months[num - 1]; // because arrays are 0-based

    }

    function BlockDateToStr(date, withtime = false){
        if(withtime === false){
            return date['day'] + '  ' + NumberToShortMonthName(date['month']) + '  ' + date['year']
        }
        else{
            return date['day'] + '  ' + NumberToShortMonthName(date['month']) + '  ' + date['year'] + '  ' + String(date['hour']).padStart(2, '0') + ':' + String(date['minute']).padStart(2, '0')
        }
    }

    function CreateJobBlock(info){
        let list_out = []
        for(let i=0; i<info.length; i++){
            let extra_info = []
            
            if("name" in info[i]){
                extra_info.push(
                    <div className = 'cm_infoleft cm_infoflex'>
                        <DotIcon/> <div className='cm_infopush'>Name:</div> <div className='cm_infoweak'>{info[i]['name']}</div>
                    </div>
                )
            }
            if("arrivaldate" in info[i]){
                extra_info.push(
                    <div className = 'cm_infoleft cm_infoflex'>
                        <DotIcon/> <div className='cm_infopush'>Arrival Date:</div> <div className='cm_infoweak'>{BlockDateToStr(info[i]['arrivaldate'])}</div>
                    </div>
                )
            }
            if("duedate" in info[i]){
                extra_info.push(
                    <div className = 'cm_infoleft cm_infoflex'>
                        <DotIcon/> <div className='cm_infopush'>Due Date:</div> <div className='cm_infoweak'>{BlockDateToStr(info[i]['duedate'])}</div>
                    </div>
                )
            }
            if("task" in info[i]){
                extra_info.push(
                    <div className = 'cm_infoleft'>
                        <div className = 'cm_infoflex'>
                            <DotIcon/> <div className='cm_infopush'>Task IDs:</div>
                        </div>
                        <div>
                            {info[i]["task"].map((id, index) => (
                                <div className='cm_infoweak cm_infoleftbig'>{id}</div>
                            ))}
                        </div>
                    </div>
                )
            }
            list_out.push(
                <div className='cm_infoblock'>
                    <div className = 'cm_infoflex'>
                        <ArrowDownIcon width={16} height={16} style={{transform: 'rotate(-90deg)'}}/> Job ID: 
                        <div className='cm_infobg'>
                            {info[i]['id']}
                        </div>
                    </div>
                    {extra_info}
                </div>
            )
        }
        return list_out
    }

    function CreateTasksuitableresourceBlock(info){
        let list_out = []
        for(let i=0; i<info.length; i++){
            list_out.push(
                <div className='cm_infoblock'>
                    <div className = 'cm_infoflex'>
                        <ArrowDownIcon width={16} height={16} style={{transform: 'rotate(-90deg)'}}/> Resource ID: {info[i]['resource']['id']}
                        {"name" in info[i]['resource'] ? (<div className='cm_infobg'>
                            {info[i]['resource']['name']}
                        </div>) : (<></>)}
                    </div>
                    {info[i]["tasks"].map((x, index) => (
                    <div className='cm_infoblock'>
                        <div className = 'cm_infoleft cm_infoflex'>
                            <DotIcon/> Task ID: {x.id} {'name' in x ? <div className='cm_infobg'>{x.name}</div> : <></>}
                        </div>
                        {'operation_time' in x ? <div className='cm_infoleftmid cm_infoflex'>Operation Time: <div className='cm_infoweak cm_infoblockmid'>{x.operation_time}</div></div> : <></>}
                    </div>
                    ))}
                </div>
            )
        }
        return list_out
    }

    function CreateTaskprecedenceconstraintBlock(info){
        let list_out = []
        for(let i=0; i<info.length; i++){
            list_out.push(
                <div className='cm_infoblock cm_infoflex'>
                    <DotIcon/> <div>{info[i]['before']} → {info[i]['next']}</div>
                </div>
            )
        }
        return list_out
    }
     
    function CreateResourceBlock(info){
        let list_out = []
        for(let i=0; i<info.length; i++){
            list_out.push(
                <div className='cm_infoblock'>
                    <div className='cm_infoflex'>
                        <DotIcon/> Resource ID: {info[i]['id']}
                            {"name" in info[i] ? (<div className='cm_infobg'>
                                {info[i]['name']}
                            </div>) : (<></>)}
                    </div>
                    {"nonworkingperiods" in info[i] ? (
                        <>
                            <div className='cm_infoleftmid'>
                                Non Working Periods:
                            </div>
                            <div className='cm_infoperiodsholder'>
                                <div className='cm_infoperiods'>
                                    {info[i]["nonworkingperiods"].map((x, index) => (
                                        <div className='cm_infoflex'><DotIcon/> {BlockDateToStr(x.fromdate, true)} → {BlockDateToStr(x.todate, true)}</div>
                                    ))}
                                </div>
                            </div>
                        </>
                    ) : (<></>)}
                </div>
            )
        }
        return list_out
    }

    async function ResumeAnswerStream(waitTitle = null){
        let response_status = null
        let qs = ((waitTitle !== null) ? '?t=' : '')
        let response = await fetch(import.meta.env.VITE_URL + 'chats/resumestream/' + linkparams.id + '/' + qs, {
            method: 'GET',
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
            ReadAnswerStream(response, linkparams, convsetState, isgeneratingsetState, convstreamgeneratingRef, waitTitle)
        }
        else if(response_status === 401 || response_status === 403){
            navigate('/login', {state: {to: '/chat/' + linkparams.id + '/', expired: true}})
        }

    }

    async function ReadAnswerStream(response, linkparams, convsetState, isgeneratingsetState, convstreamgeneratingRef, waitTitle){
        let ai_answer = ''
        let buffer_answer = ''
        let info_block = null
        let search_block = null
        let errorquit = false
        const decoder = new TextDecoder();

        while(true){
            const { done, value } = await response.read();

            if(done){
                convstreamgeneratingRef.current.delete(linkparams.id)
                if(window.location.pathname.split("/").at(-2) === linkparams.id){
                    isgeneratingsetState(false)
                }
                return
            }

            ai_answer += decoder.decode(value, { stream: true });
            let lines = ai_answer.split("\n");
            ai_answer = lines.pop()
            
            for (const line of lines) {
                if (!line.trim()) continue
                const msg = JSON.parse(line)
                
                if(msg.t !== undefined){
                    chatlist.current[waitTitle]["name"] = msg.t
                    chatnavsetState([...chatlist.current])
                }
                else if(msg.v !== undefined){
                    buffer_answer += msg.v
                }
                else if(msg.i !== undefined){
                    info_block = msg.i.q
                    search_block = msg.i.s
                }
                else if(msg.e !== undefined){
                    buffer_answer = msg.e
                    errorquit = true
                }
            }

            if(buffer_answer === '') continue
            if(window.location.pathname.split("/").at(-2) === linkparams.id){
                convsetState(prevState => [
                <div className='cm_chatbox'>
                    {CreateInfoBlock([buffer_answer], info_block, search_block)}
                </div>,
                prevState.slice(1)
                ])
            }
            if(errorquit === true) return

        }
    }

    function AddStreamBold(streamtext){
        let bold_text_split = streamtext.split('**')
        let bold_string = [bold_text_split[0]]
        if(streamtext.length > 1){
            for(let i=1; i<bold_text_split.length; i++){
                if(i % 2 == 1){
                    bold_string.push(<span className='cm_bold'>{bold_text_split[i]}</span>)
                }
                else{
                    bold_string.push(bold_text_split[i])
                }
            }
        }
        return bold_string
    }

    return(
        <div className='cm_holder'>
            <div className='cm_container'>
                <div className='cm_chat' style={isloadingState === false ? {paddingBottom: '200px'} : {paddingBottom: '0px'}} ref={cmchatRef}>
                    {isloadingState === true ? (
                        <>
                            <div className='cm_loadinguser'>
                                <div className='loading_box loading' style={{width: '75%'}}/>
                                <div className='loading_box loading' style={{width: '85%'}}/>
                            </div>
                            <div className='cm_loading'>
                                <div className='loading_box loading_blue' style={{width: '75%'}}/>
                                <div className='loading_box loading_blue' style={{width: '90%'}}/>
                                <div className='loading_box loading_blue' style={{width: '90%'}}/>
                            </div>
                            <div className='cm_loadinguser'>
                                <div className='loading_box loading' style={{width: '75%'}}/>
                            </div>
                            <div className='cm_loading'>
                                <div className='loading_box loading_blue' style={{width: '75%'}}/>
                                <div className='loading_box loading_blue' style={{width: '90%'}}/>
                            </div>
                        </>
                    ) : (convState)
                    }
                </div>
                <ChatBox chatlist={chatlist} isloadingState={isloadingState} chatthinkState={thinkState} chattype='main' convsetState={convsetState} linkparams={linkparams} isgeneratingState={isgeneratingState} isgeneratingsetState={isgeneratingsetState} convstreamgeneratingRef={convstreamgeneratingRef} ReadAnswerStream={ReadAnswerStream}/>
                <div className='cm_backwhite'/>
            </div>
        </div>
    )
}