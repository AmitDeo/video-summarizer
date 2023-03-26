import streamlit as st
import tempfile
from video_kmeans import video_kmeans

st.title('Video summarizer with ImageNet feature extracter and Kmeans Clustering!')

uploaded_file = st.file_uploader("Choose a Video file!", type="mp4")

if uploaded_file is not None and 'submitted' not in st.session_state:
    bytes_data = uploaded_file.getvalue()
    st.video(bytes_data)

    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())

    summary_file = tfile.name.split("/")[-1] + "_summary.mp4"

    video_kmeans(tfile.name, summary_file, print_fn=st.text)


    with open(summary_file, 'rb') as f:
        st.download_button('Download Summary Video', f, file_name=summary_file)
        st.session_state.submitted = True

    #summary_video = open(summary_file, "rb")
    #video_bytes = summary_video.read()

    #st.title("Here is the Summarized Video")
    #st.video(video_bytes)
