from __future__ import annotations
from typing import Union
from Vector import Vector

class Matrix:

    columns = 0
    rows = 0
    values = []

    def __init__(self, columns : int = 0, rows : int = 0, values : list = [], value : Union[int, float] = None):
        self.rows = rows
        self.columns = columns
        if value == None:
            self.isMatrixValuesSize(values)
            self.values = values.copy()
        else:
            for i in range(0, columns * rows):
                self.values.append(value)


    def GetValue(self, column : int, row : int):
        return values[(row * self.columns) + column]

    def GetValues(self):
        return self.values.copy()
    
    def GetRowVector(self, row : int):
        return Vector(self.columns, self.values[row * self.columns : (row + 1) * self.columns])

    def GetColumnVector(self, column : int):
        temp = []
        for i in range(0, self.rows):
            temp.append(self.values[column + i * self.columns])
        return Vector(self.rows, temp)

    def SetValue(self, column : int, row : int, value : Union[int, float]):
        self.isMatrixValue(value)
        self.values[(row * self.columns) + column] = value

    def SetValues(self, values : list):
        self.isMatrixValuesSize(values)
        self.values = values.copy()

    def SetRowVector(self, row : int, values : Vector):
        self.isMatrixValuesSize(values.GetValueList(), self.columns)
        for i in range(0, self.columns):
            self.values[row*self.columns + i] = values.GetValue(i)
    
    def SetColumnVector(self, column : int, values : Vector):
        self.isMatrixValuesSize(values.GetValueList(), self.rows)
        for i in range(0, self.rows):
            self.values[column + i * self.columns] = values.GetValue(i)

    def AddMatrix(self, other : Matrix):
        self.isMatrix(other)
        self.isMatrixSize(other)
        
        temp = []
        for i in range(0, self.rows * self.columns):
            temp.append(self.values[i] + other.values[i])
        return Matrix(self.columns, self.rows, temp)
    
    def SubstractMatrix(self, other : Matrix):
        self.isMatrix(other)
        self.isMatrixSize(other)
        
        temp = []
        for i in range(0, self.rows * self.columns):
            temp.append(self.values[i] - other.values[i])
        return Matrix(self.columns, self.rows, temp)

    def MultiplyMatrix(self, other : Matrix):
        self.isMatrix(other)
        if(self.columns != other.rows):
            raise ArithmeticError("Matrix Multiplication not define for given parameter")
        
        temp = []
        for i in range(0, self.rows):
            for j in range(0, other.columns):
                num = 0.0
                for k in range(0, self.columns):
                    num += self.values[(i * self.columns) + k] * other.values[(k * self.columns) + j]
                temp.append(num)
        return Matrix(other.columns, self.rows, temp)

    def DivideMatrix(self, other : Matrix):
        self.isMatrix(other)
        self.isMatrixSize(other)
        
        temp = []
        for i in range(0, self.rows * self.columns):
            temp.append(self.values[i] / other.values[i])
        return Matrix(self.columns, self.rows, temp)
    
    def MultiplyVector(self, vector : Vector):
        if(self.columns != vector.size):
            raise ArithmeticError("Matrix-Vector multiplication not defined for given paramater")

        temp = []
        for i in range(0, self.rows):
            num = 0.0
            for j in range(0, self.columns):
                num += vector.values[j] * self.values[(i * self.columns) + j]
            temp.append(num)
        return Vector(self.rows, temp)

    def AddScalar(self, value : Union[int, float]):
        temp = []
        for i in range(0, self.columns * self.rows):
            temp.append(self.values[i] + value)
        return Matrix(self.columns, self.rows, temp)

    def SubstractScalar(self, value : Union[int, float]):
        temp = []
        for i in range(0, self.columns * self.rows):
            temp.append(self.values[i] - value)
        return Matrix(self.columns, self.rows, temp)

    def MultiplyScalar(self, value : Union[int, float]):
        temp = []
        for i in range(0, self.columns * self.rows):
            temp.append(self.values[i] * value)
        return Matrix(self.columns, self.rows, temp)

    def DivideScalar(self, value : Union[int, float]):
        temp = []
        for i in range(0, self.columns * self.rows):
            temp.append(self.values[i] / value)
        return Matrix(self.columns, self.rows, temp)

    def Print(self):
        for i in range(0, self.rows):
            print(self.values[i * self.columns : (i + 1) * self.columns])

    def __add__(self, other : Matrix):
        return self.AddMatrix(other)
    def __sub__(self, other : Matrix):
        return self.SubstractMatrix(other)
    def __mul__(self, other : Union[Matrix, Vector]):
        if type(other) == Matrix:
            return self.MultiplyMatrix(other)
        elif type(other) == Vector:
            return self.MultiplyVector(other)
    def __truediv__(self, other : Matrix):
        return self.DivideMatrix()
    def __neg__(self):
        temp = []
        for value in self.values:
            temp.append(-value)
        return Matrix(self.columns, self.rows, temp)

    def ApplyToMatrix(self, func : function):
        for value in self.values:
            value = func(value)
    
    def Transpose(self):
        temp = []
        for i in range(0, self.columns):
            for j in range(0, self.rows):
                temp.append(self.values[(j * self.columns) + i])
        return Matrix(self.rows, self.columns, temp)

    @staticmethod
    def isMatrix(param : Matrix):
        if(type(param) != Matrix):
            raise TypeError("Argument type is not of type 'Matrix'")

    @staticmethod
    def isMatrixValue(param : Union[int, float]):
        if(type(param) != int and type(param) != float):
            raise TypeError("class Matrix does not support parameter's type")

    def isMatrixSize(self, other : Matrix):
        if(self.columns != other.columns or self.rows != self.rows):
            raise ArithmeticError("Matrix argument is of distinct size")
    
    def isMatrixValuesSize(self, param : list, size : int = -1):
        if(size == -1):
            size = self.columns * self.rows
        if(size != param.__len__()):
            raise ValueError("List is not of correct size")