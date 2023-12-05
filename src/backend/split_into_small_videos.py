import cv2
import os

def split_video(video_path, timestamp_pairs):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Create a folder to store the video clips
    output_folder = 'videos'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for idx, (start_time, end_time) in enumerate(timestamp_pairs):
        cap.set(cv2.CAP_PROP_POS_MSEC, start_time * 1000)
        fourcc = cv2.VideoWriter_fourcc(*'avc1')  # H.264 codec
        output_file = os.path.join(output_folder, f"{idx}.mp4")
        out = cv2.VideoWriter(output_file, fourcc, fps, (int(cap.get(3)), int(cap.get(4))), True)

        while cap.get(cv2.CAP_PROP_POS_MSEC) <= end_time * 1000:
            ret, frame = cap.read()
            if ret:
                out.write(frame)
            else:
                break

        out.release()

    cap.release()
    cv2.destroyAllWindows()

# Replace 'video_path' with the path to your video file
video_path = './files/20020924_juve_dk_02a_1.avi'

# Replace 'timestamp_pairs' with your provided pairs
timestamp_pairs = [(40.0, 43.6), (43.64, 44.44), (44.48, 62.96), (63.0, 64.68), (64.72, 74.56), (74.6, 77.0), (77.04, 93.24), (93.28, 96.2), (96.24, 103.32), (103.36, 107.0), (107.04, 120.28), (120.32, 121.96), (122.0, 127.96), (128.0, 131.0), (131.04, 141.24), (141.28, 142.0), (142.04, 144.92), (144.96, 150.56), (150.6, 153.48), (153.52, 157.08), (157.12, 161.64), (161.68, 171.96), (172.0, 174.28), (174.32, 179.32), (179.36, 182.4), (182.44, 184.12), (184.16, 191.0), (191.04, 195.64), (195.68, 199.4), (199.44, 199.96)]

# Call the function to split the video
split_video(video_path, timestamp_pairs)
