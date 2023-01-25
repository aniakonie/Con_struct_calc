import cv2 as cv
import numpy as np
import os

def cross_section_img():


	# diameter = 20
	# diameter_s = 8
	# cover = 30

	a1x = cover + diameter_s + diameter/2
	a1x = int(a1x)

	#BGR, nie RGB

	img = np.zeros((height*10, width*10, 3), dtype=np.uint8)


	# cross section
	cv.rectangle(img, (0,0), (width*10, height*10), (160,160,160), -1)

	# stirrup
	cv.rectangle(img, (cover+int(diameter_s/2),cover+int(diameter_s/2)), (width*10-cover-int(diameter_s/2), height*10-cover-int(diameter_s/2)), (64,64,64), 8)

	# rebar
	cv.circle(img, (a1x, a1x), int(diameter/2), (32,32,32), -1)


	

	path = 'C:\\Users\\konie\\OneDrive\\STUFF\\CODING\\01 ZAKOTWIENIE PRĘTÓW\\website\\static'

	os.chdir(path)
	cv.imwrite('concrete_cross_section.jpg', img)

	# cv.imshow("concrete_cross_section", img)

	# cv.waitKey(0)
	# cv.destroyAllWindows()




