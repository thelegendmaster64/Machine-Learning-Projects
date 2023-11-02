#Slavko Stevic W0724929
import random as rnd
import math as math
from matplotlib import pyplot as plt
import statistics

dataX = []
dataY = []


def readAndPlot(fileR, X, Y, title):
    X.clear()
    Y.clear()

    for line in fileR:
        row = line.split()
        X.append(float(row[0]))
        Y.append(float(row[1]))
    #end for

    plt.scatter(X, Y)
    plt.title(title)
    plt.show()
#end readAndPlot

def getXYData(file, X, Y):
    X.clear()
    Y.clear()
    for line in file:
        row = line.split()
        X.append(float(row[0]))
        Y.append(float(row[1]))
    #end for
#end getXYData

def calcMaxDist(X, Y): #getting distance for 1 * st dev
    #our center
    avgX = sum(X)/len(X)
    avgY = sum(Y)/len(Y)
    
    dists= []
    for i in range(len(X)):
        dists.append(math.sqrt(math.pow(avgX - X[i], 2) + math.pow(avgY - Y[i], 2)))
        
    stDevDist = statistics.stdev(dists)
    return stDevDist
#end calcMaxDist

def degToRad(ang):
    rad = ang * (math.pi/180.0)
    return rad


#Deterministic data generation algorithm #
def runDet():
    def generatePointsDet(file, clustSize, clustRad):
        numClust = 4 #number of clusters
        centX = [5, -5, -5, 5] #cluster centers
        centY = [5, 5, -5, -5] #cluster centers
        
        for j in range(numClust):
            #center of the cluster
            cx = centX[j] 
            cy = centY[j]
            
            #angle management + radius management
            ang = 0
            pointsPerRad = clustSize/2
            angInc = 360/pointsPerRad
            rad = clustRad/2
            
            for k in range(clustSize):
                myX = cx + rad*(math.cos(degToRad(ang)))
                myY = cy + rad*(math.sin(degToRad(ang)))
                ang = ang + angInc
                
                #writing data to file
                file.write(str(myX) + " " + str(myY) + "\n")
                
                if (ang >= pointsPerRad*angInc-0.1):
                    #0.1 is to make sure that when ang has 
                    #359.9 we reset it(case for population 100)
                    ang = 0
                    rad = 2*rad
                #end if
            #end for
        #end for
    #end generatePointsDet
    ##############################################################
    
    # 1) Cluster size 10 & cluster radius 3 
    clustSize = 10
    clustRad = 3

    fd103 = open("det 10 3", "w")
    generatePointsDet(fd103, clustSize, clustRad)
    fd103.close()

    fd103r = open("det 10 3", "r")
    readAndPlot(fd103r, dataX, dataY, "det 10 3")
    fd103r.close()
    ##############################################################

    # 2) Cluster size 30 & cluster radius 5 
    clustSize = 30
    clustRad = 5

    fd305 = open("det 30 5", "w")
    generatePointsDet(fd305, clustSize, clustRad)
    fd305.close()

    fd305r = open("det 30 5", "r")
    readAndPlot(fd305r, dataX, dataY, "det 30 5")
    fd305r.close()
    ##############################################################
    
    # 3) Cluster size 100 & cluster radius 7 
    clustSize = 100
    clustRad = 7

    fd1007 = open("det 100 7", "w")
    generatePointsDet(fd1007, clustSize, clustRad)
    fd1007.close()

    fd1007r = open("det 100 7", "r")
    readAndPlot(fd1007r, dataX, dataY, "det 100 7")
    fd1007r.close()
    
    
