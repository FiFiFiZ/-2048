# import the required libraries  
import random  
import matplotlib.pyplot as plt  
    
# store the random numbers in a list  
nums = []  
xlambda = 1.5
    
for i in range(10000):  
    temp = random.expovariate(xlambda) 
    nums.append(temp)  
        
# plotting a graph  
plt.hist(nums, bins = 200)  
plt.show() 