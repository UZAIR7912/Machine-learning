from sklearn.svm import LinearSVC
import numpy as np
import cv2 as cv
import PIL

class Model:
    def __init__(self):
        self.model = LinearSVC(max_iter=7500)
    def train_model(self, counters):
        img_lists = []
        class_lists = []

        for i in range(1, counters[0]):
            img = cv.imread(f"1/frame{i}.jpg")[:, :, 0]  # grayscale channel
            img = img.reshape(-1)  # flatten
            img_lists.append(img)
            class_lists.append(1)

        for i in range(1, counters[1]):
            img = cv.imread(f"2/frame{i}.jpg")[:, :, 0]
            img = img.reshape(-1)
            img_lists.append(img)
            class_lists.append(2)

        img_lists = np.array(img_lists)  # shape: (num_samples, img_size)
        class_lists = np.array(class_lists)

        self.model.fit(img_lists, class_lists)
        print("trained!!")
   
    def predict(self,frame):
        frame = frame[1]
        cv.imwrite('frame.jpg', cv.cvtColor(frame, cv.COLOR_RGB2GRAY))
        img = PIL.Image.open("frame.jpg")
        img.thumbnail((150, 150), PIL.Image.LANCZOS)
        img.save('frame.jpg')
        img = cv.imread("frame.jpg")[:,:,0]
        img = img.reshape(16950)
        prediction = self.model.predict(img.reshape(1, -1))
        
        return(prediction[0])

