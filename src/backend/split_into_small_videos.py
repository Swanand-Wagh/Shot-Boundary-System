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
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output_file = os.path.join(output_folder, f"{idx}.mp4")
        out = cv2.VideoWriter(output_file, fourcc, fps, (int(cap.get(3)), int(cap.get(4))))

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
timestamp_pairs = [(40.0, 41.76), (41.8, 43.6), (43.64, 44.4), (44.44, 44.44), (44.48, 47.16), (47.2, 47.76), (47.8, 55.56), (55.6, 62.96), (63.0, 64.68), (64.72, 72.44), (72.48, 74.56), (74.6, 76.96), (77.0, 77.0), (77.04, 77.88), (77.92, 78.48), (78.52, 93.24), (93.28, 93.84), (93.88, 94.04), (94.08, 96.2), (96.24, 99.84), (99.88, 102.24), (102.28, 103.32), (103.36, 105.12), (105.16, 107.08), (107.12, 120.24), (120.28, 120.28), (120.32, 120.56), (120.6, 121.96), (122.0, 122.32), (122.36, 127.96), (128.0, 129.28), (129.32, 129.4), (129.44, 131.04), (131.08, 132.76), (132.8, 136.64), (136.68, 137.56), (137.6, 138.76), (138.8, 141.24), (141.28, 141.76), (141.8, 142.0), (142.04, 143.12), (143.16, 143.36), (143.4, 144.56), (144.6, 144.96), (145.0, 145.32), (145.36, 146.04), (146.08, 146.2), (146.24, 146.64), (146.68, 147.24), (147.28, 147.84), (147.88, 150.56), (150.6, 151.44), (151.48, 151.56), (151.6, 152.12), (152.16, 153.48), (153.52, 157.08), (157.12, 159.2), (159.24, 159.4), (159.44, 159.52), (159.56, 159.72), (159.76, 159.84), (159.88, 160.16), (160.2, 160.36), (160.4, 160.48), (160.52, 160.68), (160.72, 161.64), (161.68, 164.04), (164.08, 168.68), (168.72, 168.84), (168.88, 170.0), (170.04, 171.92), (171.96, 172.68), (172.72, 174.24), (174.28, 174.28), (174.32, 179.32), (179.36, 182.4), (182.44, 183.56), (183.6, 184.28), (184.32, 185.32), (185.36, 188.8), (188.84, 190.72), (190.76, 191.0), (191.04, 195.52), (195.56, 195.64), (195.68, 196.0), (196.04, 199.4), (199.44, 199.96)]

# Call the function to split the video
split_video(video_path, timestamp_pairs)
