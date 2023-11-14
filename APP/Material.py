import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from APP.DataAnalysis import DataAnalysis as DANAL

# Class to represent a material
class material:
    
    def __init__(self, fileLocation: str, 
                        resolution: str, 
                        strainAdm: bool, 
                        engCurve: bool):
        
        # Material Variables
        self.name = None
        self.speed = None
        self.temperature = None
        self.module = None
        self.poisson = None
        self.yieldStress = None
        self.yieldStrain = None
        self.breakStress = None
        self.breakStrain = None
        self.thermalCoef = None
        self.density = None
        
        # Program variables
        self.fileLocation = fileLocation
        self.resolution = resolution
        self.strainAdm = strainAdm
        self.engCurve = engCurve
        self.trueDF =  None
        
        # Graphs
        self.graph = None
        self.axis = None
        
        
    # Getters for the variables   
    def getName(self) -> str:
        return self.name
    
    def getSpeed(self) -> float:
        return self.speed
    
    def getTemperature(self) -> float:
        return self.temperature
    
    def getModule(self) -> float:
        return self.module
    
    def getPoisson(self) -> float:
        return self.poisson
    
    def getYieldStress(self) -> float:
        return self.yieldStress
    
    def getYieldStrain(self) -> float:
        return self.yieldStrain
    
    def getBreakStress(self) -> float:
        return self.breakStress
    
    def getBreakStrain(self) -> float:
        return self.breakStrain
    
    def getThermalCoef(self) -> float:
        return self.thermalCoef
    
    def getGraph(self) -> object:
        return self.graph
    
    
    # Setters for the variables
    def setName(self, newName: str) -> None:
        self.name = newName
        
    def setSpeed(self, newSpeed: float) -> None:
        self.speed = newSpeed
    
    def setTemperature(self, newTemperature: float) -> None:
        self.temperature = newTemperature
    
    def setModule(self, newModule: float) -> None:
        self.module = newModule
        
    def setPoisson(self, newPoisson: float) -> None:
        self.poisson = newPoisson
    
    def setYieldStress(self, newStress: float) -> None:
        self.yieldStress = newStress
        
    def setYieldStrain(self, newStrain: float) -> None:
        self.yieldStrain = newStrain
    
    def setBreakStress(self, newStress: float) -> None:
        self.breakStress = newStress
    
    def setBreakStrain(self, newStrain: float) -> None:
        self.breakStrain = newStrain
    
    def setThermalCoef(self, newCoef: float) -> None:
        self.thermalCoef = newCoef
    
    
    # Begin the data calibration for the material
    def analyseData(self):
        myData = DANAL(self.fileLocation, self.resolution,
                       self.strainAdm, self.engCurve)
        myData.beginAnalysis()
        
        self.module = myData.getModule()
        self.yieldStress = myData.getYieldStress()
        self.yieldStrain = myData.getYieldStrain()
        self.breakStress = myData.getBreakStress()
        self.breakStrain = myData.getBreakStrain()
        self.graph = myData.getGraph()
        self.axis = myData.getAxis()
        self.trueDF = myData.getTrueData()
        
        
    # Creates a Excel file with the Data    
    def writeExcelFile(self):
        path = os.path.split(self.fileLocation)[0]
        fileName = os.path.splitext(self.fileLocation)[0]
        fileName = fileName + 'Treated.xlsx'
        resultDF = pd.DataFrame({'True Strain': self.trueDF['True Strain'],
                                 'True Stress':self.trueDF['True Stress'],
                                 'Emodule': self.module,
                                 'Yield Stress': self.yieldStress,
                                 'Yield Strain': self.yieldStrain,
                                 'Break Stress': self.breakStress,
                                 'Break Strain': self.breakStrain,
                                 'Poisson': self.poisson,
                                 'Density': self.density})
        resultDF.to_excel(fileName, index = False)
        
        
        