import face_recognition
import cv2
import os
from sklearn.cluster import DBSCAN
import numpy as np
from collections import defaultdict
import shutil

# Directory containing the images
image_dir = 'D:\practice for interview\Project\face_encoding\images'

# Load images and detect faces
def load_images_and_detect_faces(image_dir):
    face_encodings = []
    image_paths = []

    for file_name in os.listdir(image_dir):
        image_path = os.path.join(image_dir, file_name)
        image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(image)

        if face_locations:
            face_encoding = face_recognition.face_encodings(image, face_locations)[0]
            face_encodings.append(face_encoding)
            image_paths.append(image_path)

    return face_encodings, image_paths

face_encodings, image_paths = load_images_and_detect_faces(image_dir)

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
