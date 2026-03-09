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