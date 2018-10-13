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
                #time.sleep(5)
                file = open("testfile.txt","w")
                file.write(data)
                file.close()

                testsite_array = []
                with open('testfile.txt') as my_file:
                    for line in my_file:
                        if line[0] == "P":
                            phonenum = line[1:]
                            print("Primary Phone: " + phonenum)
                        if line[0] == "B":
                            backupnum = line[1:]
                            print("Backup Phone: " + backupnum)
                        if line[0] == "C":
                            car_color = line[1:]
                            print("Car Color: " + car_color)
                        if line[0] == "T":
                            car_type = line[1:]
                            print("Car Type: " + car_type)
                        if line[0] == "L":
                            car_license = line[1:]
                            print("License Plate: " + car_license)
                        if line[0] == "O":
                            Longitude = line[1:]
                            print("GPS Longitude: " + Longitude)
                        if line[0] == "A":
                            Latitude = line[1:]
                            print("GPS Latitude: " + Latitude)
                    testsite_array.append(line)
                
            except:
                print "App has disconnected"
                address = 0 #reset address
                stop = input("Try again? [Y=1 and N=2]")
                break #break loop begin checking if phone has reconnected

        if stop == 2: break
        
client_sock.close()
server_sock.close()
print "Program finished."
