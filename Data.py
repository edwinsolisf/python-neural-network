import time
import threading
from Matrix import Matrix
from Vector import Vector

class Data:
    inputFile = ""
    inputData = []
    inputNumber = 0
    inputSamples = 0
    inputRow = 0
    inputColumn = 0

    outputData = []
    outputFile = ""
    outputNumber = 0
    outputSamples = 0

    def __init__(self, input_file : str, output_file : str):
        self.inputFile = input_file
        self.outputFile = output_file

        t1 = threading.Thread(target=self.FetchInputData())
        t2 = threading.Thread(target=self.FetchOutputData())
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        
    def GetInputData(self):
        return self.inputData

    def GetOuputData(self):
        return self.outputData

    def GetInputDataVector(self, sample : int):
        return Vector(self.inputColumn * self.inputRow, self.inputData[sample * self.inputColumn * self.inputRow : (sample + 1) * self.inputColumn * self.inputRow] )

    def GetOutputData(self, sample : int):
        return self.outputData[sample]

    def FetchInputData(self):
        print("Started reading input file")
        startTime = time.time()
        with open(self.inputFile, "rb") as file:
            self.inputNumber = int.from_bytes(file.read(4), "big")
            self.inputSamples = int.from_bytes(file.read(4), "big")
            self.inputRow = int.from_bytes(file.read(4), "big")
            self.inputColumn = int.from_bytes(file.read(4), "big")

            byte = file.read(1)
            while byte:
                self.inputData.append(int.from_bytes(byte, "big"))
                byte = file.read(1)
        print("Finished reading in ", time.time() - startTime)

    def FetchOutputData(self):
        print("Started reading output file")
        startTime = time.time()
        with open(self.outputFile, "rb") as file:
            self.outputNumber = int.from_bytes(file.read(4), "big")
            self.outputSamples = int.from_bytes(file.read(4), "big")

            byte = file.read(1)
            while byte:
                self.outputData.append(int.from_bytes(byte, "big"))
                byte = file.read(1)
        print("Finished reading in ", time.time() - startTime)

    def SeparateData(self, byte):
        temp = []
        for i in range(self.inputColumn * self.inputRow):
            bit = byte[i]
            temp.append(int(bit))
        return temp

    def ReadData(self, file):
        return file.read(self.inputRow * self.inputColumn)

