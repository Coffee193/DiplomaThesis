import '../styling/AreaCode.css'
import { XCloseIcon, SearchIcon } from '../components/svgs/UtilIcons'
import { useState } from 'react'

export function AreaCode({ areacodesvgsetState, areacodeinputRef, areacodevisibleState, areacodevisiblesetState, country_list_full, country_list_keys, valuesRef, warningIndex, warningvalueIndex, valueIndex, existnavbar }){

    const [ac_infostate, ac_infosetState] = useState(country_list_keys.map(item => CreateAreaCodeItem(item)))

    function ChangeSearchBody(inputvalue){
        let filtered_items = country_list_keys.filter(item => { return item.toLowerCase().includes(inputvalue.toLowerCase()) })
            
            ac_infosetState(
                filtered_items.map(item => (
                    CreateAreaCodeItem(item)
                ))
            )
    }

    function CreateAreaCodeItem(item){
        return( <li key={item} onClick={() => {
                    areacodesvgsetState(country_list_full[item]['svg'])
                    areacodeinputRef.current.value = country_list_full[item]['ac'].slice(1)
                    areacodevisiblesetState(false)
                    if(valuesRef !== undefined){
                        valuesRef.current[valueIndex] = country_list_full[item]['ac'] + ' ' + valuesRef.current[valueIndex].split(' ')[1]
                        valuesRef.current[warningIndex][warningvalueIndex] = null
                    }
                }}>
                    <div className='ac_search_body_infomain'>
                        {country_list_full[item]['svg']}
                        <span className='ac_search_body_infospan'>{item}</span>
                    </div>
                    <span>{country_list_full[item]['ac']}</span>
                </li>
        )
    }

    function CalcNavBarOffset(){
        return 'calc( (100vh - var(--ac-height))/2 + ' + (Math.max( parseInt(window.getComputedStyle(document.getElementsByClassName('n_allholder')[0]).getPropertyValue('--nav-height').slice(0, 2)) - document.body.scrollTop, 0 ) /2).toString() + 'px)'
    }
        

    return(
        <>
        {/*<div className='ac_allholder' style={areacodevisibleState === true ? ({opacity: '1', transform: 'scale(1)', pointerEvents: 'all'}) : ({opacity: '0', transform: 'scale(0.75)', pointerEvents: 'none'})}>*/}
            <div className='ac_allholder' style={{...areacodevisibleState === true ? ({opacity: '1', transform: 'scale(1)', pointerEvents: 'all'}) : ({opacity: '0', transform: 'scale(0.75)', pointerEvents: 'none'}), ...existnavbar === true ? ({top: CalcNavBarOffset()}) : ({}) }}>
            <div className='ac_header'>
                <div className='ac_header_text'>Select Area Code</div>
                <div className='ac_header_x' onClick={() => areacodevisiblesetState(false)}>
                    <XCloseIcon/>
                </div>
            </div>
            <div className='ac_search'>
                <SearchIcon/>
                <input className='ac_search_input' placeholder='Search' onChange={(event) => ChangeSearchBody(event.target.value)}/>
            </div>
            <ul className='ac_search_body'>
                {ac_infostate}
            </ul>
        </div>
        <div className='ac_darkall' onClick={() => areacodevisiblesetState(false)} style={areacodevisibleState === true ? ({opacity: '1', pointerEvents: 'all'}) : ({opacity: '0', pointerEvents: 'none'})}/>
        </>
    )
}