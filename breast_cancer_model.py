import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical

data_path = "/path/to/meme_kanseri_dataset"

data = []
labels = []

class_folder = "breast_cancer"

class_path = os.path.join(data_path, class_folder)

for image_file in os.listdir(class_path):
    image_path = os.path.join(class_path, image_file)

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, (128, 128))

    data.append(image)
    labels.append(1)

data = np.array(data) / 255.0
labels = np.array(labels)

labels_categorical = to_categorical(labels, num_classes=2)

X_train, X_test, y_train, y_test = train_test_split(data, labels_categorical, test_size=0.2, random_state=42)
