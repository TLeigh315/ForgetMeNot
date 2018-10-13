import bluetooth

server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

port = 1
server_sock.bind(("",port))
server_sock.listen(1)

client_sock,address = server_sock.accept()
print "Accepted connection from ",address

data = client_sock.recv(1024)
file = open("testfile.txt","w")
file.write("Hello World.") 
file.close()
print "received [%s]" % data

while True:
    bd_addr = '50:77:05:A7:B3:99'
    server_sock.connect((bd_addr, port))
    server_sock.send("T32")

client_sock.close()
server_sock.close()
