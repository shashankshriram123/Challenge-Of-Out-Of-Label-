import os
import cv2
import pickle
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--annotations", type=str, required=True, help="Annotations Pickle File")
parser.add_argument("--output_dir", type=str, required=True, help="Folder to Save Annotated Frames")
parser.add_argument("--video_root", type=str, required=True, help="Folder containing video files")

args = parser.parse_args()

# Load the annotations data
pickle_file_path = args.annotations
with open(pickle_file_path, "rb") as f:
    data = pickle.load(f)

# Directory to save annotated frames
output_dir = args.output_dir
os.makedirs(output_dir, exist_ok=True)

# Iterate through each video in the data (assuming data is a list of dictionaries)
for entry in data:

    video_id = entry.get("video_id")
    if not video_id:
        print("Skipping entry without a video_id.")
        continue

    # Ensure we only process video_0050
    if video_id != "video_0050":
        continue

    # Create a directory for the video
    video_dir = os.path.join(output_dir, video_id)
    os.makedirs(video_dir, exist_ok=True)

    # Load the video file for the current video
    video_path = os.path.join(args.video_root, f"{video_id}.mp4")
    if not os.path.exists(video_path):
        print(f"Video file {video_path} not found. Skipping...")
        continue

    cap = cv2.VideoCapture(video_path)
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # End of video

        # Check if the frame exists in the data for this video
        if entry.get("frame_id") == frame_count:
            # Draw bounding boxes for traffic_scene
            if entry.get("type") == "traffic_scene":
                bbox = entry["bbox"]
                track_id = entry["track_id"]
                color = (0, 255, 0)  # Green for traffic_scene
                x_min, y_min, x_max, y_max = map(int, bbox)
                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), color, 2)
                label = f"ID: {track_id} (traffic_scene)"
                cv2.putText(frame, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # Draw bounding boxes for challenge_object
            elif entry.get("type") == "challenge_object":
                bbox = entry["bbox"]
                track_id = entry["track_id"]
                color = (0, 0, 255)  # Red for challenge_object
                x_min, y_min, x_max, y_max = map(int, bbox)
                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), color, 2)
                label = f"ID: {track_id} (challenge_object)"
                cv2.putText(frame, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # Save the annotated frame
            output_frame_path = os.path.join(video_dir, f"frame_{frame_count}.png")
            cv2.imwrite(output_frame_path, frame)
            print(f"Saved annotated frame: {output_frame_path}")

        frame_count += 1

    cap.release()

print(f"Annotated frames saved to: {output_dir}")
