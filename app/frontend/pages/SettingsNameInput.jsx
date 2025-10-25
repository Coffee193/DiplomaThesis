import '../styling/SettingsNameInput.css'

export function SettingsNameInput({ placeholder }){
    return(
        <div className='sni'>
            <input className='upi_s_border upi_s_height upi_s_padding sni_input' placeholder={placeholder}/>
        </div>
    )
}