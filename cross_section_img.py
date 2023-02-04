import cv2 as cv
import numpy as np
import os

#BGR, nie RGB

def cross_section_img(diameter11, diameter12, quantity11, quantity12, cover, diameter_s, height, width):


	height_mm = height*10
	width_mm = width*10
	img = np.zeros((height_mm, width_mm, 3), dtype=np.uint8)

	a1x = cover + diameter_s + diameter11/2
	a1x = int(a1x)

	# cross section
	cv.rectangle(img, (0,0), (width_mm, height_mm), (160,160,160), -1)

	# stirrup
	cv.rectangle(img, (cover+int(diameter_s/2),cover+int(diameter_s/2)), (width_mm-cover-int(diameter_s/2), height_mm-cover-int(diameter_s/2)), (64,64,64), 8)

	# rebar
	cv.circle(img, (a1x, height_mm-a1x), int(diameter11/2), (32,32,32), -1)


	width_rebar_mm = width_mm - 2*cover - 2*diameter_s
	rebar_spacing = int((width_rebar_mm - quantity11*diameter11 - quantity12*diameter12)/(quantity11 + quantity12 - 1))


	# only first type of bars
	if quantity12 == 0:

		rebar_center = a1x + rebar_spacing + diameter11

		for q in range(1,quantity11):

			cv.circle(img, (rebar_center, height_mm-a1x), int(diameter11/2), (32,32,32), -1)
			rebar_center = rebar_center + rebar_spacing + diameter11



	# first + second type of bars
	else:

		a12x = cover + diameter_s + diameter12/2
		a12x = int(a12x)

		#left hand corner bar
		cv.circle(img, (a1x, height_mm-a1x), int(diameter11/2), (32,32,32), -1)
		#right hand corner bar
		cv.circle(img, (width_mm-a1x, height_mm-a1x), int(diameter11/2), (32,32,32), -1)


		if quantity11%2 == 1:

			# rebar in the middle
			cv.circle(img, (int(width_mm/2), height_mm-a1x), int(diameter11/2), (32,32,32), -1)

			rebar_center = a1x + rebar_spacing + diameter11

			for q in range(1,int((quantity11-1)/2)):

				cv.circle(img, (rebar_center, height_mm-a1x), int(diameter11/2), (32,32,32), -1)
				cv.circle(img, (width_mm - rebar_center, height_mm-a1x), int(diameter11/2), (32,32,32), -1)
				rebar_center = rebar_center + rebar_spacing + diameter11


			rebar_center = int(rebar_center - 0.5*diameter11 + 0.5*diameter12)

			for q in range(1,int(quantity12/2)+1):

				cv.circle(img, (rebar_center, height_mm-a12x), int(diameter12/2), (32,32,32), -1)
				cv.circle(img, (width_mm - rebar_center, height_mm-a12x), int(diameter12/2), (32,32,32), -1)
				rebar_center = rebar_center + rebar_spacing + diameter12


		if quantity11%2 == 0:

			rebar_center = a1x + rebar_spacing + diameter11

			for q in range(1,int(quantity11/2)):

				cv.circle(img, (rebar_center, height_mm-a1x), int(diameter11/2), (32,32,32), -1)
				cv.circle(img, (width_mm - rebar_center, height_mm-a1x), int(diameter11/2), (32,32,32), -1)
				rebar_center = rebar_center + rebar_spacing + diameter11

			rebar_center = int(rebar_center - 0.5*diameter11 + 0.5*diameter12)

			if quantity12%2 == 0:

				for q in range(1,int(quantity12/2)+1):

					cv.circle(img, (rebar_center, height_mm-a12x), int(diameter12/2), (32,32,32), -1)
					cv.circle(img, (width_mm - rebar_center, height_mm-a12x), int(diameter12/2), (32,32,32), -1)
					rebar_center = rebar_center + rebar_spacing + diameter12


			if quantity12%2 == 1:

				#rebar in the middle
				cv.circle(img, (int(width_mm/2), height_mm-a12x), int(diameter12/2), (32,32,32), -1)

				for q in range(1,int((quantity12-1)/2)+1):

					cv.circle(img, (rebar_center, height_mm-a12x), int(diameter12/2), (32,32,32), -1)
					cv.circle(img, (width_mm - rebar_center, height_mm-a12x), int(diameter12/2), (32,32,32), -1)
					rebar_center = rebar_center + rebar_spacing + diameter12	



	path = 'C:\\Users\\konie\\OneDrive\\STUFF\\CODING\\01 ZAKOTWIENIE PRĘTÓW\\website\\static'

	os.chdir(path)
	cv.imwrite('concrete_cross_section.jpg', img)



	# # cv.imshow("concrete_cross_section", img)

	# # cv.waitKey(0)
	# # cv.destroyAllWindows()