import '../styling/ChatBoxUpload.css'
import { Document, XCloseIcon, BlocksLoad, ArrowUpload } from '../components/svgs/UtilIcons'

export function ChatBoxUpload({ cbuState, cbusetState, cbinputRef, UploadActive, EmptyTextArrowDeactive }){

    function CloseBoxUpload_Old(){
        cbusetState({'visible': false, 'isloading': true})
        cbinputRef.current.value = ''
        UploadActive()
        EmptyTextArrowDeactive()
    }

    function RemoveDocument(doc_id){
        cbusetState(prevState => ({...prevState, documents: prevState.documents.filter(doc => doc.id !== doc_id)}))
        cbinputRef.current.value = ''
        EmptyTextArrowDeactive()
    }

    function NameDot(name){
        if(name !== undefined && name.length >= 19){
            return name.slice(0, 17) + '...'
        }

        return name
    }

    function GenerateDocuments(){
        let doc_list = []
        for (const doc of cbuState['documents']){
            doc_list.push(
                <div className='cbu'>
                    {cbuState['inchat'] === true ? <a className='cbu_x' href={doc['hardpath'] === undefined ? import.meta.env.VITE_CHAT_DOCUMENT_PATH + doc['link'] + '_' + doc['id'] + '.' + doc['type'] : doc['hardpath']} download><ArrowUpload width={14} height={14} transform={'rotate(180)'}/></a> : doc['isloading'] === false ? <div className='cbu_x' onClick={() => RemoveDocument(doc.id)}><XCloseIcon width={14} height={14}/></div> : null}
                    <div className='cbu_document'>{doc['isloading'] === false || doc['inchat'] === true ? <Document width={30} height={30}/> : <BlocksLoad width={30} height={30}/>}</div>
                    <div className='cbu_info'>
                        <div className='cbu_top'>{NameDot(doc['name'])}</div>
                        <div className='cbu_bottom'>{doc['type']} {doc['size']}kB</div>
                    </div>
                </div>
            )
        }
        return doc_list
    }
    {/*<div className='cbu_holder' style={{...(cbuState['inchat'] === true && {justifyContent: 'end', width: '75%'})}}>*/}
    return(
        <>
        {cbuState['documents'].length !== 0 ? 
            <div className='cbu_holder' style={{...(cbuState['inchat'] === true && {maxWidth: '75%'})}}>
                {GenerateDocuments()}
            </div> : <></>
        }
        </>
    )
}