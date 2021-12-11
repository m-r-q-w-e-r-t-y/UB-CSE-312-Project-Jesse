import json

"""
Helps pack frames given payload
"""
class WebSocketPacker:

    # Given payload packs frame
    @staticmethod
    def packFrame(responseData):
        payload = bytearray(json.dumps(responseData).encode())
        payloadSize = len(payload)

        headerFrame = [129]

        if payloadSize < 126:
            headerFrame += [payloadSize]
            headerFrame = bytearray(headerFrame)
        else:
            headerFrame = b'\x81\x7E'
            byteValues = [((payloadSize & 0xFF00) >> 8).to_bytes(1, "big"), (payloadSize & 0xFF).to_bytes(1, "big")]
            for byte in byteValues:
                headerFrame += byte

            headerFrame = bytearray(headerFrame)

        entireFrame = headerFrame + payload
        return entireFrame
