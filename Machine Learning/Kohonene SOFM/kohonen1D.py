import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

img = "lenna99.jpg"
#img = "lenna3333.jpg"
#img = "test.jpg"
#img = "LENNA.jpg"

im_gray = np.array(Image.open(img).convert('L'))

pattern = (3,3) #our dither pattern
#the size is made so that it can take maximum number of patterns
#for image of size 99x99 it would be 33^2
codebookSize = int((im_gray.shape[0]/3)**2)

#initialize 1D codebook with random grayscale values 3x3
codebook = np.random.randint(0, 255, size=(codebookSize, pattern[0], pattern[1])) 
codebook = codebook.astype('float64')

learningRate = 0.1
iterations = 8
windowSize = codebookSize

#basic ploting of images
def plotImgs(img, count):
    original = plt.imread(img)
    fig, axes = plt.subplots(nrows=1, ncols=count+1, figsize=(30, 10))
    
    #first img
    axes[0].imshow(original, cmap='gray')
    axes[0].set_title("Original")
    
    #Compressed
    for i in range(count):
        img = plt.imread(f"{i}comp.jpg")
        axes[i+1].imshow(img, cmap='gray')
        axes[i+1].set_title(f"Compressed {i}")

    plt.show()
    
def plotImg(img, count):
    original = plt.imread(img)
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))
    
    #first img
    axes[0].imshow(original, cmap='gray')
    axes[0].set_title("Original")
    
    #Compressed
    img = plt.imread(f"{count-1}comp.jpg")
    axes[1].imshow(img, cmap='gray')
    axes[1].set_title(f"Compressed {count-1}")

    plt.show()
    
def kohonenSOFM(img, codebook, learningRate, iterations, windowSize):
    im_gray = np.array(Image.open(img).convert('L'))
    nRows, nCols = im_gray.shape
    error = 0
    
    #if window size is the whole codebook we just update every single entry
    if windowSize == len(codebook):
        for g in range(1, nRows - 1, 3):
            for u in range(1, nCols - 1, 3):
                #3x3 pattern
                patch = im_gray[g-1:g+2, u-1:u+2] 
                #closest codebook entry
                closestEntryIndex = np.argmin(np.sum((codebook - patch)**2, axis=(1,2))) 
                #updating the closest entry by learning rate * difference between the original image and closest codebook entry
                codebook[closestEntryIndex] += (learningRate * (patch - codebook[closestEntryIndex])).astype('float64') 
                
    else:
        for k in range(iterations):
            for i in range(1, nRows - 1, 3):
                for j in range(1, nCols - 1, 3):
                     #3x3 pattern
                    patch = im_gray[i-1:i+2, j-1:j+2]
                    #closest codebook entry
                    closestEntryIndex = np.argmin(np.sum((codebook - patch)**2, axis=(1,2)))
                    #updating the closest entry by learning rate * difference between the original image and closest codebook entry
                    codebook[closestEntryIndex] += (learningRate * (patch - codebook[closestEntryIndex])).astype('float64')
                    
                    #calculating error between image patch and updated codebook (might not work well)
                    error += np.sum((patch - codebook[closestEntryIndex])**2)
                    #function for calculating codebook entries that are in the window size of the current codebook entry
                    calcNearestAndUpdate(closestEntryIndex, codebook, patch, learningRate, windowSize)
                                     
    print("Iteration set")
        
    return codebook, error    

def calcNearestAndUpdate(closestEntryIndex, codebook, patch, learningRate, windowSize):   
    #we update left and right side of the current entry (half window size each way) 
    for i in range(0 - int(windowSize/2), int(windowSize/2) + 1): 
        #if statement to make sure we are not out of bounds or on the entry that was passed to the function
        if i != 0 and closestEntryIndex + i <= len(codebook)-1 and closestEntryIndex + i >= 0:
            codebook[closestEntryIndex + i] += (learningRate * (patch - codebook[closestEntryIndex + i])).astype('float64')
   
