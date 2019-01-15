# Install Intel® Movidius™ NCSDK v2.x with Docker container

# Check out the latest version of NCSDK 2 from the ncsdk2 branch
# The master branch is the version of NCSDK 1.x
git clone -b ncsdk2 http://github.com/Movidius/ncsdk

# Change the directory into "./ncsdk/"
cd ncsdk/

# Create a Docker image
docker build -t ncsdk -f ./extras/docker/Dockerfile_NoPreviligeAccess .