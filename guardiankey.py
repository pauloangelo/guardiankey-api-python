import json
import hashlib
import base64
import time
import socket
import requests
from Crypto.Cipher import AES

# Please run register.py for generate your configuration
GKconfig = {}
GKconfig['email'] = ''
GKconfig['hashid'] = ''
GKconfig['key'] = ''
GKconfig['iv'] = ''
GKconfig['service'] = ''
GKconfig['orgid'] = ''
GKconfig['groupid'] = ''
GKconfig['reverse'] = ''

# You need define how the your system get client informations (IP, User-agent):

def getClientIP():
	#...
	return ip
	
def getUserAgent():
	#...
	return UA

def create_message(username):
	global GKconfig
	keyb64      = GKconfig['key']
	ivb64 	    = GKconfig['iv']
	hashid      = GKconfig['hashid']
	orgid       = GKconfig['orgid']
	authgroupid = GKconfig['groupid']
	reverse     = GKconfig['reverse']
	timestamp   = int(time.time())
	
	if hashid is not None:
		key = base64.b64decode(key64)
		iv  = base64.b64decode(ivb64)
		clientIP = getClientIP()
		UA = getUserAgent()
		sjson = {}
		sjson['generatedTime'] = timestamp
		sjson['agentId'] = hashid
		sjson['organizationId'] = orgid
		sjson['authGroupId'] = authgroupid
		sjson['service'] = GKconfig['service']
		sjson['clientIP'] = clientIP
		sjson['clientReverse '] = socket.gethostbyname_ex(ClientIP)
		sjson['userName'] = username
		sjson['authMethod'] = ''
		sjson['loginFailed'] = '0'
		sjson['userAgent'] = UA
		sjson['psychometricTyped'] = ''
		sjson['psychometricImage'] = ''
		message = json.dumps(sjson)
		obj = AES.new(key,AES.MODE_CFB, iv, segment_size=8)
        cryptmessage = base64.b64encode(obj.encrypt(message))
        return cryptmessage
		
def sendevent(username):
	global GKconfig
	guardianKeyWS='https://api.guardiankey.io/checkaccess'
	message = create_message(username)
	payload = GKconfig['hashid']+"|"+message
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.sendto(MESSAGE, ('collector.guardiankey.net', 8888))

def checkaccess(username):
	global GKconfig
	message = create_message(username)
	tmpdata = {}
	tmpdata['id'] = GKconfig['hashid']
	tmpdata['message'] = message
	data = json.dumps(tmpdata)
	url = 'https://api.guardiankey.io/checkaccess'
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	query = requests.post(url, data=data, headers=headers)
	return query

