import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import math


# Class that calibrates the material data
class DataAnalysis():
    def __init__(self, fileLocation: str,
                        resolution: str, 
                        strainAdm: bool, 
                        engCurve: bool):
        
        # Material Variables
        self.module = None
        self.yieldStress = None
        self.yieldStrain = None
        self.breakStress = None
        self.breakStrain = None
        
        # Program variables
        self.fileLocation = fileLocation
        self.resolution = resolution
        self.strainAdm = strainAdm
        self.engCurve = engCurve
        
        # Data Frames
        self.engDataFrame = None
        self.trueDataFrame = None
        self.derivDataFrame = None
        self.reducedDataFrame = None
        self.reducedEngDataFrame = None
        self.reducedTrueDataFrame = None
        
        # Graphs
        self.graph = None
        self.axis = None
     
    # Getters for the variables    
    def getModule(self) -> float:
        return self.module
    
    def getYieldStress(self) -> float:
        return self.yieldStress
    
    def getYieldStrain(self) -> float:
        return self.yieldStrain
    
    def getBreakStress(self) -> float:
        return self.breakStress
    
    def getBreakStrain(self) -> float:
        return self.breakStrain
    
    def getEngData(self) -> object:
        return self.engDataFrame
    
    def getTrueData(self) -> object:
        return self.trueDataFrame
    
    def getGraph(self) -> object:
        return self.graph
    
    def getAxis(self) -> object:
        return self.axis
        
        
    # Read the data from the Excel file
    def readData(self) -> None:
        
        # Read data from excel
        myData = pd.read_excel(self.fileLocation, header = None)
        myData = myData.rename(columns={0: 'Strain', 1:'Stress'})
        
        # Convert the strain to Adimensional 
        if not self.strainAdm:
            toAdm = myData['Strain']/100
            myData['Strain'] = toAdm
        myData.round(decimals = 5)
        
        # Convert from Engineering Curve to True Curve (Or vice-versa)
        if self.engCurve:
            self.engDataFrame = myData
            trueStrain = np.log( 1 + myData['Strain'])
            trueStress = myData['Stress'] * ( 1 + myData['Strain'])
            self.trueDataFrame = pd.DataFrame({'True Strain' : trueStrain, 
                                               'True Stress' : trueStress})
        else:
            self.trueDataFrame = pd.DataFrame({'True Strain' : myData['Strain'], 
                                               'True Stress' : myData['Stress']})
            engStrain = math.exp(myData['Strain']) - 1
            engStress = myData['Stress'] / (1 + engStrain)
            self.trueDataFrame = pd.DataFrame({'Strain' : engStrain, 
                                               'Stress' : engStress})
            
        self.engDataFrame.round(decimals = 5)
        self.trueDataFrame.round(decimals = 5)
        
        
    # Calculate the first derivative of the Engineering curve
    def calculateDerivativeData(self) -> None:
        derivData = np.gradient(self.engDataFrame['Stress'], 
                                self.engDataFrame['Strain'])
        self.derivDataFrame = pd.DataFrame({'True Strain' : self.engDataFrame['Strain'],
                                           'Real Derivative' : derivData})
        self.derivDataFrame.round(decimals = 5)
    
    
    # Calibration of the material data
    def calibrateMaterialData(self) -> None:
        
        # Reduce the derivative data frame to clean the data
        self.reducedDataFrame = self.derivDataFrame.iloc[::self.resolution]
        self.reducedDataFrame = self.reducedDataFrame.rename(columns={'Real Derivative':'DeScaled Derivative'})
        self.reducedDataFrame = self.reducedDataFrame.round(decimals = 5)
        
        # Reduce the engineering data frame to clean the data
        self.reducedEngDataFrame = self.engDataFrame.iloc[::self.resolution]
        
        # Reduce the true data frame to clean the data
        self.reducedTrueDataFrame = self.trueDataFrame.iloc[::self.resolution]
    
    
    # Calculate modulus of elasticity
    def calculateModulus(self) -> None:
        #modulusIndex = self.reducedTrueDataFrame['True Strain'].idxmax()
        #modulusRow = self.reducedTrueDataFrame.loc[modulusIndex]
        #self.module = modulusRow['DeScaled Derivative']
        modulusIndex = self.reducedDataFrame['True Strain'].idxmax()
        modulusRow = self.reducedDataFrame.loc[modulusIndex]
        self.module = modulusRow['DeScaled Derivative']
    
    
    # Calculate the Yielding Stress and Strain
    def calculateYield(self) -> None:
        firstNegativeRow = self.reducedDataFrame.loc[self.reducedDataFrame[
            'DeScaled Derivative'] <= 0,
                'True Strain'].idxmin()
        
        firstNegativeRow = self.reducedDataFrame.loc[firstNegativeRow]
        self.yieldStrain = firstNegativeRow['True Strain']
        #self.yieldStress = self.trueDataFrame.loc[
            #self.trueDataFrame['True Strain'] == self.yieldStrain, 'True Stress']
        self.yieldStress = self.reducedTrueDataFrame.loc[
            self.reducedTrueDataFrame['True Strain'] == self.yieldStrain, 'True Stress']
        print(str(firstNegativeRow))
        print(str(self.reducedDataFrame))
        print(str(self.yieldStrain))
        print(str(self.yieldStress))
        #self.yieldStress = firstNegativeRow['True Stress']
        
        
    # Calculate the Break Stress and Strain  
    def calculateBreak(self) -> None:
        breakIndex = self.trueDataFrame['True Strain'].idxmax()
        breakRow = self.trueDataFrame.loc[breakIndex]
        self.breakStrain = breakRow['True Strain']    
        self.breakStress = breakRow['True Stress']
        
        
    # Create the Graphs
    def createGraph(self) -> None:
        
        figure, axis = plt.subplots(2,1)
        axis[0].plot(self.engDataFrame['Strain'], 
                     self.engDataFrame['Stress'], 
                     label = 'Engineering curve')
        
        axis[0].plot(self.trueDataFrame['True Strain'], 
                     self.trueDataFrame['True Stress'], 
                     label = 'True curve')
        
        axis[0].legend()
        
        axis[1].plot(self.derivDataFrame['True Strain'], 
                     self.derivDataFrame['Real Derivative'], 
                     label = '1st Derivative')
        
        axis[1].plot(self.reducedDataFrame['True Strain'], 
                     self.reducedDataFrame['DeScaled Derivative'], 
                     label = 'DeScaled Derivative')
        
        axis[1].legend()
        
        plt.tight_layout()
        self.graph = figure
        self.axis = axis
        
      
    # Analyse the material data
    def beginAnalysis(self) -> None:
        self.readData()
        self.calculateDerivativeData()
        self.calibrateMaterialData()
        self.calculateModulus()
        self.calculateYield()
        self.calculateBreak()
        self.createGraph()
            
        
            

        