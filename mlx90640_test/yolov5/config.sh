sudo rm -rf hasil/*

#mkdir hasil
echo 'Detecting humans'
python3 detect.py --weights /home/ayualr/mlx90640_test/yolov5/runs/train/exp2/weights/best.pt --source /home/ayualr/mlx90640_test/yolov5/test_image/thermal_output.jpg --project hasil/ --save-crop
echo 'Cropping detected image for temperature calculation'


if [ -z "$(ls -A hasil/exp/crops)" ]; then #if true, then `results/exp_cropped` is empty
   echo 'No human detected'
   exit 0
else
   echo 'Running temperature calculation'
fi

python3 calc_temp.py

sudo rm -rf test_image/*