import '../styling/AreaCodePopUp.css'

import { XCloseIcon } from "../components/svgs/UtilIcons"
import { SearchIcon } from "../components/svgs/UtilIcons"

import { /*country_list,*/ country_list_full } from "../components/CountriesList"

import { useState } from "react"

export function AreaCodePopUp( { BlurClassName, setcountrysvg, setareacode } ){

    const [ulState, ulsetState] = useState(country_list)
    const [input_valState, input_valsetState] = useState('')

    const filteredul_items = ulState.filter(item =>{ return item.toLowerCase().includes(input_valState.toLowerCase())})

    function close_Area_Code_PopUp(){
        document.getElementsByClassName('active')[0].classList.remove('active')
        document.getElementsByClassName('Pop_up_darken_all')[0].style.display = 'none'
        document.getElementsByClassName(BlurClassName)[0].id = ''
    }

    return(
        <>
            <div className = 'AreaCode_login_popUp light-theme' tabIndex="0" style={{top:'50vh'}}>
                <div className = 'AreacCode_login_popUp_header'>
                    <div className = 'AreacCode_login_popUp_header_Text'>Select Area Code</div>
                    <div className = 'AreacCode_login_popUp_header_X' onClick={() => {
                        close_Area_Code_PopUp();
                    }}><XCloseIcon width={24} height={24}/></div>
                </div>
                <div className = 'AreacCode_login_popUp_searchbox'>
                    <SearchIcon/>
                    <input value={input_valState} className = 'AreacCode_login_popUp_searchbox_input' type = 'text' placeholder='Search' onChange={(e) => input_valsetState(e.target.value)}></input>
                </div>
                <ul className = 'AreacCode_login_popUp_searchbody light-theme'>
                    {filteredul_items.map(item => (
                        <li key={item} onClick={(e) =>{
                            setareacode(e.target.lastChild.innerText.slice(1));
                            setcountrysvg(country_list_full[item]['svg']);
                            close_Area_Code_PopUp();
                            }}><div className='AreacCode_login_popUp_ul_div'>{country_list_full[item]['svg']}<span className = 'AreacCode_login_popUp_ul_itemText'>{item}</span></div><span>{country_list_full[item]['ac']}</span></li>
                    ))}
                </ul>
            </div>

            <div className = 'Pop_up_darken_all' onClick={(e) => {
                close_Area_Code_PopUp()
            }}>
            </div>
        </>
    )
}