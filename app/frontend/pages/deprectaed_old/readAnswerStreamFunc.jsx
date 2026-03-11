/* readAnswerStream_Old_DoesNotHaveUpdateTitle

export async function readAnswerStream(response, linkparams, convsetState, isgeneratingsetState){
    let ai_answer = ''

    await response.read().then(function readchunk({done, value}) {
        console.log(window.location.pathname)
        if(window.location.pathname.split("/").at(-2) !== linkparams.id){
            console.log('ENDING stream')
            response.cancel()
            return
        }

        ai_answer += decodeURIComponent(encodeURIComponent(String.fromCharCode.apply(null, value)))
        convsetState(prevState => [
        <div className='cm_chatbox'>
            {ai_answer}
        </div>,
        prevState.slice(1)
        ])

        if(done){
            isgeneratingsetState(false)
            return
        }
        return response.read().then(readchunk)
    })
}

*/

/* Wont cancel any more. Instead do it like ChatGPT and DeepSeek. Keep it Open but dont start multiple ones

export async function readAnswerStream(response, linkparams, convsetState, isgeneratingsetState, chatnavsetState, chatnavState){
    let ai_answer = ''
    console.log(chatnavState)
    console.log('aaa')

    await response.read().then(function readchunk({done, value}) {
        if(window.location.pathname.split("/").at(-2) !== linkparams.id){
            response.cancel()
            return
        }

        // You need to put this here. Basically after the last part is received this function runs another time with value = undefined
        // and done = True. passing undefined in String.fromChatCo.. gives '', which when passed on JSON.parse throws an error
        if(done){
            isgeneratingsetState(false)
            return
        }

        let ret_stream = JSON.parse(decodeURIComponent(encodeURIComponent(String.fromCharCode.apply(null, value))))

        // An initial value of {'v': ''} is returned from that function. This is so that the cookies are Instantly set, otherwise the
        // cookies wont be set until a single answer token is produced
        if(ai_answer === '' && ret_stream['v'] === ''){
            return response.read().then(readchunk)
        }

        ai_answer += ret_stream['v']
        convsetState(prevState => [
        <div className='cm_chatbox'>
            {ai_answer}
        </div>,
        prevState.slice(1)
        ])

        return response.read().then(readchunk)
    })
}
*/

export async function readAnswerStream(response, linkparams, convsetState, isgeneratingsetState, chatnavsetState, chatnavState, convstreamgeneratingRef){
    let ai_answer = ''
    console.log(chatnavState)
    console.log('aaa')

    await response.read().then(function readchunk({done, value}) {

        // You need to put this here. Basically after the last part is received this function runs another time with value = undefined
        // and done = True. passing undefined in String.fromChatCo.. gives '', which when passed on JSON.parse throws an error
        if(done){
            convstreamgeneratingRef.current.delete(linkparams.id)
            if(window.location.pathname.split("/").at(-2) === linkparams.id){
                isgeneratingsetState(false)
            }
            return
        }

        let ret_stream = JSON.parse(decodeURIComponent(encodeURIComponent(String.fromCharCode.apply(null, value))))

        // An initial value of {'v': ''} is returned from that function. This is so that the cookies are Instantly set, otherwise the
        // cookies wont be set until a single answer token is produced
        if(ai_answer === '' && ret_stream['v'] === ''){
            return response.read().then(readchunk)
        }

        ai_answer += ret_stream['v']

        if(window.location.pathname.split("/").at(-2) === linkparams.id){
            convsetState(prevState => [
            <div className='cm_chatbox'>
                {ai_answer}
            </div>,
            prevState.slice(1)
            ])
        }

        return response.read().then(readchunk)
    })
}