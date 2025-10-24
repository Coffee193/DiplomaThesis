import '../styling/SettingsBox.css'
import { PencilIcon } from '../components/svgs/UtilIcons'

export function SettingsBox({header, value, valueempty, shortenvalue = false, popupsetState, popupvalue}){

    function ShortValue(value){
        if(value.length > 39){
            value = value.slice(0, 37) + '...'
        }

        return value
    }

    return(
        <div className='sb_box' onClick={() => popupsetState(popupvalue)}>
            <span className='sb_header'>{header}</span>
            <div className='sb_main'>
                <div className={value === null ? ('sb_val sb_vallight') : ('sb_val')}>{value === null ? (valueempty) : (shortenvalue === false ? (value) : (ShortValue(value)))}</div>
                <div className='sb_change'><PencilIcon stroke-width={1}/></div>
            </div>
        </div>
    )
}