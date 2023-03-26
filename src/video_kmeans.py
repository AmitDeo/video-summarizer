import cv2
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from preprocess import preprocess

def video_kmeans(video_path, output_path, print_fn=print):
    video = cv2.VideoCapture(video_path)

    # Prepocess
    frames, features, number_of_clusters = preprocess(video, print_fn)

    print_fn("Preprocessed Complete! Now running K-means to cluster the key frames.")
    # Cluster the frames using K-Means
    kmeans = KMeans(n_clusters=number_of_clusters, random_state=0).fit(features)

    # Select representative frames from each cluster
    summary_frames = []
    closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_, features)

    summary_frames = np.array(frames)[sorted(closest)]

    # Save the summary as a video
    print_fn("MP4 Format.")
    video_writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), video.get(cv2.CAP_PROP_FPS), (summary_frames[0].shape[1], summary_frames[0].shape[0]))
    for frame in summary_frames:
        video_writer.write(frame)
    video_writer.release()
    print_fn("Completed summarizing the video.")

