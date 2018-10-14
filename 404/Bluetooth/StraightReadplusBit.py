import bluetooth
import time

#phone is server because it's initiating connection and sending stuff to RPi
def assignValues():
                data = client_sock.recv(1024)
                testsite_array = []
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

    return {"phonenum": phonenum, "backupnum":backupnum, "car_color":car_color, "car_type":car_type, "car_license":car_license, "Longitude":Longitude, "Latitude":Latitude}

def connected2App():
    server_sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 1
    server_sock.bind(("",port))
    server_sock.listen(1)
    client_sock,address = server_sock.accept() #recieve phone's MAC

    if (address == ('50:77:05:A7:B3:99', 1)): #if connected to phone
        print("Accepted connection from " + address)
        connected = True
    else: connected = False
    return connected
     
while (True):
    if connected2App == True:
        while (True):
            try:
                data = client_sock.recv(1024)
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
                print ("App has disconnected")
                address = 0 #reset address
                break #break loop begin checking if phone has reconnected
        
client_sock.close()
server_sock.close()
print ("Program finished.")
