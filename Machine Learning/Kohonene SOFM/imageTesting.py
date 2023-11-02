# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 08:06:49 2022

@author: userselu
"""

# Using imageio
import imageio as iio

def imageTest(imageName):
    print("Hello TV Land! \n")
    
    img = iio.imread(imageName)
    
    iio.imwrite("testLenna.jpg", img)
    
#imageTest("LENNA.BMP")
    
# Using PIL and numpy
from PIL import Image
import numpy as np

def numpyImageTest(imageName):
    # Read in image, convert it to grayscale.
    im_gray = np.array(Image.open(imageName).convert('L'))

    print(type(im_gray))
    # <class 'numpy.ndarray'>

    print(im_gray.dtype)
    # uint8
    
    nRows, nCols = im_gray.shape
    
    for j in range(nRows):
        for k in range(nCols):
            if (j == k):
                im_gray[j][k] = 0

    print(im_gray.shape)
    
    pil_img_gray = Image.fromarray(im_gray)
    print(pil_img_gray.mode)
    # L

    pil_img_gray.save("testLennaGray.jpg")
    
numpyImageTest("LENNA.BMP")
    
    
def histogramImage(name, vSize):
    # Read in image, convert it to grayscale.
    im_gray = np.array(Image.open(name).convert('L'))
    nRows, nCols = im_gray.shape

    gridHi = int(nRows/vSize) + 1
    gridWd = int(nCols/vSize) + 1
    
    # Make a vector for sampling the image.
    v0 = np.zeros((vSize, vSize), dtype = 'uint8')
    
    # Make a 2d array that tracks the identical vectors in the image
    vecGrid = np.zeros((gridHi, gridWd), dtype = 'int')
    
    # Set the vecGrid to all -1's to indicate a vector has not been identified
    for j in range(gridHi):
        for k in range(gridWd):
            vecGrid[j][k] = -1
            
    print(vecGrid)

    print(type(im_gray))
    # <class 'numpy.ndarray'>

    print(im_gray.dtype)
    # uint8
    
    # Set the vector Id to 0, each time a new one is found, it increments.
    vId = 0
    
    # Create an array to store the vectors.
    myVectors = []
    
    for j in range(0, nRows, vSize):
        
        gridR = int(j/vSize)
        for k in range(0, nCols, vSize):
            gridC = int(k/vSize)
            if (vecGrid[gridR][gridC] == -1):
                # Get the vector from the image
                loadVector(j, k, v0, vSize, im_gray, nRows, nCols)
                # Mark the id of the vector in vecGrid
                vecGrid[gridR][gridC] = vId
                # Find all similar vectors in the rest of the image.
                findDuplicates(v0, vSize, im_gray, nRows, nCols, vecGrid, vId)
                # Save the vector to our codebook.
                newVec = createArrayFromVector(v0, vSize)
                myVectors.append(newVec)
                # Increment the vector id
                vId = vId + 1
        
        print(str(j) + ' ' + str(k) + ' ' + str(vId))
                
    print("vId = "+str(vId))
    
    print("vecGrid")
    print(vecGrid)
    
    return vecGrid, gridHi, gridWd, vId, vSize, myVectors, im_gray, nRows, nCols
 
def createArrayFromVector(v0, vSize):
    # Create a new 2 d array.
    newVec = np.zeros((vSize, vSize), dtype = 'uint8')
    # Load the v0 into newVec
    for j in range(vSize):
        for k in range(vSize):
            newVec[j][k] = v0[j][k]
            
    return newVec
               
def loadVector(r, c, v, vSize, im, imHeight, imWidth):
    row = 0
    for j in range(r, r+vSize):
        col = 0
        for k in range(c, c+vSize):
            if ((j < imHeight) and (k < imWidth)):
                v[row][col] = im[j][k]
            col = col+1
        
        row = row+1
            
    return

            
            
def getVector(r, c, vSize, im):
    v = np.zeros((vSize, vSize), dtype = 'uint8')
    r = 0
    for j in range(r, r+vSize):
        c = 0
        for k in range(c, c+vSize):
            v[r][c] = im[j][k]
            c = c+1
        r = r+1
            
    return v

def euclidMe(vSize, v0, v1):
    diff = 0
    for j in range(vSize):
        for k in range(vSize):
            s = int(v1[j][k]) - int(v0[j][k])
            diff = diff + abs(s)
            
    return diff

def sumVec(vSize, vSum, v0):
    for j in range(vSize):
        for k in range(vSize):
            vSum[j][k] = vSum[j][k] + v0[j][k]
            
    return

def avVec(vSize, vSum, count):
    for j in range(vSize):
        for k in range(vSize):
            vSum[j][k] = vSum[j][k] / count
            
    return
    
    


def findDuplicates(v0, vSize, im_gray, imHeight, imWidth, vecGrid, vId):
    v1 = np.zeros((vSize, vSize), dtype = 'uint8')
    tolerence = vSize * vSize * 6
    for j in range(0, imHeight, vSize):
        gridR = int(j/vSize)
        for k in range(0, imWidth, vSize):
            gridC = int(k/vSize)
            if (vecGrid[gridR][gridC] == -1):
                loadVector(j, k, v1, vSize, im_gray, imHeight, imWidth)
                diff = euclidMe(vSize, v0, v1)
                if (diff < tolerence):
                    vecGrid[gridR][gridC] = vId
                
       
    

vecGrid, gridHi, gridWd, vId, vSize, myVectors, im_gray, imHeight, imWidth = histogramImage("LENNA.BMP", 3)

print("gridHi = "+str(gridHi)+" gridWd = "+str(gridWd))

# Make an array for the averaged codebook.
myAverageVectors = []

# Make a vector for sampling the image.
v0 = np.zeros((vSize, vSize), dtype = 'uint8')

total = 0
for j in range(vId):
    count = 0
    vecSum = np.zeros((vSize, vSize), dtype = 'uint')
    for k in range(gridHi):
        for m in range(gridWd):
            # Sum up all the codebook entries of type j.
            if (vecGrid[k][m] == j):
                count = count+1
                loadVector(k*vSize, m*vSize, v0, vSize, im_gray, imHeight, imWidth)
                for row in range(vSize):
                    for col in range(vSize):
                        vecSum[row][col] = vecSum[row][col] + v0[row][col]
    
    
    vecAv = np.zeros((vSize, vSize), dtype = 'uint8')
    # Now average.               
    for row in range(vSize):
        for col in range(vSize):
            averageMe = vecSum[row][col]/count
            vecAv[row][col] = averageMe
    
    myAverageVectors.append(vecAv)
            
            
    print("vid = "+str(j)+" "+str(count))
    total = total + count
    
print("total = "+str(total))
print("gridHi * gridWd = "+str(gridHi*gridWd))

    

print(myVectors)

# Make an array the same size or close as the image.
clunkyImage = np.zeros((gridHi*vSize, gridWd*vSize), dtype = 'uint8')

# Make a bad imagae from the un-averaged code book members.
for j in range(gridHi):
    for k in range(gridWd):
        r = j*vSize
        row = 0
        vId = vecGrid[j][k]
        for m in range(vSize):
            c = k*vSize
            col = 0
            for n in range(vSize):
                clunkyImage[r][c] = myAverageVectors[vId][row][col]
                c = c + 1
                col = col + 1
            r = r + 1
            row = row + 1
            
pil_img_gray = Image.fromarray(clunkyImage)
print(pil_img_gray.mode)
# L

pil_img_gray.save("clunkyLenna.jpg")
        
