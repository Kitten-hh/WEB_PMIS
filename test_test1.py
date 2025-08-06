
import requests
from pyamf import remoting,AMF3
from pyamf.flex import messaging
def getData():
    msg = messaging.RemotingMessage(operation='find',
                                destination='sysParamService',
                                messageId="sysParamService",
                                body=[{'CONDITION': "(ftype = 'DashBoardData')"},'Mainland'])
    req = remoting.Request(target='sysParamService', body=[msg])
    ev = remoting.Envelope(AMF3)
    ev['/0'] = req

    # Encode request
    bin_msg = remoting.encode(ev)        
    resp = requests.get('http://192.168.2.111:8888/SimpleErp/messagebroker/amf',
                    data=bin_msg.getvalue(),
                    headers={'Content-Type': 'application/x-amf'})

    # Decode response
    resp_msg = remoting.decode(resp.content)
    print(resp_msg.bodies)        

if __name__ == "__main__": 
    getData()

