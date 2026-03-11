import '../styling/ChatBody.css'
import { ChatBox } from './ChatBox'

export function ChatBody({ chatlist , isloadingState, chatnavState, chatnavsetState}){
    // pass chatnavsetState to ChatBody to update chatnavs when creatign a new Chat by asking question
    return(
        <div className = 'cbd_holder'>
            <div className='cbd_inner'>
                <div className='cbd_upper'>
                    <div className='cbd_image_holder'><img src='../components/images/MainLogo.png'/></div>
                    <div className='cbd_image_text'>How can I assist you?</div>
                </div>
                <ChatBox isloadingState={isloadingState} chatlist={chatlist} chattype='body' isgeneratingState={false} chatnavsetState={chatnavsetState}/>
            </div>
        </div>
)
}