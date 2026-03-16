import '../styling/ChatMain.css'
import { useRef, useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ChatBox } from './ChatBox'
import { ChatBoxUpload } from './ChatBoxUpload'
import { BlocksLoad, DotIcon } from '../components/svgs/UtilIcons'

export function ChatMain({ chatlist, chatnavloadingState, linkparams, chatnavsetState }){

    const navigate = useNavigate()
    const [isloadingState, isloadingsetState] = useState(true)
    const [convState, convsetState] = useState()
    const cmchatRef = useRef()
    const [isgeneratingState, isgeneratingsetState] = useState(false)
    const convstreamgeneratingRef = useRef(new Set([]))

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
        
        console.log(chatlist.current.map((e) => e['_id']).indexOf(linkparams.id))
        console.log('jkjkjk')
        console.log(response)
        console.log(response['c'].length)
        if(response['c'].length === 0){
            generateTitle = chatlist.current.map((e) => e["_id"]).indexOf(linkparams.id)
            if(chatlist.current[generateTitle]["name"] !== "New Conversation"){
                generateTitle = null
            }
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
                            {response["g"]["d"] !== undefined ? <ChatBoxUpload cbuState={{'visible': true, 'inchat': true, 'name': response["g"]["d"]["n"], 'type': response["g"]["d"]["n"].split('.')[1].toUpperCase(), 'size': response["g"]["d"]["s"], 'path': response["g"]["d"]["p"]}}/> : null}
                            {response["g"]["q"] !== undefined ?
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
                            {AddStreamBold(response["c"][i]["a"])}
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

        await response.read().then(function readchunk({done, value}) {

            // You need to put this here. Basically after the last part is received this function runs another time with value = undefined
            // and done = True. passing undefined in String.fromChatCo.. gives '', which when passed on JSON.parse throws an error
            if(done){
                convstreamgeneratingRef.current.delete(linkparams.id)
                if(window.location.pathname.split("/").at(-2) === linkparams.id){
                    isgeneratingsetState(false)
                }
                return
            }
            // remove
            //let vava = encodeURIComponent(String.fromCharCode.apply(null, value))
            //console.log(vava)
            //vava = decodeURIComponent(vava)
            //console.log(vava)
            //
            let ret_stream = decodeURIComponent(encodeURIComponent(String.fromCharCode.apply(null, value)))
            if(ret_stream.split('}').length >= 4){
                ret_stream = ret_stream.slice(9)
            }
            ret_stream = JSON.parse(ret_stream)

            // An initial value of {'v': ''} is returned from that function. This is so that the cookies are Instantly set, otherwise the
            // cookies wont be set until a single answer token is produced
            if(ai_answer === '' && (ret_stream['v'] === '' || ret_stream['v'] === undefined)){
                return response.read().then(readchunk)
            }
            
            if(waitTitle !== null && 't' in ret_stream){
                console.log('TITLEEEEEEEEE')
                chatlist.current[waitTitle]["name"] = ret_stream['t']
                console.log(chatlist.current)
                chatnavsetState([...chatlist.current])

                if(!('v' in ret_stream)){
                    return response.read().then(readchunk)
                }
            }

            ai_answer += ret_stream['v']

            if(window.location.pathname.split("/").at(-2) === linkparams.id){
                convsetState(prevState => [
                <div className='cm_chatbox'>
                    {ai_answer}
                </div>,
                prevState.slice(1)
                ])
            }

            return response.read().then(readchunk)
        })
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
        console.log(bold_string)
        console.log('&&&&&&&&&&&&&&')
        /*let fin_string = []
        for(let i=0; i<bold_string.length; i++){
            console.log(i)
            if(i % 2 === 0){
                bold_string[i] = bold_string[i].split("\n* ")
                if(bold_string[i].length > 1){
                    for(let x=0; x<bold_string[i].length; x++){
                        if(x%2 === 1){
                            bold_string[i][x] = <><br/><span className='cm_dotholder'><DotIcon/> {bold_string[i][x]}</span></>
                        }
                    }
                }
            }
        }*/
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
                <ChatBox chatlist={chatlist} isloadingState={isloadingState} chattype='main' convsetState={convsetState} linkparams={linkparams} isgeneratingState={isgeneratingState} isgeneratingsetState={isgeneratingsetState} convstreamgeneratingRef={convstreamgeneratingRef} ReadAnswerStream={ReadAnswerStream}/>
                <div className='cm_backwhite'/>
            </div>
        </div>
    )
}