# Tutorial 2 - Build a Application With Intel® Movidius™ NCS

We are going to practice how to build a application with Intel® Movidius™ NCSDK in this tutorial. We will perform image classification using deep neural networks (DNNs). Before we start, there are some prerequisite as follow:

* **Prerequisite**
    * Attach Intel® Movidius™ Neural Compute Stick (NCS) on your machine
    * Make sure you have already installed Intel® Movidius™ NCSDK
* **NOTICE:** The following opreations are used in **Ubuntu Linux 16.04 LTS** and **NCSDK 2.0**.

> We have aleady prepared the example code from [`ncsdk/ncappzoo`](https://github.com/movidius/ncappzoo/tree/ncsdk2) on branch `ncsdk2`. The following example is from [here](https://github.com/movidius/ncappzoo/tree/ncsdk2/apps/image-classifier)!

---
## 2.1 Define user configurable parameters

1. Below are some of the user configurable parameters of `./examples/image-classifier.py` and the default value is used in this repository:
    * `GRAPH_PATH`
       * Location of the graph file, against with we want to run the inference
       * Default: `./examples/caffe/GooGleNet/graph`
    * `INAGE_PATH`
       * Location of the image we want to classify
       * Default: `./examples/data/images/cat.jpg`
    * `IMAGE_DIM`
       * Dimensions of the image as defined by the choosen neural network
       * e.g., **GoogLeNet** uses 224x224 pixels, **AlexNet** uses 227x227 pixels
    * `IMAGE_STDDEV`
       * Standard deviation (scaling value) as defined by the choosen neural network
       * e.g., **GoogLeNet** uses no scaling factor, **Inception v3** uses 128 (`stddev` = 1/128)
    * `IMAGE_MEAN`
       * Mean subtraction is a common technique used in deep learning to center the data
       * For **ILSVRC** dataset, the mean is B = 102 Green = 117 Red = 123
2. Define the above parameters with arguments
    ```python
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
    ```
3. Define whole process and open Intel® Movidius™ NCS
    ```python
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
    ```

---
## 2.2 Open the enumerated device

* **NOTICE:** Make sure you have already plugged the Intel® Movidius™ NCS on your machine.

```python
# Open the enumerated device
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
```

---
## 2.3 Load graph file into the Intel® Movidius™ NCS

```python
def load_grpah(device):
    # Read the graph file into a buffer
    with open(ARGS.graph, mode='rb') as f:
        blob = f.read()
    # Load the grpah buffer into the Intel® Movidius™ NCS
    graph = mvnc.Graph(ARGS.graph)
    # Create and allocate a network graph to the device in FIFOs
    fifo_in, fifo_out = graph.allocate_with_fifos(device, blob)
    return graph, fifo_in, fifo_out
```

---
## 2.4 Preprocess the image onto the Intel® Movidius™ NCS to run inference

```python
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
```

* Preprocess the image before training
    1. Resize the image to match the dimensions defined by the pre-trained network
        ```python
        # Read and resize image (the size of image is defined during training)
        img = skimage.io.imread(ARGS.image)
        img = skimage.transform,resize(img, ARGS.dim, preserve_range=True)
        ```
    2. Subtract mean per channel (BGR) from the entire dataset
        ```python
        if ARGS.colormode == 'BGR':
            img = img[:, :, ::-1]
        img = (img - ARGS.mean) * ARGS.scale
        ```
    3. Convert the image into a half precision floating point (fp16) array and use `LoadTensor` function-call to load the image onto NCS
        * `skimage` library can do this in just one line of code

---
## 2.5 Read and print inference results from the Intel® Movidius™ NCS

```python
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
```

---
## 2.6 Unload the graph and close the device

```python
def clean_up(device, graph, fifo_in, fifo_out):
    # Unload the graph
    fifo_in.destroy()
    fifo_out.destroy()
    graph.destroy()
    # Close the device
    device.close()
    device.destroy()
```

---
## 2.7 Execution

1. Run the `Makefile` in the following command (take few minutes)
    ```bash
    # Make sure your current directory is "./examples/"
    $ make run
    ```
2. You will get a similar result as follow:
    ```bash
    ==============================================================
    Top prediction for cat.jpg
    Execution time:98.5566ms
    --------------------------------------------------------------
    40.5%	n02123159 tiger cat
    32.6%	n02123045 tabby, tabby cat
    8.9%	n02124075 Egyptian cat
    5.0%	n02127052 lynx, catamount
    1.2%	n04074963 remote control, remote

    ==============================================================
    ```
    ![](results/result_GoogLeNet.png)

---
## 2.8 Configuration

This example runs **GoogLeNet** by default, but you can configure it run other pre-trained deep nural networks. The following are some example commands:

* **NOTICE:** The following command can only be used in this repository!

1. AlexNet (Caffe): `./examples/caffe/AlexNet/`
    ```bash
    # Make sure your current directory is "./examples/"
    $ make alexnet
    $ python3 image-classifier.py --graph ./caffe/AlexNet/graph --dim 227 227 --image ./data/images/pic_053.jpg
    # You will get a similar result as follow:
    ==============================================================
    Top prediction for pic_053.jpg
    Execution time:88.8918ms
    --------------------------------------------------------------
    83.6%	n02504013 Indian elephant, Elephas maximus
    6.4%	n02397096 warthog
    4.1%	n01871265 tusker
    3.6%	n02504458 African elephant, Loxodonta africana
    1.0%	n02415577 bighorn, bighorn sheep, cimarron, Rocky Mountain bighorn, Rocky Mountain sheep, Ovis canadensis

    ==============================================================
    ```
    ![](results/result_AlexNet.png)
2. SqueezeNet (Caffe): `./examples/caffe/SqueezeNet/`
    ```bash
    # Make sure your current directory is "./examples/"
    $ make squeezenet
    $ python3 image-classifier.py --graph ./caffe/SqueezeNet/graph --dim 227 227 --image ./data/images/pic_053.jpg
    # You will get a similar result as follow:
    ==============================================================
    Top prediction for pic_053.jpg
    Execution time:51.6916ms
    --------------------------------------------------------------
    92.2%	n02504013 Indian elephant, Elephas maximus
    4.9%	n01871265 tusker
    2.9%	n02504458 African elephant, Loxodonta africana
    0.0%	n15075141 toilet tissue, toilet paper, bathroom tissue
    0.0%	n02326432 hare

    ==============================================================
    ```
    ![](results/result_SqueezeNet.png)
3. Inception v3 (TensorFlow): `./examples/tensorflow/inception_v3/`
    ```bash
    # Make sure your current directory is "./examples/"
    $ make inception_v3
    $ python3 image-classifier.py --graph ./tensorflow/inception_v3/graph --labels ./tensorflow/inception_v3/labels.txt --mean 127.5 --scale 0.00789 --dim 299 299 --colormode="RGB" --image ./data/images/pic_053.jpg
    ==============================================================
    Top prediction for pic_053.jpg
    Execution time:567.635ms
    --------------------------------------------------------------
    99.5%	386:Indian elephant, Elephas maximus
    0.4%	102:tusker
    0.1%	387:African elephant, Loxodonta africana
    0.0%	48:African chameleon, Chamaeleo chamaeleon
    0.0%	338:beaver

    ==============================================================
    ```
    ![](results/result_InceptionV3.png)

* How yo remove all the temporary and target files that are created by the `Makefile`?
    ```bash
    # Make sure your current directory is "./examples/"
    # Take "./examples/caffe/GoogLeNet" as example
    $ cd ./caffe/GoogLeNet/
    $ make clean
    ```

---
## 2.9 Customize this example!

You can use this examaple as a template for your custom image classfier applications. There are some tips to help you customize this example as follow:
1. Check if the built-in options would suffice
    ```bash
    # Make sure your current directory is "./examples/"
    # Run the following comman to list all available options
    $ python3 image-classifier.py -h
    
    ```
2. In `./examples/image-classifier.py`
   1. Step 1, 2, and 5 are common across all Intel® Movidius™ NCS apps. You can reuse those functions without modifications
   2. Step 3 is probably the most customizable function. As the name suggests, you can include all image preprocessing tasks in this funcion
   3. Step 4 should be modified only if there is a need to change the way inference results are read and printed

---
## References

* [Intel® Movidius™ Neural Compute SDK](https://movidius.github.io/ncsdk/index.html)
* [Intel® Movidius™ Neural Compute SDK Python API v2](https://movidius.github.io/ncsdk/ncapi/ncapi2/py_api/readme.html)
* [GitHub - movidius/ncsdk](https://github.com/movidius/ncsdk)
* [GitHub - movidius/ncappzoo](https://github.com/movidius/ncappzoo)
* [NCSDK Python API 2.x](https://movidius.github.io/ncsdk/ncapi/ncapi2/py_api/readme.html)
* [NCSDK C API 2.x](https://movidius.github.io/ncsdk/ncapi/ncapi2/c_api/readme.html)
* [Intel® Movidius™ Forum](https://ncsforum.movidius.com/)

---
## Contributor

* [David Lu](https://github.com/yungshenglu)

---
## License

Apache License 2.0