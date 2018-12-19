# GoogLeNet in Caffe

The [GoogLeNet](https://github.com/BVLC/caffe/tree/master/models/bvlc_googlenet) network can be used for image classification. The provided Makefile does the following:
1. Download the Caffe `prototxt` file and makes any changes necessary to work with the Movidius Neural Compute SDK
2. Download and generates the required `ilsvrc12` data
3. Download the `.caffemodel` file which was trained and provided by BVLC
3. Profile, Compile and Check the network using the Neural Compute SDK
4. There is a python example (`run.py`) and a C++ example (`cpp/run.cpp`) which both do a single inference on an image as an example of how to use this network with the Neural Compute API thats provided in the Neural Compute SDK

---
## Makefile

Provided `Makefile` describes various targets that help with the above mentioned tasks.

### `make help`

Show `Makefile` possible targets and brief descriptions

### `make all`

* Make the following: `prototxt`, `caffemodel`, `profile`, `compile`, `check`, `cpp`, `run`, `run_cpp`
* **NOTICE:** It will take few minutes during this command!

### `make prototxt`

Download the Caffe prototxt file and makes a few changes necessary to work with the Movidius Neural Compute SDK

### `make caffemodel`

Download the Caffe model file

### `make profile`

* Run the provided network on the NCS and generates per layer statistics that are helpful for understanding the performance of the network on the Neural Compute Stick
* Output diplayed on terminal and the `output_report.html` file is also created
* Demonstrates NCSDK tool: `cnprofile`

### `make browse_profile`

* Profile the network similar to make profile and then brings up `output_report.html` in a browser
* Demonstrates NCSDK tool: `mvNCProfile`

### `make compile`

* Use the network description and the trained weights files to generate a Movidius internal "graph" format file
* This file is later loaded on the Neural Compute Stick where the inferences on the network can be executed. Demonstrates NCSDK tool: `mvNCCompile`.

### `make check`

* Run the network on Caffe on the CPU and compares results when run on the Neural Compute Stick. 
* Consistency results are output to the terminal
* Demonstrates the NCSDK tool: `mvNCCheck`

### `make run_py`

* Run the provided `run.py` python script which sends a single image to the Neural Compute Stick and receives and displays the inference results

### `make cpp`

* Build the C++ example program `run_cpp` which can be executed with `make run_cpp`.

### `make run_cpp`

Runs the provided `run_cpp` executable program that is built via `make cpp`. This program sends a single image to the Neural Compute Stick and receives and displays the inference results.

### `make clean`

* Remove all the temporary and target files that are created by the `Makefile`.

---
## Example Result

Make sure you have already run `make all` before `make run` as follow:

* Run `run.py` and show an example result
    ```bash
    $ make run_py
    ......
    ......
    ------- predictions --------
    prediction 0 (probability 0.996094) is n03272010 electric guitar  label index is: 546
    prediction 1 (probability 0.00350952) is n02676566 acoustic guitar  label index is: 402
    prediction 2 (probability 0.0) is n02396427 wild boar, boar, Sus scrofa  label index is: 342
    prediction 3 (probability 0.0) is n02391049 zebra  label index is: 340
    prediction 4 (probability 0.0) is n02389026 sorrel  label index is: 339
    ```
* Run `run.cpp` and show an example result
    ```bash
    $ make run_cpp
    ......
    ......
    Successfully opened NCS device!
    Successfully allocated graph for ../graph
    Successfully loaded the tensor for image ../../../data/images/nps_electric_guitar.png
    Successfully got the inference result for image ../../../data/images/nps_electric_guitar.png
    resultData length is 1000 
    Index of top result is: 546
    Probability of top result is: 0.994141
    ```