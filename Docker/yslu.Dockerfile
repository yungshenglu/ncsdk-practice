# Download base image
FROM yungshenglu/ubuntu-env:16.04

# Update software repository
RUN apt-get update

# Install necessary packages for the installer
RUN apt-get install -y lsb-release build-essential sed tar udev

# Clean all downloaded packages
RUN apt-get clean

# Copy over the NCSDK
COPY ./ ncsdk/

# Set the current working directory to the cloned ncsdk directory
WORKDIR "/ncsdk"

# Run the installer
RUN make install