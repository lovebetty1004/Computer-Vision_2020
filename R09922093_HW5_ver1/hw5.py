import cv2
import numpy as np

lena = cv2.imread("lena.bmp", 0)
# print(lena.shape)
# threshold,bin_img = cv2.threshold(lena,127,255,cv2.THRESH_BINARY)
# cv2.imwrite("binary.bmp",lena)
bin_array = np.asarray(lena)
# bin_c = 255-bin_array
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

dilation_img = dilation(bin_array, kernel)
cv2.imwrite("dilation.bmp", dilation_img)
erosion_img = erosion(bin_array, kernel)
cv2.imwrite("erosion.bmp", erosion_img)

#opening
opening = erosion(bin_array, kernel)
opening_img = dilation(opening, kernel)
cv2.imwrite("opening.bmp",opening_img)

closing = dilation(bin_array, kernel)
closing_img = erosion(closing, kernel)
cv2.imwrite("closing.bmp",closing_img)


