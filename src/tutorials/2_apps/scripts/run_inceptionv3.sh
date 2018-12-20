# Make sure your current directory is "./examples/"
make inception_v3
python3 image-classifier.py --graph ./tensorflow/inception_v3/graph --labels ./tensorflow/inception_v3/labels.txt --mean 127.5 --scale 0.00789 --dim 299 299 --colormode="RGB" --image ./data/images/pic_053.jpg