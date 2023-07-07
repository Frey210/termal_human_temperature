# termal_human_temperature
yolov5 based human temperature detection

This is a project where we use the mlx90640 thermal camera to capture thermal images, and then utilize the YOLOv5 framework to train a model that can intelligently detect body temperature of humans within the thermal images. We then use the temperature data to control the air conditioning system in the room using infrared LEDs to send remote commands to the AC unit, with pre-hacked infrared codes.

To install YOLOv5, follow the tutorial below:
git clone https://github.com/ultralytics/yolov5  # clone
cd yolov5
pip install -r requirements.txt  # install

To run the detection program, execute the following code:
sudo python3 getiamge.py

To display the thermal camera image, run:
sudo python3 uart_test.py
