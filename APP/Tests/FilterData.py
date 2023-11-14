import numpy as np 
from scipy import signal 
import matplotlib.pyplot as plt
import pandas as pd
from scipy.integrate import cumtrapz
 
class AccelProcessor: 
    
    def __init__(self, accel_data, accel_time, disp_data, velocity_data, mass, sample_rate):
        self.velocity = velocity_data
        self.filteredVelocity = None
        self.displacement = disp_data 
        self.time = accel_time
        self.mass = mass
        self.accel_data = accel_data 
        self.sample_rate = sample_rate
        self.kinetic = None
        self.filteredAccel = None
        self.filteredKinetic = None
        self.load = None
        self.totalEnergy = None
        
        
    def filter_accel(self, lowcut, highcut): 
        nyq = 0.5 * self.sample_rate 
        low = lowcut / nyq 
        high = highcut / nyq 
        
        # Filter for Accelaration50.xlsx
        #self.filteredAccel = signal.savgol_filter(self.accel_data, window_length=14, polyorder=2)
        
        # Filter for Accelaration.xlsx 
        #self.filteredAccel = signal.savgol_filter(self.accel_data, window_length=15, polyorder=2)
       
        # Filter for AZT.xlsx low = 30 high = 49
        b, a = signal.butter(2, [low, high], btype='bandpass') 
        self.filteredAccel = signal.lfilter(b, a, self.accel_data) 
        
        
    def filter_velocity(self, lowcut, highcut):
        nyq = 0.5 * self.sample_rate 
        low = lowcut / nyq 
        high = highcut / nyq 
        #b, a = signal.butter(2, [low, high], btype='bandpass') 
        #self.filteredVelocity = signal.lfilter(b, a, self.velocity) 
        
        # Filter for Accelaration50.xlsx
        #self.filteredVelocity = signal.savgol_filter(self.velocity, window_length=63, polyorder=4)
        
        
        # Filter for Accelaration.xlsx 
        #self.filteredVelocity = signal.savgol_filter(self.velocity, window_length=25, polyorder=1)
        
        # Filter for AZT.xlsx 
        self.filteredVelocity = signal.savgol_filter(self.velocity, window_length=11, polyorder=1)
        
        
    def calculate_kinetic_energy(self): 
        velocity = np.cumsum(self.accel_data) * np.mean(np.diff(self.time)) 
        self.kinetic =  0.5 * self.mass * velocity**2
        
        filteredVelocity =  np.cumsum(self.filteredAccel) * np.mean(np.diff(self.time)) 
        self.filteredKinetic = 0.5 * self.mass * filteredVelocity**2
       
        
    def calculate_kinematic_energy_velocity(self):
        self.kinetic = 0.5 * self.mass * self.velocity**2
        self.filteredKinetic = 0.5 * self.mass * self.filteredVelocity**2
        
        
    def calculate_total_energy(self): 
        #self.totalEnergy = np.trapz(self.filteredKinetic, x=self.time)
        self.totalEnergy = cumtrapz(self.filteredKinetic, x=self.time, initial=0)
    
    
    def plot_velocity(self):
        plt.plot(self.time, self.velocity, label = 'Velocity')
        plt.plot(self.time, self.filteredVelocity, label = 'Filtered Velocity')
        plt.xlabel('Time')
        plt.ylabel('Velocity')
        plt.legend()
    
    
    def plot_kinetic_energy(self): 
        plt.plot(self.time, self.kinetic, label = 'Kinetic Energy')
        plt.plot(self.time, self.filteredKinetic, label = 'Filtered Energy') 
        plt.xlabel('Time') 
        plt.ylabel('Kinetic Energy') 
        plt.legend()
    
    
    def plot_total_energy(self): 
        plt.plot(self.time, self.totalEnergy, label = 'Total Energy')
        plt.xlabel('Time') 
        plt.ylabel('Total Kinetic Energy') 
        plt.legend()
    
    
    def calculateLoad(self):
        self.load = self.filteredAccel * self.mass
        
        
    def plot_accel(self): 
        plt.plot(self.time, self.accel_data, label = 'Accelaration') 
        plt.plot(self.time, self.filteredAccel, label = 'Filtered Accelaration') 
        plt.xlabel('Time') 
        plt.ylabel('Acceleration')
        plt.legend()
         
            
    def plt_accelDisp(self):
        plt.plot(self.displacement, self.filteredAccel*self.mass, label = 'Filtered Accelaration') 
        print(self.filteredAccel)
        plt.xlabel('Disp') 
        plt.ylabel('Load (N)')
        plt.legend()
    
    
    def write(self):
        resultDataFrame = pd.DataFrame({'Time (s)' : self.time,
                                        'Displacement (mm)' : self.displacement,
                                        'Accelaration (m/s^2)' : self.accel_data,
                                        'Filtered accelaration (m/s^2)' : self.filteredAccel,
                                        'Load (N)' : self.load,
                                        'Velocity (m/s)' : self.velocity,
                                        'Filtered Velocity (m/s)' : self.filteredVelocity,
                                        'Kinetic Energy (J)' : self.kinetic,
                                        'Filtered Kinetic (J)' : self.filteredKinetic,
                                        'Total Energy (J)' : self.totalEnergy})
        resultDataFrame.to_excel('Results-AZT.xlsx')
        
        

def test():
    mass = 5.64
    myDataFrame = pd.read_excel('AZT.xlsx', header = None)
    myDataFrame = myDataFrame.rename(columns={0: 'Time', 
                                              1 : 'Accelaration', 
                                              2 : 'Displacement',
                                              3 : 'Velocity'})
    
    myDataFrame['Accelaration'] = myDataFrame['Accelaration']/1000
    myDataFrame['Velocity'] = myDataFrame['Velocity']/1000
    
    time = np.array(myDataFrame['Time'])
    accel = np.array(myDataFrame['Accelaration'])
    disp = np.array(myDataFrame['Displacement'])
    velo = np.array(myDataFrame['Velocity'])
    
    # Create instance 
    ap = AccelProcessor(accel, time, disp, velo, mass, 100) 
    
    # Filter 
    #ap.filter_accel(1, 7) 
    ap.filter_accel(30, 49) 
    ap.filter_velocity(1, 2)
    
    # Compute kinetic energy 
    #ap.calculate_kinetic_energy() 
    ap.calculate_kinematic_energy_velocity()
    
    # Calculate total energy 
    total_energy = ap.calculate_total_energy()
    print('The total energy is equal to ' + str(total_energy) + ' J')
    
    ap.calculateLoad() 
    #ap.write()
    
    # Plot
    ap.plot_velocity() 
    #ap.plot_kinetic_energy()
    #ap.plot_total_energy() 
    #ap.plot_accel()
    #ap.plt_accelDisp() 
    plt.show()
    
test()