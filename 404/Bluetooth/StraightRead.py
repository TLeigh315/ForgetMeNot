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
                testsite_array = []
                for line in data:
                    if line != "\n":
                        testsite_array.append(line)
                        if testsite_array[0] == "P" and testsite_array[-1] == '\r':
                            phonenum = ''.join(testsite_array[1:-1])
                            print("Primary Phone: " + phonenum)
                            
                        if testsite_array[0] == "B" and testsite_array[-1] == '\r':
                            backupnum = ''.join(testsite_array[1:-1])
                            print("Backup Phone: " + backupnum)
                            
                        if testsite_array[0] == "C" and testsite_array[-1] == '\r':
                            car_color = ''.join(testsite_array[1:-1])
                            print("Car Color: " + car_color)
                            
                        if testsite_array[0] == "T" and testsite_array[-1] == '\r':
                            car_type = ''.join(testsite_array[1:-1])
                            print("Car Type: " + car_type)
                            
                        if testsite_array[0] == "L" and testsite_array[-1] == '\r':
                            car_license = ''.join(testsite_array[1:-1])
                            print("License Plate: " + car_license)
                            
                        if testsite_array[0] == "O" and testsite_array[-1] == '\r':
                            Longitude = ''.join(testsite_array[1:-1])
                            print("GPS Longitude: " + Longitude)
                            
                        if testsite_array[0] == "A" and testsite_array[-1] == '\r':
                            Latitude = ''.join(testsite_array[1:-1])
                            print("GPS Latitude: " + Latitude)
                    else:
                        testsite_array = []
                
            except:
                print "App has disconnected"
                address = 0 #reset address
                stop = input("Try again? [Y=1 and N=2]")
                break #break loop begin checking if phone has reconnected
        if stop == 2: break
        
client_sock.close()
server_sock.close()
print "Program finished."
