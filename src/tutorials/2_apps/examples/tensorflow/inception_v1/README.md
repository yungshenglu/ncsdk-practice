# Inception v1 in TensorFlow

The [Inception v1](https://github.com/tensorflow/models/tree/master/slim/nets) network can be used for image classification. The provided Makefile does the following:
1. Download the TensorFlow checkpoint file
2. Run the conversion/save python script to generate `network.meta` file
3. Profile, Compile and Check the network using the Neural Compute SDK
4. There is a `run.py` provided that does a single inference on a provided image as an example on how to use the network using the Neural Compute API

---
## Makefile

Provided `Makefile` describes various targets that help with the above mentioned tasks.

### `make all`

* Makes the following: `profile`, `compile`, and `run`.
* **NOTICE:** It will take few minutes during this command!

### `make profile`

Runs the provided network on the NCS and generates per layer statistics that are helpful for understanding the performance of the network on the Neural Compute Stick.

### `make compile`

* Uses the network description and the trained weights files to generate a Movidius internal "graph" format file. 
* This file is later used for loading the network on to the Neural Compute Stick and executing the network.

### `make run`

Runs the provided `run.py` file which sends a single image to the Neural Compute Stick and receives and displays the inference results.

### `make check`

Runs the network on Caffe on CPU and runs the network on the Neural Compute Stick. Check then compares the two results to make sure they are consistent with each other.

### `make clean`

Removes all the temporary files that are created by the `Makefile`

---
## Example Result

Make sure you have already run `make all` before `make run` as follow:

```bash
# Run "run.py" and show an example result
$ make run
......
......
Number of categories: 1001
Start download to NCS...
*******************************************************************************
inception-v1 on NCS
*******************************************************************************
547 electric guitar 0.972656
403 acoustic guitar 0.0121994
883 vacuum, vacuum cleaner 0.00608444
421 banjo 0.00369072
492 chain saw, chainsaw 0.00059557
*******************************************************************************
Finished
```