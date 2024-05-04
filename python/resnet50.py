# -*- coding: utf-8 -*-
"""resnet50.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZXIIYkQ1Gw4whrhPER_Yb9gdaybrhKBP

## DL Project - Reading in Data

This is a script to read in the ACDC dataset. Download the dataset from this url:

https://humanheart-project.creatis.insa-lyon.fr/database/#collection/637218c173e9f0047faa00fb

Then edit the paths below to match where the training and testing data is (these folders should be located in the downloaded data). Currently extracting just 1 of the 7-9 images for each subject (note: the index is 2 bc index 0 didn't always have a gt with it), so this is something we can change if we need.

Should see 200 training images and 100 testing images.
"""

from google.colab import drive
drive.mount('/content/drive')

# Edit these variables to match your setup
dataset_path_training = '/content/drive/My Drive/python/Resources/training'
dataset_path_testing = '/content/drive/My Drive/python/Resources/testing'

# dataset_path_training = '/Users/calebhallinan/Desktop/jhu/classes/deep_learning/DL_Final_Project_2024/data/ACDC/training'
# dataset_path_testing = '/Users/calebhallinan/Desktop/jhu/classes/deep_learning/DL_Final_Project_2024/data/ACDC/testing'

### Import packages

import os
import nibabel as nib
import numpy as np
import re
from skimage.transform import resize
import configparser
import pandas as pd


### Functions to load in the data ###

# Regular expression to extract the patient number and frame number from filenames
filename_pattern = re.compile(r'patient(\d+)_frame(\d+)(_gt)?\.nii\.gz')

# Function to get sorting key from the filename
def get_sort_key(filepath):
    match = filename_pattern.search(os.path.basename(filepath))
    if match:
        patient_num = int(match.group(1))
        frame_num = int(match.group(2))
        return (patient_num, frame_num)
    else:
        raise ValueError(f'Filename does not match expected pattern: {filepath}')

    # Function to extract the patient number and sort by it
def extract_patient_number(file_path):
    match = re.search(r"patient(\d+)", file_path)
    return int(match.group(1)) if match else None

# Lists to hold the file paths for images and ground truths
image_file_paths_train = []
ground_truth_file_paths_train = []
class_file_paths_train = []

# Walk through the directory and collect all relevant file paths
for root, dirs, files in os.walk(dataset_path_training):
    for file in files:
        if 'frame' in file:
            full_path = os.path.join(root, file)
            if '_gt' in file:
                ground_truth_file_paths_train.append(full_path)
            else:
                image_file_paths_train.append(full_path)
        if "Info" in file:
            class_file_paths_train.append(os.path.join(root, file))


# Sort the file paths to ensure alignment
image_file_paths_train.sort(key=get_sort_key)
ground_truth_file_paths_train.sort(key=get_sort_key)
class_file_paths_train = sorted(class_file_paths_train, key=extract_patient_number)

# Check to make sure each image has a corresponding ground truth
assert len(image_file_paths_train) == len(ground_truth_file_paths_train)
for img_path, gt_path in zip(image_file_paths_train, ground_truth_file_paths_train):
    assert get_sort_key(img_path) == get_sort_key(gt_path), "Mismatch between image and ground truth files"

# Extract the class labels from the config files
class_labels_train = []
for class_file in class_file_paths_train:
        config = pd.read_csv(class_file, sep=':', header=None)
        class_labels_train.append(config[config[0] == "Group"][1][2].strip())
        class_labels_train.append(config[config[0] == "Group"][1][2].strip()) # doing twice bc there are 2 files per patient

# Load the images and ground truths into numpy arrays
# using 2 index bc not all 0 index had a gt
images_train = [resize(nib.load(path).get_fdata()[:,:,2], (224,224)) for path in image_file_paths_train]
ground_truths_train = [resize(nib.load(path).get_fdata()[:,:,2], (224,224)) for path in ground_truth_file_paths_train]

# Stack the arrays into 4D numpy arrays
images_array_train = np.stack(images_train)
ground_truths_array_train = np.stack(ground_truths_train)

print(f'Training Images array shape: {images_array_train.shape}')
print(f'Training Ground truths array shape: {ground_truths_array_train.shape}')
print(f'Class labels: {class_labels_train}', '\n', "Total Class Labels: ",len(class_labels_train))


### Read in testing data ###

# Lists to hold the file paths for images and ground truths
image_file_paths_test = []
ground_truth_file_paths_test = []
class_file_paths_test = []

# Walk through the directory and collect all relevant file paths
for root, dirs, files in os.walk(dataset_path_testing):
    for file in files:
        if 'frame' in file:
            full_path = os.path.join(root, file)
            if '_gt' in file:
                ground_truth_file_paths_test.append(full_path)
            else:
                image_file_paths_test.append(full_path)
        if "Info" in file:
            class_file_paths_test.append(os.path.join(root, file))

# Sort the file paths to ensure alignment
image_file_paths_test.sort(key=get_sort_key)
ground_truth_file_paths_test.sort(key=get_sort_key)
class_file_paths_test = sorted(class_file_paths_test, key=extract_patient_number)

# Check to make sure each image has a corresponding ground truth
assert len(image_file_paths_test) == len(ground_truth_file_paths_test)
for img_path, gt_path in zip(image_file_paths_test, ground_truth_file_paths_test):
    assert get_sort_key(img_path) == get_sort_key(gt_path), "Mismatch between image and ground truth files"

