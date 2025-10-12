export function pressKey(event, onpressEnter, onpressEnterValue, onpressTab, onpressTabValue){
        if(onpressEnter !== undefined){
            if(event.key === 'Enter'){
                if(onpressEnterValue !== undefined){
                    setTimeout(function(){
                        onpressEnter(onpressEnterValue)
                    }, 50)
                }
                else{
                    onpressEnter()
                }
            }
        }
        if(event.key === 'Tab'){
            if(onpressTab !== undefined){
                if(onpressTabValue !== undefined){
                    setTimeout(function(){
                        onpressTab(onpressTabValue)
                    }, 50)
                }
                else{
                    onpressTab()
                }
            }
            else{
                event.preventDefault()
            }
        }
    }