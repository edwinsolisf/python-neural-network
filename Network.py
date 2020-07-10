from __future__ import annotations
import random
import time
from typing import Union
from math import exp

from Vector import Vector
from Matrix import Matrix
import gc
class Network:
    inputLayerWeights = Matrix()
    inputLayerBiases = Vector()

    hiddenLayersWeights = []
    hiddenLayersBiases = Matrix()

    outputLayerWeights = Matrix()
    outputLayerBiases = Vector()

    aValues = Matrix()
    errorValues = Matrix()
    zPrimeValues = Matrix()

    inputs = 0
    outputs = 0
    layers = 0
    neurons = 0
    batchSize = 0
    learningRate = 1.0
    inputData = []
    outputData = []
    
    def  __init__(self, inputs : int, outputs : int, layers : int, neurons : int):
        print("Initializing Network")
        startTime = time.time()
        self.inputs = inputs
        self.outputs = outputs
        self.layers = layers
        self.neurons = neurons

        self.inputLayerWeights = Matrix(inputs, neurons, [], 0.0)
        self.inputLayerBiases = Vector(neurons, [], 0.0)
    
        for i in range(0, layers):
            self.hiddenLayersWeights.append(Matrix(neurons, neurons, [], 0.0))
        self.hiddenLayersBiases = Matrix(neurons, layers, [], 0.0)
    
        self.outputLayerWeights = Matrix(neurons, outputs, [], 0.0)
        self.outputLayerBiases = Vector(outputs, [], 0.0)
    
        self.aValues = Matrix(neurons, layers + 1, [], 0.0)
        self.errorValues = Matrix(neurons, layers + 1, [], 0.0)
        self.zPrimeValues = Matrix(neurons, layers + 1, [], 0.0)

        self.InitializeNetwork()
        print("Finished Initializing network in ", time.time() - startTime)

    def LoadData(self, samples : int, inputData : list, outputData : list):
        print("Loading data to network")
        startTime = time.time()
        for i in range(0, samples):
            inputTemp = []
            for j in range(0, self.inputs):
                inputTemp.append(inputData[(i * self.inputs) + j])
            for j in range(0, self.outputs):
                self.outputData.append(outputData[i + j])
            
            self.inputData.append(inputTemp)
        print("Finished loading data in ", time.time() - startTime)

    def Train(self, samples : int, batchSize : int):
        print("Starting network training")
        startTime = time.time()
        self.batchSize = batchSize

        start = time.time()
        for i in range(0, samples // batchSize):
            gradient = Vector(self.outputs, [], 0.0)
            for j in range(0, batchSize):
                output = self.TestTrainingSample(Vector(self.inputs, self.inputData[(i * batchSize) + j]))
                expectedOutput = self.GetExpectedOutput((i * batchSize) + j)
                cost = output - expectedOutput
                gradient = gradient + cost
            self.AdjustNetwork(gradient, output, Vector(self.inputs, self.inputData[(i * batchSize) + j]))
            if(time.time() - start > 15):
                print("Training done: ", 100.0 * i * batchSize / samples)
                start = time.time()
                gc.collect()

        print("Finished training in ", time.time() - startTime)

    def TestTrainingSample(self, inputSample : Vector):
        result = self.inputLayerWeights.MultiplyVector(inputSample) + self.inputLayerBiases
        self.zPrimeValues.SetRowVector(0, result)
        result.ApplyToVector(Sigmoid)
        self.aValues.SetRowVector(0, result)

        for i in range(0, self.layers):
            result = self.hiddenLayersWeights[i].MultiplyVector(result) + self.hiddenLayersBiases.GetRowVector(i)
            self.zPrimeValues.SetRowVector(i + 1, result)
            result.ApplyToVector(Sigmoid)
            self.aValues.SetRowVector(i + 1, result)

        output = self.outputLayerWeights.MultiplyVector(result) + self.outputLayerBiases
        output.ApplyToVector(Sigmoid)

        return output

    def TestSample(self, inputSample : Vector):
        result = self.inputLayerWeights.MultiplyVector(inputSample) + self.inputLayerBiases
        result.ApplyToVector(Sigmoid)

        for i in range(0, self.layers):
            result = self.hiddenLayersWeights[i].MultiplyVector(result) + self.hiddenLayersBiases.GetRowVector(i)
            result.ApplyToVector(Sigmoid)

        output = self.outputLayerWeights.MultiplyVector(result) + self.outputLayerBiases
        output.ApplyToVector(Sigmoid)
        
        return output

    def AdjustNetwork(self, gradient : Vector, output : Vector, sample : Vector):
        output_layer_w_error = Matrix(self.neurons, self.outputs, [], 0.0)
        output_layer_b_error = gradient * output * (Vector(self.outputs, [], 1.0) - output)

        for i in range(0, self.outputs):
            output_layer_w_error.SetRowVector(i, self.aValues.GetRowVector(self.layers).MultiplyScalar(output_layer_b_error.GetValue(i)))

        self.errorValues.SetRowVector(self.layers, self.zPrimeValues.GetRowVector(self.layers) * (self.outputLayerWeights.Transpose() * output_layer_b_error))
        
        self.outputLayerWeights = self.outputLayerWeights - output_layer_w_error.MultiplyScalar(self.learningRate)
        self.outputLayerBiases = self.outputLayerBiases - output_layer_b_error.MultiplyScalar(self.learningRate)

        for i in range(0, self.layers):
            layer_w_error = Matrix(self.neurons, self.neurons, [], 0.0)
            layer_b_error = self.errorValues.GetRowVector(self.layers - 1 - i + 1)

            for j in range(0, self.neurons):
                layer_w_error.SetRowVector(j, self.aValues.GetRowVector(self.layers - 1 - i).MultiplyScalar(layer_b_error.GetValue(j)))
            self.errorValues.SetRowVector(self.layers - 1 - i, self.zPrimeValues.GetRowVector(self.layers - 1 - i) * (self.hiddenLayersWeights[self.layers - 1 - i].Transpose() * layer_b_error))
            
            self.hiddenLayersWeights[self.layers - 1 - i] = self.hiddenLayersWeights[self.layers - 1 - i] - layer_w_error.MultiplyScalar(self.learningRate)
            self.hiddenLayersBiases.SetRowVector(self.layers - 1 - i, self.hiddenLayersBiases.GetRowVector(self.layers - 1 - i) - layer_b_error.MultiplyScalar(self.learningRate))

        input_layer_w_error = Matrix(self.inputs, self.neurons, [], 0.0)
        input_layer_b_error = self.errorValues.GetRowVector(0)

        for i in range(0,self.neurons):
            input_layer_w_error.SetRowVector(i, sample.MultiplyScalar(input_layer_b_error.GetValue(i)))

        self.inputLayerWeights = self.inputLayerWeights - input_layer_w_error.MultiplyScalar(self.learningRate)
        self.inputLayerBiases = self.inputLayerBiases - input_layer_b_error.MultiplyScalar(self.learningRate)

    def GetExpectedOutput(self, sample : int):
        temp = Vector(self.outputs, [], 0.0)
        temp.SetValue(self.outputData[sample], 1.0)
        return temp

    def InitializeNetwork(self):
        self.inputLayerBiases.ApplyToVector(initializeRandom)
        self.inputLayerWeights.ApplyToMatrix(initializeRandom)
        for i in range(self.layers):
            self.hiddenLayersWeights[i].ApplyToMatrix(initializeRandom)
        self.hiddenLayersBiases.ApplyToMatrix(initializeRandom)
        self.outputLayerWeights.ApplyToMatrix(initializeRandom)
        self.outputLayerBiases.ApplyToVector(initializeRandom)

def initializeRandom(value : Union[int, float]):
    return random.random()

def Sigmoid(value : Union[int, float]):
    return 1.0 / (1.0 + exp(-value))

def SigmoidPrime(value : Union[int, float]):
    return Sigmoid(value) * (1.0 - Sigmoid(value))        