# Extract the class labels from the config files
class_labels_test = []
for class_file in class_file_paths_test:
        config = pd.read_csv(class_file, sep=':', header=None)
        class_labels_test.append(config[config[0] == "Group"][1][2].strip())
        class_labels_test.append(config[config[0] == "Group"][1][2].strip())


# Load the images and ground truths into numpy arrays
# using 2 index bc not all 0 index had a gt
images_test = [resize(nib.load(path).get_fdata()[:,:,2], (224,224)) for path in image_file_paths_test]
ground_truths_test = [resize(nib.load(path).get_fdata()[:,:,2], (224,224)) for path in ground_truth_file_paths_test]

# Stack the arrays into 4D numpy arrays
images_array_test = np.stack(images_test)
ground_truths_array_test = np.stack(ground_truths_test)

print(f'Test Images array shape: {images_array_test.shape}')
print(f'Test Ground truths array shape: {ground_truths_array_test.shape}')
print(f'Class labels: {class_labels_test}', '\n', "Total Class Labels: ",len(class_labels_test))

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import TensorDataset, DataLoader, random_split
from torchvision.models.segmentation import deeplabv3_resnet50

# Check if CUDA is available and set the device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Initialize the model
model = deeplabv3_resnet50(pretrained=False, progress=True, num_classes=4).to(device)
model.backbone.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)

# Assuming you have only 10 images for training and 5 for validation
num_train_images = 100
num_val_images = 100

# Assuming you have defined images_array_train, ground_truths_array_train, and class_labels_train
# with shapes (num_train_images, height, width) for images and ground truths, and (num_train_images,) for labels
images_array_train = np.zeros((num_train_images, 224, 224))  # Fill with your data
ground_truths_array_train = np.zeros((num_train_images, 224, 224))  # Fill with your data
class_labels_train = ['NOR', 'MINF', 'DCM', 'HCM', 'RV'] * (num_train_images // 5)  # Example labels

images_array_train = np.stack((images_array_train,) * 3, axis=1)

images_array_val = np.zeros((num_val_images, 224, 224))  # Fill with your data
ground_truths_array_val = np.zeros((num_val_images, 224, 224))  # Fill with your data
class_labels_val = ['NOR', 'MINF', 'DCM', 'HCM', 'RV'] * (num_val_images // 5)  # Example labels

images_array_val = np.stack((images_array_val,) * 3, axis=1)

# Convert numpy arrays to PyTorch tensors
images_tensor_train = torch.from_numpy(images_array_train).float().to(device)
ground_truths_tensor_train = torch.from_numpy(ground_truths_array_train).long().to(device)

images_tensor_val = torch.from_numpy(images_array_val).float().to(device)
ground_truths_tensor_val = torch.from_numpy(ground_truths_array_val).long().to(device)

# Create TensorDatasets
train_dataset = TensorDataset(images_tensor_train, ground_truths_tensor_train)
val_dataset = TensorDataset(images_tensor_val, ground_truths_tensor_val)

# Create DataLoaders
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=16, shuffle=False)

# Setup loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
num_epochs = 5

train_losses = []
val_losses = []

for epoch in range(num_epochs):
    model.train()
    running_train_loss = 0.0
    for i, data in enumerate(train_loader, 0):
        inputs, labels = data[0].to(device), data[1].to(device)
        optimizer.zero_grad()
        outputs = model(inputs)['out']
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_train_loss += loss.item()

    train_loss = running_train_loss / len(train_loader)
    train_losses.append(train_loss)

    model.eval()
    running_val_loss = 0.0
    with torch.no_grad():
        for data in val_loader:
            inputs, labels = data[0].to(device), data[1].to(device)
            outputs = model(inputs)['out']
            loss = criterion(outputs, labels)
            running_val_loss += loss.item()

    val_loss = running_val_loss / len(val_loader)
    val_losses.append(val_loss)

    print(f'Epoch [{epoch + 1}/{num_epochs}], '
          f'Training Loss: {train_loss:.4f}, '
          f'Validation Loss: {val_loss:.4f}')

# Plotting the losses
plt.plot(train_losses, label='Training Loss')
plt.plot(val_losses, label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training and Validation Losses')
plt.legend()
plt.show()

import os
import numpy as np
import matplotlib.pyplot as plt
from torchvision.transforms import functional as F
from skimage.transform import resize
import nibabel as nib

# Assuming you have already defined class_labels_test, images_array_test, and ground_truths_array_test

# Select the first 5 images for testing
num_images_to_test = 100
images_array_test_subset = images_array_test[:num_images_to_test]
ground_truths_array_test_subset = ground_truths_array_test[:num_images_to_test]

# Preprocess images similar to training and validation data
images_array_test_preprocessed = np.stack((images_array_test_subset,) * 3, axis=1)
images_tensor_test = torch.from_numpy(images_array_test_preprocessed).float().to(device)

# Test the model
model.eval()
with torch.no_grad():
    outputs_test = model(images_tensor_test)['out']
    _, predicted_test = torch.max(outputs_test, 1)

# Visualize the results
for i in range(5):
    # Original image
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 3, 1)
    plt.imshow(images_array_test_subset[i], cmap='gray',interpolation=None)
    plt.title('Original Image')
    plt.axis('off')

    # Ground truth
    plt.subplot(1, 3, 2)
    plt.imshow(ground_truths_array_test_subset[i], cmap='jet',interpolation=None)
    plt.title('Ground Truth')
    plt.axis('off')

    # Model prediction
    plt.subplot(1, 3, 3)
    plt.imshow(predicted_test[i].cpu(), cmap='jet',interpolation=None)
    plt.title('Model Prediction')
    plt.axis('off')

    plt.show()









