# -*- coding: utf-8 -*-
"""Homework_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YlSTow2GmuqgY90otGdHGmVgiXsFPvEq
"""

#Utilities
import torch
import torchvision
from matplotlib import pyplot as plt
from tqdm.notebook import tqdm

#Import and read dataset from a github repository
!wget -c https://github.com/Horea94/Fruit-Images-Dataset/archive/master.tar.gz
!tar -xzf master.tar.gz
!rm master.tar.gz
!rm ./Fruit-Images-Dataset-master/readme.md

#Dataset folders
import os
dest_dir = "./Fruit-Images-Dataset-master"
os.listdir(dest_dir)

#Others utilities
import torchvision.transforms as T
from torch.utils.data import Dataset, DataLoader
from pathlib import Path
from PIL import Image

class FruitImagesDataset(Dataset):
  def __init__(self, dset_dir, train=True, transforms=T.Compose([])):
    split = "Training" if train else "Test"
    self.dset_dir = Path(dset_dir)/split
    
    self.transforms = transforms

    self.files = []

    folders = sorted(os.listdir(self.dset_dir))
    for folder in folders:
      class_idx = folders.index(folder)

      folder_dir = self.dset_dir/folder

      files = os.listdir(folder_dir)

      self.files += [{"file": folder_dir/x, "class": class_idx} for x in files]

  def __len__(self):
    return len(self.files)

  def __getitem__(self, i):
    item = self.files[i]
    file = item['file']
    class_idx = torch.tensor(item['class'])

    img = Image.open(file).convert("RGB")
    img = self.transforms(img)
    return img, class_idx

#Resize img and trasform in tensors
transforms = T.Compose([
        T.Resize(32),
        T.ToTensor(),
        T.Normalize(0.5, 0.5)
    ])

#Create train and test sets
train_dset = FruitImagesDataset(dest_dir, train=True, transforms=transforms)
test_dset = FruitImagesDataset(dest_dir, train=False, transforms=transforms)

#Checking the dimension of one element
data, label = train_dset[0]
print(data.shape)

#Checking dataset len
num_train = len(train_dset)
num_test = len(test_dset)
print(f"Num. training samples: {num_train}")
print(f"Num. test samples:     {num_test}")

# List of indexes on the training set
train_idx = list(range(num_train))
# List of indexes of the test set
test_idx = list(range(num_test))

# Shuffle the training set
import random

random.shuffle(train_idx)
for i in range(10):
  print(train_idx[i])

#Building validation set as a fraction of the 10% of the original train set
val_frac = 0.1
#Number of samples of the validation set
num_val = int(num_train * val_frac) 
num_train = num_train - num_val

# Split training set
val_idx = train_idx[num_train:]
train_idx = train_idx[:num_train]

print(f"{num_train} samples used as train set")
print(f"{num_val}  samples used as val set")

#Print all values of the three sets
print(f"{num_train} samples used as train set")
print(f"{num_val}  samples used as val set")
print(f"{num_test} samples used as test set")

# Split train_dataset into training and validation
from torch.utils.data import Subset

val_dset = Subset(train_dset, val_idx)
train_dset = Subset(train_dset, train_idx)

#Create the three dataloaders
train_loader = DataLoader(train_dset, batch_size=32, shuffle=True, drop_last=True, num_workers=2)
validation_loader = DataLoader(val_dset, batch_size=32, shuffle=False, drop_last=False, num_workers=2)
test_loader = DataLoader(test_dset, batch_size=32, shuffle=False, drop_last=False, num_workers=2)

#Checking the dimension of train loader
inputs, labels = next(iter(train_loader))
print(inputs.shape)
print(labels.shape)

#CNN Model
import torch.nn as nn

class MyFruitCNN(nn.Module):

  #Constructor
  def __init__(self, in_size=3, use_norm=False):
    #Call parent contructor
    super().__init__()
    self.layers = nn.Sequential(
      #Layer 1
      nn.Conv2d(in_channels=in_size, out_channels=64, kernel_size=3, padding=1, stride=1),
      nn.ReLU(),
      #Layer 2
      nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, padding=1, stride=1),
      nn.ReLU(),
      nn.MaxPool2d(kernel_size=2, stride=2),
      #Layer 3
      nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, padding=1, stride=1),
      nn.ReLU(),
      nn.MaxPool2d(kernel_size=2, stride=2),
      #Layer 4
      nn.Conv2d(in_channels=256, out_channels=512, kernel_size=3, padding=1, stride=1),
      nn.ReLU(),
      nn.MaxPool2d(kernel_size=2, stride=2),
      #Layer 5
      nn.Conv2d(in_channels=512, out_channels=512, kernel_size=3, padding=1, stride=1),
      nn.ReLU(),
      nn.MaxPool2d(kernel_size=2, stride=2)
    )

    #Forward
  def forward(self, x):
    x = self.layers(x)
    return x

#Print the convolutional model
net = MyFruitCNN()
print(net)

#Get an element from the dataset
test_x, _ = train_dset[0]
print(data.shape)

#Adding one dimension at the position 0
test_x = test_x.unsqueeze(dim=0)
test_x.size()

output = net(test_x)
output.shape

#Compute the final size and pass it to the fully connected layer
out_features = output.size(1) * output.size(2) * output.size(3)
print(out_features)

