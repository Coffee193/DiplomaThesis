import '../styling/ChatBoxModelPopUp.css'
import { XCloseIcon, Tick } from '../components/svgs/UtilIcons'
import { model_list } from './modelList'

export function ChatBoxModelPopUp({current_model, isactiveState, isactivesetState, changemodelState}){

    const items = [
        {'name': 'Llama3.1:7B - Agent', 'type': 'local', 'agent': 'json-agent', 'id': 1},
        {'name': 'Llama3.1:7B', 'type': 'local', 'agent': '', 'id': 2},
        {'name': 'DeepSeek', 'type': 'cloud', 'agent': '', 'id': 3},
    ]

    function CreateModelList(models){
        console.log(current_model)
        let outlist = []
        for (let i of model_list) {
            if(i['id'] === current_model['id']){
                outlist.push(<div className='cbmp_item cbmp_item_select' onClick={() => isactivesetState(false)}><div>{i['name']}</div> <Tick width={17} height={17}/></div>)
            }
            else{
                outlist.push(<div className='cbmp_item' onClick={() => {changemodelState(i); isactivesetState(false)}}>{i['name']}</div>)
            }
        }

        return outlist
    }

    return(
        <div className="cbmp_holder" style={isactiveState === false ? {opacity: '0', pointerEvents: 'none', 'transform': 'scale(0.8)'} : {opacity: '1', pointerEvents: 'all', 'transform': 'scale(1)'}}>
            <div className='cbmp_top'>
                <div className='cbmp_title'>Models</div>
                <div className='cbmp_x' onClick={() => isactivesetState(false)}><XCloseIcon/></div>
            </div>
            <div className='cbmp_main'>
                {CreateModelList(model_list)}
            </div>
        </div>
    )
}