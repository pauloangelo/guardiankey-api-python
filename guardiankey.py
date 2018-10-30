import json
import base64
import time
import socket
import requests
from Crypto.Cipher import AES

# Please run register.py for generate your configuration
GKconfig = {}
GKconfig['agentid'] = ''
GKconfig['key'] = ''
GKconfig['iv'] = ''
GKconfig['service'] = 'TestService'
GKconfig['orgid'] = ''
GKconfig['authgroupid'] = ''
GKconfig['reverse'] = True

# You need define how the your system get client informations (IP, User-agent):
def getClientIP():
    #...
    ip = "1.1.1.1" # SET-ME
    return ip

def getUserAgent():
    #...
    UA="Set-me"
    return UA

def create_message(username,loginfailed=0,eventType='Authentication'):
    global GKconfig
    keyb64      = GKconfig['key']
    ivb64         = GKconfig['iv']
    agentid     = GKconfig['agentid']
    orgid       = GKconfig['orgid']
    authgroupid = GKconfig['authgroupid']
    reverse     = GKconfig['reverse']
    timestamp   = int(time.time())
    
    if agentid is not None:
        key = base64.b64decode(keyb64)
        iv  = base64.b64decode(ivb64)
        clientIP = getClientIP()
        UA = getUserAgent()
        sjson = {}
        sjson['generatedTime'] = timestamp
        sjson['agentId'] = agentid
        sjson['organizationId'] = orgid
        sjson['authGroupId'] = authgroupid
        sjson['service'] = GKconfig['service']
        sjson['clientIP'] = clientIP
        try:
            sjson['clientReverse'] = socket.gethostbyaddr(clientIP)[0] if reverse else ""
        except:
            sjson['clientReverse'] = ""
        sjson['userName'] = username
        sjson['authMethod'] = ''
        sjson['loginFailed'] = str(loginfailed)
        sjson['userAgent'] = UA
        sjson['psychometricTyped'] = ''
        sjson['psychometricImage'] = ''
        sjson['event_type'] = eventType
        message = json.dumps(sjson)
        obj = AES.new(key,AES.MODE_CFB, iv, segment_size=8)
        cryptmessage = base64.b64encode(obj.encrypt(message))
        return cryptmessage
        
def sendevent(username,loginfailed=0,eventType='Authentication'):
    global GKconfig
    message = create_message(username,loginfailed,eventType)
    payload = GKconfig['authgroupid']+"|"+message
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(payload, ('collector.guardiankey.net', 8888))

def checkaccess(username,loginfailed=0,eventType='Authentication'):
    global GKconfig
    message = create_message(username,loginfailed,eventType)
    tmpdata = {}
    tmpdata['id'] = GKconfig['authgroupid']
    tmpdata['message'] = message
    data = json.dumps(tmpdata)
    url = 'https://api.guardiankey.io/checkaccess'
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    query = requests.post(url, data=data, headers=headers)
    try:
        gkreturn = json.loads(query.text)
        return gkreturn
    except:
        return {"response":"ERROR"}

