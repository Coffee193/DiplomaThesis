import '../styling/ChatNavPopUp.css'
import { PencilIcon, TrashIcon } from '../components/svgs/UtilIcons'

export function ChatNavPopUp({ cnpState, cnpsetState }){
    return(
        <>
        <div className='cnp' style={cnpState['visible'] === false ? {opacity: '0', pointerevents: 'none', transform: 'scale(0.8)', top: '0'} : {opacity: '1', pointerEvents: 'all', transform: 'scale(1)', top: cnpState['top']}}>
            <div><PencilIcon width={24} height={24}/><span>Rename</span></div>
            <div><TrashIcon width={24} height={24}/><span>Delete</span></div>
        </div>
        <div className='cnp_bg' style={cnpState['visible'] === false ? {opacity: '0', pointerEvents: 'none'} : {opacity: '1', pointerEvents: 'all'}} onClick={() => cnpsetState({'visible': false})}/>
        </>
    )
}