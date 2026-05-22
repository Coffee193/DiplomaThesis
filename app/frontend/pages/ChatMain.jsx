import '../styling/ChatMain.css'
import { useRef, useEffect, useState } from 'react'
import { data, useNavigate } from 'react-router-dom'
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
    const [modelState, modelsetState] = useState('')
    const cmlastdocRef = useRef(undefined)

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
        
        if(response_status === 200){
            if(response['c'].length === 0){
                generateTitle = chatlist.current.map((e) => e["_id"]).indexOf(linkparams.id)
            }

            let conv_vals = []

            if('g' in response){
                cmlastdocRef.current = response.g.u?.u || response.c.findLast(item => item.d?.length)?.d
                isgeneratingsetState(true)
                console.log('*********************')
                console.log(response["g"]["u"])
                conv_vals.push(
                        <div className='cm_chatbox cb_answerload'>
                            <BlocksLoad/>
                        </div>,
                        <div className='cm_chatuser'>
                            {response["g"]["u"] !== undefined && <ChatBoxUpload cbuState={{'inchat': true, 'documents': response["g"]["u"].map( doc => ({name: doc.name, type: doc.name.split('.')[1].toUpperCase(), size: doc.size, link: linkparams.id, id: doc.id, isloading: false}) )}}/>}
                            {response["g"]["q"] !== "" ?
                            <div className='cm_chatbox cm_boxuser'>
                                {response["g"]["q"]}
                            </div> : null
                            }
                        </div>
                )
            }
            else{
                cmlastdocRef.current = response.c.findLast(item => item.d?.length)?.d
            }

            for(let i=response['c'].length - 1; i>=0; i--){
                let doc_info = response["c"][i]["d"]
                if(doc_info === undefined){
                    for (let j = i - 1; j >= 0; j--) {
                        if (response['c'][j]['d']) {
                        doc_info = response['c'][j]['d'];
                        break;   // first hit going down = closest lower index
                        }
                    }
                }

                conv_vals.push(
                    <>
                        <div className='cm_chatbox'>
                            {CreateInfoBlock(AddStreamBold(response["c"][i]["a"]), response["c"][i]["i"], response["c"][i]["s"], doc_info)}
                        </div>
                        <div className='cm_chatuser'>
                            {/*response["c"][i]["d"] !== undefined ? <ChatBoxUpload cbuState={{'visible': true, 'inchat': true, 'name': response["c"][i]["d"]["name"], 'type': response["c"][i]["d"]["name"].split('.')[1].toUpperCase(), 'size': response["c"][i]["d"]["size"], 'id': response["c"][i]["d"]["id"], 'link': linkparams.id}}/> : null*/}
                            {response["c"][i]["d"] !== undefined ? <ChatBoxUpload cbuState={{'inchat': true, 'documents': response["c"][i]["d"].map( doc => ({name: doc.name, type: doc.name.split('.')[1].toUpperCase(), size: doc.size, id: doc.id, link: linkparams.id, isloading: false}) )}}/> : null}
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
            modelsetState(response['m'])

            if('g' in response){
                console.log('ggggggggggg')
                console.log(response['g']) /* {'q': 'return all tasks', 'u': [{'id': 123, 'name': 'InputJSON.json', 'size': '152.3'}, {'id': 456, 'name': 'InputJSON2.json', 'size': '330'}]} */
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

    function CreateInfoBlock(data, info, search, documents){
        if(info !== undefined){
            if(data.length === 1){
                data = data[0].split(/(\(DATA\))/)
            }
            console.log('ppp')
                console.log(documents)
            /*if(documents === undefined){
                documents = cmlastdocRef.current
            }*/
            for(let i=1; i<data.length; i++){
                if(data[i] === "(DATA)"){
                    data[i] =
                    <div className='cm_infoboxholder'>
                        <div className = {(Object.keys(info[0]).length === 0 || Object.keys(info[0][0]).length > 2) && (search === 'jobs' || search === 'tasksuitableresources') ? 'cm_infobox cm_infoboxgap': 'cm_infobox'}>
                            {info.length === 1 ? CreateBlock(info[0], search, documents[0]['name']) : CreateMultiBlock(info, search, documents)}
                        </div>
                    </div> 
                }
            }
        }
        return data
    }

    function CreateDocumentNameBlock(name, found_count, margin_remove, search){
        let style = {}
        if (search === 'jobs'){
            style.margin = 0
        }
        else if (margin_remove === true){
            style.marginTop = 0
        }

        return (
            <div className='cm_infodocumentname' style={style}>
                <div>{DocumentNameBlockTruncate(name)}</div>
                <div className='cm_infodocumentcount'>({found_count})</div>
            </div>
        )
    }

    function DocumentNameBlockTruncate(name){
        if(name.length > 25){
            return name.slice(0, 22) + '...'
        }
        else{
            return name
        }
    }

    function CreateMultiBlock(info, search, documents){
        let out_block = []
        for (let i=0; i<info.length; i++){
            console.log('vvvvvvvvvvvvvvvv')
            console.log(i)
            console.log(info)
            console.log(search)
            console.log(documents)
            out_block.push(CreateDocumentNameBlock(documents[i]['name'], info[i].length, i === 0 ? true : false, search))
            out_block.push(CreateBlock(info[i], search, documents[i]['name']))
        }
        return out_block
    }

    function CreateBlock(info, search, document_name){
        const name = document_name.toLowerCase()

        const hasInput = name.includes('input')
        const hasOutput = name.includes('output')

        if(hasInput && !hasOutput){
            return CreateInputBlock(info, search)
        }
        else if(hasOutput && !hasInput){
            return CreateOutputBlock(info, search)
        }
        else{
            return CreateInvalidNameBlock()
        }
    }

    function CreateOutputBlock(info, search){
        if (info.length === 0) return CreateNoDataBlock()
        return CreateOutputDataBlock(info)
    }

    function CreateInputBlock(info, search){
        if(info.length === 0){
            return CreateNoDataBlock()
        }
        else if(search == 'jobs'){
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

    function BlockDateToStr(date, withtime = false, withsecond = false){
        if(withtime === false){
            return date['day'] + '  ' + NumberToShortMonthName(date['month']) + '  ' + date['year']
        }
        else{
            if(withsecond === false){
                return date['day'] + '  ' + NumberToShortMonthName(date['month']) + '  ' + date['year'] + '  ' + String(date['hour']).padStart(2, '0') + ':' + String(date['minute']).padStart(2, '0')
            }
            else{
                return date['day'] + '  ' + NumberToShortMonthName(date['month']) + '  ' + date['year'] + '  ' + String(date['hour']).padStart(2, '0') + ':' + String(date['minute']).padStart(2, '0') + ':' + String(date['second']).padStart(2, '0')
            }
        }
    }

    function MsToTimeString(ms_int){
        const total_seconds = Math.floor(ms_int / 1000)
        const hours = Math.floor(total_seconds / 3600)
        const minutes = Math.floor((total_seconds % 3600) / 60)
        const seconds = total_seconds % 60

        let out_string = []
        if (hours > 0) out_string.push(`${hours}h`)
        if (minutes > 0) out_string.push(`${minutes}m`)
        if (seconds > 0 || out_string.length === 0) out_string.push(`${seconds}s`)
        
        const formatted_ms = ms_int.toLocaleString()
        
        return `${out_string.join(' ')}   (${formatted_ms} ms)`
    }

    function SToTimeString(s_double){
        const hours = Math.floor(s_double / 3600)
        const minutes = Math.floor((s_double % 3600) / 60)
        const seconds = s_double % 60

        let out_string = []
        if (hours > 0) out_string.push(`${hours}h`)
        if (minutes > 0) out_string.push(`${minutes}m`)
        
        const sec_str = Number(seconds.toFixed(0))
        out_string.push(`${sec_str}s`)

        const formatted_ms = s_double.toLocaleString()
        
        return `${out_string.join(' ')}   (${formatted_ms} s)`
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
                        {'operation_time' in x ? <div className='cm_infoleftmid cm_infoflex'>Operation Time: <div className='cm_infoweak cm_infoblockmid'>{SToTimeString(x.operation_time)}</div></div> : <></>}
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

    function CreateOutputDataBlock(info){
        let out_list = []
        for (let i=0; i<info.length; i++){
            out_list.push(
                <div className='cm_infoblock'>
                    <div className = 'cm_infoflex'>
                        <ArrowDownIcon width={16} height={16} style={{transform: 'rotate(-90deg)'}}/> Assignment No. 
                        <div className='cm_infobg'>
                            {i + 1}
                        </div>
                    </div>
                </div>
            )
            for (let key in info[i]){
                let big_text = ''
                let small_text = ''
                if(key === 'task'){
                    big_text = 'Task ID: '
                    small_text = info[i][key]
                }
                else if(key === 'resource'){
                    big_text = 'Resource ID: '
                    small_text = info[i][key]
                }
                else if(key === 'dispatch'){
                    big_text = 'Dispatch Time: '
                    small_text = BlockDateToStr(info[i][key], true, true)
                }
                else if(key === 'durationinmilliseconds'){
                    big_text = 'Duration: '
                    small_text = MsToTimeString(info[i][key])
                }

                if(big_text !== ''){
                    out_list.push(
                        <div className='cm_infoleft cm_infoflex'>
                            <DotIcon/>
                            <div className='cm_infopush'>{big_text}</div>
                            <div className='cm_infoweak'>{small_text}</div>
                        </div>
                    )
                }
            }
        }
        return out_list
    }

    function CreateNoDataBlock(){
        return (
            <div className='cm_nodata'> <DotIcon/> No Data Found <DotIcon/> </div>
        )
    }

    function CreateInvalidNameBlock(){
        return(
            <div className='cm_nodata'> <DotIcon/> The Uploaded File is invalid. Its name should contain the words 'input' or 'ouput'. Please upload a file with proper naming convention <DotIcon/> </div>
        )
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
        let document_info = undefined

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
                else if(msg.u !== undefined){
                    document_info = msg.u
                    cmlastdocRef.current = msg.u
                }
            }

            console.log('valval')
            console.log(cmlastdocRef.current)
            if (document_info === undefined) document_info = cmlastdocRef.current
            if(buffer_answer === '') continue
            if(window.location.pathname.split("/").at(-2) === linkparams.id){
                convsetState(prevState => [
                <div className='cm_chatbox'>
                    {CreateInfoBlock([buffer_answer], info_block, search_block, document_info)}
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
                <ChatBox chatlist={chatlist} isloadingState={isloadingState} modelState={modelState} chattype='main' convsetState={convsetState} linkparams={linkparams} isgeneratingState={isgeneratingState} isgeneratingsetState={isgeneratingsetState} convstreamgeneratingRef={convstreamgeneratingRef} ReadAnswerStream={ReadAnswerStream}/>
                <div className='cm_backwhite'/>
            </div>
        </div>
    )
}