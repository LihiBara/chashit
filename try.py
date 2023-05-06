def send(packet):
    plen = len(packet)
    tosend = str(plen)+'#'+packet
    socket.sendall(tosend)

def recieve():
    solamit = ''
    plen = ''
    while solamit != '#':
        solamit = socket.recv(1).decode()
        if solamit != '#':
            plen += solamit
        plen = int(len)
        packet = socket.recv(plen).decode()


len# cmd="" /r/n, amount = "" /r/n, touser="" /r/n, fromuser="" /r/n, credit= "" /r/n
#לעשות split בין /r/n כדי לקבל כל פקודה בנפרד ולהעביר לפונקציה המתאימה לי כל cmd