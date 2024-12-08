import os
import cv2
import argparse

# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--input_dir", type=str, required=True, help="Directory containing video frame folders")
parser.add_argument("--output_dir", type=str, required=True, help="Directory to save the output videos")
parser.add_argument("--fps", type=int, default=30, help="Frames per second for the videos")
args = parser.parse_args()

# Ensure the output directory exists
os.makedirs(args.output_dir, exist_ok=True)

# Iterate through folders named video_001 to video_0200


folder_name = "video_0050"  # Process only video_0050
folder_path = os.path.join(args.input_dir, folder_name)

if os.path.isdir(folder_path):
    output_video_path = os.path.join(args.output_dir, f"annotated_{folder_name}.mp4")
    print(f"Processing folder: {folder_name}")

    # Get the list of frame files sorted by frame index
    frame_files = sorted([os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.startswith("frame_") and f.endswith(".jpg")])
    
    if not frame_files:
        print(f"No frames found in {folder_path}.")
    else:
        # Read the first frame to get video dimensions
        first_frame = cv2.imread(frame_files[0])
        height, width, _ = first_frame.shape

        # Initialize the video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4
        video_writer = cv2.VideoWriter(output_video_path, fourcc, args.fps, (width, height))

        # Write each frame to the video
        for frame_file in frame_files:
            frame = cv2.imread(frame_file)
            video_writer.write(frame)

        video_writer.release()
        print(f"Video saved to {output_video_path}")
else:
    print(f"Folder {folder_name} does not exist. Skipping...")




##/Users/shashankshriram/Downloads/mi3Lab/New_Code/COOOL_Benchmark/output_frames
## /Users/shashankshriram/Downloads/mi3Lab/New_Code/COOOL_Benchmark/frame_to_video