# Non-Deterministic data generation #
def runNonDet():
    def generatePointsNonDet(file, clustSize, clustRad):
        numClust = 4 #number of clusters
        centX = [5, -5, -5, 5] #cluster centers
        centY = [5, 5, -5, -5] #cluster centers
        
        for j in range(numClust):
            #cluster center
            cx = centX[j]
            cy = centY[j]
            
            for k in range(clustSize):
                angD = rnd.randint(0, 359)
                #point distance from the center
                magnitude = rnd.random() * clustRad
                
                myX = cx + magnitude*(math.cos(angD))
                myY = cy + magnitude*(math.sin(angD))
                
                #writing data to file
                file.write(str(myX) + " " + str(myY) + "\n")
            #end for
        #end for

    # 1) Cluster size 10 & cluster radius 3 
    clustSize = 10
    clustRad = 3

    fnd103 = open("non-det 10 3", "w")
    generatePointsNonDet(fnd103, clustSize, clustRad)
    fnd103.close()

    fnd103r = open("non-det 10 3", "r")
    readAndPlot(fnd103r, dataX, dataY, "non-det 10 3")
    fnd103r.close()
    ##############################################################

    # 2) Cluster size 30 & cluster radius 5
    clustSize = 30
    clustRad = 5

    fnd305 = open("non-det 30 5", "w")
    generatePointsNonDet(fnd305, clustSize, clustRad)
    fnd305.close()

    fnd305r = open("non-det 30 5", "r")
    readAndPlot(fnd305r, dataX, dataY, "non-det 30 5")
    fnd305r.close()
    ##############################################################

    # 3) Cluster size 100 & cluster radius 7
    clustSize = 100
    clustRad = 7

    fnd1007 = open("non-det 100 7", "w")
    generatePointsNonDet(fnd1007, clustSize, clustRad)
    fnd1007.close()

    fnd1007r = open("non-det 100 7", "r")
    readAndPlot(fnd1007r, dataX, dataY, "non-det 100 7")
    fnd1007r.close()


# Ad-Hoc
def adHoc(X, Y, maxDist):
    nClusts = 0
    clusters = [] #coordinates of each cluster's centroid
    clusterPointCount = [] #how many points each cluster has
    
    def findClosestCluster(X, Y, clusters):
        closeDist = math.sqrt(math.pow(X - clusters[0][0], 2) + math.pow(Y - clusters[0][1], 2))
        closeIndex = 0
        
        for i in range(1, len(clusters)-1):
            dist = math.sqrt(math.pow(X - clusters[i][0], 2) + math.pow(Y - clusters[i][1], 2))
            
            if dist < closeDist:
                closeDist = dist
                closeIndex = i
            #end if
        #end for
        return closeDist, closeIndex
    #end findClosestCluster
        
    for j in range(len(X)):
        #if no clusters, 1st point becomes the center of a new cluster
        if (nClusts == 0):
            newCenter = [X[j], Y[j]]
            clusters.append(newCenter)
            clusterPointCount.append(1)
            nClusts = nClusts + 1
        #end if
        else:
            closeDist, closeIndex = findClosestCluster(X[j], Y[j], clusters)
            
            if (closeDist < maxDist): #if the closest cluster is close enough, we average this point into it
                #we provide the max distance from our stdev calculation (can be seen later in the code)
                pointsInCluster = clusterPointCount[closeIndex]
                
                most = pointsInCluster/(pointsInCluster+1)
                rest = 1/(pointsInCluster+1)
                
                newCenterX = (clusters[closeIndex][0] * most) + (X[j] * rest)
                newCenterY = (clusters[closeIndex][1] * most) + (Y[j] * rest)
            
                clusters[closeIndex][0] = newCenterX
                clusters[closeIndex][1] = newCenterY
                
                clusterPointCount[closeIndex] = clusterPointCount[closeIndex] + 1
            #end if
            else:
                #else we make this point a new cluster's center
                newCenter = [X[j], Y[j]]
                clusters.append(newCenter)
                clusterPointCount.append(1)
                nClusts = nClusts + 1
            #end else
        #end else
    #end for
    return clusters

