import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

img = "lenna99.jpg"
#img = "lenna3333.jpg"
#img = "test.jpg"
#img = "LENNA510.jpg"

im_gray = np.array(Image.open(img).convert('L'))

pattern = (3,3) #our dither pattern
codebookSize = int((im_gray.shape[0]/3))

#initialize 2D codebook with random grayscale values 3x3 (x, y, 3, 3)
codebook = np.random.randint(0, 255, size=(codebookSize, codebookSize, pattern[0], pattern[1])) 
codebook = codebook.astype('float64')

learningRate = 0.1
iterations = 16
windowSize = codebookSize

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
    
def plotCBs(count):
    fig, axes = plt.subplots(nrows=1, ncols=count, figsize=(30, 10))

    #Codebook
    for i in range(count):
        img = plt.imread(f"{i}codebook.jpg")
        axes[i].imshow(img, cmap='gray')
        axes[i].set_title(f"Codebook {i}")
        
    plt.show()

def kohonenSOFM(img, codebook, learningRate, iterations, windowSize):
    im_gray = np.array(Image.open(img).convert('L'))
    nRows, nCols = im_gray.shape
    error = 0
    
    #similar as to 1D codebook but we add one more dimension
    if windowSize == len(codebook):
        for g in range(1, nRows - 1, 3):
            for u in range(1, nCols - 1, 3):
                #3x3 pattern
                patch = im_gray[g-1:g+2, u-1:u+2]
                #this line of code calculated differences between all codebook entries and current patch
                #then it find the minimal difference and returns the index of that codebook entry
                #then it gets unraveled into row + column index with .shape[:2] - 2 is for 2 dimensions
                rowIndex, colIndex = np.unravel_index(np.argmin(np.sum((codebook - patch)**2, axis=(2,3))), codebook.shape[:2])
                #we update the closest codebook entry
                codebook[rowIndex, colIndex] += (learningRate * (patch - codebook[rowIndex, colIndex])).astype('float64')
    else:
        for k in range(iterations):
            for i in range(1, nRows - 1, 3):
                for j in range(1, nCols - 1, 3):
                    #3x3 pattern
                    patch = im_gray[i-1:i+2, j-1:j+2] 
                    #same thing as above if code
                    rowIndex, colIndex = np.unravel_index(np.argmin(np.sum((codebook - patch)**2, axis=(2,3))), codebook.shape[:2])
                    codebook[rowIndex, colIndex] += (learningRate * (patch - codebook[rowIndex, colIndex])).astype('float64')
                    
                    #calculating error between image patch and updated codebook
                    error += np.sum((patch - codebook[rowIndex, colIndex])**2)
                    #here we update the codebook entries that are around the current entry
                    #if window size is 1 it means it will update entries around the current entry, so 8 entries
                    calcNearestAndUpdate(rowIndex, colIndex, codebook, patch, learningRate, windowSize)
                                   
    print("Iteration set")
        
    return codebook, error    

def calcNearestAndUpdate(rowIndex, colIndex, codebook, patch, learningRate, windowSize):
    #if statements to avoid out of bounds 
    for i in range(0 - windowSize, windowSize + 1):
        for j in range(0 - windowSize, windowSize + 1):
            if (rowIndex + i <= len(codebook)-1 and colIndex + j <= len(codebook)-1 and
                rowIndex + i >= 0 and colIndex + j >= 0):
                #avoiding codebook entry that has been passed to the function
                if rowIndex + i == rowIndex and colIndex + j == colIndex:
                    pass
                else:
                    codebook[rowIndex + i, colIndex + j] += (learningRate * (patch - codebook[rowIndex + i, colIndex + j])).astype('float64') 
    
def compressImage(img, codebook):
    #same as 1D but in 2D
    im_gray = np.array(Image.open(img).convert('L'))
    nRows, nCols = im_gray.shape
    compressedImg = [] #hold indexes from codebook
    
    for i in range(1, nRows - 1, 3):
        for j in range(1, nCols - 1, 3):
            patch = im_gray[i-1:i+2, j-1:j+2] #3x3 pattern

            rowIndex, colIndex = np.unravel_index(np.argmin(np.sum((codebook - patch)**2, axis=(2,3))), codebook.shape[:2])

            compressedImg.append((rowIndex, colIndex))
    
    return compressedImg

def decompressImage(compImg, codebook):
    nRows = len(codebook)*3
    nCols = len(codebook)*3
    #blank image
    decImg = np.zeros((nRows//3*3, nCols//3*3), dtype=np.uint8)
    
    compImgIndex = 0
    for i in range(1, nRows - 1, 3):
        for j in range(1, nCols - 1, 3): 
            #same as 1D
            decImg[i-1:i+2, j-1:j+2] = codebook[compImg[compImgIndex]]
            compImgIndex += 1
            
    return decImg

def decompressCodebook(codebook):
    #here codebook is 2D so rows and columns are the same
    nRows = len(codebook) * 3
    nCols = len(codebook) * 3 
    #blank image
    cbImg = np.zeros((nRows//3*3, nCols//3*3), dtype=np.uint8)
    
    cbX = 0
    for i in range(1, nRows - 1, 3):
        cbY = 0
        for j in range(1, nCols - 1, 3):
            #x axis is always the same because its just one row
            cbImg[i-1:i+2, j-1:j+2] = codebook[cbX, cbY]
            cbY += 1
        cbX += 1
    
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
    if windowSize != 1:
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
    if windowSize == 1:
        done = True
              
    if abs(error - newError) < 1000000:
        done = True
    else:
        error = newError
    
    if done == True:
        break    
    
plotImgs(img, count)
plotImg(img, count)
plotCBs(count)