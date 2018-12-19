# Intel® Movidius™ NCSDK Practice

This repository is used to practice some basic operations in Intel® Movidius™ Neural Compute SDK (Intel® Movidius™ NCSDK) and the original repository is [here](https://github.com/movidius/ncsdk).

* **NOTICE:** The following opreations are used in **Ubuntu Linux 16.04 LTS**.

---
## Overview

### Introduction

> The following descriptions are from [here](https://movidius.github.io/ncsdk/index.html).

The **Intel® Movidius™ Neural Compute SDK (Intel® Movidius™ NCSDK)** enables rapid prototyping and deployment of deep neural networks (DNNs) on compatible neural compute devices like the [Intel® Movidius™ Neural Compute Stick](https://movidius.github.io/ncsdk/ncs.html). The NCSDK includes a set of software tools to compile, profile, and check (validate) DNNs as well as the Intel® Movidius™ Neural Compute API (Intel® Movidius™ NCAPI) for application development in C/C++ or Python.

The NCSDK has two general usages:
* Profiling, tuning, and compiling a DNN model on a development computer (host system) with the [tools](https://movidius.github.io/ncsdk/tools/tools_overview.html) provided in the NCSDK.
* Prototyping a user application on a development computer (host system), which accesses the neural compute device hardware to accelerate DNN inferences using the [NCAPI](https://movidius.github.io/ncsdk/ncapi/readme.html).

![](https://movidius.github.io/ncsdk/images/ncs_workflow.jpg)

### Intel® Movidius™ Neural Compute Stick (Intel® Movidius™ NCS)

* Prerequisite (one of the following)
    * Intel® Movidius™ Neural Compute SDK (Intel® Movidius™ NCSDK)
    * Neural Compute API (NCAPI)
* Interface
    * USB 2.0 High Speed interface
    * USB 3.0 High Speed interface
* Architecture
    * Powered by *Intel® Movidius™ Myriad™ 2 vision processing unit (VPU)*

![](https://movidius.github.io/ncsdk/images/NCS1_ArchDiagram.jpg)

---
## Contents

* [Tutorials](src/tutorials)

---
## Contributing

To know how to contribute this repository, please refer to this [document](CONTRIBUTING.md) first. Thanks for your cooperation.

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

[Apache License 2.0](LICENSE)