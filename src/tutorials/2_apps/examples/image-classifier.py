#!/usr/bin/python3
#
# ****************************************************************************
# Copyright(c) 2017 Intel Corporation. 
# License: MIT See LICENSE file in root directory.
# ****************************************************************************

# How to classify images using DNNs on Intel Neural Compute Stick (NCS)

import os
import sys
import numpy
import ntpath
import argparse
import skimage.io
import skimage.transform
import mvnc.mvncapi as mvnc

# Number of top prodictions to print
NUM_PREDICTIONS	= 5
# Variable to store commandline arguments
ARGS = None

# Step 1. Open the enumerated device and get a handle to it
def open_ncs_device():
    # Look for enumerated Intel® Movidius™ NCS devices; quit program if none found
    devices = mvnc.enumerate_devices()
    if len(devices) == 0:
        print('[INFO] No devices found')
        quit()
    # Get a handle to the first enumerated device and open it
    device = mvnc.Device(devices[0])
    device.open()
    return device

# Step 2. Load a graph file onto the NCS device
def load_graph(device):
    # Read the graph file into a buffer
    with open(ARGS.graph, mode='rb') as f:
        blob = f.read()
    # Load the grpah buffer into the Intel® Movidius™ NCS
    graph = mvnc.Graph(ARGS.graph)
    # Create and allocate a network graph to the device in FIFOs
    fifo_in, fifo_out = graph.allocate_with_fifos(device, blob)
    
    return graph, fifo_in, fifo_out

# Step 3. Preprocess the image onto the Intel® Movidius™ NCS to run inference 
def pre_process_image():
    # Read and resize image (the size of image is defined during training)
    img = skimage.io.imread(ARGS.image)
    img = skimage.transform.resize(img, ARGS.dim, preserve_range=True)
    # Convert RGB to BGR (Caffe uses BGR)
    if ARGS.colormode == 'BGR':
        img = img[:, :, ::-1]
    # Mean subtraction and scaling (center the data)
    img = (img - ARGS.mean) * ARGS.scale
    return img

# Step 4. Read and print inference results from the Intel® Movidius™ NCS
def infer_image(graph, img, fifo_in, fifo_out):
    # Load the lables file
    labels = [line.rstrip('\n') for line in open(ARGS.labels) if line != 'classes\n']
    # Take a dummy forward pass for the first inference takes an additional ~20ms due to memory initialization
    graph.queue_inference_with_fifo_elem(fifo_in, fifo_out, img.astype(numpy.float32), None)
    output, userobj = fifo_out.read_elem()
    # Load the image as an array
    graph.queue_inference_with_fifo_elem(fifo_in, fifo_out, img.astype(numpy.float32), None)
    # Get the results from Intel® Movidius™ NCS
    output, userobj = fifo_out.read_elem()
    # Sort the indices of top predictions
    order = output.argsort()[::-1][:NUM_PREDICTIONS]
    # Get execition time
    inference_time = graph.get_option(mvnc.GraphOption.RO_TIME_TAKEN)
    # Print the inference results
    print('\n==============================================================')
    print('Top prediction for', ntpath.basename(ARGS.image))
    print('Execution time:' + str(numpy.sum(inference_time)) + 'ms')
    print('--------------------------------------------------------------')
    for i in range(0, NUM_PREDICTIONS):
        print('%3.1f%%\t' % (100.0 * output[order[i]]) + labels[order[i]])
    print('\n==============================================================')
    # Show the image on which inference was performed
    if 'DISPLAY' in os.environ:
        skimage.io.imshow(ARGS.image)
        skimage.io.show()

# Step 5. Unload the graph and close the device
def clean_up(device, graph, fifo_in, fifo_out):
    # Unload the graph
    fifo_in.destroy()
    fifo_out.destroy()
    graph.destroy()
    # Close the device
    device.close()
    device.destroy()

# Main function
def main():
    # Open the enumerated device
    device = open_ncs_device()
    # Load graph file into the Intel® Movidius™ NCS
    graph, fifo_in, fifo_out = load_graph(device)
    # Offload a single image onto the Intel® Movidius™ NCS to run inference
    img = pre_process_image()
    # Read and print inference results from the Intel® Movidius™ NCS
    infer_image(graph, img, fifo_in, fifo_out)
    # Unload the graph and close the device
    clean_up(device, graph, fifo_in, fifo_out)

# Entry point
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Image classifier using Intel® Movidius™ Neural Compute Stick.')
    parser.add_argument('-g', '--graph',
        type=str,
        default='./caffe/GoogLeNet/graph',
        help='Absolute path to the neural network graph file')
    parser.add_argument('-i', '--image',
        type=str,
        default='./data/images/cat.jpg',
        help='Absolute path to the image that needs to be inferred')
    parser.add_argument('-l', '--labels',
        type=str,
        default='./data/ilsvrc12/synset_words.txt',
        help='Absolute path to labels file')
    parser.add_argument('-M', '--mean',
        type=float,
        nargs='+',
        default=[104.00698793, 116.66876762, 122.67891434],
        help='"," delimited floating point values for image mean')
    parser.add_argument('-S', '--scale',
        type=float,
        default=1,
        help='Absolute path to labels file')
    parser.add_argument('-D', '--dim',
        type=int,
        nargs='+',
        default=[224, 224],
        help='Image dimensions. ex. -D 224 224')
    parser.add_argument('-c', '--colormode',
        type=str,
        default='BGR',
        help='RGB vs BGR color sequence. TensorFlow = RGB, Caffe = BGR')
    ARGS = parser.parse_args()
    main()