class CNN(nn.Module):
  #Constructor
  def __init__(self, in_size=3, out_size=131, use_norm=False):
   
    super().__init__()
    #Create convolution layers
    self.layers = nn.Sequential(
      #Layer 1
      nn.Conv2d(in_channels=in_size, out_channels=64, kernel_size=3, padding=1, stride=1),
      nn.ReLU(),
      #Layer 2
      nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, padding=1, stride=1),
      nn.ReLU(),
      nn.MaxPool2d(kernel_size=2, stride=2),
      #Layer 3
      nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, padding=1, stride=1),
      nn.ReLU(),
      nn.MaxPool2d(kernel_size=2, stride=2),
      #Layer 4
      nn.Conv2d(in_channels=256, out_channels=512, kernel_size=3, padding=1, stride=1),
      nn.ReLU(),
      nn.MaxPool2d(kernel_size=2, stride=2),
      #Layer 5
      nn.Conv2d(in_channels=512, out_channels=512, kernel_size=3, padding=1, stride=1),
      nn.ReLU(),
      nn.MaxPool2d(kernel_size=2, stride=2)
    )
    #Create fully-connected layers
    self.fc_layers = nn.Sequential(
        nn.Linear(2048, 1024),
        nn.ReLU(),
        #The final Classification Layer
        nn.Linear(1024, out_size)
    )

  #Forward
  def forward(self, x):
    x = self.layers(x)
    x = x.view(x.size(0), -1)
    output = self.fc_layers(x)
    return output

#Print the final model
net = CNN()
print(net)
output = net(test_x)
output.shape

def train(net, loaders, optimizer, criterion, epochs=10, device=torch.device('cpu')):
    try:
        net = net.to(device)
        print(net)
        #Initialize history
        history_loss = {"train": [], "val": [], "test": []}
        history_accuracy = {"train": [], "val": [], "test": []}
        #Process each epoch
        for epoch in range(epochs):
            #Initialize epoch variables
            sum_loss = {"train": 0, "val": 0, "test": 0}
            sum_accuracy = {"train": 0, "val": 0, "test": 0}
            #Process each split
            for split in ["train", "val", "test"]:
                if split == "train":
                  net.train()
                else:
                  net.eval()
                #Process each batch
                for (input, labels) in tqdm(loaders[split],desc=split):
                    #Move to CUDA
                    input = input.to(device)
                    labels = labels.to(device)
                    #Reset gradients
                    optimizer.zero_grad()
                    #Compute output
                    pred = net(input)
                    loss = criterion(pred, labels)
                    #Update loss
                    sum_loss[split] += loss.item()
                    #Check parameter update
                    if split == "train":
                        #Compute gradients
                        loss.backward()
                        #Optimize
                        optimizer.step()
                    #Compute accuracy
                    _,pred_labels = pred.max(1)
                    batch_accuracy = (pred_labels == labels).sum().item()/input.size(0)
                    #Update accuracy
                    sum_accuracy[split] += batch_accuracy
            #Compute epoch loss/accuracy
            epoch_loss = {split: sum_loss[split]/len(loaders[split]) for split in ["train", "val", "test"]}
            epoch_accuracy = {split: sum_accuracy[split]/len(loaders[split]) for split in ["train", "val", "test"]}
            #Update history
            for split in ["train", "val", "test"]:
                history_loss[split].append(epoch_loss[split])
                history_accuracy[split].append(epoch_accuracy[split])
            #Print info
            print(f"Epoch {epoch+1}:",
                  f"TrL={epoch_loss['train']:.4f},",
                  f"TrA={epoch_accuracy['train']:.4f},",
                  f"VL={epoch_loss['val']:.4f},",
                  f"VA={epoch_accuracy['val']:.4f},",
                  f"TeL={epoch_loss['test']:.4f},",
                  f"TeA={epoch_accuracy['test']:.4f},")
    except KeyboardInterrupt:
        print("Interrupted")
    finally:
        #Plot loss
        plt.title("Loss")
        for split in ["train", "val", "test"]:
            plt.plot(history_loss[split], label=split)
        plt.legend()
        plt.show()
        #Plot accuracy
        plt.title("Accuracy")
        for split in ["train", "val", "test"]:
            plt.plot(history_accuracy[split], label=split)
        plt.legend()
        plt.show()

import torch
import torch.nn.functional as F
import torch.optim as optim

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

net = CNN()
optimizer = optim.SGD(net.parameters(), lr = 0.005)
criterion = nn.CrossEntropyLoss()

#Define dictionary of loaders
loaders = {"train": train_loader,
           "val": validation_loader,
           "test": test_loader}

train(net, loaders, optimizer, criterion, epochs=10, device=device)

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix
import seaborn as sn
import pandas as pd

#Computing the confusion matrix
y_pred = []
y_true = []

#Iterate on test set
for inputs, labels in test_loader:
  
  inputs, labels = inputs.cuda(), labels.cuda()
  output = net(inputs) 
  output = (torch.max(torch.exp(output), 1)[1]).data.cpu().numpy()
  y_pred.extend(output)
  labels = labels.data.cpu().numpy()
  y_true.extend(labels) 

#Classes
dest_dir = "./Fruit-Images-Dataset-master/Training"
classes = os.listdir(dest_dir)

#Build confusion matrix
cm = confusion_matrix(y_true, y_pred)
cmn = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

fig, ax = plt.subplots(figsize=(170,100))
sn.heatmap(cmn, annot=True, xticklabels=classes, yticklabels=classes)
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.show(block=False)
