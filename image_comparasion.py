from imaging_interview import preprocess_image_change_detection, compare_frames_change_detection
import glob
import os
import cv2
import shutil
from pathlib import Path
import argparse
  
'''
This program uses the function preprocess_image_change_detection and compare_frames_change_detection. 
Using those functions one can compare two images using compare frames_change_detection function 
which give score and restultant contours. By thresholding the score we can decide wether the images
look similar or not.

"I added the cv2.resize(gray, (640,480)) line in the function preprocess_image_change_detection 
to get both images for similar size".

inputs:
--score_threshold : Integer value for thresholding the similarity score
--min_contour_area: Integer value for min_contour area for thresholding contour areas obtained from the 
                    imutils.grab_contours
--dataset_path    : Path where you palced your dataset.
--destination_path: Path to move the similar images
--image_extention : extention of the images we are working with in our case it is '.png'.
'''

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--score_threshold', type=int, default=10000, help='Score threshold for comparison')
    parser.add_argument('-m','--min_contour_area', type=int, default=5000, help='minmum contour area')
    parser.add_argument('-d','--dataset_path', help='Specify the dataset_path', type=str)
    parser.add_argument('-des','--destination_path', help='Specify the path for moving the similar images', type=str)
    parser.add_argument('-e','--image_extention', type=str, default='.png', help='.jpg or .png or any other image extentions')
    args = parser.parse_args()

    destination_folder = Path(args.destination_path)
    destination_folder.mkdir(parents=True, exist_ok=True)
    image_type = args.image_extention
    dataset_path = args.dataset_path
    dataset_path = dataset_path+'/*'+image_type
    images = glob.glob(dataset_path)
    score_threshold = args.score_threshold 
    reference_frame = cv2.imread(images[0])
    for i  in range(1,len(images)):
        next_frame = cv2.imread(images[i])
        prev_frame = preprocess_image_change_detection(reference_frame)
        next_frame = preprocess_image_change_detection(next_frame)
        score, _,_ = compare_frames_change_detection(prev_frame ,next_frame ,min_contour_area=args.min_contour_area)
        if score > score_threshold:
            reference_frame = cv2.imread(images[i])
        if score < score_threshold:
            img_path,img_name = os.path.split(images[i])
            src = Path(images[i])
            dst = destination_folder/Path(img_name)
            shutil.move(src,dst)



