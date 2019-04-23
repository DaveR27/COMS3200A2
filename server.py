import socket

class host():
    def __init__(self):
        self.host_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host_socket.bind(('localhost', 0))
        print("Server listening")
        print(self.host_socket.getsockname()[1])
        print(self.host_socket.getsockname()[0])

        while(True):
            conn, addr = self.host_socket.recvfrom(4096)
            print('Connected with ' + addr[0] + ':' + str(addr[1]))

        self.host_socket.close()
  
def main():
    server = host()

if __name__ == "__main__":
    main()