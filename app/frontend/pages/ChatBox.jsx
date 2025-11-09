import '../styling/ChatBox.css'
import { ArrowUpload } from '../components/svgs/UtilIcons'
import { useRef } from 'react'

export function ChatBox({ isloadingState }){

    const cbtextareaRef = useRef()

    return(
        <div className='cb_holder'>
            { isloadingState === false ? (
            <>
                <textarea className='cb_textarea' placeholder='Ask Sapling' onChange={() => CheckQuestion()} ref={cbtextareaRef}/>
                <div className='cb_infoholder'>
                    <div className='cb_arrow cb_arrowdeactive' onClick={() => AskQuestion()}><ArrowUpload/></div>
                </div>
                <div className='cb_bg' onClick={() => cbtextareaRef.current.focus()}/>
                </>
            ) : (
                <div className='cb_loading'>
                    <div className='cb_arrowload loading'/>
                </div>
            )
            }
        </div>
    )
}