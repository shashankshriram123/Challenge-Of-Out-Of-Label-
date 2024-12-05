import os
import pickle
import matplotlib.pyplot as plt
import matplotlib.patches as patches

print(f"imported os, pickle, matplotlib successfully ")


# Load the pickle file
pickle_file_path = "/Users/shashankshriram/Downloads/mi3Lab/annotations_public.pkl" 
with open(pickle_file_path, "rb") as f:
    data = pickle.load(f)

# Directory to save frames with bounding boxes
output_dir = "output_frames"
os.makedirs(output_dir, exist_ok=True)


def save_bounding_boxes_for_video(video_id):
    video_data = data.get(video_id, {})
    if not video_data:
        print(f"No data available for video '{video_id}'.")
        return

    for frame_id, frame_content in video_data.items():
        frame_data = frame_content.get("traffic_scene", [])
        
        # Create a blank canvas
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.set_xlim(0, 1280)  # Adjust based on your frame resolution
        ax.set_ylim(0, 720)   # Adjust based on your frame resolution
        ax.invert_yaxis()     # Match the coordinate system
        ax.set_title(f"Video {video_id}, Frame {frame_id}")
        ax.set_xlabel("Width")
        ax.set_ylabel("Height")

        # Draw each bounding box
        for obj in frame_data:
            bbox = obj["bbox"]
            track_id = obj["track_id"]
            rect = patches.Rectangle(
                (bbox[0], bbox[1]),  # Bottom-left corner
                bbox[2] - bbox[0],   # Width
                bbox[3] - bbox[1],   # Height
                linewidth=2,
                edgecolor='red',
                facecolor='none'
            )
            ax.add_patch(rect)
            ax.text(bbox[0], bbox[1] - 10, f"ID {track_id}", color='blue', fontsize=10)

        # Save the frame with the naming format: {video_name}_frame_<frame_id>.png
        output_path = os.path.join(output_dir, f"{video_id}_frame_{frame_id}.png")
        plt.savefig(output_path, bbox_inches='tight')
        plt.close(fig)

    print(f"Frames for video '{video_id}' have been saved with the naming format {video_id}_frame_<frame_id>.png.")





##save_bounding_boxes_for_video("/Users/shashankshriram/Downloads/mi3Lab/dataset/COOOL_Benchmark/video_0050.mp4")