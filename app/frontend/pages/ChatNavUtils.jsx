import { ChatNavSearch } from "./ChatNavSearch"
import { ChatNavPopUp } from "./ChatNavPopUp"
import { ChatNavRenameDelete } from "./ChatNavRenameDelete"
import { useState, useRef } from "react"

export function ChatNavUtils({ chatclickRef, convsetState, chatlist, createConversations, cnpState, cnpsetState }){

    const [cnrdState, cnrdsetState] = useState({'visible': false})
    const searchchatinputRef = useRef()

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
            convsetState(createConversations(templist, false, indexlist))
        }
        else{
            convsetState(createConversations(chatlist.current, false))
        }
    }

    return(
        <>
            <ChatNavSearch searchchatinputRef={searchchatinputRef} SearchChat={SearchChat}/>
            <ChatNavPopUp cnpState={cnpState} cnpsetState={cnpsetState} cnrdsetState={cnrdsetState} chatclickRef={chatclickRef}/>
            <ChatNavRenameDelete cnrdState={cnrdState} cnrdsetState={cnrdsetState} convsetState={convsetState} searchchatinputRef={searchchatinputRef} SearchChat={SearchChat}/>
        </>
    )
}