def plotAdHoc(X, Y, maxDist, clusters, title):
    currClustPtsX = []
    currClustPtsY = []
    
    for i in range(len(clusters)):
        currClustPtsX.clear()
        currClustPtsY.clear()
        for k in range(len(X)):
            dist = math.sqrt(math.pow(X[k] - clusters[i][0], 2) + math.pow(Y[k] - clusters[i][1], 2))
            
            if dist <= maxDist:
                currClustPtsX.append(X[k])
                currClustPtsY.append(Y[k])
            #end if
        plt.scatter(currClustPtsX, currClustPtsY)
        #end for k
    #end for i
    plt.title(title)
    plt.show()

def runAdHoc():
    # AdHoc on deterministic population 10 radius 3
    adHocDet103 = open("det 10 3", "r")
    getXYData(adHocDet103, dataX, dataY)
    adHocDet103.close()

    maxDist = 5*calcMaxDist(dataX, dataY) #this generates 4 clusters
    clusters = adHoc(dataX, dataY, maxDist)
    plotAdHoc(dataX, dataY, maxDist, clusters, "Ad-Hoc det 10 3")
    ##############################################################

    # AdHoc on deterministic population 30 radius 5
    adHocDet305 = open("det 30 5", "r")
    getXYData(adHocDet305, dataX, dataY)
    adHocDet305.close()

    maxDist = 3*calcMaxDist(dataX, dataY)
    clusters = adHoc(dataX, dataY, maxDist)
    plotAdHoc(dataX, dataY, maxDist, clusters, "Ad-Hoc det 30 5")
    ##############################################################

    # AdHoc on deterministic population 100 radius 7
    adHocDet1007 = open("det 100 7", "r")
    getXYData(adHocDet1007, dataX, dataY)
    adHocDet1007.close()

    maxDist = 3*calcMaxDist(dataX, dataY)
    clusters = adHoc(dataX, dataY, maxDist)
    plotAdHoc(dataX, dataY, maxDist, clusters, "Ad-Hoc det 100 7")
    ##############################################################

    # AdHoc on non-deterministic population 10 radius 3
    adHocNonDet103 = open("non-det 10 3", "r")
    getXYData(adHocNonDet103, dataX, dataY)
    adHocNonDet103.close()

    maxDist = 5*calcMaxDist(dataX, dataY) #this generates 4 clusters
    clusters = adHoc(dataX, dataY, maxDist)
    plotAdHoc(dataX, dataY, maxDist, clusters, "Ad-Hoc non-det 10 3")
    ##############################################################

    # AdHoc on non-deterministic population 30 radius 5
    adHocNonDet305 = open("non-det 30 5", "r")
    getXYData(adHocNonDet305, dataX, dataY)
    adHocNonDet305.close()

    maxDist = 5*calcMaxDist(dataX, dataY)
    clusters = adHoc(dataX, dataY, maxDist)
    plotAdHoc(dataX, dataY, maxDist, clusters, "Ad-Hoc non-det 30 5")
    ##############################################################

    # AdHoc on non-deterministic population 100 radius 7
    adHocNonDet1007 = open("non-det 100 7", "r")
    getXYData(adHocNonDet1007, dataX, dataY)
    adHocNonDet1007.close()

    maxDist = 5*calcMaxDist(dataX, dataY)
    clusters = adHoc(dataX, dataY, maxDist)
    plotAdHoc(dataX, dataY, maxDist, clusters, "Ad-Hoc non-det 100 7")


# K-Means
def getXYDataKMeans(file, X, Y):
    X.clear()
    Y.clear()
    points = []
    for line in file:
        row = line.split()
        X = float(row[0])
        Y = float(row[1])
        
        points.append([X, Y])
    #end for
    return points

