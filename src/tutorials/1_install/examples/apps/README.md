# Examples - Hello World, NCS!

This directory contains a Python 3 and a C++ example that shows the Movidius NCSDK software is installed and is correctly configured on your system such that an application can access the stick via the NCSDK's API.

---
## Prerequisites

This code example requires that the following components are available:
* For `./apps/hello_ncs_cpp/`
    * Movidius Neural Compute Stick
    * Movidius Neural Compute SDK
* For `./apps/hello_ncs_py/`
    * Movidius Neural Compute Stick
    * Movidius Neural Compute SDK
    * Python 3

---
## Execution

* For `./apps/hello_ncs_cpp/`
    ```bash
    # Make sure your current directory is "./examples/apps/hello_ncs_cpp/"
    $ make run
    making hello_ncs_cpp
    g++ hello_ncs.cpp -o hello_ncs_cpp -lmvnc
    Created hello_ncs_cpp executable

    making run
    ./hello_ncs_cpp;
    Hello world, NCS! Device opened normally.
    Goodbye NCS!  Device Closed normally.
    NCS device working.
    ```
* For `./apps/hello_ncs_py/`
    ```bash
    # Make sure your current directory is "./examples/apps/hello_ncs_py/"
    $ make run
    ......
    ......
    Hello world, NCS! Device opened normally.
    Goodbye NCS! Device closed normally.
    NCS device working.
    ```