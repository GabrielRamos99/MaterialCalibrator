import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np


def analyse(resolution):
    
    # Access the book
    file = 'Book5.xlsx'
    cwd = os.getcwd()
    filePath = os.path.join(cwd, file)
    df = pd.read_excel(filePath, header = None)
    df = df.rename(columns={0 : 'Strain', 1 : 'Stress'})
    
    # Turn Strain from % to Adimensional
    toAdm = df['Strain']
    df['Strain'] = toAdm
    df = df.round(decimals=5)
    
    # Calculate True Strain and True Stress
    trueStrain = np.log( 1 + df['Strain'])
    trueStress = df['Stress']*( 1 + df['Strain'])
    
    # Create the result dataframe
    resultDf = pd.DataFrame({'True Strain': trueStrain, 'True Stress': trueStress})
    resultDf = resultDf.round(decimals=5)
    
    # Calculate the first derivative
    derivData = np.gradient(df['Stress'], df['Strain'])
    derivDf = pd.DataFrame({'True Strain': df['Strain'] ,'Real Derivative': derivData})
    derivDf = derivDf.round(decimals=5)
    
    # Calculate the Yield Stress and Strain
    reducedDf = derivDf.iloc[::resolution]
    reducedDf = reducedDf.rename(columns={'Real Derivative':'DeScaled Derivative'})
    reducedDf = reducedDf.round(decimals=5)
    
    firstNegativeIndex = reducedDf.loc[reducedDf['DeScaled Derivative'] <= 0, 'True Strain'].idxmin()
    firstNegativeRow = reducedDf.loc[firstNegativeIndex]
    yieldStrain = firstNegativeRow['True Strain']
    yieldStress = resultDf.loc[resultDf['True Strain'] == yieldStrain, 'True Stress']
    
    # Calculate the Break Stress and Strain
    breakIndex  =  resultDf['True Strain'].idxmax()
    breakRow = resultDf.loc[breakIndex]
    breakStrain = breakRow['True Strain']
    breakStress = breakRow['True Stress']
    
    # Calculate modulus of elasticity
    modulusIndex  =  reducedDf['DeScaled Derivative'].idxmax()
    modulusRow = reducedDf.loc[modulusIndex]
    modulus = modulusRow['DeScaled Derivative']
    
    # Plot the results
    figure, axis = plt.subplots(2,1)
    axis[0].plot(df['Strain'], df['Stress'], label = 'Engineering curve')
    axis[0].plot(resultDf['True Strain'], resultDf['True Stress'], label = 'True curve')
    axis[0].legend()
    
    axis[1].plot(derivDf['True Strain'], derivDf['Real Derivative'], label = '1st Derivative')
    axis[1].plot(reducedDf['True Strain'], reducedDf['DeScaled Derivative'], label = 'DeScaled Derivative')
    axis[1].legend()
    
    plt.tight_layout()
    plt.show()
    

analyse(15)