def plotKMeans(points, centroids, thisPointsCentroid, title):
    centroidIndex = 0
    currClustPtsX = []
    currClustPtsY = []
    
    for c in centroids:
        pointIndex = 0
        #ploting the points by adding them to an array that holds one centroid's points
        #and we reset the array for each centroid
        #that way each centroid will have its own color
        for p in points:
            if centroidIndex == thisPointsCentroid[pointIndex]:
                currClustPtsX.append(p[0])
                currClustPtsY.append(p[1])
            #end if
            pointIndex = pointIndex + 1
        centroidIndex = centroidIndex + 1
        
        plt.scatter(currClustPtsX, currClustPtsY)
        currClustPtsX.clear()
        currClustPtsY.clear()
        #end for k
    #end for i
    
    currClustPtsX.clear()
    currClustPtsY.clear()
    
    #ploting the centroids
    for c in centroids:
        currClustPtsX.append(c[0])
        currClustPtsY.append(c[1])
    plt.scatter(currClustPtsX, currClustPtsY, c='k', marker='x')
    plt.title(title)
    plt.show()

def kMeansFixedIterations(points, n, k):
    centroids = [] #k centroids
    thisPointsCentroid = [-1]*n #which points belongs to which centroid
    p2CDists = [0]*k #distance from a point to a centroid
    
    for j in range(k):
        myIndex = rnd.randint(0, n-1)
        centroids.append(points[myIndex].copy()) 
        #this unlinks array centroids and points so when we change centroids, points stay the same
    
    for num in range(1000):
        #match each points with closest centroid
        pointIndex = 0
        for p in points:
            #find dist from p to each centroid, put in point2CDists[]
            centroidIndex = 0
            for c in centroids:
                dist = math.sqrt(math.pow(p[0] - c[0], 2) + math.pow(p[1] - c[1], 2))
                p2CDists[centroidIndex] = dist
                centroidIndex = centroidIndex+1
            
            #find minimum distance in point2CDists
            minDist = min(p2CDists)
            closestCent = p2CDists.index(minDist)
            thisPointsCentroid[pointIndex] = closestCent
            
            pointIndex = pointIndex + 1
        #end for p
        for c in centroids:
            centroidIndex = 0
            xSum = 0
            ySum = 0
            pointIndex = 0
            count = 0
            for p in points:
                #if a points belong to the current centroid in the iteration
                if centroidIndex == thisPointsCentroid[pointIndex]:
                    xSum = xSum + p[0]
                    ySum = ySum + p[1]
                    count = count + 1
                pointIndex = pointIndex+1
            xAv = xSum/count
            yAv = ySum/count
            #we average that point into the centroid
            centroids[centroidIndex][0] = xAv
            centroids[centroidIndex][1] = yAv
            
            centroidIndex = centroidIndex + 1
            #end for p
        #end for c
    #end for num
    return centroids, thisPointsCentroid

def kMeansStopMoving(points, n, k):
    centroids = [] #centroids
    thisPointsCentroid = [-1]*n #which points belongs to which centroid
    p2CDists = [0]*k #distance from a point to a centroid
    
    diffs = [] #differences between new and old centroids
    finished = 0 #our boolean for while loop
    
    #picking random centroids from our n points
    for j in range(k):
        myIndex = rnd.randint(0, n-1)
        
        centroids.append(points[myIndex].copy())
    
    while(finished == 0):
        #match each points with closest centroid
        pointIndex = 0
        for p in points:
            #find dist from p to each centroid, put in point2CDists[]
            centroidIndex = 0
            for c in centroids:
                dist = math.sqrt(math.pow(p[0] - c[0], 2) + math.pow(p[1] - c[1], 2))
                p2CDists[centroidIndex] = dist
                centroidIndex = centroidIndex+1
            
            #find minimum distance in point2CDists
            minDist = min(p2CDists)
            closestCent = p2CDists.index(minDist)
            thisPointsCentroid[pointIndex] = closestCent
            
            pointIndex = pointIndex + 1
        #end for p
        
        centroidIndex = 0
        diffs.clear()
        for c in centroids:
            xSum = 0
            ySum = 0
            pointIndex = 0
            count = 0
            for p in range(len(points)):
                if centroidIndex == thisPointsCentroid[pointIndex]:
                    xSum = xSum + points[pointIndex][0]
                    ySum = ySum + points[pointIndex][1]
                    count = count + 1
                pointIndex = pointIndex+1
            if (count == 0):
                continue
            xAv = xSum/count
            yAv = ySum/count
            
            #calculating the distance of how much a centroid moved
            diffs.append(math.sqrt(math.pow(xAv - c[0], 2) + math.pow(yAv - c[1], 2)))
            centroids[centroidIndex][0] = xAv
            centroids[centroidIndex][1] = yAv
            
            centroidIndex = centroidIndex + 1
            #end for p
        countD = 0
        #if each centroid has moved very little, we finish the loop 
        for d in diffs:
            if d < 0.001: #this is very little
                countD = countD + 1
            if countD == k:
                finished = 1
        #end for c
    #end of while
    return centroids, thisPointsCentroid

