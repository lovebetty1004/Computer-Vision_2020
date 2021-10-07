import cv2
import matplotlib.pyplot as plt
import numpy as np

def plothis(image, color, filename):
	resultlist= []
	for i in range (image.shape[0]):
		for j in range(image.shape[1]):
			resultlist.append(image[i, j])
	plt.figure(figsize=(10,7))
	plt.hist(resultlist, range(0,255), color = color)
	# plt.show()
	plt.savefig(filename)

def intensity(image):
	image1 = image.copy()
	# new = lena.copy()
	for i in range (image1.shape[0]):
		for j in range(image1.shape[1]):
			image1[i, j] = image1[i, j] // 3
	cv2.imwrite("intensity.bmp",image1)
	return image1


def equalization(image):
	n = [0] * 256
	s = [0] * 256
	image2 = image.copy()
	for i in range(image2.shape[0]):
		for j in range(image2.shape[1]):
			n[image2[i, j]]+=1
	for i in range(256):
		for j in range(i+1):
			s[i] += n[j]/(image2.shape[0] * image2.shape[1])
		s[i] *= 255
	equal_im = np.empty([image2.shape[0],image2.shape[1]])
	for i in range(image2.shape[0]):
		for j in range(image2.shape[1]):
			equal_im[i, j] = s[image2[i, j]]
	cv2.imwrite("equalization.bmp", equal_im)
	return equal_im

lena = cv2.imread("lena.bmp", 0)
cv2.imwrite("original.bmp", lena)
# image = lena.copy()
plothis(lena, "green" , "histogram_1.jpg")
intensity_image = intensity(lena)
plothis(intensity_image, "black", "histogram_2.jpg")
equal_image = equalization(intensity_image)
plothis(equal_image, "blue", "histogram_3.jpg")
