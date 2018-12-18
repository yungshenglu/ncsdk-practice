# Tutorial 2 - Build a Application With Intel® Movidius™ NCS

We are going to practice how to build a application with Intel® Movidius™ NCSDK in this tutorial. We will perform image classification using deep neural networks (DNNs). Before we start, there are some prerequisite as follow:

* **Prerequisite**
    * Attach Intel® Movidius™ Neural Compute Stick (NCS) on your machine
    * Make sure you have already installed Intel® Movidius™ NCSDK
* **NOTICE:** The following opreations are used in **Ubuntu Linux 16.04 LTS** and **NCSDK 2.0**.

> We have aleady prepared the example code from [`ncsdk/ncappzoo`](https://github.com/movidius/ncappzoo/tree/ncsdk2) on branch `ncsdk2`. The following example is from [here](https://github.com/movidius/ncappzoo/tree/ncsdk2/apps/image-classifier)!

---
## 2.1 Define user configurable parameters

1. Below are some of the user configurable parameters of `image-classifier.py` and the default value is used in this repository:
   * `GRAPH_PATH`
       * Location of the graph file, against with we want to run the inference
       * Default: `~/workspace/ncappzoo/caffe/GooGleNet/graph`
   * `INAGE_PATH`
       * Location of the image we want to classify
       * Default: `~/workspace/ncappzoo/data/images/cat.jpg`
   * `IMAGE_DIM`
       * Dimensions of the image as defined by the choosen neural network
       * e.g., **GoogLeNet** uses 224x224 pixels, **AlexNet** uses 227x227 pixels
   * `IMAGE_STDDEV`
       * Standard deviation (scaling value) as defined by the choosen neural network
       * e.g., **GoogLeNet** uses no scaling factor, **Inception v3** uses 128 (stddev = 1/128)
   * `IMAGE_MEAN`
       * Mean subtraction is a common technique used in deep learning to center the data
       * For **ILSVRC** dataset, the mean is B = 102 Green = 117 Red = 123
2. Define the above parameters
    ```python
    
    ```

---
## 2.2 Open the enumerated device

* **NOTICE:** Make sure you have already plugged the Intel® Movidius™ NCS on your machine.

```python
# Open the enumerated device
def open_ncs_device():
    # Look for enumerated Intel Movidius NCS devices; quit program if none found
    devices = mvnc.EnumerateDevices()
    if len(devices) == 0:
        print('[INFO] No devices found')
        quit()
    # Get a handle to the first enumerated device and open it
    device = mvnc.Device(device[0])
    device.open()
    return device
```

---
## 2.3 Load graph file into the NCS

```python
def load_grpah(device):
    # Read the graph file into a buffer
    with open(ARGS.graph, mode='rb') as f:
        blob = f.read()
    # Load the grpah buffer into the NCS
    graph = mvnc.Graph(ARGS.graph)
    # Create and allocate a network graph to the device in FIFOs
    fifo_in, fifo_out = graph.allocate_with_fifos(device, blob)
    return graph, fifo_in, fifo_out
```

---
## 2.4 Offload a single image onto the Intel® Movidius™ NCS to run inference

```python
def pre_process_image():
    # Read and resize image (the size of image is defined during training)
    img = skimage.io.imread(ARGS.image)
    img = skimage.transform,resize(img, ARGS.dim, preserve_range=True)
    # Convert RGB to BGR (Caffe uses BGR)
    if ARGS.colormode = 'BGR':
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
    3. Convert the image into a half precision floating 

---
## 2.5

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