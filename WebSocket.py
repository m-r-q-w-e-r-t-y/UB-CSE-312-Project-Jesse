import json

class WebSocket:
    frame = None
    payload = None
    payloadLength = None
    maskingKey = None
    
    def __init__(self, frame):
        self.frame = frame
        self.extractPayload()

    def extractPayload(self):
        self.payloadLength = self.frame[1]-128
        self.maskingKey = self.frame[2:6]
        self.payload = bytearray([self.frame[6:6+self.payloadLength][i] ^ self.maskingKey[i%4] for i in range(self.payloadLength)])
        # # payload = bytearray([ encrypted_payload[i] ^ mask[i%4] for i in range(payload_len)])
        # index = 0
        # end = ""
        # while index < range(self.payloadLength):
        #     end+=(self.frame[6:6+self.payloadLength][i] ^ self.maskingKey[i%4])
        #     index+=1
        # self.payload = bytearray(end)

    def getPayload(self):
        return self.payload

    def getOpcode(self):
        return self.frame[0] & 15

    def getMask(self):
        return self.frame[1] & 1

    def getPayloadLength(self):
        return self.frame[1] & 127

    def toStringOpcode(self):
        return format(self.getOpcode(), "04b")

    def toStringMask(self):
        return format(self.getMask(), "01b")

    def toStringPayloadLength(self):
        return format(self.getPayloadLength(), "07b")

    def getResponse(self):
        payload = self.replaceHTML()
        frame = [129] + [len(payload)]
        return bytearray(frame) + payload

    def replaceHTML(self):
        dictPayload = json.loads(self.payload.decode("utf-8"))
        for k in dictPayload:
            if "&" in dictPayload[k]: 
                dictPayload[k] = dictPayload[k].replace("&", "&amp")
                self.payloadLength += 3
            if "<" in dictPayload[k]:
                dictPayload[k] = dictPayload[k].replace("<", "&lt")
                self.payloadLength += 2
            if ">" in dictPayload[k]:
                dictPayload[k] = dictPayload[k].replace(">", "&gt")
                self.payloadLength += 2
        jsonDict = json.dumps(dictPayload)
        return bytearray(jsonDict.encode())

    def dictionary(self):
        return json.loads(self.replaceHTML().decode("utf-8"))





    # def getDecodedFrame(self):
    #     # payloadLen = self.frame[1]-128

    #     # mask = self.frame[2:6]
    #     # encrypted_payload = self.frame[6:6+payload_len]

    #     # payload = bytearray([ encrypted_payload[i] ^ mask[i%4] for i in range(payload_len)])

    #     # return payload