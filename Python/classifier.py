import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.neural_network import MLPClassifier
from skimage.feature import hog
from skimage import data, exposure
import numpy as np
import cv2


x_train = []
for i in range(16):
    x_train.append(cv2.imread("positive/opencv_frame_{}.png".format(i)).flatten())
for i in range(16):
    x_train.append(cv2.imread("negative/opencv_frame_{}.png".format(i)).flatten())

y_train = np.concatenate((np.ones(16), np.zeros(16)), axis=0)
x_train = np.array(x_train)
print(y_train.shape)
print(x_train.shape)
# mlp = MLPClassifier(hidden_layer_sizes=(10, 10, 10), max_iter=1000)
classifier = svm.SVC(gamma=0.001)
classifier.fit(x_train, y_train)
# mlp.fit(X_train, y_train.values.ravel())
prediction = classifier.predict(np.array([cv2.imread("negative/opencv_frame_{}.png".format(i)).flatten()]))
print(prediction)
# i = 1
# image = cv2.imread("positive/opencv_frame_{}.png".format(i))

# fd, hog_image = hog(image, orientations=8, pixels_per_cell=(16, 16),
#                     cells_per_block=(1, 1), visualize=True, multichannel=True)
#
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4), sharex=True, sharey=True)
#
# ax1.axis('off')
# ax1.imshow(image, cmap=plt.cm.gray)
# ax1.set_title('Input image')
#
# # Rescale histogram for better display
# hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 10))
#
# ax2.axis('off')
# ax2.imshow(hog_image_rescaled, cmap=plt.cm.gray)
# ax2.set_title('Histogram of Oriented Gradients')
# plt.show()
