import '../styling/ChatNavSearch.css'
import { XCloseIcon, SearchIcon } from '../components/svgs/UtilIcons';
import { useRef } from 'react';

export function ChatNavSearch({ searchchatinputRef , SearchChat}){

    const searchiconRef = useRef()
    const xcloseRef = useRef()

    function SearchValueChange(value){
        console.log('aaa')
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

    return(
        <div className='cn_util_search'>
            <div ref={searchiconRef} style={{transition: '0.1s ease-out'}}><SearchIcon/></div>
            <input placeholder='Search Chat' onChange={(e) => SearchValueChange(e.target.value)} onFocus={() => searchiconRef.current.classList.add('color_blue_hover_evenmore')} onBlur={() => searchiconRef.current.classList.remove('color_blue_hover_evenmore')} ref={searchchatinputRef} tabIndex="-1"/>
            <div className='cn_util_xclose' ref={xcloseRef} onClick={() => {SearchValueChange(''); searchchatinputRef.current.value = ''}}><XCloseIcon/></div>
        </div>
    )
}