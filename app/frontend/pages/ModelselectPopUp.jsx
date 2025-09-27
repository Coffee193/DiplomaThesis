import '../styling/ModelSelectPopUp.css'
import { useEffect, useState, useRef } from 'react'
import { XCloseIcon, Tick } from '../components/svgs/UtilIcons'

export function ModelSelectPopUp( {BlurClassName, modelpopupclicked, changemodel} ){

    const [modelselectState, modelselectsetState] = useState([<Tick/>, , ])
    const modelselectref = useRef()
    const popuppagebackgroundref = useRef()

    useEffect(() => {
        if(modelpopupclicked === 0){
            return
        }
        modelselectref.current.style.opacity = '1'
        modelselectref.current.style.transform = 'scale(1.2, 1.2)'
        modelselectref.current.style.pointerEvents = 'all'
        document.getElementsByClassName(BlurClassName)[0].classList.add('blur_element')
        popuppagebackgroundref.current.style.pointerEvents = 'all'
    }, [modelpopupclicked])
    

    function ClickModel(index, modelname){
        let model_array = [, , ]
        model_array[index] = <Tick/>
        modelselectsetState(model_array)
        CloseModelSelectPopUp()
        changemodel(modelname)
    }

    function CloseModelSelectPopUp(){
        document.getElementsByClassName(BlurClassName)[0].classList.remove('blur_element')
        modelselectref.current.style.opacity = '0'
        modelselectref.current.style.transform = 'scale(1, 1)'
        modelselectref.current.style.pointerEvents = 'none'
        popuppagebackgroundref.current.style.pointerEvents = 'none'
    }

    return(
        <div className='modelselect_allholder' ref={popuppagebackgroundref} onClick={() => CloseModelSelectPopUp()}>
            <div className='modelselect_mainholder' ref={modelselectref}>
                <div className='modelselect_maintext'>
                    Select Model
                    <div className='modelselect_close' onClick={() => CloseModelSelectPopUp()}>
                        <XCloseIcon/>
                    </div>
                </div>
                <ul className='modelselect_modelholder'>
                    <li onClick={() => ClickModel(0, 'Llama 3.0')}><div className='modelselect_name'>Llama 3.0</div><div>{modelselectState[0]}</div></li>
                    <li onClick={() => ClickModel(1, 'ChatGPT 4.0')}><div className='modelselect_name'>ChatGPT 4.0</div><div>{modelselectState[1]}</div></li>
                    <li onClick={() => ClickModel(2, 'Llama 2.0')}><div className='modelselect_name'>Llama 2.0</div><div>{modelselectState[2]}</div></li>
                </ul>
                <div className='modelselect_lowertext'>
                    An existing conversation's model cannot change
                </div>
            </div>
        </div>
    )
}