import '../styling/TermsPolicies.css'
import { NavBar } from './NavBar'

export function TermsPolicies(){

    return(
        <div className='termspolicies_allholder'>
            <NavBar/>
            <div className='termspolicies_mainholder'>
                <div className='termspolicies_title'>
                    <div className='termspolicies_titlemain'>
                        Terms & Policies
                    </div>
                    <div className='termspolicies_titlesecond'>
                        Thanks for using Sampling! &#10024;
                    </div>
                </div>
                <div className='termspolicies_maintext'>
                    <span>This Software and associated files are the intellectual property of the author, Chris Gertzos</span>
                    <span><b>All rights are reserved.</b> Unauthorized copying, distribution, modification or use of this software, in whole or in part, is strictly prohibited without the express written permission of the author</span>
                    <span>This Software is provided for <b>academic review</b> and <b>examination purposes</b> only, and may not be used for commercial, educational, or research purposes beyond the scope of the diploma thesis without prior consent</span>
                </div>
            </div>
        </div>
    )

}