import '../styling/Referal.css'
import { ArrowDownIcon } from '../components/svgs/UtilIcons'
import { Link } from 'react-router-dom'
import { useEffect, useState } from 'react'

export function Referal(){

    const [referalstate, referalsetState] = useState()

    useEffect(() => {
        let refval = []
        for(let i=0; i<5; i++){
            refval.push(<div className='referal_val'>
                                <div className='referal_val_header'>NBUKO&*()P</div>
                                <div className='referal_val_extra'>
                                    <div className='referal_val_exp'>
                                        <span>EXP</span>
                                        <span>13:33 9/31/2025</span>
                                    </div>
                                    <div className='referal_val_info'>
                                        REDEEMED
                                    </div>
                                </div>
                                <div className='referal_line'/>
                                <div className='referal_val_extra'>
                                    <div>
                                        chrisg@gmail.com
                                    </div>
                                    <div>
                                        15:30 9/30/2025
                                    </div>
                                </div>
                            </div>)
        }
        referalsetState(refval)
    },[])

    function CreateReferal(){
        referalsetState(oldstate => [...oldstate, <div className='referal_val'>
                                <div className='referal_val_header'>NBUKO&*()P</div>
                                <div className='referal_val_extra'>
                                    <div className='referal_val_exp'>
                                        <span>EXP</span>
                                        <span>13:33 9/31/2025</span>
                                    </div>
                                    <div className='referal_val_info'>
                                        REDEEMED
                                    </div>
                                </div>
                                <div className='referal_line'/>
                                <div className='referal_val_extra'>
                                    <div>
                                        chrisg@gmail.com
                                    </div>
                                    <div>
                                        15:30 9/30/2025
                                    </div>
                                </div>
                            </div>])
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