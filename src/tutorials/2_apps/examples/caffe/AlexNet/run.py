#! /usr/bin/env python3

# Copyright (c) 2017-2018 Intel Corporation. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from mvnc import mvncapi as mvnc 
import sys
import numpy
import cv2
import time
import csv
import os
import sys

dim=(227,227)
EXAMPLES_BASE_DIR='../../'

# ***************************************************************
# get labels
# ***************************************************************
labels_file=EXAMPLES_BASE_DIR+'data/ilsvrc12/synset_words.txt'
labels=numpy.loadtxt(labels_file,str,delimiter='\t')

# ***************************************************************
# configure the NCS
# ***************************************************************
mvnc.global_set_option(mvnc.GlobalOption.RW_LOG_LEVEL, 2)

# ***************************************************************
# Get a list of ALL the sticks that are plugged in
# ***************************************************************
devices = mvnc.enumerate_devices()
if len(devices) == 0:
	print('No devices found')
	quit()

# ***************************************************************
# Pick the first stick to run the network
# ***************************************************************
device = mvnc.Device(devices[0])

# ***************************************************************
# Open the NCS
# ***************************************************************
device.open()

network_blob='graph'

#Load blob
with open(network_blob, mode='rb') as f:
	blob = f.read()

graph = mvnc.Graph('graph')
graph.allocate(device, blob)

# ***************************************************************
# Load the image
# ***************************************************************
ilsvrc_mean = numpy.load(EXAMPLES_BASE_DIR+'data/ilsvrc12/ilsvrc_2012_mean.npy').mean(1).mean(1) #loading the mean file
img = cv2.imread(EXAMPLES_BASE_DIR+'data/images/nps_electric_guitar.png')
img=cv2.resize(img,dim)
img = img.astype(numpy.float32)
img[:,:,0] = (img[:,:,0] - ilsvrc_mean[0])
img[:,:,1] = (img[:,:,1] - ilsvrc_mean[1])
img[:,:,2] = (img[:,:,2] - ilsvrc_mean[2])

# ***************************************************************
# Initialize Fifos
# ***************************************************************
fifoIn = mvnc.Fifo("fifoIn0", mvnc.FifoType.HOST_WO)
fifoOut = mvnc.Fifo("fifoOut0", mvnc.FifoType.HOST_RO)

descIn = graph.get_option(mvnc.GraphOption.RO_INPUT_TENSOR_DESCRIPTORS)
descOut = graph.get_option(mvnc.GraphOption.RO_OUTPUT_TENSOR_DESCRIPTORS)

fifoIn.allocate(device, descIn[0], 2)
fifoOut.allocate(device, descOut[0], 2)

# ***************************************************************
# Send the image to the NCS
# ***************************************************************
graph.queue_inference_with_fifo_elem(fifoIn, fifoOut, img, 'user object')

# ***************************************************************
# Get the result from the NCS
# ***************************************************************
output, userobj = fifoOut.read_elem()

# ***************************************************************
# Print the results of the inference form the NCS
# ***************************************************************
order = output.argsort()[::-1][:6]
print('\n------- predictions --------')
for i in range(0,5):
	print ('prediction ' + str(i) + ' (probability ' + str(output[order[i]]*100) + '%) is ' + labels[order[i]] + '  label index is: ' + str(order[i]) )


# ***************************************************************
# Clean up the graph and the device
# ***************************************************************
fifoIn.destroy()
fifoOut.destroy()
graph.destroy()
device.close()
    



