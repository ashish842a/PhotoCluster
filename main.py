import cv2
import os
import numpy as np
from sklearn.cluster import DBSCAN
from collections import defaultdict
import shutil

# Function to extract face embeddings
def extract_face_embeddings(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) == 0:
        return None

    (x, y, w, h) = faces[0]
    face = image[y:y+h, x:x+w]
    face = cv2.resize(face, (100, 100))
    face_flatten = face.flatten()
    return face_flatten

# Directory containing the images
image_dir = 'D:\practice for interview\Project\face_encoding\images'

# Load images and extract face embeddings
def load_images_and_extract_faces(image_dir):
    face_encodings = []
    image_paths = []

    for file_name in os.listdir(image_dir):
        image_path = os.path.join(image_dir, file_name)
        face_encoding = extract_face_embeddings(image_path)
        if face_encoding is not None:
            face_encodings.append(face_encoding)
            image_paths.append(image_path)

    return face_encodings, image_paths

face_encodings, image_paths = load_images_and_extract_faces(image_dir)

# Cluster faces
def cluster_faces(face_encodings):
    dbscan = DBSCAN(metric='euclidean', n_jobs=-1)
    labels = dbscan.fit_predict(face_encodings)
    return labels

labels = cluster_faces(face_encodings)

# Group images by person
def group_images_by_person(labels, image_paths):
    groups = defaultdict(list)
    for label, image_path in zip(labels, image_paths):
        groups[label].append(image_path)
    return groups

grouped_images = group_images_by_person(labels, image_paths)

# Save grouped images into directories
def save_grouped_images(groups, output_dir='grouped_images'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for label, image_paths in groups.items():
        label_dir = os.path.join(output_dir, f'person_{label}')
        if not os.path.exists(label_dir):
            os.makedirs(label_dir)

        for image_path in image_paths:
            shutil.copy(image_path, label_dir)

save_grouped_images(grouped_images)
