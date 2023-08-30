
# Class to represent a material
class material:
    
    def __init__(self):
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
        
        self.plasticStrain = {}
        
    def getName(self):
        return self.name
    
    def getSpeed(self):
        return self.speed
    
    def getTemperature(self):
        return self.temperature
    
    def getModule(self):
        return self.module
    
    def getPoisson(self):
        return self.poisson
    
    def getYieldStress(self):
        return self.yieldStress
    
    def getYieldStrain(self):
        return self.yieldStrain
    
    def getBreakStress(self):
        return self.breakStress
    
    def getBreakStrain(self):
        return self.breakStrain
    
    def getThermalCoef(self):
        return self.thermalCoef
    
    def setName(self, newName):
        self.name = newName
        
    def setSpeed(self, newSpeed):
        self.speed = newSpeed
    
    def setTemperature(self, newTemperature):
        self.temperature = newTemperature
    
    def setModule(self, newModule):
        self.module = newModule
        
    def setPoisson(self, newPoisson):
        self.poisson = newPoisson
    
    def setYieldStress(self, newStress):
        self.yieldStress = newStress
        
    def setYieldStrain(self, newStrain):
        self.yieldStrain = newStrain
    
    def setBreakStress(self, newStress):
        self.breakStress = newStress
    
    def setBreakStrain(self, newStrain):
        self.breakStrain = newStrain
    
    def setThermalCoef(self, newCoef):
        self.thermalCoef = newCoef
    
       