import cv2
import numpy as np
# import math
lena = cv2.imread("lena.bmp", 0)
lena_img = cv2.copyMakeBorder(lena,1,1,1,1,cv2.BORDER_REFLECT)
lena_guassian = cv2.copyMakeBorder(lena,5,5,5,5,cv2.BORDER_REFLECT)
def mask(image, i, j, kernel):
	result = 0
	for k in range(kernel.shape[0]):
		for l in range(kernel.shape[1]):
			result += image[i+k][j+l] * kernel[k][l]
	return result

def laplacian(image, threshold, kernel):
	laplacian_result = np.full((512,512),0)
	for i in range(512):
		for j in range(512):
			value = mask(image, i, j, kernel)        
			if value >= threshold:
				laplacian_result[i][j] = 1
			elif value <= threshold*(-1):
				laplacian_result[i][j] = -1
			else: 
				laplacian_result[i][j] = 0
	return laplacian_result

def check(image,i,j):
	for a in range(3):
		for b in range(3):
			if image[i+a-1][j+b-1] == -1:
				return 1
			
	return -1
def zerocross(image):
	zerocross = np.full((512,512),0)
	for i in range(1,image.shape[0]-1):
		for j in range(1,image.shape[1]-1):      
			if image[i][j] == -1 or image[i][j] == 0:
				zerocross[i-1][j-1] = 255
			elif check(image,i,j) == 1: 
				zerocross[i-1][j-1] = 0
			else: 
				zerocross[i-1][j-1] = 255
	return zerocross

Laplacian1 = np.array([[0, 1, 0],[1,-4, 1],[0, 1, 0]])
laplacian1_result = laplacian(lena_img, 15, Laplacian1)
laplacian1_result = cv2.copyMakeBorder(laplacian1_result,1,1,1,1,cv2.BORDER_REFLECT)
laplacian1_result_cross = zerocross(laplacian1_result)
cv2.imwrite('Laplacian_15_1.png',laplacian1_result_cross)

Laplacian2 = np.array([[1, 1, 1],[1,-8, 1],[1, 1, 1]])
Laplacian2 = np.divide(Laplacian2, 3)
laplacian2_result = laplacian(lena_img, 15, Laplacian2)
laplacian2_result = cv2.copyMakeBorder(laplacian2_result,1,1,1,1,cv2.BORDER_REFLECT)
laplacian2_result_cross = zerocross(laplacian2_result)
cv2.imwrite('Laplacian_15_2.png',laplacian2_result_cross)

Laplacian_minimum = np.array([[ 2, -1, 2],[-1, -4,-1],[ 2, -1, 2]])
Laplacian_minimum = np.divide(Laplacian_minimum, 3)
laplacian_min_result = laplacian(lena_img, 20, Laplacian_minimum)
laplacian_min_result = cv2.copyMakeBorder(laplacian_min_result,1,1,1,1,cv2.BORDER_REFLECT)
laplacian_min_result_cross = zerocross(laplacian_min_result)
cv2.imwrite('Laplacian_min_20.png',laplacian_min_result_cross)

Laplacian_gaussian = np.array([[ 0, 0,  0, -1, -1, -2, -1, -1,  0, 0, 0],
						       [ 0, 0, -2, -4, -8, -9, -8, -4, -2, 0, 0],
						       [ 0,-2, -7,-15,-22,-23,-22,-15, -7,-2, 0],
						       [-1,-4,-15,-24,-14, -1,-14,-24,-15,-4,-1],
						       [-1,-8,-22,-14, 52,103, 52,-14,-22,-8,-1],
						       [-2,-9,-23, -1,103,178,103, -1,-23,-9,-2],
						       [-1,-8,-22,-14, 52,103, 52,-14,-22,-8,-1],
						       [-1,-4,-15,-24,-14, -1,-14,-24,-15,-4,-1],
						       [ 0,-2, -7,-15,-22,-23,-22,-15, -7,-2, 0],
						       [ 0, 0, -2, -4, -8, -9, -8, -4, -2, 0, 0],
						       [ 0, 0,  0, -1, -1, -2, -1, -1,  0, 0, 0]])
laplacian_gaussian = laplacian(lena_guassian, 3000, Laplacian_gaussian)
laplacian_gaussian = cv2.copyMakeBorder(laplacian_gaussian,1,1,1,1,cv2.BORDER_REFLECT)
laplacian_gaussian_cross = zerocross(laplacian_gaussian)
cv2.imwrite('Laplacian_of_gaussian_3000.png',laplacian_gaussian_cross)

Laplacian_diff = np.array([[-1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1],
						   [-3, -5, -8,-11,-13,-13,-13,-11, -8, -5, -3],
						   [-4, -8,-12,-16,-17,-17,-17,-16,-12, -8, -4],
						   [-6,-11,-16,-16,  0, 15,  0,-16,-16,-11, -6],
						   [-7,-13,-17,  0, 85,160, 85,  0,-17,-13, -7],
						   [-8,-13,-17, 15,160,283,160, 15,-17,-13, -8],
						   [-7,-13,-17,  0, 85,160, 85,  0,-17,-13, -7],
						   [-6,-11,-16,-16,  0, 15,  0,-16,-16,-11, -6],
						   [-4, -8,-12,-16,-17,-17,-17,-16,-12, -8, -4],
						   [-3, -5, -8,-11,-13,-13,-13,-11, -8, -5, -3],
						   [-1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1]])
laplacian_diff = laplacian(lena_guassian, 1, Laplacian_diff)
laplacian_diff = cv2.copyMakeBorder(laplacian_diff,1,1,1,1,cv2.BORDER_REFLECT)
laplacian_diff_cross = zerocross(laplacian_diff)
cv2.imwrite('Laplacian_of_diff_1.png',laplacian_diff_cross)