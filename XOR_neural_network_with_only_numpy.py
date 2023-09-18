import numpy as np # pip install numpy

def sigmoid(z):
    z= 1/(1+np.exp(-z))
    return z

def Rev_sigmoid(z):
    z = sigmoid(z)
    return z * (1 - z)

rng = np.random.default_rng()

w1 = rng.random((2,2))
b1 = rng.random((2,1))

x = np.array([[0,0],[0,1],[1,0],[1,1]])

w2 = rng.random((1,2))
b2 = rng.random((1,))

y = np.array([0,1,1,0])

# increase the range for accurate values
for i in range(10000):
    z = sigmoid(w1 @ x.T + b1)
    p = sigmoid(w2 @ z + b2)

    loss = y - p
    if i % 100 == 0:
        print("Cost after ", i, " itr's: ", np.sum(loss*loss)/4)

    tmp = 0.1 * 2 * loss * sigmoid(p)*(1-sigmoid(p))
    dz1 = tmp * z * Rev_sigmoid(z)
    
    w1 = w1 + (dz1 @ x).T / 4 # comment this and uncomment below line
    # w1 = w1 + np.sum(dz1.T @ x.T, axis=0).reshape(2,2) / 4 # this also works 
    b1 = b1 + dz1  / 4 

    w2 = w2 + np.average(tmp * z)
    b2 = b2 + np.average(tmp)

print("Done :)")
print("Final Cost: ", np.sum(loss*loss)/4)

print("\nLayer 1: ")
print("Weigth: \n", w1)
print("Bias:\n" , b1)

print("\nLayer 2: ")
print("Weigth: \n", w1)
print("Bias:\n" ,b1)

print("\nInputs: \n", x)
print("Predictions: \n", p)
print("Expected: \n", y)
