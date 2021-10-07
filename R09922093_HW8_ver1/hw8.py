import cv2
import numpy as np
import math
image_dict = {}
def SNR(o_img,o_n_img):
	row, col = o_img.shape
	SUM = 0
	
	o_n_img.astype(np.float64)
	n_img = np.divide(o_n_img, 255)

	o_img.astype(np.float64)
	img = np.divide(o_img, 255)

	for i in range (row):
		for j in range (col):
			SUM += img[i][j]
	mu = SUM / (row * col)
	#print('mu',mu)
	
	SUM = 0
	for i in range (row):
		for j in range (col):
			SUM += (img[i][j]-mu)**2
   
	sigma = SUM / (row * col)
	#print('sigma',sigma)
	
	SUM = 0
	for i in range (row):
		for j in range (col):
			SUM += (n_img[i][j] - img[i][j])
	mu_n = SUM / (row *col)
	#print('mu_n',mu_n)
	
	SUM = 0
	for i in range (row):
		for j in range (col):
			SUM += (n_img[i][j] - img[i][j] - mu_n)**2
	sigma_n = SUM / (row *col)
	#print('sigma_n',sigma_n)

	SNR = 10 * ( math.log10(sigma) - math.log10(sigma_n))
	#print('log sigma',math.log10(sigma))
	#print('log sigma_n',math.log10(sigma_n))
	
	# print(SNR)
	return SNR
def gussian_noise(amplitude, img, img_row, img_column):
	gussian = np.full((img_row, img_column), 0)
	mu, sigma = 0, 1
	s1 = np.random.normal(mu, sigma, (img_row,img_column))
	for i in range (img_row):
		for j in range (img_column):
			tmp = img[i][j] + amplitude * s1[i][j]
			if tmp > 255:
				gussian[i][j] = 255
			elif tmp < 0:
				gussian[i][j] = 0
			else:
				gussian[i][j] = tmp
	return gussian
lena = cv2.imread("lena.bmp", 0)
row, column = lena.shape[0], lena.shape[1]
gussian_10 = gussian_noise(10, lena, row, column)
gussian_30 = gussian_noise(30, lena, row, column)
cv2.imwrite("gussian_10.bmp", gussian_10)
image_dict["gussian_10"] = SNR(lena, gussian_10)
cv2.imwrite("gussian_30.bmp", gussian_30)
image_dict["gussian_30"] = SNR(lena, gussian_30)
def salt_pepper(probability, img, img_row, img_column):
	saltpepper = np.full((img_row, img_column), 0)
	s2 = np.random.uniform(0, 1, (img_row,img_column))
	for i in range (img_row):
		for j in range (img_column):
			if s2[i][j] < probability:
				saltpepper[i][j] = 0
			elif s2[i][j] > 1 - probability:
				saltpepper[i][j] = 255
			else:
				saltpepper[i][j] = img[i][j]
	return saltpepper
sp_005 = salt_pepper(0.05, lena, row, column)
sp_01 = salt_pepper(0.1, lena, row, column)
cv2.imwrite("sp_005.bmp", sp_005)
image_dict["sp_005"] = SNR(lena, sp_005)
cv2.imwrite("sp_01.bmp", sp_01)
image_dict["sp_01"] = SNR(lena, sp_01)

def box_filter(img, img_row, img_column, box_size):
	boxfilter = np.full((img_row, img_column),0)
	padding = box_size // 2
	img_padding = cv2.copyMakeBorder(img, padding, padding, padding, padding, cv2.BORDER_REFLECT)
	for i in range(img_row):
		for j in range(img_column):
			boxfilter[i, j] = np.mean(img_padding[i:i+box_size, j:j+box_size])
	return boxfilter
def median_filter(img, img_row, img_column, box_size):
	medianfilter = np.full((img_row, img_column),0)
	padding = box_size // 2
	img_padding = cv2.copyMakeBorder(img, padding, padding, padding, padding, cv2.BORDER_REFLECT)
	for i in range(img_row):
		for j in range(img_column):
			medianfilter[i, j] = np.median(img_padding[i:i+box_size, j:j+box_size])
	return medianfilter
