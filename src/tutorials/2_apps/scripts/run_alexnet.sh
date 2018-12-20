# Make sure your current directory is "./examples/"
make alexnet
python3 image-classifier.py --graph ./caffe/AlexNet/graph --dim 227 227 --image ./data/images/pic_053.jpg