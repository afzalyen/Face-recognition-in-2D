# -*- coding: utf-8 -*-
"""428_Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dKCrfvsxrP2HQtvgdRpKwX4UlNF5cjau

# **An Efficient Deep Learning Approach for Face Recognition Using Multiple Angular 2D Images**

**Add this Folder to your Google Drive:**
https://drive.google.com/drive/folders/15ECp7l8aEBI9l4O6MpQXhoiHbGvGeGkA?usp=sharing

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""

from keras.models import Model
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing import image
import numpy as np
from glob import glob
import matplotlib.pyplot as plt
import os
import pandas as pd
from keras.models import Model
import cv2
from google.colab import drive
drive.mount('/content/drive')
from google.colab.patches import cv2_imshow

# imported VGG16
model = VGG16(weights='imagenet', include_top=False)

# imported Haar Cascade
haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Extracting feature vectors from training images using VGG16
train_feature ={}
for i in range(1,51):
  folder = os.listdir(f'/content/drive/MyDrive/428_Project_Data/train/{i}/')
  parent = f"/content/drive/MyDrive/428_Project_Data/train/{i}/"
  for i in folder:
    img_path = parent+i
    print(img_path)
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    features = model.predict(x)
    train_feature[i] = features

# created Dataframe
df = pd.DataFrame(columns=['file', 'features'])
df['file'] = list(train_feature.keys())
df['features'] = list(train_feature.values())

# Saved the dataframe as pickle file in Google Drive so that we don't have to train every time we re-run the code. 
df.to_pickle('/content/drive/MyDrive/428_Project_Data/face_train.pickle')

# Haar Cascade function
def haar_cascade_face_detection(img):
  faces_rect = haar_cascade.detectMultiScale(img, 1.1, 9)
  for (x, y, w, h) in faces_rect:
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), thickness=5)
  cv2.waitKey(0)
  return img

# Tested Face Detection and Face Recognition on Test dataset.
trained_pickle = pd.read_pickle("/content/drive/MyDrive/428_Project_Data/face_train.pickle")
length = len(trained_pickle)
correct=0
incorrect=0
for n in range(1,52):
  folder = os.listdir(f'/content/drive/MyDrive/428_Project_Data/test/{n}/')
  parent = f"/content/drive/MyDrive/428_Project_Data/test/{n}/"
  for i in folder:
    img_path = parent+i
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    features = model.predict(x)
    min_dist = 10000
    name=''
    for j in range(length):
      f = trained_pickle['features'][j]
      dist=np.linalg.norm(features - f)
      if(min_dist>dist):
        min_dist = dist
        name = trained_pickle['file'][j]
    plot_test_img = cv2.imread(img_path)
    similar_subject=os.listdir(f'/content/drive/MyDrive/428_Project_Data/train/{name[:-7]}/')
    if min_dist<450:
      plot_similar_image=cv2.imread(f'/content/drive/MyDrive/428_Project_Data/train/{name[:-7]}/{name[:-6]}00.jpg')
      if int(name[:-7]) == n:
        correct+=1
      else:
        incorrect+=1
    else:
      plot_similar_image=cv2.imread(f'/content/drive/MyDrive/428_Project_Data/NO.jpg')
      if n<=50:
        incorrect+=1
      else:
        correct+=1
    Hori = np.concatenate((haar_cascade_face_detection(plot_test_img), (plot_similar_image)), axis=1)
    imS = cv2.resize(Hori, (324, 108))                 
    cv2_imshow(imS) 
    print(min_dist, name, i)

# Calculated the accuracy of Face recognition on Test Dataset.
accuracy = (correct*100)/(correct+incorrect)
print("Normal Accuracy : ",accuracy,"%")

# Tested face Detection and face Recognition on Dark dataset
folder = os.listdir(f'/content/drive/MyDrive/428_Project_Data/dark_test/')
parent = f"/content/drive/MyDrive/428_Project_Data/dark_test/"
dark_correct=0
dark_incorrect=0
for i in folder:
  img_path = parent+i
  img = image.load_img(img_path, target_size=(224, 224))
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)
  x = preprocess_input(x)
  features = model.predict(x)
  min_dist = 10000
  name=''
  for j in range(length):
    f = trained_pickle['features'][j]
    dist=np.linalg.norm(features - f)
    if(min_dist>dist):
      min_dist = dist
      name = trained_pickle['file'][j]
  if int(name[:-7]) == int(i[:-7]):
    dark_correct+=1
  else:
    dark_incorrect+=1
  plot_test_img = cv2.imread(img_path)
  similar_subject=os.listdir(f'/content/drive/MyDrive/428_Project_Data/train/{name[:-7]}/')
  plot_similar_image=cv2.imread(f'/content/drive/MyDrive/428_Project_Data/train/{name[:-7]}/{name[:-6]}00.jpg')
  Hori = np.concatenate((haar_cascade_face_detection(plot_test_img), (plot_similar_image)), axis=1)
  imS = cv2.resize(Hori, (324, 108))                 
  cv2_imshow(imS) 
  print(min_dist, name, i)

# Calculated the accuracy of Face recognition on Dark Dataset.
accuracy = (dark_correct*100)/(dark_correct+dark_incorrect)
print("Dark Accuracy : ",accuracy,"%")

# Added Motion Blur to the Test Dataset and saved the blurred pictures on a new folder.
for n in range(1,21):
  folder = os.listdir(f'/content/drive/MyDrive/428_Project_Data/test/{n}/')
  parent = f"/content/drive/MyDrive/428_Project_Data/test/{n}/"
  for i in folder:
    img_path = parent+i
    img = cv2.imread(img_path)
    kernel_size = 30
    kernel_v = np.zeros((kernel_size, kernel_size))
    kernel_v[:, int((kernel_size - 1)/2)] = np.ones(kernel_size)
    kernel_v /= kernel_size
    vertical_mb = cv2.filter2D(img, -1, kernel_v)
    cv2.imwrite(f'/content/drive/MyDrive/428_Project_Data/motion_test/{i}', vertical_mb)

# Tested face Detection and face Recognition on Blurred dataset
folder = os.listdir(f'/content/drive/MyDrive/428_Project_Data/motion_test/')
parent = f"/content/drive/MyDrive/428_Project_Data/motion_test/"
motion_correct=0
motion_incorrect=0
for i in folder:
  img_path = parent+i
  img = image.load_img(img_path, target_size=(224, 224))
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)
  x = preprocess_input(x)
  features = model.predict(x)
  min_dist = 10000
  name=''
  for j in range(length):
    f = trained_pickle['features'][j]
    dist=np.linalg.norm(features - f)
    if(min_dist>dist):
      min_dist = dist
      name = trained_pickle['file'][j]
  if int(name[:-7]) == int(i[:-7]):
    motion_correct+=1
  else:
    motion_incorrect+=1
  plot_test_img = cv2.imread(img_path)
  similar_subject=os.listdir(f'/content/drive/MyDrive/428_Project_Data/train/{name[:-7]}/')
  plot_similar_image=cv2.imread(f'/content/drive/MyDrive/428_Project_Data/train/{name[:-7]}/{name[:-6]}00.jpg')
  Hori = np.concatenate((haar_cascade_face_detection(plot_test_img), (plot_similar_image)), axis=1)
  imS = cv2.resize(Hori, (324, 108))                 
  cv2_imshow(imS) 
  print(min_dist, name, i)

# Calculated the accuracy of Face recognition on Blurred Dataset.
accuracy = (motion_correct*100)/(motion_correct+motion_incorrect)
print("Blurred Accuracy : ",accuracy,"%")