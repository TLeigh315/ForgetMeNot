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

