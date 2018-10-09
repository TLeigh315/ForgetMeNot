import bluetooth
import time


#phone is server because it's initiating connection and sending stuff to RPi

while (True):
    server_sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 1
    server_sock.bind(("",port))
    server_sock.listen(1)
    client_sock,address = server_sock.accept() #recieve phone's MAC
    
    if (address == ('50:77:05:A7:B3:99', 1)): #if connected to phone
        print"Accepted connection from ", address

        while (True):
            try:
                data = client_sock.recv(1024) 
            except:
                print "App has disconnected"
                
                address = 0 #reset address
                break #break loop begin checking if phone has reconnected

client_sock.close()
server_sock.close()
print "Program finished."
