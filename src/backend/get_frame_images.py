import cv2
import os

# Path to your video file
video_path = './20020924_juve_dk_02a_1.avi'

# Create a directory to save the extracted images
output_dir = 'images'
os.makedirs(output_dir, exist_ok=True)

# Frame numbers from the merged_array
frame_numbers = [1000, 1091, 1112, 1180, 1575, 1618, 1865, 1926, 2332, 2406, 2584, 2678, 3008, 3050, 3059, 3200, 3277, 3532, 3551, 3625, 3656, 3765, 3838, 3928, 4013, 4042, 4299, 4357, 4358, 4484, 4561, 4608, 4776, 4986]

# Open the video file
cap = cv2.VideoCapture(video_path)

# Counter for image naming
count = 0

# Loop through each frame number and extract the corresponding frame
for frame_number in frame_numbers:
    # Set the frame number to extract
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    # Read the frame
    ret, frame = cap.read()

    if ret:
        # Save the frame as a PNG image
        output_path = os.path.join(output_dir, f"{count}.png")
        cv2.imwrite(output_path, frame)
        print(f"Frame {frame_number} saved as {output_path}")
        count += 1

# Release the video capture object and close the video file
cap.release()
cv2.destroyAllWindows()
