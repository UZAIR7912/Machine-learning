import os
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import tensorflow as tf

mnist = tf.keras.datasets.mnist
(x_train,y_train),(x_test,y_test) = mnist.load_data()

x_train = tf.keras.utils.normalize(x_train,axis=1)
x_test = tf.keras.utils.normalize(x_test,axis=1)

model = tf.keras.models.load_model("digit_recognizer.keras")

img = cv.imread("digit2.jpg")[:,:,0]
img = np.invert(np.array([img]))
prediction = model.predict(img)
print(f"this digit is probably a {np.argmax(prediction)}")
plt.imshow(img[0],cmap=plt.cm.binary)
plt.show()