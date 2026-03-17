import '../styling/SettingsImage.css'
import { useState, useRef } from 'react'
import { SettingsImagePreview } from './SettingsImagePreview'

export function SettingsImage({ imageval, valuesRef, warningIndex, warningvalueIndex, imageIndex }){

    const [siboxState, siboxsetState] = useState(imageval === undefined ? false : true)
    const [siimageState, siimagesetState] = useState(imageval)
    const imageprevvalRef = useRef([undefined, false])

    const siinputRef = useRef()
    const [sipreviewState, sipreviewsetState] = useState({'visible': false})

    function SelectImage(){
        siinputRef.current.click()
    }

    function ImagePreview(){
        if(siinputRef.current.value === ''){
            return
        }
        sipreviewsetState({'visible': true})
        let imgreader = new FileReader();
        imgreader.readAsDataURL(siinputRef.current.files[0])
        imgreader.onloadend = () => {
            sipreviewsetState(prevState => ({...prevState, 'img': imgreader.result}))
        }
    }

    function DeleteImage(){
        if(imageprevvalRef.current[1] === false){
            imageprevvalRef.current = [siimageState, true]
            valuesRef.current[warningIndex][warningvalueIndex] = null
        }
        else if(imageprevvalRef.current[0] === undefined){
            imageprevvalRef.current = [undefined, false]
            valuesRef.current[warningIndex][warningvalueIndex] = 'Image was not changed'
        }
        siboxsetState(false)
        siinputRef.current.value = ''
    }

    return(
        <>
            <SettingsImagePreview previewState={sipreviewState} previewsetState={sipreviewsetState} imageinputRef={siinputRef} imageprevvalRef={imageprevvalRef} boxsetState={siboxsetState} valuesRef={valuesRef} warningIndex={warningIndex} warningvalueIndex={warningvalueIndex} imagesetState={siimagesetState} imageIndex={imageIndex} imageState={imageval}/>
            <div className='si_box'>
                { siboxState === true ? (
                <>
                    <div className='si_holder'>
                        <img src={siimageState} className='si_image'/>
                    </div>
                    <div className='si_utilholder'>
                        <div className='si_util si_utilblue' onClick={() => SelectImage()}>CHANGE IMAGE</div>
                        <div className='si_util si_utilred' onClick={() => DeleteImage()}>DELETE IMAGE</div>
                    </div>
                </>
                ) : (
                    <div className='si_utilholder'>
                        <div className='si_util si_utilblue' onClick={() => SelectImage()}>UPLOAD IMAGE</div>
                    </div>
                )}
                <input type='file' className='si_input' accept='image/*' ref={siinputRef} onChange={() => ImagePreview()} onClick={() => siinputRef.current.value = null}/>
            </div>
        </>
    )
}