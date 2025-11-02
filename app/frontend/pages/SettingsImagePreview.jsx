import '../styling/SettingsImagePreview.css'
import { XCloseIcon, Tick } from '../components/svgs/UtilIcons'
import { useRef } from 'react'
import html2canvas from 'html2canvas'

export function SettingsImagePreview({ previewState, previewsetState, imageinputRef, imageprevvalRef, imageState, imagesetState, boxsetState, valuesRef, warningIndex, warningvalueIndex, imageIndex }){

    const imgcanmoveRef = useRef(false)
    const imgmoveposRef = useRef()
    const imgholderRef = useRef()
    const screenshotRef = useRef()

    function PreviewClose(remove = false){
        previewsetState({'visible': false})
        if(remove === true){
            imageinputRef.current.value = ''
        }
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

    function Screenshot(){
        html2canvas(screenshotRef.current, {scale: 2}).then((canvas) => {
            let img = canvas.toDataURL('image/jpeg')
            if(imageprevvalRef.current[1] === false){
                imageprevvalRef.current = [imageState, true]
                valuesRef.current[warningIndex][warningvalueIndex] = null
            }
            imagesetState(img)
            boxsetState(true)
            PreviewClose()
            valuesRef.current[imageIndex] = img
            //valuesRef.current[1] = 'image'
        })
    }

    return(
        <>
            <div className='sip_holder' style={previewState['visible'] === false ? {display: 'none'} : {display: 'block'}}>
                <div className='sip_box'>
                    <div className='sip_circle'>
                        <div className='sip_circlescreenshot' ref={screenshotRef}>
                            <div className='sip_imgholder' onMouseDown={(event) => ImageMouseDown(event)} onMouseUp={() => ImageMouseUp()} onMouseMove={(event) => ImageMouseMove(event)} ref={imgholderRef}>
                                <img className='sip_img' src={previewState['img']}/>
                            </div>
                            <div className='sip_imgbg'/>
                        </div>
                    </div>
                </div>
                <div className='sip_utilholder'>
                    <div className='sip_util sip_accept' onClick={() => Screenshot()}><Tick width={24} height={24}/></div>
                    <div className='sip_util sip_cancel' onClick={() => PreviewClose(true)}><XCloseIcon/></div>
                </div>
            </div>
            <div className='sip_darkbg' style={previewState['visible'] === false ? {display: 'none'} : {display: 'block'}} onClick={() => PreviewClose(true)}/>
        </>
    )
}