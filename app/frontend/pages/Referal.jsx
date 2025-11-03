import '../styling/Referal.css'
import { ArrowDownIcon } from '../components/svgs/UtilIcons'
import { Link, useNavigate } from 'react-router-dom'
import { useEffect, useState } from 'react'

export function Referal(){

    const [referalstate, referalsetState] = useState([])
    const navigate = useNavigate()

    const [isloadingState, isloadingsetState] = useState(true)

    useEffect(() => {
        GetAllReferals()
    },[])

    async function CreateReferal(){
        let response_status = null
        let response = await fetch(import.meta.env.VITE_URL + 'referal/createreferal/', {
            method: 'POST',
            credentials: 'include',
        }).then(res => {
            response_status = res.status
            return res.json()
        }).then(data => data)

        if(response_status === 401 || response_status === 403){
            navigate('/login', {state: '/referalcodes'})
            return
        }
        else if(response_status === 200){
            let date_created = new Date(response['date_created'])
            referalsetState(oldstate => [
                <div className='r_val'>
                    <div className='r_val_header'>{response['value']}</div>
                    <div className='r_val_extra'>
                        <div className='r_val_exp'>
                            <span>EXP</span>
                            <span>{date_created.toLocaleString()}</span>
                        </div>
                        <div className='r_val_info'>
                            ACTIVE
                        </div>
                    </div>
                </div>,
                ...oldstate
            ])
        }
        
    }

    async function GetAllReferals(){
        let response_status = null
        let response = await fetch(import.meta.env.VITE_URL + 'referal/getallreferals/', {
            method: 'GET',
            credentials: 'include',
        }).then(res => {
            response_status = res.status
            return res.json()
        }).then(data => data)

        if(response_status === 401 || response_status === 403){
            navigate('login/')
            return
        }
        else if(response_status === 200){
            let update_val = []
            for(let i=0; i<response.length; i++){
                let exp_date = new Date(Date.parse(response[i]['date_created']) + 86400000)
                let status = null
                let extr_class = null
                let user_redeem = null
                let date_redeem = null
                
                if(response[i]['date_redeem'] !== null){
                    status = 'REDEEMED'
                    extr_class = ['r_line', 'r_val_extra']
                    date_redeem = new Date(Date.parse(response[i]['date_redeem'])).toLocaleString()
                    if(response[i]['userid_redeem__email'] === null){
                        user_redeem = response[i]['userid_redeem__phone']
                    }
                    else{
                        user_redeem = response[i]['userid_redeem__email']
                    }
                }
                else{
                    extr_class = ['display_none', 'display_none']
                    if(new Date() - exp_date > 0){
                        status = 'EXPIRED'
                    }
                    else{
                        status = 'ACTIVE'
                    }
                }

                update_val.push(
                    <div className='r_val'>
                        <div className='r_val_header'>{response[i]['value']}</div>
                        <div className='r_val_extra'>
                            <div className='r_val_exp'>
                                <span>EXP</span>
                                <span>{exp_date.toLocaleString()}</span>
                            </div>
                            <div className='r_val_info'>
                                {status}
                            </div>
                        </div>
                            <div className={extr_class[0]}/>
                            <div className={extr_class[1]}>
                                <div>{user_redeem}</div>
                                <div>{date_redeem}</div>
                            </div>
                    </div>
                )
            }
            
            referalsetState(update_val)
            isloadingsetState(false)

        }

    }

    return(
        <div className='r_holder'>
            <div className='r_outer'>
                <div className='r_box'>
                    <div className='r_utils'>
                        <Link to='/settings'>
                            <div className='r_util'>
                                <ArrowDownIcon style={{transform: 'rotate(90deg)'}} height={24} width={24}/>
                                Back
                            </div>
                        </Link>
                        <div className='r_util'>
                            <div className='r_create' style={isloadingState === true ? {backgroundColor: 'var(--color-text-main-hover-blue-experimental-lighter)', cursor: 'default'} : {}} onClick={() => isloadingState === false ? CreateReferal() : ''}>
                                Create
                                <div className='r_create_plus'>&#43;</div>
                            </div>
                        </div>
                    </div>
                    <div className='r_main'>
                        <div className='r_header'>
                            Referal Codes
                        </div>
                        <div className='r_val_holder' style={isloadingState === true ? {width: '100%'} : {width: '80%'}}>
                            {isloadingState === true ? (
                            <>
                                <div className='loading_box loading'/>
                                <div className='loading_box loading'/>
                                <div className='loading_box loading' style={{width: '90%'}}/>
                            </>
                            ) : (
                                <>
                                {referalstate.length === 0 ? (
                                    <div className='r_empty'>
                                        No referal codes created
                                    </div>
                                ) : (referalstate)}
                                </>
                                )
                            }
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}