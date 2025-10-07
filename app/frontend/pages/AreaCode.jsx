import '../styling/AreaCode.css'
import { XCloseIcon, SearchIcon } from '../components/svgs/UtilIcons'
import { useState, useEffect, useRef } from 'react'

import { country_list, country_list_full } from '../components/CountriesList'

export function AreaCode({ areacodevisibility, areacodeinputsetState, areacodecountrysetState }){

    const [ac_infostate, ac_infosetState] = useState()
    const [ac_inputvalstate, ac_inputvalsetState] = useState('')

    const ac_popupRef = useRef()
    const ac_darkRef = useRef()

    useEffect(() => {
        if(areacodevisibility !== 0){
            ChangeVisibility('show')
        }
        else if(areacodevisibility === 0){
            ChangeSearchBody()
            InitialAreaCode()
        }
    }, [areacodevisibility])

    function ChangeVisibility(visibility){
        if(visibility === 'show'){
            ac_popupRef.current.style.opacity = '1'
            ac_popupRef.current.style.transform = 'scale(1)'
            ac_popupRef.current.style.pointerEvents = 'all'
            ac_darkRef.current.style.opacity = '1'
            ac_darkRef.current.style.pointerEvents = 'all'
        }
        else if(visibility === 'hidden'){
            ac_popupRef.current.style.opacity = '0'
            ac_popupRef.current.style.transform = 'scale(0.75)'
            ac_popupRef.current.style.pointerEvents = 'none'
            ac_darkRef.current.style.opacity = '0'
            ac_darkRef.current.style.pointerEvents = 'none'
        }
    }

    function ChangeSearchBody(){
        let filtered_items = country_list.filter(item => { return item.toLowerCase().includes(ac_inputvalstate.toLowerCase()) })

        ac_infosetState(
            filtered_items.map(item => (
                <li key={item} onClick={() => {
                    areacodeinputsetState(country_list_full[item]['ac'].slice(1))
                    areacodecountrysetState(country_list_full[item]['svg'])
                    ChangeVisibility('hidden')
                }}>
                    <div className='ac_search_body_infomain'>
                        {country_list_full[item]['svg']}
                        <span className='ac_search_body_infospan'>{item}</span>
                    </div>
                    <span>{country_list_full[item]['ac']}</span>
                </li>
            ))
        )
    }

    function InitialAreaCode(){
        let country = Intl.DateTimeFormat().resolvedOptions().timeZone;
        
    }

    return(
        <>
        <div className='ac_allholder' tabIndex='0' ref={ac_popupRef}>
            <div className='ac_header'>
                <div className='ac_header_text'>Select Area Code</div>
                <div className='ac_header_x' onClick={() => ChangeVisibility('hidden')}>
                    <XCloseIcon/>
                </div>
            </div>
            <div className='ac_search'>
                <SearchIcon/>
                <input className='ac_search_input' placeholder='Search' onChange={(e) => {
                    ac_inputvalsetState(e.target.value)
                    ChangeSearchBody()
                }}/>
            </div>
            <ul className='ac_search_body'>
                {ac_infostate}
            </ul>
        </div>
        <div className='ac_darkall' ref={ac_darkRef} onClick={() => ChangeVisibility('hidden')}/>
        </>
    )
}