import '../styling/SettingsPopUp.css'
import { XCloseIcon, BlocksLoad, Tick } from '../components/svgs/UtilIcons'
import { UsernamePhoneInput } from './UsernamePhoneInput'
import { PasswordInput } from './PasswordInput'
import { SettingsNameInput } from './SettingsNameInput'
import { SettingsImage } from './SettingsImage'
import { useState, useRef } from 'react'
import { useNavigate } from 'react-router-dom'

export function SettingsPopUp({ popupState, popupsetState, valuesRef, notificationsetState, updatenavbarsetState}){

    //const [spnotificationState, spnotificationsetState] = useState({'text': '', 'svg': null, 'visible': false, 'class': null})
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
        let ivalstart = popupState['extrainfo'] === 'deleteaccount' || popupState['extrainfo'] === 'deletechats' ? 1 : 0
        let ivalend = popupState['extrainfo'] === 'deleteaccount' || popupState['extrainfo'] === 'deletechats' ? 3 : 2
        for(let i=ivalstart; i<ivalend; i++){
            if(valuesRef.current[3][i] !== null){
                notificationsetState({'text': valuesRef.current[3][i], 'svg': <XCloseIcon/>, 'visible': true, 'class': 's_notificationred'})
                return
            }
        }
        ClickButton(false)

        if(popupState['inputtype'] === 'image'){
            UpdateImage()
        }
        else if(popupState['extrainfo'] === 'deleteaccount'){
            DeleteAccount()
        }
        else if(popupState['extrainfo'] === 'deletechats'){
            DeleteAllChats()
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
            response_status = res.status
            return res.json()
        }).then(data => data)
        .catch(() => notificationsetState({'text': 'Could not connect to the server', 'svg': <XCloseIcon/>, 'visible': true, 'class': 's_notificationred'}))

        ClickButton(true)
        if(response_status === 401 || response_status === 403){
            navigate('/login', {state: '/settings'})
            return
        }
        else if(response_status === 409){
            notificationsetState({'text': response, 'svg': <XCloseIcon/>, 'visible': true, 'class': 's_notificationred'})
        }
        else if(response_status === 200){
            if(popupState['setState'] !== undefined){
                popupState['setState'](valuesRef.current[0])
            }
            notificationsetState({'text': response, 'visible': true, 'svg': <Tick/>, 'class': 's_notificationgreen'})
            if(valuesRef.current[1] === 'name'){
                updatenavbarsetState(prevState => ({...prevState, 'name': valuesRef.current[0]}))
            }
            ClosePopUp(true)
        }
    }

    async function UpdateImage(){
        let response_status = null
        let request = {"p": valuesRef.current[2]}
        let formdata = new FormData()
        formdata.append("data", JSON.stringify(request))
        formdata.append("img", JSON.stringify(valuesRef.current[0]))
        let response = await fetch(import.meta.env.VITE_URL + 'loginregister/updateimage/', {
            method: 'POST',
            credentials: 'include',
            body: formdata,
        }).then(res => {
            response_status = res.status
            return res.json()
        }).then(data => data)
        .catch(() => notificationsetState({'text': 'Could not connect to the server', 'svg': <XCloseIcon/>, 'visible': true, 'class': 's_notificationred'}))

        ClickButton(true)
        if(response_status === 403 || response_status === 401){
            navigate('/login')
            return
        }
        else if(response_status === 415 || response_status === 409 || response_status === 413){
            notificationsetState({'text': response, 'svg': <XCloseIcon/>, 'visible': true, 'class': 's_notificationred'})
            return
        }
        else if(response_status === 200){
            popupState['setState'](null, valuesRef.current[0])
            notificationsetState({'text': 'Image successfully updated', 'visible': true, 'svg': <Tick/>, 'class': 's_notificationgreen'})
            updatenavbarsetState(prevState => ({...prevState, 'image': valuesRef.current[0]}))
            ClosePopUp(true)
        }
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

    function ClosePopUp(keepnotification = false){
        popupsetState({'visible': false})
        valuesRef.current = [null, null, null, ['Field is empty', 'Password field is empty', 'Passwords do not match']]
        if(keepnotification === false){
            notificationsetState({'visible': false})
        }
    }

    async function DeleteAllChats(){
        let response_status = null
        let request = {"v": valuesRef.current[0], "t": valuesRef.current[1]}
        let response = await fetch(import.meta.env.VITE_URL + 'chats/deleteallchats/', {
            method: 'DELETE',
            credentials: 'include',
            body: JSON.stringify(request),
        }).then(res => {
            response_status = res.status
            return res.json()
        }).then(data => data)
        .catch(() => notificationsetState({'text': 'Could not connect to the server', 'svg': <XCloseIcon/>, 'visible': true, 'class': 's_notificationred'}))


        ClickButton(true)
        if(response_status === 403 || response_status === 401){
            navigate('/login')
            return
        }
        else if(response_status === 200){
            notificationsetState('All Chats Successfully Deleted! (' + response + ')')
            ClosePopUp(true)
        }
    }

    async function DeleteAccount(){
        let response_status = null
        let request = {"v": valuesRef.current[0], "t": valuesRef.current[1]}
        let response = await fetch(import.meta.env.VITE_URL + 'loginregister/deleteaccount/', {
            method: 'DELETE',
            body: JSON.stringify(request),
            credentials: 'include',
        }).then(res => {
            response_status = res.status
            return res.json()
        }).then(data => data)
        .catch(() => notificationsetState({'text': 'Could not connect to the server', 'svg': <XCloseIcon/>, 'visible': true, 'class': 's_notificationred'}))

        ClickButton(true)
        if(response_status === 403 || response_status === 401){
            navigate('/login')
            return
        }
        else if(response_status === 200){
            navigate('/')
            window.location.reload()
        }
        else if(response_status === 409){
            notificationsetState({'text': response, 'svg': <XCloseIcon/>, 'visible': true, 'class': 's_notificationred'})
        }
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
                                    <UsernamePhoneInput alwaysPhone={true} classtype='s' placeholder={popupState['placeholderfirst']} existnavbar={true} tabIndex="-1" onpressTab={FocusElement} onpressTabValue={'ps'} autoFocus={true} ref={spphoneRef} valuesRef={valuesRef} valueIndex={0} typeIndex={1} warningIndex={3} warningvalueIndex={0} onpressEnter={ClickSubmitDelete} allowEmpty={popupState['allowEmpty']}/>
                                )
                            }
                            else if(popupState['inputtype'] === 'password'){
                                return(
                                    <PasswordInput classtype='s' placeholder={popupState['placeholderfirst']} tabIndex="-1"  onpressTab={FocusElement} onpressTabValue={'ps'} ref={sppasswordfirstRef} autoFocus={true} valuesRef={valuesRef} passwordIndex={0} warningIndex={3} warningvalueIndex={popupState['extrainfo'] === 'deleteaccount' || popupState['extrainfo'] === 'deletechats' ? 1 : 0} isconfirmpassword={false} onpressEnter={ClickSubmitDelete}/>
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
                        <PasswordInput classtype='s' placeholder={popupState['placeholdersecond']} ref={sppasswordRef} tabIndex="-1" onpressTab={FocusElement} onpressTabValue={popupState['inputtype'] !== undefined ? popupState['inputtype'].slice(0, 2) : ''} valuesRef={valuesRef} passwordIndex={popupState['extrainfo'] === 'deleteaccount' || popupState['extrainfo'] === 'deletechats' ? 0 : 2} warningIndex={3} warningvalueIndex={popupState['extrainfo'] === 'deleteaccount' || popupState['extrainfo'] === 'deletechats' ? 2 : 1} isconfirmpassword={popupState['extrainfo'] === 'deleteaccount' || popupState['extrainfo'] === 'deletechats' ? true : false} onpressEnter={ClickSubmitDelete}/>
                    ) : (<></>)}
                    {popupState['inputtype'] === 'image' ? <div/> : ''}
                </div>
                <div className='sp_buttonholder'>
                    <div className={'sp_button' + (popupState['visible'] === true ? ' sp_buttonactive ' : ' ') + popupState['classbutton']} ref={spbuttonRef} onClick={() => ClickSubmitDelete()}>{popupState['textbutton']}</div>
                </div>
            </>)}
        </div>
        {/*<div className='sp_notificationholder' style={spnotificationState['visible'] === true ? ({opacity: '1', transform: 'scale(1)', pointerEvents: 'all'}) : ({opacity: '0', transform: 'scale(0.8)', pointerEvents: 'none'})}>
            <div className='sp_notification'>
                <div>{spnotificationState['text']}</div>
                <div className={'sp_notificationsvg ' + spnotificationState['class']} onClick={() => spnotificationsetState(prevState => ({...prevState, 'visible': false}))}>{spnotificationState['svg']}</div>
            </div>
        </div>*/}
        <div className='sp_darkbg' style={popupState['visible'] === true ? ({ opacity: '1', pointerEvents: 'all' }) : ({ opacity: '0', pointerEvents: 'none' })} onClick={() => ClosePopUp()}/>
        </>
    )
}