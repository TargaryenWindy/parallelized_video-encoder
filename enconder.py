import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
import uuid
import shutil

# Define the folder to move encoded files
encoded_folder = "encoded"
os.makedirs(encoded_folder, exist_ok=True)

# Number of parallel encodings
parallel_encodings = 3 

# x265 encoding arguments
x265_args = "--crf 20 --preset slow --rc-lookahead=60 --lookahead-slices=1 --b-adapt=2 --bframes=6 --no-sao --rskip=2 --rskip-edge-threshold=4 --limit-tu=2 --qcomp=0.60 --ctu=32 --merange=30 --vbv-maxrate=9856 --vbv-bufsize=19712" 

# Function to check if the file was already encoded
def already_encoded(file_name):
    encoded_file = os.path.join(encoded_folder, file_name)
    return os.path.exists(encoded_file)

# Function to encode a video
def encode_video(file_path):
    file_name = os.path.basename(file_path)
    output_video = os.path.join(encoded_folder, file_name)

    if already_encoded(file_name):
        print(f"Skipping {file_name}, already encoded.")
        return

    print(f"Encoding {file_name}...")

    # Create a unique temporary directory for each encoding process
    temp_dir = os.path.join(os.getcwd(), f"temp_{uuid.uuid4()}")
    os.makedirs(temp_dir, exist_ok=True)
    temp_encoded_file = os.path.join(temp_dir, f"{file_name}_encoded.mkv")

    # Ensure the file path is absolute
    file_path_abs = os.path.abspath(file_path)
    output_video_abs = os.path.abspath(output_video)

    # Use ffmpeg to pipe the video to x265 for encoding in raw yuv format
    ffmpeg_cmd = [
        "ffmpeg", "-i", file_path_abs, "-f", "yuv4mpegpipe", "-bufsize", "2000k", "-"
    ]
    x265_cmd = [
        "x265", *x265_args.split(), "-o", temp_encoded_file, "--y4m", "-"
    ]

    # subprocess to run ffmpeg and pipe it to x265
    ffmpeg = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE)
    subprocess.run(x265_cmd, stdin=ffmpeg.stdout, check=True)
    ffmpeg.stdout.close()

    # Merge the encoded video with the audio, subtitles, and metadata from the original
    mkvmerge_cmd = [
        "mkvmerge", "-o", output_video_abs, temp_encoded_file, "-D", file_path_abs
    ]
    subprocess.run(mkvmerge_cmd, check=True)

    # delete temporary folder
    shutil.rmtree(temp_dir)
    print(f"Finished encoding {file_name}")

# process all video files in the directory
def process_videos():
    video_extensions = ['.mkv', '.mp4', '.avi', '.mov']
    video_files = [f for f in os.listdir() if os.path.splitext(f)[1].lower() in video_extensions]

    with ThreadPoolExecutor(max_workers=parallel_encodings) as executor:
        for video_file in video_files:
            file_path = os.path.join(os.getcwd(), video_file)
            executor.submit(encode_video, file_path)

if __name__ == "__main__":
    process_videos()
