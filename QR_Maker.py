import urllib.request
import qrcode
import multiprocessing as mp
import http.server
import socketserver
import socket
import time
import PIL

#You probaly dont have to change this
mp.set_start_method('fork')
Port = 8000
exitFlat = 0

def main():
    IP = GetIP()
    ServerThread = mp.Process(target=Server, args=(IP,))
    QRThread = mp.Process(target=QR, args=(IP,))
    ServerThread.start()
    print("TEST")
    time.sleep(0.5)
    QRThread.start()

    ServerThread.join()
    QRThread.join()
    



def GetIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('1.3.3.7', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return str(IP)


def QR(IP):

    url = "http://"+IP+":"+str(Port)

    HttpPage = urllib.request.urlopen(url)

    for bline in HttpPage:
        line = str(bline)
        if(".cia" in line):
            line = line.strip("b'<li><a href=")
            line = line.strip('"')
            line = line.split('"',1)
            Code = IP+":"+str(Port)+"/"+str(line[0])

            QRCode = qrcode.make(Code)
            QRCode.show()





def Server(IP):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
   
    handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer((str(IP), Port), handler) as httpd:
        print("Server started...")
        httpd.serve_forever()





main()