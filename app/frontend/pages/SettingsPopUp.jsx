import '../styling/SettingsPopUp.css'
import { XCloseIcon } from '../components/svgs/UtilIcons'
import { UsernamePhoneInput } from './UsernamePhoneInput'
import { PasswordInput } from './PasswordInput'
import { SettingsNameInput } from './SettingsNameInput'
import { SettingsImage } from './SettingsImage'
import { useState, useRef } from 'react'

export function SettingsPopUp({ popupState, popupsetState}){

    const [spwarningState, spwarningsetState] = useState('')
    const sppasswordRef = useRef()
    const spemailRef = useRef()
    const sppasswordfirstRef = useRef()
    const spnameRef = useRef()
    const spphoneRef = useRef()

    function FocusElement(element){
        if(element === 'ps'){
            sppasswordRef.current.focus()
        }
        else if(element === 'em'){
            spemailRef.current.focusInput()
        }
        else if(element === 'pa'){
            sppasswordfirstRef.current.focus()
        }
        else if(element === 'na'){
            spnameRef.current.focus()
        }
        else if(element === 'ph'){
            spphoneRef.current.focusAreaCode()
        }
    }

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
                                    <UsernamePhoneInput alwaysEmail={true} classtype='s' placeholder={popupState['placeholderfirst']} tabIndex="-1" onpressTab={FocusElement} onpressTabValue={'ps'} ref={spemailRef} autoFocus={true}/>
                                )
                            }
                            else if(popupState['inputtype'] === 'phone'){
                                return(
                                    <UsernamePhoneInput alwaysPhone={true} classtype='s' placeholder={popupState['placeholderfirst']} existnavbar={true} tabIndex="-1" onpressTab={FocusElement} onpressTabValue={'ps'} autoFocus={true} ref={spphoneRef}/>
                                )
                            }
                            else if(popupState['inputtype'] === 'password'){
                                return(
                                    <PasswordInput classtype='s' placeholder={popupState['placeholderfirst']} tabIndex="-1"  onpressTab={FocusElement} onpressTabValue={'ps'} ref={sppasswordfirstRef} autoFocus={true}/>
                                )
                            }
                            else if(popupState['inputtype'] === 'name'){
                                return(
                                    <SettingsNameInput placeholder={popupState['placeholderfirst']} tabIndex="-1" onpressTab={FocusElement} onpressTabValue={'ps'} autoFocus={true} ref={spnameRef}/>
                                )
                            }
                            else if(popupState['inputtype'] === 'image'){
                                return(
                                    <SettingsImage existimage={popupState['existimage']}/>
                                )
                            }
                        })()
                    }
                    <PasswordInput classtype='s' placeholder={popupState['placeholdersecond']} ref={sppasswordRef} tabIndex="-1" onpressTab={FocusElement} onpressTabValue={popupState['inputtype'] !== undefined ? popupState['inputtype'].slice(0, 2) : ''}/>
                    <div className='sp_warning'>{spwarningState}</div>
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