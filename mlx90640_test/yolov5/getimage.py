import serial, time
import datetime as dt
import numpy as np
import cv2
import schedule
import subprocess

# function to get Emissivity from MCU
def get_emissivity(ser):
    ser.write(serial.to_bytes([0xA5,0x55,0x01,0xFB]))
    read = ser.read(4)
    return read[2]/100

# function to get temperatures from MCU (Celsius degrees x 100)
def get_temp_array(d):

    # getting ambient temperature
    T_a = (int(d[1540]) + int(d[1541])*256)/100

    # getting raw array of pixels temperature
    raw_data = d[4:1540]
    T_array = np.frombuffer(raw_data, dtype=np.int16)
    
    return T_a, T_array

# function to convert temperatures to pixels on image
def td_to_image(f):
    norm = np.uint8((f/100 - Tmin)*255/(Tmax-Tmin))
    norm.shape = (24,32)
    return norm

########################### Main cycle #################################
# Color map range
Tmax = 40
Tmin = 20

print ('Configuring Serial port')
ser = serial.Serial ('/dev/serial0')
ser.baudrate = 115200

# set frequency of module to 4 Hz
ser.write(serial.to_bytes([0xA5,0x25,0x01,0xCB]))
time.sleep(0.1)

# Starting automatic data colection
ser.write(serial.to_bytes([0xA5,0x35,0x02,0xDC]))
t0 = time.time()

# initialize the first frame
data = ser.read(1544)
Ta, temp_array = get_temp_array(data)
ta_img = td_to_image(temp_array)

# Image processing
img = cv2.applyColorMap(ta_img, cv2.COLORMAP_JET)
img = cv2.resize(img, (1280, 720), interpolation = cv2.INTER_LINEAR) # menggunakan cv2.INTER_LINEAR
img = cv2.flip(img, 0)

try:
    while True:
        # waiting for data frame
        ser = serial.Serial ('/dev/serial0')
        ser.baudrate = 115200
        ser.write(serial.to_bytes([0xA5,0x25,0x01,0xCB]))
        time.sleep(1)
        data = ser.read(1544)
        
        # The data is ready, let's handle it!
        Ta, temp_array = get_temp_array(data)
        ta_img = td_to_image(temp_array)
        
        # Image processing
        img = cv2.applyColorMap(ta_img, cv2.COLORMAP_JET)
        img = cv2.resize(img, (1280, 720), interpolation = cv2.INTER_LINEAR)
        img = cv2.flip(img, 1)
        
        #text = 'Tmin = {:+.1f} Tmax = {:+.1f} FPS = {:.2f}'.format(temp_array.min()/100, temp_array.max()/100, 1/(time.time() - t0))
        #cv2.putText(img, text, (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1)
        #cv2.imshow('Output', img)
        #schedule.every(1).minute.do(taking_picture)
        # Saving of picture
        fname = '/home/ayualr/mlx90640_test/yolov5/test_image/thermal_output.jpg'
        cv2.imwrite(fname, img)
        path = r'/home/ayualr/mlx90640_test/yolov5/test_image/thermal_output.jpg'
        image = cv2.imread(path)
        cv2.imshow('Output', image)
        print('image taken')
        print("processing...")
        time.sleep(10)

        # to terminate the cycle
        cv2.destroyAllWindows()

        subprocess.run(['bash', '/home/ayualr/mlx90640_test/yolov5/config.sh'], check=True)
        print("success")
        ser.close()
        


        


except KeyboardInterrupt:
	# to terminate the cycle
	ser.write(serial.to_bytes([0xA5,0x35,0x01,0xDB]))
	ser.close()
	cv2.destroyAllWindows()
	print(' Stopped')

# just in case 
ser.close()
cv2.destroyAllWindows()