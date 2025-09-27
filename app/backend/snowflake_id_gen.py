import time
import warnings
'''
snowflake ids will be of the form:
64-bits
(its really close to Discord's snowflake id but has features from twitter as well)
https://www.youtube.com/watch?v=aLYKd7h7vgY

1st 42-bits: for timestamp (seconds since 21Dec 2023 00:00 UTC)
2nd: 5-bits: Gunicorn Worker ID ( how you get it -> https://stackoverflow.com/questions/34629514/get-worker-id-from-gunicorn-worker-itself
                                 not sure what this is -> https://stackoverflow.com/questions/38425620/gunicorn-workers-and-threads
                                 how it looks & why 5 bits -> https://gunicorn.org/)
3rd: 5-bits: Process ID (Above it was Worker ID/Thread ID, here it is proccess ID)
4-th: 12-bits: An increment (because its incrementing and it is 12 bits max value (in 10s representation) is 4096)
                that goes back to 0 every millisecond

For 2 ids to share the same value, 2 requests must have the same timestamp, be processed by same worker, by the same machine
, and the sequence number to have reached 4096 (because then we restrict the program from increasing it)

All this means that every single worker of every server/machine can handle 4096 requests per millisecond

#https://abheist.com/blogs/twitter-snowflake-for-unique-ids
This link is twitters
Instead of worker id and proccess id it has:
Datacenter id
machine id
which honestly i like more
'''

request_counter = -1
saved_lastreq_time = 0

def GenerateSnowflake(return_type = 'int'):
    warnings.warn('GenerateSnowflake: worker_id and department_id are hardcoded. Change them when Gunicord in production')
    warnings.warn('GenerateSnowflake: snowflakes are not thread safe! Reimplement this func when nginx is set for public testing')
    # https://stackoverflow.com/questions/2680902/python-django-global-variables
    global saved_lastreq_time
    global request_counter
    #print('saved_lr_t: ' + str(saved_lastreq_time))
    #print('rq_: ' + str(request_counter))
    request_time = int(time.time() * 1000)
    if(request_time - saved_lastreq_time > 0.001):
        request_counter = -1
    request_counter += 1
    saved_lastreq_time = int(time.time() * 1000)
    # timestamp worker_id department_id(or process_id haven't decided yet) request_num_this_millisecond
    if(return_type == 'int'):
        return int('{0:042b}'.format(request_time - 1703109600000) + '{0:05b}'.format(30) + '{0:05b}'.format(5) + '{0:012b}'.format(request_counter),2)
    if(return_type == 'hex'):
        return hex(int('{0:042b}'.format(request_time - 1703109600000) + '{0:05b}'.format(30) + '{0:05b}'.format(5) + '{0:012b}'.format(request_counter),2))
    # Note: id_ was the exact above variable that is now in return
    #print('id is:' +str(id_))
    #return id_
    #return int('{0:042b}'.format(request_time - 1703109600000) + '{0:05b}'.format(30) + '{0:05b}'.format(5) + '{0:012b}'.format(request_counter),2)

    ###
    #       WE WILL NOT UNITE THE FRONTEND AND BACKEND
    #       ALSO CALLED         HEADLESS ARCHITECTURE
    #       AS IT IS GENERALLY PREFERED
    #       https://www.google.com/search?q=does+amazon+use+headless+commerce&sca_esv=596374102&rlz=1C1JJTC_enGR995GR995&sxsrf=AM9HkKk3DXumSNG-iApDAZm3inRsQX5Vyw%3A1704642060232&ei=DMaaZa7iDeuoi-gPoYKDmA8&udm=&ved=0ahUKEwiumODDzsuDAxVr1AIHHSHBAPMQ4dUDCBA&uact=5&oq=does+amazon+use+headless+commerce&gs_lp=Egxnd3Mtd2l6LXNlcnAiIWRvZXMgYW1hem9uIHVzZSBoZWFkbGVzcyBjb21tZXJjZTIFECEYoAFIiElQ6gRYmUhwCHgAkAEBmAG2AaABhSWqAQQ0LjM1uAEDyAEA-AEBwgIKEAAYRxjWBBiwA8ICBBAjGCfCAhEQLhiDARjHARixAxjRAxiABMICDhAuGIAEGIoFGLEDGIMBwgILEAAYgAQYsQMYgwHCAgUQABiABMICCBAAGIAEGLEDwgIOEAAYgAQYigUYsQMYgwHCAggQABiABBjLAcICChAAGIAEGMsBGArCAgYQABgeGA3CAgcQIxiwAhgnwgIHEAAYgAQYDcICBhAAGBYYHsICBBAhGBXCAgUQIRifBcICBxAhGAoYoAHiAwQYACBBiAYBkAYI&sclient=gws-wiz-serp
    #       AMAZON USES IT (above Link)
    #       https://business.adobe.com/blog/the-latest/best-headless-ecommerce-platforms
    #       Also accroding to Adobe (Google etc.. -> Check Above Link)
    #       https://www.google.com/search?q=does+netflix+use+headless+commerce&sca_esv=596374102&rlz=1C1JJTC_enGR995GR995&sxsrf=AM9HkKkkm288fkiIsNpbEIIJ6xZYmuCTAQ%3A1704642105202&ei=OcaaZdmBDLOZi-gPndWS6Ak&udm=&ved=0ahUKEwiZgpnZzsuDAxWzzAIHHZ2qBJ0Q4dUDCBA&uact=5&oq=does+netflix+use+headless+commerce&gs_lp=Egxnd3Mtd2l6LXNlcnAiImRvZXMgbmV0ZmxpeCB1c2UgaGVhZGxlc3MgY29tbWVyY2UyCBAAGIAEGKIEMggQABiABBiiBDIIEAAYgAQYogQyCBAAGIAEGKIESIwWUIMFWPYRcAJ4AJABAJgBlgGgAd0GqgEDMC43uAEDyAEA-AEBwgIIECEYoAEYwwTCAgoQIRgKGKABGMMEwgIMECEYChigARjDBBgK4gMEGAEgQYgGAQ&sclient=gws-wiz-serp
    #       Also Netflix, Amazon, Uber (Check above Link)
    ###