import cv2 
import numpy as np 
import win32gui, win32ui, win32con, win32api 
import time 
import pyautogui 
import tensorflow as tf 
import threading 
from object_detection.utils import ops as utils_ops 
from object_detection.utils import label_map_util 
import glob 
import random 
(topY, topX, bottomY, bottomX) = (0,0,300,300) 
basari = 3 

def duraw(): 
  print("durdum") 
  
def devam(): 
  global basari 
  if basari < 4: 
    basari = basari + 1 
  else: 
    pass 

def stop(): 
  global basari 
  if basari == 0: 
    duraw() 
  else: 
    basari = basari - 1 
    
txtfiles = []

for file in glob.glob("ssdnet_all_sezers_bag/*.jpg"): 
  txtfiles.append(file) 
random.shuffle(txtfiles) 
model_path = "C:/Users/asus/Desktop/final-1-ekm/saved_model" 

physical_devices = tf.config.experimental.list_physical_devices("GPU") 
tf.config.experimental.set_memory_growth(physical_devices[0], True) 

model = tf.saved_model.load(model_path) 
model_fn = model.signatures['serving_default'] 
#284:796, 704:1216 
def run_inference_for_single_image(model, image): 
  #image = np.asarray(image) 
  # The input needs to be a tensor, convert it using `tf.convert_to_tensor`. 
  input_tensor = tf.convert_to_tensor(image) 
  # The model expects a batch of images, so add an axis with `tf.newaxis`. 
  input_tensor = input_tensor[tf.newaxis,...] 

  # Run inference 
  output_dict = model(input_tensor) 

  # All outputs are batches tensors. 
  # Convert to numpy arrays, and take index [0] to remove the batch dimension. 
  # We're only interested in the first num_detections. 
  num_detections = int(output_dict.pop('num_detections')) 
  output_dict = {key: value[0, :num_detections].numpy() 
  for key, value in output_dict.items()} 
  output_dict['num_detections'] = num_detections

  # detection_classes should be ints. 
  output_dict['detection_classes'] = output_dict['detection_classes'].astype(np.int64) 

  return output_dict 

muallak = 0 

for name in txtfiles: 
  dosya, foto = name.split("\\") 
  isim, uzanti = foto.split(".") 
  if True:
    frame = cv2.imread(name) 
    frame = cv2.resize(frame, (300, 300)) 
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
    output = run_inference_for_single_image(model_fn, frame) 
    if output["detection_multiclass_scores"][0][1] > .55: 
      box = output["detection_boxes"][0] (
      topY, topX, bottomY, bottomX) = box 
      topY = int(topY * 300) 
      topX = int(topX * 300) 
      bottomY = int(bottomY * 300)
      bottomX = int(bottomX * 300) 
      cv2.rectangle(frame, (topX, topY), (bottomX, bottomY), (0, 50, 255), 1) 

    if bottomY > 297 or topY < 3 or output["detection_multiclass_scores"][0][1] < 0.55: 
      muallak = 1 
    else: 
      muallak = 0 

    if muallak == 0: 
      print(8000/(bottomY - topY)) 
      devam() 
    elif muallak == 1: 
      stop() 

frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) 
frame = cv2.resize(frame, (900, 900)) 
cv2.imshow("frame", frame) 
cv2.waitKey(1)
