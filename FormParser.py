def formParser(byteRequest: bytes):
    boundary = byteRequest.split(b'Content-Type: multipart/form-data; boundary=')[1]
    boundary = b'--' + boundary.split(b'\r\n')[0]
    #print(byteRequest)
    form_body = byteRequest.split(boundary)[1:-1]
    form = {}
    for field in form_body:
        name = field.split(b'"')[1].decode("utf-8")
        value = field.split(b'\r\n')[-2]
        form[name] = value

    return form





