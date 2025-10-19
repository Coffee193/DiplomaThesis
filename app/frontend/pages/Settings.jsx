import '../styling/Settings.css'
import { useEffect, useState, useRef } from 'react'
import { UserIconThin, PencilIcon, XCloseIcon, EyeIcon, EyeCloseIcon, Tick } from '../components/svgs/UtilIcons'
import { useNavigate, Link } from 'react-router-dom'
import html2canvas from 'html2canvas'

export function Settings({updatenavbarsetState}){
    
    const [simgState, simagesetState] = useState(<div className='s_img_dim s_loading'/>)
    const [snameholderState, snameholdersetState] = useState(<div className='s_loading_box s_loading'/>)
    const [scontentbodyState, scontentbodysetState] = useState(
        <>
            <div className='s_loading_box s_loading'/>
            <div className='s_loading_box s_loading' style={{width: '75%'}}/>
        </>
    )

    useEffect(() => {
        
    }, [])

    return(
        <div className='s_allholder'>
            <div className='s_mainholder'>
                <div className='s_box'>

                    <div className='s_img'>
                        <div className='s_imgholder'>
                            {simgState}
                        </div>
                        {snameholderState}
                    </div>

                    <div className='s_content'>
                        {scontentbodyState}
                    </div>

                </div>
            </div>
        </div>
    )
}