def kMeansStopMovingAndMerge(points, n, k):
    centroids, thisPointsCentroid = kMeansStopMoving(points, n, k)
    #getting the centroids when they stop moving
    
    centroidDistances = [] #2D array of how many distances each centroid has with its points
    dists = []
    
    centroidIndex = 0
    for c in centroids:
        pointIndex = 0
        dists.clear()
        for p in points:
            #getting distances of a centroid with its points
            if centroidIndex == thisPointsCentroid[pointIndex]:
                distance = math.sqrt(math.pow(p[0] - c[0], 2) + math.pow(p[1] - c[1], 2))
                dists.append(distance)
            pointIndex = pointIndex + 1
            #end if
        #end for p
        centroidIndex = centroidIndex + 1
        centroidDistances.append(dists.copy())
    #end for c
    
    #calculating stdev of each centroid's distances with its points
    centroidDistStDev = []
    for cd in centroidDistances:
        centroidDistStDev.append(statistics.stdev(cd))
    #end for cd
    
    centroidIndex = 0
    for c in centroids:
        for i in range(len(centroids)):
            #we can't compare a centroid with itself
            if i != centroidIndex:
                centroidDist = math.sqrt(math.pow(centroids[centroidIndex][0] - centroids[i][0], 2) 
                                         + math.pow(centroids[centroidIndex][1] - centroids[i][1], 2))
                
                #if the centroid[i] is close enough to the current centroid[centroidIndex]
                #we will merge them by assigning all of centroid[i]'s points to the
                #current centroid[centroidIndex]
                #averaging the centroids together and then mixing their points together would've been too complicated
                #but not impossible
                if 6*centroidDistStDev[centroidIndex] > centroidDist:
                    for p in range(len(points)):
                        if i == thisPointsCentroid[p]:
                            thisPointsCentroid[p] = centroidIndex
            
        centroidIndex = centroidIndex+1
    
    return centroids, thisPointsCentroid

