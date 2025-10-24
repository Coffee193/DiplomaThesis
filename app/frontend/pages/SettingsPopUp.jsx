import '../styling/SettingsPopUp.css'
import { XCloseIcon } from '../components/svgs/UtilIcons'
import { UsernamePhoneInput } from './UsernamePhoneInput'
import { PasswordInput } from './PasswordInput'
import { useState } from 'react'

export function SettingsPopUp({ popupState, popupsetState}){

    const [spbuttonState, spbuttonsetState] = useState('Submit')

    return(
        <>
        <div className='sp' style={popupState['visible'] === true ? ({opacity: '1', transform: 'scale(1)', pointerEvents: 'all'}) : ({opacity: '0', transform: 'scale(0.8)', pointerEvents: 'none'})}>
            <div className='sp_header'>
                {popupState['header']}
                <XCloseIcon className={'sp_close ' + popupState['classclose']} onClick={() => popupsetState({'visible': false})}/>
            </div>
            <div className='sp_holder'>
                {
                    (() => {
                        if(popupState['inputtype'] === 'email'){
                            return(
                                <UsernamePhoneInput alwaysEmail={true} classtype='s' placeholder={popupState['placeholderfirst']}/>
                            )
                        }
                        else if(popupState['inputtype'] === 'phone'){
                            return(
                                <UsernamePhoneInput alwaysPhone={true} classtype='s' placeholder={popupState['placeholderfirst']}/>
                            )
                        }
                        else if(popupState['inputtype'] === 'password'){
                            return(
                                <PasswordInput classtype='s' placeholder={popupState['placeholderfirst']}/>
                            )
                        }
                    })()
                }
                <PasswordInput classtype='s' placeholder={popupState['placeholdersecond']}/>
            </div>
            <div className='sp_buttonholder'>
                <div className={'sp_button sp_buttoninactive ' + popupState['classbutton']}>{spbuttonState}</div>
            </div>
        </div>
        <div className='sp_darkbg' style={popupState['visible'] === true ? ({ opacity: '1', pointerEvents: 'all' }) : ({ opacity: '0', pointerEvents: 'none' })} onClick={() => popupsetState({'visible': false})}/>
        </>
    )
}