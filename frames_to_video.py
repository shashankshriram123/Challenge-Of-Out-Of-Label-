import os
import cv2
import argparse
import re  

# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--input_dir", type=str, required=True, help="Directory containing video frame folders")
parser.add_argument("--output_dir", type=str, required=True, help="Directory to save the output videos")
parser.add_argument("--fps", type=int, default=30, help="Frames per second for the videos")
args = parser.parse_args()

# Ensure the output directory exists
os.makedirs(args.output_dir, exist_ok=True)

# Iterate through folders named video_0001 to video_0200
for i in range(1, 201):  
    folder_name = f"video_{i:04d}" 
    folder_path = os.path.join(args.input_dir, folder_name)
    print(f"Processing folder: {folder_path}")

    if os.path.isdir(folder_path):  # Ensure it's a valid directory
        output_video_path = os.path.join(args.output_dir, f"{folder_name}.mp4")
        print(f"Processing folder: {folder_name}")

        try:
            # Filter and sort frame files
            frame_files = sorted(
                [os.path.join(folder_path, f) for f in os.listdir(folder_path)
                 if f.startswith("frame_") and f.endswith(".png") and f.split("_")[1].split(".")[0].isdigit()],
                key=lambda x: int(x.split("_")[1].split(".")[0])  # Sort by numerical suffix
            )

            # Debugging: Print the filenames being processed
            print(f"Frame files in {folder_name}: {frame_files}")

            if not frame_files:
                print(f"No valid frames found in {folder_path}. Skipping...")
                continue

            # Read the first frame to get video dimensions
            first_frame = cv2.imread(frame_files[0])
            height, width, _ = first_frame.shape

            # Initialize the video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
            video_writer = cv2.VideoWriter(output_video_path, fourcc, args.fps, (width, height))

            # Write each frame to the video
            for frame_file in frame_files:
                frame = cv2.imread(frame_file)
                video_writer.write(frame)

            video_writer.release()
            print(f"Video saved to {output_video_path}")
        except Exception as e:
            print(f"Error processing folder {folder_name}: {e}")
            continue
    else:
        print(f"Folder {folder_name} does not exist. Skipping...")