def runKMeansFixIte():
    #K-Means on deterministic population size 10 radius 3
    kMeansFixIterDet103 = open("det 10 3", "r")
    points = getXYDataKMeans(kMeansFixIterDet103, dataX, dataY)
    kMeansFixIterDet103.close()

    centroids, thisPointsCentroid = kMeansFixedIterations(points, 40, 4)
    plotKMeans(points, centroids, thisPointsCentroid, "k-means fixed iterations det 10 3")
    #####################################################################

    #K-Means on deterministic population size 30 radius 5
    kMeansFixIterDet305 = open("det 30 5", "r")
    points = getXYDataKMeans(kMeansFixIterDet305, dataX, dataY)
    kMeansFixIterDet305.close()

    centroids, thisPointsCentroid = kMeansFixedIterations(points, 120, 4)
    plotKMeans(points, centroids, thisPointsCentroid, "k-means fixed iterations det 30 5")
    #####################################################################

    #K-Means on deterministic population size 100 radius 7
    kMeansFixIterDet1007 = open("det 100 7", "r")
    points = getXYDataKMeans(kMeansFixIterDet1007, dataX, dataY)
    kMeansFixIterDet1007.close()

    centroids, thisPointsCentroid = kMeansFixedIterations(points, 400, 4)
    plotKMeans(points, centroids, thisPointsCentroid, "k-means fixed iterations det 100 7")
    #####################################################################

    #K-Means on non-deterministic population size 10 radius 3
    kMeansNonDet103 = open("non-det 10 3", "r")
    points = getXYDataKMeans(kMeansNonDet103, dataX, dataY)
    kMeansNonDet103.close()

    centroids, thisPointsCentroid = kMeansFixedIterations(points, 40, 4)
    plotKMeans(points, centroids, thisPointsCentroid, "k-means fixed iterations non-det 10 3")
    ######################################################################

    #K-Means on non-deterministic population size 30 radius 5
    kMeansNonDet305 = open("non-det 30 5", "r")
    points = getXYDataKMeans(kMeansNonDet305, dataX, dataY)
    kMeansNonDet305.close()

    centroids, thisPointsCentroid = kMeansFixedIterations(points, 120, 4)
    plotKMeans(points, centroids, thisPointsCentroid, "k-means fixed iterations non-det 30 5")
    ######################################################################

    #K-Means on non-deterministic population size 100 radius 7
    kMeansNonDet1007 = open("non-det 100 7", "r")
    points = getXYDataKMeans(kMeansNonDet1007, dataX, dataY)
    kMeansNonDet1007.close()

    centroids, thisPointsCentroid = kMeansFixedIterations(points, 400, 4)
    plotKMeans(points, centroids, thisPointsCentroid, "k-means fixed iterations non-det 100 7")
    ######################################################################

def runKMeansStopMoving():
    #K-Means on deterministic population size 10 radius 3
    kMeansFixIterDet103 = open("det 10 3", "r")
    points = getXYDataKMeans(kMeansFixIterDet103, dataX, dataY)
    kMeansFixIterDet103.close()

    centroids, thisPointsCentroid = kMeansStopMoving(points, 40, 4)
    plotKMeans(points, centroids, thisPointsCentroid, "k-means stop moving det 10 3")
    #####################################################################

    #K-Means on deterministic population size 30 radius 5
    kMeansFixIterDet305 = open("det 30 5", "r")
    points = getXYDataKMeans(kMeansFixIterDet305, dataX, dataY)
    kMeansFixIterDet305.close()

    centroids, thisPointsCentroid = kMeansStopMoving(points, 120, 4)
    plotKMeans(points, centroids, thisPointsCentroid, "k-means stop moving det 30 5")
    #####################################################################

    #K-Means on deterministic population size 100 radius 7
    kMeansFixIterDet1007 = open("det 100 7", "r")
    points = getXYDataKMeans(kMeansFixIterDet1007, dataX, dataY)
    kMeansFixIterDet1007.close()

    centroids, thisPointsCentroid = kMeansStopMoving(points, 400, 4)
    plotKMeans(points, centroids, thisPointsCentroid, "k-means stop moving det 100 7")
    #####################################################################

    #K-Means on non-deterministic population size 10 radius 3
    kMeansNonDet103 = open("non-det 10 3", "r")
    points = getXYDataKMeans(kMeansNonDet103, dataX, dataY)
    kMeansNonDet103.close()

    centroids, thisPointsCentroid = kMeansStopMoving(points, 40, 4)
    plotKMeans(points, centroids, thisPointsCentroid, "k-means stop moving non-det 10 3")
    ######################################################################

    #K-Means on non-deterministic population size 30 radius 5
    kMeansNonDet305 = open("non-det 30 5", "r")
    points = getXYDataKMeans(kMeansNonDet305, dataX, dataY)
    kMeansNonDet305.close()

    centroids, thisPointsCentroid = kMeansStopMoving(points, 120, 4)
    plotKMeans(points, centroids, thisPointsCentroid, "k-means stop moving non-det 30 5")
    ######################################################################

    #K-Means on non-deterministic population size 100 radius 7
    kMeansNonDet1007 = open("non-det 100 7", "r")
    points = getXYDataKMeans(kMeansNonDet1007, dataX, dataY)
    kMeansNonDet1007.close()

    centroids, thisPointsCentroid = kMeansStopMoving(points, 400, 4)
    plotKMeans(points, centroids, thisPointsCentroid, "k-means stop moving non-det 100 7")
    ######################################################################

