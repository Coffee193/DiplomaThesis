import { SearchIcon } from '../components/svgs/UtilIcons';
import { useRef } from 'react';

export function ChatNavSearch({ searchchatinputRef , SearchChat}){

    const searchiconRef = useRef()

    return(
        <div className='cn_util_search'>
            <div ref={searchiconRef} style={{transition: '0.1s ease-out'}}><SearchIcon/></div>
            <input placeholder='Search Chat' onChange={(e) => SearchChat(e.target.value)} onFocus={() => searchiconRef.current.classList.add('color_blue_hover_evenmore')} onBlur={() => searchiconRef.current.classList.remove('color_blue_hover_evenmore')} ref={searchchatinputRef} tabIndex="-1"/>
        </div>
    )
}