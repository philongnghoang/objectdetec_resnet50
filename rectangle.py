import sys
import cv2
import numpy as np
# Load modun Object Detection
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
			cv2.rectangle(img, top_left_pt, bottom_right_pt, (0,255,0), 2)
	# Detecting the mouse button up event
	elif event == cv2.EVENT_LBUTTONUP:
		drawing = False
		top_left_pt, bottom_right_pt = (x_init,y_init), (x,y)
		# Create the "negative" film effect for the selected # region
		img[y_init:y, x_init:x] = 255 - img[y_init:y, x_init:x]
		# Draw rectangle around the selected region
		cv2.rectangle(img, top_left_pt, bottom_right_pt, (0,255,0), 2)
		rect_final = (x_init, y_init, x-x_init, y-y_init)
		print(rect_final)
		x,y,w,h = rect_final
		crop_img = img[y:y+h, x:x+w] 
		cv2.imshow('hinh',crop_img)
		return crop_img

if __name__=='__main__':
	img_input = cv2.imread("4.jpg")
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