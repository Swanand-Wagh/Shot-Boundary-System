import cv2
import numpy as np
import pandas as pd
import time
import os

video_path = './20020924_juve_dk_02a_1.avi'

# Function to calculate intensity histogram vectorized
def calculate_intensity_vectorized(rgb_image):
    # Calculate intensity from RGB values for an entire image
    intensity = np.dot(rgb_image[..., :3], [0.299, 0.587, 0.114])
    return np.histogram(intensity, bins=np.arange(0, 256, 10))[0]

# Function to read video frames and extract intensity histograms
def read_video_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return None  # Return None if the video cannot be opened

    frames_to_process = range(1000, 5000)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print("Total frames in the video:", total_frames)

    intensity_histograms = []

    for frame_index in range(total_frames):
        ret, frame = cap.read()
        if not ret:
            break

        if frame_index in frames_to_process:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            intensity_histogram = calculate_intensity_vectorized(rgb_frame)
            intensity_histograms.append(intensity_histogram)

    cap.release()
    print("Number of frames processed:", len(intensity_histograms))

    return np.array(intensity_histograms)

# Function to convert video frames to histograms
def video_to_histograms(video_path):
    file_name = video_path.split('/')[-1].split('.')[0]
    time_start = time.time()

    histograms_array = read_video_frames(video_path)
    if histograms_array is None or len(histograms_array) == 0:
        print("Error: Histograms could not be generated.")
        return None

    np.save(f'./histograms_array_{file_name}.npy', histograms_array)
    
    end_time = time.time()
    print("Time taken in seconds : ", (end_time - time_start))

    return histograms_array

# Function to load histograms from file or generate if not available
def load_or_generate_histograms(video_path):
    file_name = video_path.split('/')[-1].split('.')[0]
    npy_file_path = f'./histograms_array_{file_name}.npy'

    if os.path.exists(npy_file_path):
        histograms_array = np.load(npy_file_path)
    else:
        histograms_array = video_to_histograms(video_path)

    return histograms_array

# Function to calculate distance between consecutive histograms
def calculate_distance(histograms_arrays: np.ndarray):
    distances = []
    for i in range(0, len(histograms_arrays) - 1):
        first_histogram = histograms_arrays[i]
        second_histogram = histograms_arrays[i + 1]
        sub = np.subtract(first_histogram, second_histogram)
        distances.append(np.sum(np.abs(sub)))
    return np.array(distances)

# Function to calculate thresholds based on distances
def calculate_threshold(distances: np.ndarray):
    Tb = np.mean(distances) + np.std(distances) * 11
    Ts = np.mean(distances) * 2
    return Tb, Ts

# Function to identify pairs based on thresholds and tolerance
def calculate_pairs(distances: np.ndarray, Tb: float, Ts: float, tor: int):
    cs_ce_pairs = [] 
    fs_fe_pairs = []  

    fs_candi = -1
    fe_candi = -1

    tor_counter = 0

    candi_sum = 0
    for i in range(len(distances)):
        if distances[i] >= Tb:
            if fe_candi != -1:
                if candi_sum >= Tb:
                    fs_fe_pairs.append((fs_candi, fe_candi))
                    candi_sum = 0
            cs_ce_pairs.append((i, i + 1))
            fs_candi = -1
            fe_candi = -1
            tor_counter = 0
            
        elif Ts <= distances[i] < Tb:
            if fs_candi == -1:
                fs_candi = i
            fe_candi = i
            tor_counter = 0
            candi_sum += distances[i]
            
        elif distances[i] < Ts:
            tor_counter += 1
            if tor_counter >= tor:
                if fe_candi != -1:
                    if candi_sum >= Tb:
                        fs_fe_pairs.append((fs_candi, fe_candi))
                        candi_sum = 0
                fs_candi = -1
                fe_candi = -1

    return cs_ce_pairs, fs_fe_pairs


def get_fps(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return None

    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return fps


def generate_timestamp_pairs(merged_array, frame_start, frame_end, fps):
    frame_pairs = []
    start_frame = frame_start

    for idx, frame_index in enumerate(merged_array):
        end_frame = frame_index - 1
        frame_pairs.append((start_frame, end_frame))
        start_frame = frame_index

    # Add the last frame pair from the last frame in merged_array to frame_end
    frame_pairs.append((start_frame, frame_end))
    timestamps_pairs = [(start / fps, end / fps) for start, end in frame_pairs]

    return frame_pairs, timestamps_pairs


# Load or generate histograms for the given video
histograms = load_or_generate_histograms(video_path)

# Perform calculations if histograms are available
if histograms is None:
    print("Error: Histograms could not be generated or loaded.")
else:
    # Calculate distances between consecutive histograms
    sd = calculate_distance(histograms)

    # Calculate thresholds for segmentation
    tb, ts = calculate_threshold(sd)
    tor = 2  # Tolerance threshold
    # print("tb=",tb,"ts=",ts)

    # Identify pairs based on thresholds and tolerance
    cs_ce_pairs, fs_fe_pairs = calculate_pairs(sd, tb, ts, tor)
    # Adjust indices to match the original frame numbers
    cs_ce_pairs = [(cs + 1000, ce + 1000) for cs, ce in cs_ce_pairs]
    fs_fe_pairs = [(fs + 1000, fe + 1000) for fs, fe in fs_fe_pairs]

    # Extract specific indices for display
    ce = [ce for _, ce in cs_ce_pairs]
    fs = [(fs + 1) for fs, _ in fs_fe_pairs]
    print("ce =", ce)
    print("fs =", fs)

    # Merging ce and fs+1 arrays
    merged_array = ce + fs
    merged_array.sort()
    # print("merged array=",merged_array)

    # Generate timestamp pairs for display
    frame_pairs, timestamps_pairs = generate_timestamp_pairs(merged_array, 1000, 4999, get_fps(video_path) or 25)
    # print("Frame pairs:", frame_pairs)
    # print("Timestamp pairs:", timestamps_pairs)
