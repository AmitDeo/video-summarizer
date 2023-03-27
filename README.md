# Video Summarization with ImageNet and K-means with MLOps


## INTRODUCTION

This project is about video summarization using the ImageNet VGG16 feature extraction and using the K-means clustering to group the similar features to summarize the video. This project also demonstrates using multistage Docker to bundle the app to be run and deployed on any machine or server. The developed model is served through the Streamlit which is creates the web app for the user to upload video and download the summarized video. This project uses the poetry to install and manage the dependencies.



## GETTING STARTED
1.	Clone the repository on your local machine

    `git clone git@github.com:AmitDeo/video-summarizer.git`


2.	Go inside video-summarizer folder.

3.	Make sure you have docker installed on your machine.
https://docs.docker.com/engine/install/

4.	Build the image and run the container. This can take a while to build and run the container.
`docker compose up --build`

5.	Open the webapp powered by streamlit on http://localhost:8000 .
6.	Upload the video. Make sure it’s less than 100mb.
7.	You will see progress bar until you see the download for summarized video

## DATASET

The dataset used to extract the features was VGG16 from imagenet. The dataset was not explicitly downloaded to train the model as the trained model is available through `tensorflow.keras.applications.vgg16` .


## METHODOLOGY

### Feature Extraction

The video was loaded through OpenCV and the frames were extracted by the library. The frames were fed to vgg16 Imagenet model to extract the features. The features were saved as array. So the length of features array was equal to length of the frames in the video.

### Kmeans Clustering

The features array was fed to Kmeans algorithm to cluster the features. The number of centroids or the number of clusters was set to 10% of total frames. So if the video have 1000 frames the summary video will have 100 frames. The frame that was closest to centroid was chose for the summarization. Later the summarized frames was sorted as per the timeline. The summarized frames was encoded into mp4 format and saved as file for download.

### Docker and Poetry for MLOps

The multistage docker image was built using DockerFile and docker-compose.yml. The python-slim which Debian version of inux image was used. The multi-stage dockerization technique was used. The required libraries for opencv, numpy, pandas and tensorflow was installed during image building process. Poetry was used to manage the python version and dependency libraries. Poetry is the tool that helps us to install the dev and root dependencies separately.

### Streamlit

Streamlit is the fast tools that helps us to spin up the web app to serve the data apps. It provides many html and model serving tools that help to easily serve the model for the world to consume through web browser. I have used the streamlit to spin up the web app where user can upload the video. The video is fed through model for summarization. While summarization is long process, the progress bar is visible. After summarization, the download link is presented to download the video file.

You can see full video and summarized video in sample folder.


## LIMITATIONS

1.	Video file can be huge and all the frames was loaded in memory at once. So, this model cannot be used for the big size video. We can use the technique where the frames can
be processed and clustered in the batch.
2.	The VGG16 was used to extract the features. We could use the ResNet50 or Inception pre trained models for faster computation time and lesser memory consumptions.
3.	It is using simple unsupervised learning Kmeans. The model summarization could be enhanced using LSTM to take advantage of previous frames on current frame.



## SUMMARY

This project is demonstration of Deep Learning, Machine Learning and MLOps. It uses pre-trained Imagenet deep learning models to extract features. It uses Machine Learning KMeans algorithm to cluster. It takes advantage of Dockerization and Poetry to ship the models without effect of Operating System. It uses the Streamlit to serve the models as sleek web app.



## REFERENCES

- “Kmeans clustering for video summarization” - https://pdfs.semanticscholar.org/7fac/bc3ea6324fbda6e9db8ab4aec25100e59e9b.pdf
- “Docker for Machine Learning” - https://mlinproduction.com/docker-for-ml-part-3/
- “Docker Reference Guide” https://docs.docker.com/engine/reference/builder/
- “How to install Poetry to manage Python Dependencies on Ubuntu 22.04” https://www.digitalocean.com/community/tutorials/how-to-install-poetry-to-manage-python-dependencies-on-ubuntu-22-04
- “Reading and writing Videos using OpenCV” https://learnopencv.com/reading-and-writing-videos-using-opencv/
- “Streamlit API Reference” https://docs.streamlit.io/library/api-reference
