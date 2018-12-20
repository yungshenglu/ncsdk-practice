# Make sure your current directory is "./examples/"
make squeezenet
python3 image-classifier.py --graph ./caffe/SqueezeNet/graph --dim 227 227 --image ./data/images/pic_053.jpg