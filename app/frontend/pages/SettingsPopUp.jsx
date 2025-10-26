import '../styling/SettingsPopUp.css'
import { XCloseIcon } from '../components/svgs/UtilIcons'
import { UsernamePhoneInput } from './UsernamePhoneInput'
import { PasswordInput } from './PasswordInput'
import { SettingsNameInput } from './SettingsNameInput'
import { useState } from 'react'

export function SettingsPopUp({ popupState, popupsetState}){

    return(
        <>
        <div className='sp' style={popupState['visible'] === true ? ({opacity: '1', transform: 'none', pointerEvents: 'all'}) : ({opacity: '0', transform: 'scale(0.8)', pointerEvents: 'none'})}>
            <div className='sp_header'>
                <div className={popupState['headerred'] === true ? ('sp_red') : ('')}>{popupState['header']}</div>
                <XCloseIcon className={'sp_close ' + popupState['classclose']} onClick={() => popupsetState({'visible': false})}/>
            </div>
            { (popupState['isadmin'] === true && popupState['header'] === 'DELETE ACCOUNT') ? (
                <div className='sp_deleteadminaccount'>
                    <div>You <b>cannot</b> delete an admin account.</div>
                    <div>In order to delete it, contact the appropriate department and delete it straight from the database</div>
                </div>
            ) : (<>
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
                                    <UsernamePhoneInput alwaysPhone={true} classtype='s' placeholder={popupState['placeholderfirst']} existnavbar={true}/>
                                )
                            }
                            else if(popupState['inputtype'] === 'password'){
                                return(
                                    <PasswordInput classtype='s' placeholder={popupState['placeholderfirst']}/>
                                )
                            }
                            else if(popupState['inputtype'] === 'name'){
                                return(
                                    <SettingsNameInput placeholder={popupState['placeholderfirst']}/>
                                )
                            }
                        })()
                    }
                    <PasswordInput classtype='s' placeholder={popupState['placeholdersecond']}/>
                </div>
                <div className='sp_buttonholder'>
                    <div className={'sp_button sp_buttoninactive ' + popupState['classbutton']}>{popupState['textbutton']}</div>
                </div>
            </>)}
        </div>
        <div className='sp_darkbg' style={popupState['visible'] === true ? ({ opacity: '1', pointerEvents: 'all' }) : ({ opacity: '0', pointerEvents: 'none' })} onClick={() => popupsetState({'visible': false})}/>
        </>
    )
}