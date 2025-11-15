import '../styling/ChatBoxUpload.css'
import { Document, XCloseIcon, BlocksLoad } from '../components/svgs/UtilIcons'
import { useState } from 'react'

export function ChatBoxUpload({ cbuState, cbusetState, cbinputRef, UploadActive, EmptyTextArrowDeactive }){

    function CloseBoxUpload(){
        cbusetState({'visible': false, 'isloading': true})
        cbinputRef.current.value = ''
        UploadActive()
        EmptyTextArrowDeactive()
    }

    return(
        <div className='cbu_holder' style={cbuState['visible'] === false ? {display: 'none'} : null}>
            <div className='cbu'>
                {cbuState['isloadingState'] === true ? '' : <div className='cbu_x' onClick={() => CloseBoxUpload()}><XCloseIcon width={14} height={14}/></div>}
                <div className='cbu_document'>{cbuState['isloadingState'] === true ? <BlocksLoad width={30} height={30}/> : <Document width={30} height={30}/>}</div>
                <div className='cbu_info'>
                    <div className='cbu_top'>{cbuState['name']}</div>
                    <div className='cbu_bottom'>{cbuState['type']} {cbuState['size']}kB</div>
                </div>
            </div>
        </div>
    )
}