def compressImage(img, codebook):
    im_gray = np.array(Image.open(img).convert('L'))
    nRows, nCols = im_gray.shape
    #hold indexes from codebook
    compressedImg = []
    
    for i in range(1, nRows - 1, 3):
        for j in range(1, nCols - 1, 3):
            #3x3 pattern
            patch = im_gray[i-1:i+2, j-1:j+2]
            #closest codebook entry - same function as in Kohonen
            closestEntryIndex = np.argmin(np.sum((codebook - patch)**2, axis=(1,2))) 
            #save the closest entry to the array
            compressedImg.append(closestEntryIndex)
    
    return compressedImg

def decompressImage(compImg, codebook):
    nRows = int(np.sqrt(len(codebook))*3)
    nCols = int(np.sqrt(len(codebook))*3)
    #making the blank image 
    decImg = np.zeros((nRows//3*3, nCols//3*3), dtype=np.uint8)
    
    compImgIndex = 0
    for i in range(1, nRows - 1, 3):
        for j in range(1, nCols - 1, 3): 
            #filling up the blank image as directed by codebook entries
            #compImg holds the array of codebook indexes 
            #so that way we pass the correct patch to the correct spot
            decImg[i-1:i+2, j-1:j+2] = codebook[compImg[compImgIndex]]
            compImgIndex += 1
            
    return decImg

def decompressCodebook(codebook):
    #because every pattern has height 3
    nRows = 3 
    #cols are just the size of codebook * 3 because each pattern has width 3
    nCols = len(codebook) * 3 
    #blank image
    cbImg = np.zeros((nRows, nCols), dtype=np.uint8)
    
    cbIndex = 0
    for i in range(1, nCols - 1, 3):
        #x axis is always the same because its just one row
        cbImg[(-1, 0, 1), i-1:i+2] = codebook[cbIndex]
        cbIndex += 1
    
    return cbImg

########################################################################################################################################################################################

#FIRST SET OF ITERATIONS
#kohonen + compress
updatedCodebook, error = kohonenSOFM(img, codebook, learningRate, iterations, windowSize)    
compImg = compressImage(img, updatedCodebook)

#decompress + save codebook image
decImg = decompressImage(compImg, updatedCodebook)
imgFromArray = Image.fromarray(decImg.astype(np.uint8)) #from array to image
imgFromArray.save("0comp.jpg", "JPEG")

cbImg = decompressCodebook(updatedCodebook)
imgFromArray = Image.fromarray(cbImg.astype(np.uint8)) #from array to image
imgFromArray.save("0codebook.jpg", "JPEG")

###########################################################################################################################################################################################

#ITERATING
done = False
count = 1
while 1:
    
    #incrementing and decrementing our iteration variables after each set of iterations
    iterations *= 2
    learningRate /= 2
    if windowSize != 1: #we can't go under 1 window size
        windowSize = int(windowSize/2)
    
    #update codebook + compress
    updatedCodebook, newError = kohonenSOFM(img, updatedCodebook, learningRate, iterations, windowSize)
    compImg = compressImage(img, updatedCodebook)
    
    #decompress + show codebook
    decImg = decompressImage(compImg, updatedCodebook)
    imgFromArray = Image.fromarray(decImg.astype(np.uint8)) #from array to image
    imgFromArray.save(f"{count}comp.jpg", "JPEG")
    
    cbImg = decompressCodebook(updatedCodebook)
    imgFromArray = Image.fromarray(cbImg.astype(np.uint8)) #from array to image
    imgFromArray.save(f"{count}codebook.jpg", "JPEG")
    
    count += 1
        
    #checking when to stop iterating
    #if windowSize == 1:
        #done = True
    
    #for lenna 99x99
    if windowSize <= 20:
        done = True
        
    if abs(error - newError) < 10000:
        done = True
    else:
        error = newError
    
    if done == True:
        break    
    
plotImgs(img, count)
plotImg(img, count)