def runKMeansStopMovingAndMerge():
    #K-Means on deterministic population size 10 radius 3
    kMeansFixIterDet103 = open("det 10 3", "r")
    points = getXYDataKMeans(kMeansFixIterDet103, dataX, dataY)
    kMeansFixIterDet103.close()

    centroids, thisPointsCentroid = kMeansStopMovingAndMerge(points, 40, 5)
    plotKMeans(points, centroids, thisPointsCentroid, "k-means stop moving and merge det 10 3")
    #####################################################################

    #K-Means on deterministic population size 30 radius 5
    kMeansFixIterDet305 = open("det 30 5", "r")
    points = getXYDataKMeans(kMeansFixIterDet305, dataX, dataY)
    kMeansFixIterDet305.close()

    centroids, thisPointsCentroid = kMeansStopMovingAndMerge(points, 120, 6)
    plotKMeans(points, centroids, thisPointsCentroid, "k-means stop moving and merge det 30 5")
    #####################################################################

    #K-Means on deterministic population size 100 radius 7
    kMeansFixIterDet1007 = open("det 100 7", "r")
    points = getXYDataKMeans(kMeansFixIterDet1007, dataX, dataY)
    kMeansFixIterDet1007.close()

    centroids, thisPointsCentroid = kMeansStopMovingAndMerge(points, 400, 10)
    plotKMeans(points, centroids, thisPointsCentroid, "k-means stop moving and merge det 100 7")
    #####################################################################
    
    #K-Means on non-deterministic population size 10 radius 3
    kMeansNonDet103 = open("non-det 10 3", "r")
    points = getXYDataKMeans(kMeansNonDet103, dataX, dataY)
    kMeansNonDet103.close()

    centroids, thisPointsCentroid = kMeansStopMovingAndMerge(points, 40, 5)
    plotKMeans(points, centroids, thisPointsCentroid, "k-means stop moving and merge non-det 10 3")
    ######################################################################
    
    #K-Means on non-deterministic population size 30 radius 5
    kMeansNonDet305 = open("non-det 30 5", "r")
    points = getXYDataKMeans(kMeansNonDet305, dataX, dataY)
    kMeansNonDet305.close()

    centroids, thisPointsCentroid = kMeansStopMovingAndMerge(points, 120, 6)
    plotKMeans(points, centroids, thisPointsCentroid, "k-means stop moving and merge non-det 30 5")
    ######################################################################
    
    #K-Means on non-deterministic population size 100 radius 7
    kMeansNonDet1007 = open("non-det 100 7", "r")
    points = getXYDataKMeans(kMeansNonDet1007, dataX, dataY)
    kMeansNonDet1007.close()

    centroids, thisPointsCentroid = kMeansStopMovingAndMerge(points, 400, 10)
    plotKMeans(points, centroids, thisPointsCentroid, "k-means stop moving and merge non-det 100 7")
    ######################################################################

#running
runDet()
runNonDet()
runAdHoc()
#The following algorithms show their centroids with an X 
runKMeansFixIte()
runKMeansStopMoving()
#The following algorithm will merge centroid's points but won't average the 2 centroids into a new one 
#so we can have 2 X's representing one cluster
runKMeansStopMovingAndMerge()