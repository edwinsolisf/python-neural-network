from __future__ import annotations
from typing import Union

class Vector:
    
    size = 0
    values = []

    def __init__(self, size : int = 0, values : list = [], value : Union[int, float] = None):
        if value == None:
            if values.__len__() != size:
                raise ArithmeticError("List is not of correct size")
            self.values = values.copy()
        else:
            for i in range(0, size):
                self.values.append(value)    
        self.size = size

    def AppendValue(self, value : Union[int, float]):
        self.values.append(value)
        self.size += value

    def AddVector(self, other : Vector):
        Vector.isVector(other)
        self.isVectorSize(other)

        temp = []
        for i in range(0, self.size):
            temp.append(self.values[i] + other.values[i])
        return Vector(self.size, temp)

    def AddScalar(self, scalar : Union[int, float]):
        Vector.isVectorValue(scalar)

        temp = []
        for value in self.values:
            temp.append(value + scalar)
        return Vector(self.size, temp)

    def SubstractVector(self, other : Vector):
        Vector.isVector(other)
        self.isVectorSize(other)

        temp = []
        for i in range(0, self.size):
            temp.append(self.values[i] - other.values[i])
        return Vector(self.size, temp)

    def SubstractScalar(self, scalar : Union[int, float]):
        Vector.isVectorValue(scalar)
        
        temp = []
        for value in self.values:
            temp.append(value - scalar)
        return Vector(self.size, temp)

    def MultiplyVector(self, other : Vector):
        Vector.isVector(other)
        self.isVectorSize(other)

        temp = []
        for i in range(0, self.size):
            temp.append(self.values[i] * other.values[i])
        return Vector(self.size, temp)

    def MultiplyScalar(self, scalar : Union[int, float]):
        Vector.isVectorValue(scalar)
        
        temp = []
        for value in self.values:
            temp.append(value * scalar)
        return Vector(self.size, temp)

    def DivideVector(self, other : Vector):
        Vector.isVector(other)
        self.isVectorSize(other)

        temp = []
        for i in range(0, self.size):
            temp.append(self.values[i] / other.values[i])
        return Vector(self.size, temp)

    def DivideScalar(self, scalar : Union[int, float]):
        Vector.isVectorValue(scalar)
        
        temp = []
        for value in self.values:
            temp.append(value / scalar)
        return Vector(self.size, temp)

    def DotProduct(self, other : Vector):
        Vector.isVector(other)
        self.isVectorSize(other)

        temp = 0.0
        for i in range(0, self.size):
            temp += self.values[i] * other.values[i]
        return temp

    def Print(self):
        print(self.values)

    def __add__(self, other : Vector):
        return self.AddVector(other)
    def __sub__(self, other : Vector):
        return self.SubstractVector(other)
    def __mul__(self, other : Vector):
        return self.MultiplyVector(other)
    def __truediv__(self, other : Vector):
        return self.DivideVector(other)
    def __neg__(self):
        temp = []
        for value in self.values:
            temp.append(-value)
        return Vector(self.size, temp)

    def ApplyToVector(self, func : function):
        for value in self.values:
            value = func(value)
    
    @staticmethod
    def isVector(param : Vector):
        if(type(param) != Vector):
            raise TypeError("Argument type is not of type 'Vector'")

    def isVectorSize(self, param : Vector):
        if(self.size != param.size):
            raise ArithmeticError("Vector argument is of distinct size")
    
    @staticmethod
    def isVectorValue(param : Union[int, float]):
        if(type(param) != int and type(param) != float):
            raise TypeError("class Vector does not support parameter's type")

    def GetValueList(self):
        return self.values.copy()

    def GetValue(self, index : int):
        return self.values[index]

    def SetValue(self, index : int, value : Union[int, float]):
        self.values[index] = value