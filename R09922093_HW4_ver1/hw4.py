import cv2
import numpy as np

lena = cv2.imread("lena.bmp", 0)
threshold,bin_img = cv2.threshold(lena,127,255,cv2.THRESH_BINARY)
# cv2.imwrite("binary.bmp",bin_img)
bin_array = np.asarray(bin_img)
bin_c = 255 - bin_array
kernel = np.array([[0, 1, 1, 1, 0],
				   [1, 1, 1, 1, 1],
				   [1, 1, 1, 1, 1],
				   [1, 1, 1, 1, 1],
				   [0, 1, 1, 1, 0]])
def dilation_check(image, kernel, x, y):
	p_x = x - (kernel.shape[0]//2)
	p_y = y - (kernel.shape[1]//2)
	for i in range(kernel.shape[0]):
		for j in range(kernel.shape[1]):
			if kernel[i][j] == 1:
				if p_x + i >=0 and p_x + i < image.shape[0] and p_y + j >=0 and p_y + j < image.shape[1]:
					image[p_x+i][p_y+j] = 255
def dilation(image, kernel):
	result = np.full((image.shape[0],image.shape[1]),0)
	for i in range(image.shape[0]):
		for j in range(image.shape[1]):
			if image[i][j] == 255:  
				dilation_check(result, kernel, i, j)
	return result
	# cv2.imwrite("dilation.bmp", result)

def erosion_check(image, kernel, x, y):
	p_x = x - (kernel.shape[0]//2)
	p_y = y - (kernel.shape[1]//2)
	for i in range(kernel.shape[0]):
		for j in range(kernel.shape[1]):
			if kernel[i][j] == 1:
				if p_x + i <0 or p_x + i >= image.shape[0] or p_y + j < 0 or p_y + j >= image.shape[1] :
					return 0
				if image[p_x+i][p_y+j] != 255:
					return 0
	return 255
def erosion(image, kernel):
	result = np.full((image.shape[0],image.shape[1]),0)
	for i in range(image.shape[0]):
		for j in range(image.shape[1]): 
			result[i][j] = erosion_check(image, kernel, i, j)
	return result
	# cv2.imwrite("erosion.bmp", result)

dilation_img = dilation(bin_array, kernel)
cv2.imwrite("dilation_img.bmp", dilation_img)
erosion_img = erosion(bin_array, kernel)
cv2.imwrite("erosion_img.bmp", erosion_img)

##opening
opening = erosion(bin_array, kernel)
opening_img = dilation(opening, kernel)
cv2.imwrite("open_img.bmp",opening_img)

closing = dilation(bin_array, kernel)
closing_img = erosion(closing, kernel)
cv2.imwrite("close_img.bmp",closing_img)

J = np.array([[0, 0, 0],
			  [1, 1, 0],
			  [0, 1, 0]])

K = np.array([[0, 1, 1],
			  [0, 0, 1],
			  [0, 0, 0]])
def hit_and_miss(image, image1, J, K):
	result = np.full((image.shape[0],image.shape[1]),0)
	erosion_1 = erosion(image,J)
	erosion_2 = erosion(image1,K)
	for i in range(erosion_1.shape[0]):
		for j in range(erosion_1.shape[1]):
			if(erosion_1[i][j] == 255 and erosion_2[i][j] == 255):
				result[i][j] = 255
	# print(result)
	return result

hit = hit_and_miss(bin_array, bin_c, J, K)
cv2.imwrite("hit-and-miss.bmp", hit)


