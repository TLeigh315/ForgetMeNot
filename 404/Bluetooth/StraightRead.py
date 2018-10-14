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
                print(data)
                testsite_array = []
                for line in data:
                    if line != "\n":
                        testsite_array.append(line)

                    else:
                        if testsite_array[0] == "P":
                            phonenum = testsite_array[1:]
                            print("Primary Phone: " + phonenum)
                        if testsite_array[0] == "B":
                            backupnum = testsite_array[1:]
                            print("Backup Phone: " + backupnum)
                        if testsite_array[0] == "C":
                            car_color = testsite_array[1:]
                            print("Car Color: " + car_color)
                        if testsite_array[0] == "T":
                            car_type = testsite_array[1:]
                            print("Car Type: " + car_type)
                        if testsite_array[0] == "L":
                            car_license = testsite_array[1:]
                            print("License Plate: " + car_license)
                        if testsite_array[0] == "O":
                            Longitude = testsite_array[1:]
                            print("GPS Longitude: " + Longitude)
                        if testsite_array[0] == "A":
                            Latitude = testsite_array[1:]
                            print("GPS Latitude: " + Latitude)
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
