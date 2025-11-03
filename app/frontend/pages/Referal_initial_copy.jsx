import '../styling/Referal.css'
import { ArrowDownIcon } from '../components/svgs/UtilIcons'
import { Link, useNavigate } from 'react-router-dom'
import { useEffect, useState } from 'react'

export function Referal(){

    const [referalstate, referalsetState] = useState([])
    const navigate = useNavigate()

    useEffect(() => {
        GetAllReferals()
    },[])

    async function CreateReferal(){
        let response_status = null
        let response = await fetch('http://127.0.0.1:8000/referal/createreferal/', {
            method: 'POST',
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
            let date_created = new Date(response['date_created'])
            referalsetState(oldstate => [
                <div className='referal_val'>
                    <div className='referal_val_header'>{response['value']}</div>
                    <div className='referal_val_extra'>
                        <div className='referal_val_exp'>
                            <span>EXP</span>
                            <span>{date_created.toLocaleString()}</span>
                        </div>
                        <div className='referal_val_info'>
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
        let response = await fetch('http://127.0.0.1:8000/referal/getallreferals/', {
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
                    extr_class = ['referal_line', 'referal_val_extra']
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
                    <div className='referal_val'>
                        <div className='referal_val_header'>{response[i]['value']}</div>
                        <div className='referal_val_extra'>
                            <div className='referal_val_exp'>
                                <span>EXP</span>
                                <span>{exp_date.toLocaleString()}</span>
                            </div>
                            <div className='referal_val_info'>
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

        }

    }

    return(
        <div className='referal_holder'>
            <div className='referal_outer'>
                <div className='referal_box'>
                    <div className='referal_utils'>
                        <Link to='/settings'>
                            <div className='referal_util'>
                                <ArrowDownIcon style={{transform: 'rotate(90deg)'}} height={24} width={24}/>
                                Back
                            </div>
                        </Link>
                        <div className='referal_util'>
                            <div className='referal_create' onClick={() => CreateReferal()}>
                                Create
                                <div className='referal_create_plus'>&#43;</div>
                            </div>
                        </div>
                    </div>
                    <div className='referal_main'>
                        <div className='referal_header'>
                            Referal Codes
                        </div>
                        <div className='referal_val_holder'>
                            {referalstate}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}