import '../styling/SettingsPopUp.css'
import { XCloseIcon, BlocksLoad } from '../components/svgs/UtilIcons'
import { UsernamePhoneInput } from './UsernamePhoneInput'
import { PasswordInput } from './PasswordInput'
import { SettingsNameInput } from './SettingsNameInput'
import { SettingsImage } from './SettingsImage'
import { useState, useRef } from 'react'
import { useNavigate } from 'react-router-dom'

export function SettingsPopUp({ popupState, popupsetState, valuesRef}){

    const [spnotificationState, spnotificationsetState] = useState({'text': '', 'svg': null, 'visible': false, 'class': null})
    const sppasswordRef = useRef()
    const spemailRef = useRef()
    const sppasswordfirstRef = useRef()
    const spnameRef = useRef()
    const spphoneRef = useRef()
    const spbuttonRef = useRef()
    const navigate = useNavigate()

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

    function ClickSubmitDelete(){
        let ivalstart = popupState['inputtype'] === 'password' ? 1 : 0
        let ivalend = popupState['inputtype'] === 'password' ? 3 : 2
        for(let i=ivalstart; i<ivalend; i++){
            if(valuesRef.current[3][i] !== null){
                spnotificationsetState({'text': valuesRef.current[3][i], 'svg': <XCloseIcon/>, 'visible': true, 'class': 'sp_notificationred'})
                return
            }
        }
        ClickButton(false)

        if(popupState['inputtype'] === 'image'){
            UpdateImage()
        }
        else if(popupState['extrainfo'] === 'deleteaccount'){

        }
        else if(popupState['extrainfo'] === 'deletechats'){

        }
        else{
            UpdateValue()
        }
    }

    async function UpdateValue(){
        let response_status = null
        let request = {"v": valuesRef.current[0], "t": valuesRef.current[1], "p": valuesRef.current[2]}
        let response = await fetch(import.meta.env.VITE_URL + 'loginregister/updatevalue/', {
            method: 'POST',
            body: JSON.stringify(request),
            credentials: 'include',
        }).then(res => {
            response_status = res.status()
            return res.json()
        }).then(data => data).catch(() => spnotificationsetState({'text': 'Could not connect to the server', 'svg': <XCloseIcon/>, 'visible': true, 'class': 'sp_notificationred'}))

        ClickButton(true)
        if(response_status === 401 || response_status === 403){
            navigate('/login', {state: '/settings'})
            return
        }
        else if(response_status === 200){
            popupState['setState'](valuesRef.current[0])
            spnotificationsetState({'visible': false})
        }
    }

    async function UpdateImage(){
        popupState['setState'](null, valuesRef.current[0])
        ClickButton(true)
        ClosePopUp()
        //valuesRef.current[1] = false
    }

    function ClickButton(active){
        if(active === false){
            spbuttonRef.current.classList.remove('sp_buttonactive')
            popupsetState(prevState => ({...prevState, 'textbuttoninit': prevState['textbutton'], 'textbutton': <BlocksLoad/>}))
        }
        else{
            spbuttonRef.current.classList.add('sp_buttonactive')
            popupsetState(prevState => ({...prevState, 'textbutton': prevState['textbuttoninit']}))
        }
    }

    function ClosePopUp(){
        popupsetState({'visible': false})
        valuesRef.current = [null, null, null, ['Field is empty', 'Password field is empty', 'Passwords do not match']]
        spnotificationsetState({'visible': false})
    }

    return(
        <>
        <div className='sp' style={popupState['visible'] === true ? ({opacity: '1', transform: 'none', pointerEvents: 'all'}) : ({opacity: '0', transform: 'scale(0.8)', pointerEvents: 'none'})}>
            <div className='sp_header'>
                <div className={popupState['headerred'] === true ? ('sp_red') : ('')} onClick={() => console.log(valuesRef.current)}>{popupState['header']}</div>
                <XCloseIcon className={'sp_close ' + popupState['classclose']} onClick={() => ClosePopUp()}/>
            </div>

            { (popupState['isadmin'] === true && popupState['extrainfo'] === 'deleteaccount') ? (
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
                                    <UsernamePhoneInput alwaysEmail={true} classtype='s' placeholder={popupState['placeholderfirst']} tabIndex="-1" onpressTab={FocusElement} onpressTabValue={'ps'} ref={spemailRef} autoFocus={true} valuesRef={valuesRef} valueIndex={0} typeIndex={1} warningIndex={3} warningvalueIndex={0} onpressEnter={ClickSubmitDelete} allowEmpty={popupState['allowEmpty']}/>
                                )
                            }
                            else if(popupState['inputtype'] === 'phone'){
                                return(
                                    <UsernamePhoneInput alwaysPhone={true} classtype='s' placeholder={popupState['placeholderfirst']} existnavbar={true} tabIndex="-1" onpressTab={FocusElement} onpressTabValue={'ps'} autoFocus={true} ref={spphoneRef} valuesRef={valuesRef} valueIndex={0} typeIndex={1} warningIndex={3} warningvalueIndex={0} onpressEnter={ClickSubmitDelete}/>
                                )
                            }
                            else if(popupState['inputtype'] === 'password'){
                                return(
                                    <PasswordInput classtype='s' placeholder={popupState['placeholderfirst']} tabIndex="-1"  onpressTab={FocusElement} onpressTabValue={'ps'} ref={sppasswordfirstRef} autoFocus={true} valuesRef={valuesRef} passwordIndex={2} warningIndex={3} warningvalueIndex={1} isconfirmpassword={false} onpressEnter={ClickSubmitDelete}/>
                                )
                            }
                            else if(popupState['inputtype'] === 'name'){
                                return(
                                    <SettingsNameInput placeholder={popupState['placeholderfirst']} tabIndex="-1" onpressTab={FocusElement} onpressTabValue={'ps'} autoFocus={true} ref={spnameRef} valuesRef={valuesRef} nameIndex={0} warningIndex={3} warningvalueIndex={0} onpressEnter={ClickSubmitDelete} allowEmpty={popupState['allowEmpty']}/>
                                )
                            }
                            else if(popupState['inputtype'] === 'image'){
                                return(
                                    <SettingsImage imageval={popupState['imageval']} valuesRef={valuesRef} warningIndex={3} warningvalueIndex={0} imageIndex={0}/>
                                )
                            }
                        })()
                    }
                    { popupState['visible'] === true ? (
                        <PasswordInput classtype='s' placeholder={popupState['placeholdersecond']} ref={sppasswordRef} tabIndex="-1" onpressTab={FocusElement} onpressTabValue={popupState['inputtype'] !== undefined ? popupState['inputtype'].slice(0, 2) : ''} valuesRef={valuesRef} passwordIndex={2} warningIndex={3} warningvalueIndex={popupState['inputtype'] === 'password' ? 2 : 1} isconfirmpassword={popupState['inputtype'] === 'password' ? true : false} onpressEnter={ClickSubmitDelete}/>
                    ) : (<></>)}
                    {popupState['inputtype'] === 'image' ? <div/> : ''}
                </div>
                <div className='sp_buttonholder'>
                    <div className={'sp_button' + (popupState['visible'] === true ? ' sp_buttonactive ' : ' ') + popupState['classbutton']} ref={spbuttonRef} onClick={() => ClickSubmitDelete()}>{popupState['textbutton']}</div>
                </div>
            </>)}
        </div>
        <div className='sp_notificationholder' style={spnotificationState['visible'] === true ? ({opacity: '1', transform: 'scale(1)', pointerEvents: 'all'}) : ({opacity: '0', transform: 'scale(0.8)', pointerEvents: 'none'})}>
            <div className='sp_notification'>
                <div>{spnotificationState['text']}</div>
                <div className={'sp_notificationsvg ' + spnotificationState['class']} onClick={() => spnotificationsetState(prevState => ({...prevState, 'visible': false}))}>{spnotificationState['svg']}</div>
            </div>
        </div>
        <div className='sp_darkbg' style={popupState['visible'] === true ? ({ opacity: '1', pointerEvents: 'all' }) : ({ opacity: '0', pointerEvents: 'none' })} onClick={() => ClosePopUp()}/>
        </>
    )
}