from PIL import Image
import numpy as np
import serial
import time
import csv
from datetime import datetime
import random

# Baca gambar termal
image = Image.open("/home/ayualr/mlx90640_test/yolov5/hasil/exp/crops/Human/thermal_output.jpg")

# Konversi gambar ke array NumPy
thermal_array = np.array(image)

# Konversi gambar ke skala abu-abu
gray_image = image.convert("L")

# Ekstraksi suhu dari palet jet
temperature_array = np.array(gray_image)

# Menentukan rentang suhu yang terkait dengan palet jet (sesuaikan dengan palet jet yang digunakan)
min_temperature = -10
max_temperature = 40

# Menghitung suhu tertinggi dalam Celcius
suhu_tertinggi_celcius = (temperature_array.max() / 255) * (max_temperature - min_temperature) + min_temperature

# Cetak suhu tertinggi dalam Celcius
print("Suhu tertinggi: {:.2f}°C".format(suhu_tertinggi_celcius))

# Membaca suhu AC saat ini dari Arduino
suhu_ac = 24 # suhu ac initial value
ac_change_time = time.strftime("%M")
if ac_change_time[-1] == '0':
    if suhu_tertinggi_celcius > 33 :
        suhu_ac -= 1
        if suhu_ac < 16 :
            suhu_ac = 16
    else :
        suhu_ac += 1
        if suhu_ac > 30 :
            suhu_ac = 30    
#suhu_ac = 25 #ser.readline().decode().strip()
print("Suhu AC saat ini:", suhu_ac)

# Inisialisasi koneksi Serial dengan Arduino
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Ganti '/dev/ttyUSB0' dengan port USB yang sesuai dan 9600 dengan baud rate yang sesuai
print("Configure serial port")

# Delay singkat untuk memastikan koneksi Serial terbentuk
time.sleep(2)

# Mengirimkan suhu tertinggi ke Arduino
ser.write(str(int(suhu_ac)).enco_csv_writede())
print("Succes sending data")

current_csv_write_time = time.strftime("%S")
if current_csv_write_time == '00':
    # Membuka file CSV untuk menulis data
    csv_file_path = '/home/ayualr/thermal_data_log/data.csv'
    with open(csv_file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Mengecek apakah file kosong atau tidak
        file_empty = csvfile.tell() == 0

        # Menentukan judul kolom pada baris pertama
        if file_empty:
            writer.writerow(['Suhu Tubuh (°C)', 'Suhu AC Saat Ini (°C)', 'Tanggal', 'Waktu'])

        # Mencatat tanggal, bulan, dan tahun saat ini
        tanggal = datetime.now().strftime("%d-%m-%Y")
        waktu = datetime.now().strftime("%H:%M:%S")

        # Menulis data ke dalam file CSV
        writer.writerow([suhu_tertinggi_celcius, suhu_ac, tanggal, waktu])

# Menutup koneksi Serial
ser.close()







