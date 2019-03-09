import sys
import cv2
import numpy as np

# Load modun Object Detection
from imageai.Detection import ObjectDetection
import os
import shutil
import time
execution_path = os.getcwd()
detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.0.1.h5"))
detector.loadModel(detection_speed="fastest")
# Draw rectangle on top of the input image
def draw_rectangle(event, x, y, flags, params):
	global x_init, y_init, drawing, top_left_pt, bottom_right_pt, img_orig
	# Detecting a mouse click
	if event == cv2.EVENT_LBUTTONDOWN:
		drawing = True
		x_init, y_init = x, y
	# Detecting mouse movement
	elif event == cv2.EVENT_MOUSEMOVE:
		if drawing:
			top_left_pt, bottom_right_pt = (x_init,y_init), (x,y)
			img[y_init:y, x_init:x] = 255 - img_orig[y_init:y, x_init:x]
			#cv2.rectangle(img, top_left_pt, bottom_right_pt, (0,255,0), 1)
	# Detecting the mouse button up event
	elif event == cv2.EVENT_LBUTTONUP:
		drawing = False
		top_left_pt, bottom_right_pt = (x_init,y_init), (x,y)
		# Create the "negative" film effect for the selected # region
		img[y_init:y, x_init:x] = 255 - img[y_init:y, x_init:x]
		# Draw rectangle around the selected region
		#cv2.rectangle(img, top_left_pt, bottom_right_pt, (0,255,0), 1)
		rect_final = (x_init, y_init, x-x_init, y-y_init)
		print('Click',rect_final)
		x,y,w,h = rect_final
		crop_img = img[y:y+h, x:x+w] 
		#cv2.imshow('hinh',crop_img)
		img_out = detecobject(crop_img)
		img[y:y+h, x:x+w] = img_out
		#cv2.imshow('result',img)
def detecobject(img_in):
	returned_image, detections, extracted_objects = detector.detectObjectsFromImage(
			input_type = "array",
			input_image=img_in,
			output_type="array", 
			extract_detected_objects=True, 
			minimum_percentage_probability=50)
	print('detections',detections)
	for eachObject in detections:
				#pos = detections[0, 1, :4].astype(int)
				#print ('pos',pos)
				print('eachObject:',eachObject)
	    		
	return returned_image
if __name__=='__main__':
	img_input = cv2.imread("9.jpg")
	drawing = False
	img = np.copy(img_input)
	img_orig = np.copy(img_input)
	cv2.namedWindow('Input')
	cv2.setMouseCallback('Input', draw_rectangle)
	#cv2.imshow('anh',anh)
	while True:
		cv2.imshow('Input', img)

		c = cv2.waitKey(10)
		if c == 27:
			break
	cv2.destroyAllWindows()