gussian_10_box_33 = box_filter(gussian_10, row, column, 3)
gussian_10_box_55 = box_filter(gussian_10, row, column, 5)
gussian_30_box_33 = box_filter(gussian_30, row, column, 3)
gussian_30_box_55 = box_filter(gussian_30, row, column, 5)
sp_005_box_33 = box_filter(sp_005, row, column, 3)
sp_005_box_55 = box_filter(sp_005, row, column, 5)
sp_01_box_33 = box_filter(sp_01, row, column, 3)
sp_01_box_55 = box_filter(sp_01, row, column, 5)
gussian_10_median_33 = median_filter(gussian_10, row, column, 3)
gussian_10_median_55 = median_filter(gussian_10, row, column, 5)
gussian_30_median_33 = median_filter(gussian_30, row, column, 3)
gussian_30_median_55 = median_filter(gussian_30, row, column, 5)
sp_005_median_33 = median_filter(sp_005, row, column, 3)
sp_005_median_55 = median_filter(sp_005, row, column, 5)
sp_01_median_33 = median_filter(sp_01, row, column, 3)
sp_01_median_55 = median_filter(sp_01, row, column, 5)
cv2.imwrite("gussian_10_box_33.bmp", gussian_10_box_33)
cv2.imwrite("gussian_10_box_55.bmp", gussian_10_box_55)
cv2.imwrite("gussian_30_box_33.bmp", gussian_30_box_33)
cv2.imwrite("gussian_30_box_55.bmp", gussian_30_box_55)
cv2.imwrite("sp_005_box_33.bmp", sp_005_box_33)
cv2.imwrite("sp_005_box_55.bmp", sp_005_box_55)
cv2.imwrite("sp_01_box_33.bmp", sp_01_box_33)
cv2.imwrite("sp_01_box_55.bmp", sp_01_box_55)
cv2.imwrite("gussian_10_median_33.bmp", gussian_10_median_33)
cv2.imwrite("gussian_10_median_55.bmp", gussian_10_median_55)
cv2.imwrite("gussian_30_median_33.bmp", gussian_30_median_33)
cv2.imwrite("gussian_30_median_55.bmp", gussian_30_median_55)
cv2.imwrite("sp_005_median_33.bmp", sp_005_median_33)
cv2.imwrite("sp_005_median_55.bmp", sp_005_median_55)
cv2.imwrite("sp_01_median_33.bmp", sp_01_median_33)
cv2.imwrite("sp_01_median_55.bmp", sp_01_median_55)
image_dict["gussian_10_box_33.bmp"]= SNR(lena, gussian_10_box_33)
image_dict["gussian_10_box_55.bmp"]= SNR(lena, gussian_10_box_55)
image_dict["gussian_30_box_33.bmp"]= SNR(lena, gussian_30_box_33)
image_dict["gussian_30_box_55.bmp"]= SNR(lena, gussian_30_box_55)
image_dict["sp_005_box_33.bmp"]= SNR(lena, sp_005_box_33)
image_dict["sp_005_box_55.bmp"]= SNR(lena, sp_005_box_55)
image_dict["sp_01_box_33.bmp"]= SNR(lena, sp_01_box_33)
image_dict["sp_01_box_55.bmp"]= SNR(lena, sp_01_box_55)
image_dict["gussian_10_median_33.bmp"]= SNR(lena, gussian_10_median_33)
image_dict["gussian_10_median_55.bmp"]= SNR(lena, gussian_10_median_55)
image_dict["gussian_30_median_33.bmp"]= SNR(lena, gussian_30_median_33)
image_dict["gussian_30_median_55.bmp"]= SNR(lena, gussian_30_median_55)
image_dict["sp_005_median_33.bmp"]= SNR(lena, sp_005_median_33)
image_dict["sp_005_median_55.bmp"]= SNR(lena, sp_005_median_55)
image_dict["sp_01_median_33.bmp"]= SNR(lena, sp_01_median_33)
image_dict["sp_01_median_55.bmp"]= SNR(lena, sp_01_median_55)
kernel = np.array([[0, 1, 1, 1, 0],
				   [1, 1, 1, 1, 1],
				   [1, 1, 1, 1, 1],
				   [1, 1, 1, 1, 1],
				   [0, 1, 1, 1, 0]])
