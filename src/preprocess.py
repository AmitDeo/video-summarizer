import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.vgg16 import preprocess_input
import streamlit as st


def extract_features(frame):
    # Resize the frame to the input size of the VGG16 model (224 x 224)
    frame = cv2.resize(frame, (224, 224))
    # Preprocess the frame for the VGG16 model
    frame = preprocess_input(frame)
    # Load the pre-trained VGG16 model
    model = tf.keras.applications.VGG16(weights='imagenet', include_top=False)
    # Extract features from the frame using the VGG16 model
    features = model.predict(np.expand_dims(frame, axis=0))[0]
    # Flatten the feature tensor into a feature vector
    feature_vector = features.flatten()
    return feature_vector

# Extract features from the frames
def preprocess(video, print_fn=print):
    length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total {length} frames!")

    frames = []
    features = []

    with st.spinner("Using Imagenet VGG16 to extract the feature. It can take a while."):
        progress_bar = st.progress(0)
        for i in range(length):
            ret, frame = video.read()
            if not ret:
                break
            frames.append(frame)

            feature = extract_features(frame)
            features.append(feature)

            # Update the progress bar
            progress_bar.progress((i + 1) / length)

    number_of_clusters = int(len(features)*0.1)

    return frames, features, number_of_clusters

'''
features = []
for frame in frames:
    feature = extract_features(frame)
    features.append(feature)

# Save Frames for model to use
with open('frames.pkl', 'wb') as f:
    pickle.dump(frames, f)

# Save Features for model to use
with open('features.pkl', 'wb') as f:
    pickle.dump(features, f)
'''
