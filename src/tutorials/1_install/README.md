# Tutorial 1 - Installation

We are going to install Intel® Movidius™ NCSDK in this tutorial. There are some prerequisite as follow in this installation.

* Prerequisite
    * Intel® Movidius™ Neural Compute Stick (NCS)
    * Git
    * Development computer with a supported OS:
        * x86-64 with Ubuntu Linux (64-bit) 16.04 Desktop
        * Raspberry Pi 3 with Raspbian Stretch (starting with SDK 1.09.xx)
            * Upgrade Raspbian Jessie to Stretch
        * Other operating environments (with supported OS):
            * Virtual Machine ([follow here!](https://movidius.github.io/ncsdk/vm_config.html))
            * Docker
            * virtualenv ([follow here!](https://movidius.github.io/ncsdk/virtualenv.html))
            * Internet connection
            * USB camera (optional, needed for some examples)
* **NOTICE:** The following opreations are used in **Ubuntu Linux 16.04 LTS** and **NCSDK 2.0**.

---
## 1.1 Basic installation on Ubuntu Linux

We are going to install *Intel® Movidius™ NCSDK* on **Ubuntu Linux 16.04 LTS (64-bit)** first.

1. Clone the repository from the GitHub
    ```bash
    # Check out the latest version of NCSDK 2 from the ncsdk2 branch
    # The master branch is the version of NCSDK 1.x
    $ git clone -b ncsdk2 http://github.com/Movidius/ncsdk
    ```
2. Change the directory to `./ncsdk/` and preform the `Makefile` to install (take few minutes)
    ```bash
    $ cd ncsdk && make install
    ```

* How to uninstall *Intel® Movidius™ NCSDK*?
    ```bash
    # Make sure your current directory is in "./ncsdk/"
    $ make uninstall
    ```

* **NOTICE:** We are going to use the latest version of **NCSDK 2** in this tutorials!

---
## 1.2 Basic installation on Raspberry Pi

If you don't need to install *Intel® Movidius™ NCSDK* on Raspberry Pi, feel free to skip this section. For Raspberry Pi, we recommend a **16GB SD card** for a full NCSDK installation.
 
1. Edit the value of `CONF_SWAPSIZE` in `/etc/dphys-swapfile` to increase the swapfile size
    ```bash
    $ sudo vim /etc/dphys-swapfile
    ```
    * We recommend you to change the size from the default value is 100MB to **1024MB or greater**
2. Restart the swapfile service
    ```bash
    $ sudo /etc/init.d/dphys-swapfile restart
    ```
3. Clone the repository from the GitHub
    ```bash
    # Check out the latest version of NCSDK 2 from the ncsdk2 branch
    # The master branch is the version of NCSDK 1.x
    $ git clone -b ncsdk2 http://github.com/Movidius/ncsdk
    ```
4. Change the directory to `./ncsdk/` and preform the `Makefile` to install (take few minutes)
    ```bash
    $ cd ncsdk && make install
    ```
5. Edit the value of `CONF_SWAPSIZE` in `/etc/dphys-swapfile` to change the swapfile size back to **100MB**
    ```bash
    $ sudo vim /etc/dphys-swapfile
    ```
    * Change the size back to the default value is 100MB
6. Restart the swapfile service
    ```bash
    $ sudo /etc/init.d/dphys-swapfile restart
    ```

* How to uninstall *Intel® Movidius™ NCSDK*?
    ```bash
    # Make sure your current directory is in "./ncsdk/"
    $ make uninstall
    ```

---
## 1.3 Installation with Docker (optional)

* **NOTICE:** This feature is only available with *Intel® Movidius™ Neural Compute SDK 2.x*.

1. Prerequisite
    * Make sure you have already installed *Docker* on your Ubuntu Linux host
    * Follow the instructions to install `docker-ce` on your Ubuntu Linux host [here](https://docs.docker.com/install/linux/docker-ce/ubuntu)!
2. Proxy configuration (for *Ubuntu Linux 16.04 LTS*) (optional)
    1. Create a docker config file at `~/.docker/config.json`
        ```json
        // Replace the example proxy info with your proxy info
        {
            "proxies": {
                "default": {
                    "httpProxy": "http://proxy.exmaple.com:80"
                }
            }
        }
        ```
    2. Edit `/etc/default/docker`
        ```bash
        # Change the line as follow:
        #export http_proxy="http://127.0.0.1:3128/"
        # To this (with the info for your proxy):
        http_proxy="http://proxy.com:80"
        ```
    3. Edit `/lib/systemd/system/docker.service`
        ```bash
        # Add the following line into tje Services section
        EnvironmentFile=/etc/default/docker
        ```
    4. Reload services
        ```bash
        $ sudo systemctl daemon-reload
        $ sudo systemctl restart docker
        ```
    5. Edit `/etc/NetworkManager/NetworkManager.conf` (optional)
        ```bash
        # Comment out the line as follow
        #dns=dnsmasq
        ```
    6. Restart the service
        ```bash
        $ sudo systemctl restart network-manager
        ```
    7. Pull the Docker image for *Ubuntu Linux 16.04 LTS*
        ```bash
        $ sudo docker pull ubuntu:16.04
        ```
3. `sudo` configuration (for using Docker without `sudo`)
    ```bash
    $ sudo groupadd docker
    $ sudo usermod -aG docker $USER
    ```
    * Reboot your machine for this to take effect!

### 1.3.1 Use non-privileged Docker containers

The following instructions are focus on **non-privileged Docker containers**. Versions of the Intel® Movidius™ NCSDK *prior to 2.08* required that the docker run command was issued with the `–privileged` flag. This is due to the way the NCS device boots and loads its firmware. If you need to run your Docker container with the `–privileged` flag you can skip this section and follow the instructions [here](https://movidius.github.io/ncsdk/docker.html#privileged-docker-containers).

4. Create a Docker image for the Intel® Movidius™ NCSDK
    ```bash
    # Change the directory to "./ncsdk/"
    $ cd ./ncsdk/
    # Create a Docker image
    $ docker build -t ncsdk -f ./extras/docker/Dockerfile_NoPreviligeAccess .
    ```
5. Prepare Intel® Movidius™ NCS device
    ```bash
    # Chaneg the directory to "./ncsdk/extras/docker/"
    $ cd ./ncsdk/extras/docker/
    # Export the path to API src directory
    $ export MVNC_API_PATH=../../../api/src
    # Build the "ncs_boot_devices" program which loads the device firmware
    $ make ncs_boot_devices
    # Run the "ncs_boot_devices" to boot the devices and load the firmware
    # Make sure all NCS devices are plugged into the host system at this point
    $ make run
    ```
6. Run the *non-privileged* Docker container
    ```bash
    # The devices in the system have been booted with correct firmware
    # Change the directory to "./ncsdk/extras/docker/"
    $ cd ./ncsdk/extras/docker/
    # Start the Docker container
    $ ./docker_cmd.sh
    ```

### 1.3.2 Use privileged Docker containers

* **NOTICE:** We have provided a Docker image for building the Intel® Movidius™ NCSDK environement. You can also follow the instructions [here](https://github.com/yungshenglu/Dockerfiles/tree/master/ncsdk-env).

The simplest way to use the Intel® Movidius™ NCS within a docker container is to do it from a container thats running with the `–privileged` flag. This is not always desirable.

1. Create a Docker image for the Intel® Movidius™ NCSDK (take few minutes)
    ```bash
    # Change your current directory to "./ncsdk/"
    $ cd ./ncsdk/
    # Create a Docker image
    $ docker build -t ncsdk-env -f ./extras/docker/Dockerfile .
    ```
2. Create and run a privileged Docker container from the built image
    ```bash
    $ docker run --net=host --privileged -v /dev:/dev --name ncsdk-env_c -i -t ncsdk-env /bin/bash
    ```

### 1.3.3 How to use the Docker container with Intel® Movidius™ NCSDK?

1. Start the Docker container
    ```bash
    $ docker start -a -i ncsdk-env_c
    ```
2. Build Intel® Movidius™ NCSDK examples (optional)
    ```bash
    # Run the following command inside of your Docker container
    $ make examples
    ```
3. Exit the Docker container
    ```bash
    # Run the following command inside of your Docker container
    $ exit
    ```

---
## 1.4 Installation with virtualenv (optional)

[virtualenv](https://virtualenv.pypa.io/en/stable/) is a tool to create isolated Python environments that help avoid issues caused by conflicting package dependencies for different applications.

* **NOTICE:** This feature is only available with *Intel® Movidius™ Neural Compute SDK 2.x*.

1. Modify the configuration file `./ncsdk/ncsdk.conf`
    ```bash
    # Make sure your current directory is "./ncsdk/"
    $ vim ncsdk.conf
    # Modify the following setting from "no" to "yes"
    USE_VIRTUALENV=yes
    ```
    * Make sure to save the change and then proceed the following instructions
2. Proceed the instructions in [basic installation on Ubuntu Linux]().
3. Activate the `virtualenv`
    ```bash
    $ source /opt/movidius/virtualenv-python/bin/activate
    # To deactivate the "virtualenv", use the command as follow
    $ deactivate
    ```
    * When using the virtualenv, Python packages will be installed to `/opt/movidius/virtualenv-python/lib/python3.5/site-packages`.

---
## 1.5 Run examples!

1. Attach a *Intel® Movidius™ NCS* to your system first
2. Download necessary prerequisites and models and build all examples (take few minutes)
    ```bash
    # Make sure your current directory is "./ncsdk/"
    $ make examples
    ```
3. To build and run individual examples, run the following command within that example's directory
    ```bash
    # Make sure your current directory is in that example's directory
    $ make run
    ```

We provide the example code [`./examples/apps/hello_ncs_py/`](examples/apps/hello_ncs_py/) and [`./examples/apps/hello_ncs_cpp/`](examples/apps/hello_ncs_cpp/) in this tutorial. You can run the examples by the following commands:

* `./examples/apps/hello_ncs_cpp/`
    ```bash
    # Make sure your current directory is "./examples/apps/hello_ncs_cpp/"
    $ make run
    making hello_ncs_cpp
    g++ hello_ncs.cpp -o hello_ncs_cpp -lmvnc
    Created hello_ncs_cpp executable

    making run
    ./hello_ncs_cpp;
    Hello NCS! Device opened normally.
    Goodbye NCS!  Device Closed normally.
    NCS device working.
    ```
* `./examples/apps/hello_ncs_py/`
    ```bash
    # Make sure your current directory is "./examples/apps/hello_ncs_py/"
    $ make run
    ......
    ......
    Hello NCS! Device opened normally.
    Goodbye NCS! Device closed normally.
    NCS device working.
    ```

---
## 1.6 More examples in Caffe and TensorFlow

The following examples which used Caffe and TensorFlow are also provided in NCSDK. The training data are stored in `./examples/data/`.

* Caffe (`./examples/caffe/`)
    ```bash
    # Removes all the temporary and target files
    $ make clean
    # Run the Makefile
    $ make all
    # Run "run.py"
    $ make run_py
    # Run "run.cpp"
    % make run_cpp
    ```
    * **AlexNet**
    * **GoogLeNet**
    * **SqueezeNet v1.0**
* TensorFlow (`./examples/tensorflow/`)
    ```bash
    # Removes all the temporary and target files
    $ make clean
    # Run the Makefile
    $ make all
    # Run "run.py"
    $ make run
    ```
    * **Inception v1**
    * **Inception v3**

---
## 1.7 Troublshooting (optional)

* Please follow [Movidius Forum](https://ncsforum.movidius.com/).

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