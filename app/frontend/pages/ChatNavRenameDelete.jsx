import '../styling/ChatNavRenameDelete.css'
import { XCloseIcon } from '../components/svgs/UtilIcons'

export function ChatNavRenameDelete({ cnrdState, cnrdsetState }){
    return(
        <>
        <div className='cnrd_holder'>
            <div className='cnrd_header'>
                <div className={'cnrd_xclose ' + cnrdState['closeclass']}><XCloseIcon/></div>
                <div className={cnrdState['titleclass']}>{cnrdState['title']}</div>
            </div>
            <div className='cnrd_body'>
                <div className='cnrd_text'>{cnrdState['text']}
                    <span>{cnrdState['convname']}</span>
                </div>
                <input className='cnrd_input' maxLength='50'/>
            </div>
            <div className='cnrd_utilholder'>
                <div className='cnrd_util cnrd_cancel'>Cancel</div>
                <div className={'cnrd_util ' + cnrdState['buttonclass']}>{cnrdState['buttontext']}</div>
            </div>
        </div>
        <div className='cnrd_bg'/>
        </>
    )
}