import '../styling/ChatBoxUpload.css'
import { Document, XCloseIcon, BlocksLoad } from '../components/svgs/UtilIcons'
import { useState } from 'react'

export function ChatBoxUpload({ cbuState, cbusetState }){

    const [isloadingState, isloadingsetState] = useState(true)

    return(
        <div className='cbu_holder' style={cbuState['visible'] === false ? {display: 'none'} : null}>
            <div className='cbu'>
                {isloadingState === true ? '' : <div className='cbu_x'><XCloseIcon width={14} height={14}/></div>}
                <div className='cbu_document'>{isloadingState === true ? <BlocksLoad width={30} height={30}/> : <Document width={30} height={30}/>}</div>
                <div className='cbu_info'>
                    <div className='cbu_top'>Name of the Doc is this</div>
                    <div className='cbu_bottom'>XML 50kB</div>
                </div>
            </div>
        </div>
    )
}