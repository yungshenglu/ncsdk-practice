#!/usr/bin/python3
#
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

# Python script to open and close a single NCS device

import mvnc.mvncapi as fx

# Entry point
if __name__=="__main__":
    # Set the logging level for the NC API
    fx.global_set_option(fx.GlobalOption.RW_LOG_LEVEL, 0)

    # Get a list of names for all the devices plugged into the system
    devices = fx.enumerate_devices()
    if (len(devices) < 1):
        print("Error - no NCS devices detected, verify an NCS device is connected.")
        quit() 

    # Get the first NCS device by its name
    # For this program we will always open the first NCS device
    dev = fx.Device(devices[0])

    # Try to open the device
    # This will throw an exception if someone else has it open already
    try:
        dev.open()
    except:
        print("Error - Could not open NCS device.")
        quit()
    print("Hello NCS! Device opened normally.")
    
    try:
        dev.close()
    except:
        print("Error - could not close NCS device.")
        quit()
    print("Goodbye NCS! Device closed normally.")
    print("NCS device working.")
    
