import '../styling/ChatNavSearch.css'
import { XCloseIcon, SearchIcon } from '../components/svgs/UtilIcons';
import { useRef } from 'react';

export function ChatNavSearch({ convsetState, chatlist, createConversations }){

    const searchiconRef = useRef()
    const searchchatinputRef = useRef()
    const xcloseRef = useRef()

    function SearchValueChange(value){
        if(value !== ''){
            xcloseRef.current.style.opacity = '1'
            xcloseRef.current.style.pointerEvents = 'all'
        }
        else{
            xcloseRef.current.style.opacity = '0'
            xcloseRef.current.style.pointerEvents = 'none'
        }
        SearchChat(value)
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
            convsetState(createConversations(templist, false, indexlist))
        }
        else{
            convsetState(createConversations(chatlist.current, false))
        }
    }

    return(
        <div className='cn_util_search'>
            <div ref={searchiconRef} style={{transition: '0.1s ease-out'}}><SearchIcon/></div>
            <input placeholder='Search Chat' onChange={(e) => SearchValueChange(e.target.value)} onFocus={() => searchiconRef.current.classList.add('color_blue_hover_evenmore')} onBlur={() => searchiconRef.current.classList.remove('color_blue_hover_evenmore')} ref={searchchatinputRef} tabIndex="-1"/>
            <div className='cn_util_xclose' ref={xcloseRef} onClick={() => {SearchValueChange(''); searchchatinputRef.current.value = ''}}><XCloseIcon/></div>
        </div>
    )
}