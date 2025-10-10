import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from tensorflow.keras import datasets,layers,models #type: ignore
(training_images,training_labels),(testing_images,testing_labels)=datasets.cifar10.load_data()
training_images,testing_images = training_images/255,testing_images/255
class_names = ["Plane","Car","Bird","Cat","Deer","Dog","Frog","Horse","Ship","Truck"]
for i in range(16):
    plt.subplot(4,4,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(training_images[i],cmap=plt.cm.binary)
    plt.xlabel(class_names[training_labels[i][0]])

training_images = training_images[:20000]
training_labels = training_labels[:20000]
testing_images = testing_images[:4000]
testing_labels = testing_labels[:4000]

model = models.load_model("image_classifier.keras")

images_downloaded = ["car.jpg","deer.jpg","horse.jpg","plane.jpg"]

for i in range(0,4):
    img = cv.imread(images_downloaded[i])
    img = cv.cvtColor(img,cv.COLOR_BGR2RGB)
    plt.imshow(img,cmap=plt.cm.binary)
    prediction = model.predict(np.array([img]) / 255)
    index = np.argmax(prediction)
    print(f"prediction is: {class_names[index]}")