def dilation_check(image, kernel, x, y):
	value = 0
	p_x = x - (kernel.shape[0]//2)
	p_y = y - (kernel.shape[1]//2)
	for i in range(kernel.shape[0]):
		for j in range(kernel.shape[1]):
			if kernel[i][j] == 1:
				if p_x + i >=0 and p_x + i < image.shape[0] and p_y + j >=0 and p_y + j < image.shape[1]:
					if image[p_x+i][p_y+j] > value:
						value = image[p_x+i][p_y+j]
	return value
def dilation(image, kernel):
	result = np.full((image.shape[0],image.shape[1]),0)
	for i in range(image.shape[0]):
		for j in range(image.shape[1]):
				result[i][j] = dilation_check(image, kernel, i, j)
	return result
	# cv2.imwrite("dilation.bmp", result)

def erosion_check(image, kernel, x, y):
	value = 256
	p_x = x - (kernel.shape[0]//2)
	p_y = y - (kernel.shape[1]//2)
	for i in range(kernel.shape[0]):
		for j in range(kernel.shape[1]):
			if kernel[i][j] == 1:
				if p_x + i >=0 and p_x + i < image.shape[0] and p_y + j >= 0 and p_y + j < image.shape[1] :
					if image[p_x+i][p_y+j] < value:
						value = image[p_x+i][p_y+j]
	return value
def erosion(image, kernel):
	result = np.full((image.shape[0],image.shape[1]),0)
	for i in range(image.shape[0]):
		for j in range(image.shape[1]): 
			result[i][j] = erosion_check(image, kernel, i, j)
	return result
def opening(image, img_row, img_column):
	opening = np.full((img_row,img_column),0)
	img_bin = np.asarray(image)
	opening = erosion(img_bin, kernel)
	opening = dilation(opening, kernel)
	return opening

def closing(image, img_row, img_column):
	closing = np.full((img_row,img_column),0)
	img_bin = np.asarray(image)
	closing = dilation(img_bin, kernel)
	closing = erosion(closing, kernel)
	return closing

gussian_10_opening = opening(gussian_10, row, column)
gussian_10_opening_closing = closing(gussian_10_opening, row, column)
cv2.imwrite("gussian_10_opening_closing.bmp",gussian_10_opening_closing)
image_dict["gussian_10_opening_closing"] = SNR(lena, gussian_10_opening_closing)

gussian_10_closing = closing(gussian_10, row, column)
gussian_10_closing_opening = opening(gussian_10_closing, row, column)
cv2.imwrite("gussian_10_closing_opening.bmp",gussian_10_closing_opening)
image_dict["gussian_10_closing_opening"] = SNR(lena, gussian_10_closing_opening)

gussian_30_opening = opening(gussian_30, row, column)
gussian_30_opening_closing = closing(gussian_30_opening, row, column)
cv2.imwrite("gussian_30_opening_closing.bmp",gussian_30_opening_closing)
image_dict["gussian_30_opening_closing"] = SNR(lena, gussian_30_opening_closing)

gussian_30_closing = closing(gussian_30, row, column)
gussian_30_closing_opening = opening(gussian_30_closing, row, column)
cv2.imwrite("gussian_30_closing_opening.bmp",gussian_30_closing_opening)
image_dict["gussian_30_closing_opening"] = SNR(lena, gussian_30_closing_opening)

sp_005_opening = opening(sp_005, row, column)
sp_005_opening_closing = closing(sp_005_opening, row, column)
cv2.imwrite("sp_005_opening_closing.bmp",sp_005_opening_closing)
image_dict["sp_005_opening_closing"] = SNR(lena, sp_005_opening_closing)

sp_005_closing = closing(sp_005, row, column)
sp_005_closing_opening = opening(sp_005_closing, row, column)
cv2.imwrite("sp_005_closing_opening.bmp",sp_005_closing_opening)
image_dict["sp_005_closing_opening"] = SNR(lena, sp_005_closing_opening)

sp_01_opening = opening(sp_01, row, column)
sp_01_opening_closing = closing(sp_01_opening, row, column)
cv2.imwrite("sp_01_opening_closing.bmp",sp_01_opening_closing)
image_dict["sp_01_opening_closing"] = SNR(lena, sp_01_opening_closing)

sp_01_closing = closing(sp_01, row, column)
sp_01_closing_opening = opening(sp_01_closing, row, column)
cv2.imwrite("sp_01_closing_opening.bmp",sp_01_closing_opening)
image_dict["sp_01_closing_opening"] = SNR(lena, sp_01_closing_opening)


for keys,values in image_dict.items():
    print("{:30}".format(keys),end='')
    print("{:8.5f}".format(values))