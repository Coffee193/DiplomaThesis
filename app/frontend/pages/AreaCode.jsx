import '../styling/AreaCode.css'
import { XCloseIcon, SearchIcon } from '../components/svgs/UtilIcons'
import { useState, useRef } from 'react'

import { country_list_full } from '../components/CountriesList'

export function AreaCode({ areacodeinputsetState, areacodecountrysetState, areacodevisibleState, areacodevisiblesetState }){

    const country_list = Object.keys(country_list_full)
    const [ac_infostate, ac_infosetState] = useState(Object.keys(country_list_full).map(item => CreateAreaCodeItem(item)))

    function ChangeSearchBody(inputvalue){
        let filtered_items = country_list.filter(item => { return item.toLowerCase().includes(inputvalue.toLowerCase()) })
            
            ac_infosetState(
                filtered_items.map(item => (
                    CreateAreaCodeItem(item)
                ))
            )
    }

    function CreateAreaCodeItem(item){
        return( <li key={item} onClick={() => {
                    areacodeinputsetState(country_list_full[item]['ac'].slice(1))
                    areacodecountrysetState(country_list_full[item]['svg'])
                    areacodevisiblesetState(false)
                }}>
                    <div className='ac_search_body_infomain'>
                        {country_list_full[item]['svg']}
                        <span className='ac_search_body_infospan'>{item}</span>
                    </div>
                    <span>{country_list_full[item]['ac']}</span>
                </li>
        )
    }

    function InitialAreaCode(){
        let country = Intl.DateTimeFormat().resolvedOptions().timeZone;
        
    }

        

    return(
        <>
        <div className='ac_allholder' style={areacodevisibleState === true ? ({opacity: '1', transform: 'scale(1)', pointerEvents: 'all'}) : ({opacity: '0', transform: 'scale(0.75)', pointerEvents: 'none'})}>
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