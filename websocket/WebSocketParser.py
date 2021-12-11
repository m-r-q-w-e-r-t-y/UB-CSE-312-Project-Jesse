import json

"""
Helps get payload given frame
"""
class WebSocketParser:
    frame = None
    payload = None
    payloadLength = None
    maskingKey = None

    def __init__(self, frame):
        self.frame = frame
        self.extractPayload()

    def extractPayload(self):
        self.payloadLength = self.frame[1] - 128
        self.maskingKey = self.frame[2:6]
        self.payload = bytearray(
            [self.frame[6:6 + self.payloadLength][i] ^ self.maskingKey[i % 4] for i in range(self.payloadLength)])

    def getPayload(self):
        return json.loads(self.payload.decode("utf-8"))

    def getOpcode(self):
        return self.frame[0] & 15

    def getMask(self):
        return self.frame[1] & 1

    def getPayloadLength(self):
        return self.frame[1] & 127
