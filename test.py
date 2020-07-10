from Network import Network
from Data import Data
import random

input_file = "data/train-images.idx3-ubyte"
output_file = "data/train-labels.idx1-ubyte"

file = open(input_file, "rb")
data = Data(input_file, output_file)

n = Network(28*28, 10, 2, 8)
n.LoadData(50000, data.GetInputData(), data.GetOuputData())
n.Train(8000, 1)

for i in range(10):
    print(data.GetOutputData(i))
    n.TestSample(data.GetInputDataVector(i)).Print()