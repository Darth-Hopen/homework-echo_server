import os
import socket
from http import HTTPStatus

HOST = "127.0.0.1"
PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    srv_address = (HOST, PORT)
    print(f'Starting on {srv_address}, pid: {os.getpid()}')

    s.bind(srv_address)
    s.listen(1)

    while True:
        print("Waiting for a connection...")
        conn, address = s.accept()
        print('Connection from: ', address)

        rec_bytes = conn.recv(1024)
        text = rec_bytes.decode('utf-8')

        method_from_request = text.split(" /")[0]
        headers_from_requst = text.split("\r\n")[1:]
        sub_str_with_status = text.split("\r\n")[0]
        try:
            status_from_request = int(sub_str_with_status.split(" ")[1].split("status=")[1])
            status = HTTPStatus(status_from_request)
        except:
            status = HTTPStatus(200)

        body = f"<div>Request Method: {method_from_request}</div>" \
               f"<div>Request Source: {srv_address}</div>" \
               f"<div>Response Status: {status.value} {status.name}</div>" \
               f"<br></br>"
        for item in headers_from_requst:
            body += f"<div>{item}</div>"

        status_line = f"HTTP/1.1 {status.value} {status.name}"
        headers = '\r\n'.join([
            status_line,
            f'Content-Length: {len(body)}',
            'Content-Type: text/html'
        ])

        resp = '\r\n\r\n'.join([
            headers,
            body
        ])

        conn.send(resp.encode('utf-8'))
        conn.close()
