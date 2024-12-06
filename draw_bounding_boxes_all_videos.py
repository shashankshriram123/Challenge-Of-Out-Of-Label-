import os
import cv2
import pickle
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--annotations", type=str, required=True, help="Annotations Pickle File")
parser.add_argument("--output_dir", type=str, required=True, help="Folder to Save Annotated Frames")
parser.add_argument("--video_root", type=str, required=True, help="Folder containing video files")

args = parser.parse_args()

# Load the annotations
with open(args.annotations, "rb") as f:
    data = pickle.load(f)

# Iterate through each video in the data
for video_id in {entry["video_id"] for entry in data}:  # Unique video IDs
    print(f"Processing video: {video_id}")

    # Create a directory for the video
    video_dir = os.path.join(args.output_dir, video_id)
    os.makedirs(video_dir, exist_ok=True)

    # Load the video file
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

        # Collect all bounding boxes for the current frame
        frame_entries = [e for e in data if e["video_id"] == video_id and e["frame_id"] == frame_count]

        # Draw all bounding boxes for the current frame
        for obj in frame_entries:
            bbox = obj["bbox"]
            track_id = obj["track_id"]
            bbox_type = obj["type"]

            # Set color based on type
            color = (0, 255, 0) if bbox_type == "traffic_scene" else (0, 0, 255)
            x_min, y_min, x_max, y_max = map(int, bbox)

            # Draw the rectangle and label
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), color, 2)
            label = f"ID: {track_id} ({bbox_type})"
            cv2.putText(frame, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Save the annotated frame after all boxes are drawn
        output_frame_path = os.path.join(video_dir, f"frame_{frame_count}.png")
        cv2.imwrite(output_frame_path, frame)
        print(f"Saved annotated frame: {output_frame_path}")

        frame_count += 1

    cap.release()

print(f"Annotated frames saved to: {args.output_dir}")