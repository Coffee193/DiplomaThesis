import '../styling/ChatNavPopUp.css'
import { PencilIcon, TrashIcon } from '../components/svgs/UtilIcons'

export function ChatNavPopUp({ cnpState, cnpsetState, cnrdsetState, chatclickRef }){

    function OpenRenameDelete(type){
        if(type === 'delete'){
            cnrdsetState({'visible': true, 'closeclass': 'cnrd_xclosered', 'titleclass': 'cnrd_titlered', 'title': 'Delete Chat', 'text': 'This will delete ', 'convname': cnpState['name'], 'buttonclass': 'cnrd_delete', 'buttontext': 'Delete', 'id': cnpState['id'], 'index': cnpState['index']})
        }
        else if(type === 'rename'){
            cnrdsetState({'visible': true, 'closeclass': 'cnrd_xcloseblue', 'titleclass': 'cnrd_titleblue', 'title': 'Rename Chat', 'text': 'This will rename ', 'convname': cnpState['name'], 'buttonclass': 'cnrd_rename', 'buttontext': 'Rename', 'id': cnpState['id'], 'index': cnpState['index']})
        }
        chatclickRef.current = null
        cnpsetState({'visible': false, 'id': null})
    }

    return(
        <>
        <div className='cnp' style={cnpState['visible'] === false ? {opacity: '0', pointerevents: 'none', transform: 'scale(0.8)', top: '0'} : {opacity: '1', pointerEvents: 'all', transform: 'scale(1)', top: cnpState['top']}}>
            <div onClick={() => OpenRenameDelete('rename')}><PencilIcon width={24} height={24}/><span>Rename</span></div>
            <div onClick={() => OpenRenameDelete('delete')}><TrashIcon width={24} height={24}/><span>Delete</span></div>
        </div>
        <div className='cnp_bg' style={cnpState['visible'] === false ? {opacity: '0', pointerEvents: 'none'} : {opacity: '1', pointerEvents: 'all'}} onClick={() => {chatclickRef.current = null; cnpsetState({'visible': false, 'id': null})}}/>
        </>
    )
}