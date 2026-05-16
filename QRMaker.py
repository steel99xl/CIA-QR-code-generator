import urllib.request
import qrcode
import multiprocessing as mp
import http.server
import socketserver
import socket
import time
import PIL

Port = 8000
exitFlag = 0

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
    
    try:
        HttpPage = urllib.request.urlopen(url)
        
        for bline in HttpPage:
            line = bline.decode('utf-8')
            if(".cia" in line):
                if 'href="' in line:
                    start = line.find('href="') + 6
                    end = line.find('"', start)
                    if start > 5 and end > start:
                        filename = line[start:end]
                        Code = "http://"+IP+":"+str(Port)+"/"+filename
                        QRCode = qrcode.make(Code)
                        QRCode.show()
    except Exception as e:
        print(f"An error occurred whilst generating the QR code: {e}")

def Server(IP):
    handler = http.server.SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(('0.0.0.0', Port), handler) as httpd:
        print(f"Server started at http://{IP}:{Port}")
        print("Press Ctrl+C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")

if __name__ == "__main__":
    main()
