import cv2
import numpy as np
import glob
import os
import math

# --- 1. SETUP BOARD PARAMETERS ---
image_folder = 'calibration_images'
images = glob.glob(f'{image_folder}/*.*')

if len(images) == 0:
    print(f"ERROR: Found 0 images in the '{image_folder}' folder.")
    exit()

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

layouts = [
    ((8, 11), True,  "8x11 (Legacy calib.io default)"),
    ((8, 11), False, "8x11 (Modern OpenCV)"),
    ((11, 8), True,  "11x8 (Legacy calib.io default)"),
    ((11, 8), False, "11x8 (Modern OpenCV)")
]

working_board = None
working_detector = None
image_size = None

# --- 2. AUTO-DETECT LAYOUT ---
print(f"Found {len(images)} images. Testing board layouts...")
test_img = cv2.imread(images[0])
test_gray = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
image_size = test_gray.shape[::-1] 

for grid_size, is_legacy, name in layouts:
    board = cv2.aruco.CharucoBoard(grid_size, 0.020, 0.015, aruco_dict)
    board.setLegacyPattern(is_legacy)
    
    detector = cv2.aruco.CharucoDetector(board)
    charuco_corners, charuco_ids, _, _ = detector.detectBoard(test_gray)
    
    if charuco_corners is not None and len(charuco_corners) > 3:
        print(f"✅ SUCCESS! The physical board matches: {name}")
        working_board = board
        working_detector = detector
        break

if working_detector is None:
    print("❌ ERROR: None of the board layouts worked.")
    exit()

# --- 3. PROCESS DATASET ---
all_charuco_corners = []
all_charuco_ids = []
valid_images = 0

print(f"\nExtracting corners from dataset at {image_size[0]}x{image_size[1]} resolution...")
for fname in images:
    img = cv2.imread(fname)
    if img is None: continue
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    charuco_corners, charuco_ids, _, _ = working_detector.detectBoard(gray)
    
    if charuco_corners is not None and charuco_ids is not None and len(charuco_corners) > 3:
        all_charuco_corners.append(charuco_corners)
        all_charuco_ids.append(charuco_ids)
        valid_images += 1

# --- 4. COMPUTE INTRINSICS & ACCURACY ---
print(f"Successfully extracted data from {valid_images} out of {len(images)} images.")

if valid_images > 0:
    ret, mtx, dist, rvecs, tvecs = cv2.aruco.calibrateCameraCharuco(
        all_charuco_corners, all_charuco_ids, working_board, image_size, None, None)

    print("\n=== CALIBRATION MATRICES ===")
    print("\nIntrinsic Camera Matrix (K):")
    print(np.round(mtx, 4))
    print("\nDistortion Coefficients:")
    print(np.round(dist, 6))

    # --- 5. 200MP ACCURACY ANALYSIS ---
    print("\n=== 200MP ACCURACY ANALYSIS ===")
    
    img_width, img_height = image_size
    diag_pixels = math.sqrt(img_width**2 + img_height**2)
    
    # 1. Relative Percentage Error (Error divided by total diagonal pixel span)
    percent_error = (ret / diag_pixels) * 100
    
    # 2. 1080p Equivalent Error (Normalizing it to standard robotics cameras)
    equiv_1080p = ret * (1920 / img_width)

    print(f"Raw Reprojection Error : {ret:.4f} pixels")
    print(f"Sensor Diagonal Span   : {diag_pixels:.0f} pixels")
    print(f"Relative Accuracy      : {percent_error:.5f}% error across the sensor")
    print(f"1080p Equivalent Error : {equiv_1080p:.4f} pixels (Standard 'Good' is < 1.0)")
    
    print("\n=== PER-IMAGE ACCURACY (1080p Equivalent) ===")
    all_obj_points = working_board.getChessboardCorners()
    
    for i in range(len(all_charuco_corners)):
        obj_points = np.array([all_obj_points[idx[0]] for idx in all_charuco_ids[i]])
        projected_points, _ = cv2.projectPoints(obj_points, rvecs[i], tvecs[i], mtx, dist)
        
        raw_error = cv2.norm(all_charuco_corners[i], projected_points, cv2.NORM_L2) / len(projected_points)
        norm_error = raw_error * (1920 / img_width)
        
        print(f"Image {i+1} Normalized Error: {norm_error:.4f} pixels")

else:
    print("\nCalibration failed: No valid images to process.")