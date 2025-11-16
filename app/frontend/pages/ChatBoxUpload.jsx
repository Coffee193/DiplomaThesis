import '../styling/ChatBoxUpload.css'
import { Document, XCloseIcon, BlocksLoad, ArrowUpload } from '../components/svgs/UtilIcons'

export function ChatBoxUpload({ cbuState, cbusetState, cbinputRef, UploadActive, EmptyTextArrowDeactive }){

    function CloseBoxUpload(){
        cbusetState({'visible': false, 'isloading': true})
        cbinputRef.current.value = ''
        UploadActive()
        EmptyTextArrowDeactive()
    }

    return(
        <div className='cbu_holder' style={{...cbuState['visible'] === false ? {display: 'none'} : null, ...cbuState['inchat'] === true ? {justifyContent: 'end'} : null}}>
            <div className='cbu'>
                {cbuState['inchat'] === true ? <div className='cbu_x'><ArrowUpload width={14} height={14} transform={'rotate(180)'}/></div> : cbuState['isloading'] === false ? <div className='cbu_x' onClick={() => CloseBoxUpload()}><XCloseIcon width={14} height={14}/></div> : null}
                {/*{cbuState['isloadingState'] === true || cbuState['inchat'] === true ? '' : <div className='cbu_x' onClick={() => CloseBoxUpload()}><XCloseIcon width={14} height={14}/></div>}*/}
                <div className='cbu_document'>{cbuState['isloading'] === false || cbuState['inchat'] === true ? <Document width={30} height={30}/> : <BlocksLoad width={30} height={30}/>}</div>
                <div className='cbu_info'>
                    <div className='cbu_top'>{cbuState['name']}</div>
                    <div className='cbu_bottom'>{cbuState['type']} {cbuState['size']}kB</div>
                </div>
            </div>
        </div>
    )
}

/* change line 16 div with a. and pass attribute download. Also use the env variable VITE_CHAT_DOCUMENT_PATH */