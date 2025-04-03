import numpy as np
#0-D array
arr=np.array(100)
print(arr)
#1-D array
arr1=np.array([10,20,30,40])
print(arr1)
#2-D array
arr2=np.array([[1,2,3,4,5],[5,6,7,8,9]])
print(arr2)
#3-D array
arr3=np.array([[[1,2,3,4,5],[6,7,8,9,10]],[[11,12,13,14,15],[16,17,18,19,20]]])
print(arr3)
#print element of 3d array
print(arr3[1][1][2])
print(arr3[1,-1,2])
#dimension of array
print(arr3.ndim)
    #prints the sub-list of 3D array
print(arr3[1,-1,2])
#higher dimensional arrays, let the number elements be the multiples of the dimensions
arr4=np.array([1,2,3,4,5,6,7,8],ndmin=4)
print(arr4)
#slicing
arr2d=np.array([[1,2,3,4,5,6,7],[8,9,10,11,12,13,14]])
print(arr2d[1,1:4])
print(arr2d[0:2,1:4])
print(arr2d[0:2,1:4])
#reshaping
#the number of elements in the arrays should correspond to 3*3*1
re=np.array([10,20,30,40,50,60,70,80,90]).reshape(3,3,1)
#error as the number of elements is only 9, whereas reshape needs 27
# re=np.array([10,20,30,40,50,60,70,80,90]).reshape(3,3,3)
print(re)
#axis
table=np.array([[5,3,7,1],[2,6,7,9],[2,2,2,2],[4,3,2,0]])
#max element in all lists
print(table.max())
#gives the max element column-wise
print(table.max(axis=0))
#gives the max element row-wise
print(table.max(axis=1))