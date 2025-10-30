import '../styling/SettingsImagePreview.css'
import { XCloseIcon, Tick } from '../components/svgs/UtilIcons'
import { useRef } from 'react'

export function SettingsImagePreview({ previewState, previewsetState }){

    const imgcanmoveRef = useRef(false)
    const imgmoveposRef = useRef()
    const imgholderRef = useRef()

    function PreviewClose(){
        previewsetState({'visible': false})
    }

    function ImageMouseDown(event){
        imgcanmoveRef.current = true
        imgmoveposRef.current = event.sclientX
    }

    function ImageMouseUp(){
        imgcanmoveRef.current = false
    }

    function ImageMouseMove(event){
        if(imgcanmoveRef.current === true){
            let pos = imgmoveposRef.current - event.clientX
            imgmoveposRef.current = event.clientX
            imgholderRef.current.style.left = (imgholderRef.current.offsetLeft - pos) + 'px'
        }
    }

    return(
        <>
            <div className='sip_holder' style={previewState['visible'] === false ? {display: 'none'} : {display: 'block'}}>
                <div className='sip_box'>
                    <div className='sip_circle'>
                        <div className='sip_circlescreenshot'>
                            <div className='sip_imgholder' onMouseDown={(event) => ImageMouseDown(event)} onMouseUp={() => ImageMouseUp()} onMouseMove={(event) => ImageMouseMove(event)} ref={imgholderRef}>
                                <img className='sip_img' src={previewState['img']}/>
                            </div>
                            <div className='sip_imgbg'/>
                        </div>
                    </div>
                </div>
                <div className='sip_utilholder'>
                    <div className='sip_util sip_accept'><Tick width={24} height={24}/></div>
                    <div className='sip_util sip_cancel'><XCloseIcon/></div>
                </div>
            </div>
            <div className='sip_darkbg' style={previewState['visible'] === false ? {display: 'none'} : {display: 'block'}} onClick={() => PreviewClose()}/>
        </>
    )
}