import '../styling/termsPoliciesCheckbox.css'
import { Link } from 'react-router-dom'
import { forwardRef } from 'react'

export const TermsPoliciesCheckbox = forwardRef(({ valuesRef, warningIndex, warningvalueIndex}, termspoliciesRef) => {

    return(
        <div className='tpc_termsholder'>
            <div className='tpc_termscheckbox'>
                <input type='checkbox' onClick={(e) => { e.target.checked === true ? (valuesRef.current[warningIndex][warningvalueIndex] = null) : (valuesRef.current[warningIndex][warningvalueIndex] = 'You must agree to our Terms and Policies')}} ref={(element) => {termspoliciesRef !== null ? (termspoliciesRef.current = element) : ('')}}/>
            </div>
            <div>
                By Signing Up you agree to our <Link className='tpc_termslink' to='/termspolicies'>Terms of Use</Link> and our <Link className='tpc_termslink' to='/termspolicies'>Privacy Policy</Link>
            </div>
        </div>
    )
})