import '../styling/SettingsImage.css'
import { useState, useRef } from 'react'
import { SettingsImagePreview } from './SettingsImagePreview'

export function SettingsImage({ existimage }){

    const [siboxState, siboxsetState] = useState(existimage)
    const [siimageState, siimagesetState] = useState()

    const siinputRef = useRef()
    const [sipreviewState, sipreviewsetState] = useState({'visible': false})

    function SelectImage(){
        siinputRef.current.click()
    }

    function ImagePreview(){
        sipreviewsetState({'visible': true})
        let imgreader = new FileReader();
        imgreader.readAsDataURL(siinputRef.current.files[0])
        imgreader.onloadend = () => {
            sipreviewsetState(prevState => ({...prevState, 'img': imgreader.result}))
        }
    }

    return(
        <>
            <SettingsImagePreview previewState={sipreviewState} previewsetState={sipreviewsetState}/>
            <div className='si_box'>
                { siboxState === true ? (
                <>
                    <div className='si_holder'>
                        {siimageState}
                    </div>
                    <div className='si_utilholder'>
                        <div className='si_util si_utilblue'>CHANGE IMAGE</div>
                        <div className='si_util si_utilred'>DELETE IMAGE</div>
                    </div>
                </>
                ) : (
                    <div className='si_utilholder'>
                        <div className='si_util si_utilblue' onClick={() => SelectImage()}>UPLOAD IMAGE</div>
                    </div>
                )}
                <input type='file' className='si_input' accept='image/*' ref={siinputRef} onChange={() => ImagePreview()}/>
            </div>
        </>
    )
}