# From https://github.com/perbu/dgram

import uselect
import usocket
import uasyncio
import boatData 

queue = boatData.RcvdMsgQueue()

# UDP server
class UDPServer:
    def __init__(self, polltimeout=1, max_packet=1024):
        self.polltimeout = polltimeout
        self.max_packet = max_packet

    
    def close(self):
        self.sock.close()

    async def serve(self, host, port, backlog=5):
        ai = usocket.getaddrinfo(host, port)[0]  # blocking!
        s = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)
        self.sock = s
        s.setblocking(False)
        s.bind(ai[-1])

        p = uselect.poll()
        p.register(s,uselect.POLLIN)
        to = self.polltimeout
        while True:
            try:
                if p.poll(to):
                    buf, addr = s.recvfrom(125)
                    queue.add(buf)
                    await uasyncio.sleep(0)
                await uasyncio.sleep(0)
            except uasyncio.core.CancelledError:
                # Shutdown server
                s.close()
                return