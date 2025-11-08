import { ChatNavSearch } from "./ChatNavSearch"
import { ChatNavPopUp } from "./ChatNavPopUp"
import { ChatNavRenameDelete } from "./ChatNavRenameDelete"

export function ChatNavUtils(){
    return(
        <>
            <ChatNavSearch/>
            <ChatNavPopUp/>
            <ChatNavRenameDelete/>
        </>
    )
}