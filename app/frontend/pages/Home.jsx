import '../styling/Home.css'
import { useEffect } from 'react'

export function Home(){

    useEffect(() => {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if(entry.isIntersecting){
                entry.target.classList.add('h_visible')
            }
        })
    }, {
        threshold: 0.5,
    })
    const contentElements = document.querySelectorAll('.h_content')
    contentElements.forEach(element => observer.observe(element))
    }, [])

    return(
        <div className='h_holder'>
            <div className='h_imgholder'>
                <img src='../components/images/SamplingLandingPage.jfif'/>
                <div className='h_imgtext1'><span>Welcome</span><span>to</span></div>
                <div className='h_imgtext2'>Sampling</div>
            </div>
            

            <div className='h_box'>
                <div className='h_content h_end'>
                    <div className='h_boximgholder'>
                        <img src='../components/images/Papers.jfif'/>
                    </div>
                </div>
                <div className='h_content h_start'>
                    <div className='h_boxtext'>
                        <b>Sampling</b> is is an AI chatbot designed to translate<br/> natural language input into appropriate<br/> production-scheduling commands.
                    </div>
                </div>
            </div>
            <div className='h_box'>
                <div className='h_content h_end'>
                    <div className='h_boxtext'>
                        To achieve this it ultilizes a fined-tuned<br/> version of <b>Llama 3.0</b><br/>
                        The natural language input is converted<br/> into appropriate XML parameters<br/>
                        which are then sent to a server of<br/> University of Patras, that runs the proprietary<br/> production-scheduling functions.
                    </div>
                </div>
                <div className='h_content h_start'>
                    <div className='h_boximgholder'>
                        <img src='../components/images/SamplingLlama.jfif'/>
                    </div>
                </div>
            </div>

            <div className='h_endtext'>
                This program was developed by Chris Gertzos as part of his diploma thesis and was completed under the supervision of<br/> Emmanouil Bakopoulos and Kosmas Alexopoulos.
            </div>
        </div>
    )
}