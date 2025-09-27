import { GreeceIcon } from "./svgs/CountriesIcons"
import { GermanyIcon } from "./svgs/CountriesIcons"
import { AustriaIcon } from "./svgs/CountriesIcons"

const PhoneNumbers={
    'Europe/Athens': { 
    'n': +30,
    'c': 'GR',
    'svg': <GreeceIcon/>},

    'Europe/Berlin': {
        'n': +49,
        'c': 'DE',
        'svg': <GermanyIcon/>
    },

    'Austria': {
        'n': +43,
        'c': 'AT',
        'svg': <AustriaIcon/>
    }
}


export {PhoneNumbers}