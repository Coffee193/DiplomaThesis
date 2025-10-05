let strdate = '2025-11-04 00:03:45+00:00'
let dateval = new Date(Date.parse(strdate))
let currentdate = new Date()
let day_ahead = new Date(currentdate.getTime() + 86400000)

console.log(dateval)
console.log(dateval.toLocaleString())
console.log(typeof dateval.toLocaleString())
console.log(currentdate)
console.log(currentdate.getTimezoneOffset())
console.log(currentdate - dateval)
console.log(dateval.getMonth())
console.log(dateval.getDate())
console.log(dateval.getFullYear())
console.log((currentdate - dateval) / (1000 * 60 * 60 * 24))
console.log(currentdate)
console.log(day_ahead)
console.log(dateval)
console.log(new Date(Date.parse(dateval) + 86400000))
console.log(new Date(Date.parse(strdate) + 86400000))
console.log('***********')
console.log(new Date() - dateval)
console.log((dateval - new Date()) / (1000 * 60 * 60 * 24))
console.log(dateval - new Date() > 86400000)

if(currentdate <= dateval){
    console.log('active')
}
else if(currentdate > dateval){
    console.log('expired')
}