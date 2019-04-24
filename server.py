import socket
import struct

PACKET_SIZE = 1472
PAYLOAD_SIZE = 1466
PAYLOAD_SIZE_BITS = PAYLOAD_SIZE * 8

RECV_SIZE = 1500

class Rush():
    def __init__(self, header_binary, data):
        self.sequence_number_binary = header_binary[:16]
        self.ack_number_binary = header_binary[16:32]
        self.flags_binary = header_binary[32:37]
        self.reserved = header_binary[37:49]
        self.bottom_bits = self.flags_binary + self.reserved
        self.data = data
        self.data_decoded = data.decode('UTF-8')
        self.flags = {'ACK':self.flags_binary[0], 'NAK':self.flags_binary[1], 'GET':self.flags_binary[2], 
                    'DAT':self.flags_binary[3], 'FIN': self.flags_binary[4]}
        


    def FIN_packet(self):
        self.set_flag(4)

        pkt = struct.pack('>hhh', 
            int(self.sequence_number_binary,2),
            int(self.ack_number_binary,2),
            int(self.bottom_bits,2)
            )
    
        return pkt
                
    
    def set_flag(self, flag_pos):
        new_flag = ''
        i = 0
        while i <= 4:
            if i == flag_pos:
                new_flag += '1'
            else:
                new_flag += '0'
            i = i+1
        self.flags_binary = new_flag
        self.bottom_bits = self.flags_binary + self.reserved




class host():
    def __init__(self):
        self.host_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host_socket.bind(('localhost', 0))
        print(self.host_socket.getsockname()[1])
        print(self.host_socket.getsockname()[0])

        while(True):
            pkt, addr = self.host_socket.recvfrom(4096)
            print('Connected with ' + addr[0] + ':' + str(addr[1]))
            header, data = self.packet_spliter(pkt)
            pkt = Rush(header, data)
            fin_pack = pkt.FIN_packet()
            self.host_socket.sendto(fin_pack, addr)


    def pkt_task(self, pkt):
        if pkt.flags['ACK'] == 1:
            pass
        if pkt.flags['NAK'] == 1:
            pass
        if pkt.flags['GET'] == 1:
            pass
        if pkt.flags['DAT'] == 1:
            pass
        if pkt.flags['FIN'] == 1:
            pass


    def packet_spliter(self, pkt):
        header_hex = bytes(pkt)[:6]
        hbt = struct.unpack('>hhh', header_hex)  #header_binary_tuple
        header_binary = '{0:016b}{1:016b}{2:016b}'.format(hbt[0], hbt[1], hbt[2])
        data_hex = bytes(pkt)[7:]
        return (header_binary, data_hex)

    

  
def main():
    server = host()

if __name__ == "__main__":
    main()