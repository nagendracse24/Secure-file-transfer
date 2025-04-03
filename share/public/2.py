import numpy as np
arr1=np.array(['M','C','A'])
print(arr1.dtype)
#create arrays with specific data type
arr2=np.array([21,22,23,24,25],dtype='S')
print(arr2)
#adjusts the number of bytes per digit
arr3=np.array([21,22,23,24],dtype='i4')
print(arr3.dtype)
#valueError converting A to integer
# arr4=np.array(['1','B'],dtype='i')
# print(arr4)
#astype
arr5=np.array([0.2,1.2,3.9,4.0])
narr=arr5.astype('bool')
print(narr)
print(narr.dtype)
#copy-creates a array and owns the data and changes made to copy will not affect the original array
arr6=np.array([1,2,3,4,50])
x=arr6.copy()
arr6[2]=10
print("New Array ",x)
print("Old Array ",arr6)
#View does not own any data unlike copy, so what changes made in orginal will be there in view