from tkinter import filedialog
import tkinter as tk
import os

class GUInstance():
    
    # Constructor with internal variables
    def __init__(self):
        self.root = None
        self.padxVal = 5
        self.padyVal = 5
        self.withVal = 15
        self.resolution = '650x200'
        
    # Get input file name and create the output file name
    def select_input_file(self):
            
        # Get file from dialog box 
        file_path = filedialog.askopenfilename(
            filetypes=[("Input Files", "*.xlsx")])
        
        # 
        if file_path:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, file_path)
            
            #Get original file name
            output_file_name = os.path.basename(file_path).split('.')[0] + "_80char"
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, output_file_name)
    
    def select_option(self, varState1, varState2, option):
        if option == 1:
            varState1.set(True)
            varState2.set(False)
        else:
            varState1.set(False)
            varState2.set(True)
        
    def run(self):
        
        # GUI Object 
        self.root = tk.Tk()
        
        # GUI Title
        self.root.title('Material Calibrator')

        # Window resolution
        self.root.geometry('650x200')
        
        # Text Boxes
        output_label = tk.Label(self.root, text='Material Name:')
        output_label.grid(row=0, column=0, columnspan=2, padx=self.padxVal, pady=self.padyVal)
        output_entry = tk.Entry(self.root, width=self.withVal)
        output_entry.grid(row=0, column=2, columnspan=2, padx=self.padxVal, pady=self.padyVal)

        output_label = tk.Label(self.root, text='Temperature:')
        output_label.grid(row=0, column=4, columnspan=2, padx=self.padxVal, pady=self.padyVal)
        output_entry = tk.Entry(self.root, width=self.withVal)
        output_entry.grid(row=0, column=6, columnspan=2, padx=self.padxVal, pady=self.padyVal)

        output_label = tk.Label(self.root, text='Type:')
        output_label.grid(row=1, column=0, columnspan=2, padx=self.padxVal, pady=self.padyVal)
        output_entry = tk.Entry(self.root, width=self.withVal)
        output_entry.grid(row=1, column=2, columnspan=2, padx=self.padxVal, pady=self.padyVal)

        output_label = tk.Label(self.root, text='Rate:')
        output_label.grid(row=1, column=4, columnspan=2, padx=self.padxVal, pady=self.padyVal)
        output_entry = tk.Entry(self.root, width=self.withVal)
        output_entry.grid(row=1, column=6, columnspan=2, padx=self.padxVal, pady=self.padyVal)

        output_label = tk.Label(self.root, text='Manufacturer:')
        output_label.grid(row=2, column=0, columnspan=2, padx=self.padxVal, pady=self.padyVal)
        output_entry = tk.Entry(self.root, width=self.withVal)
        output_entry.grid(row=2, column=2, columnspan=2, padx=self.padxVal, pady=self.padyVal)

        output_label = tk.Label(self.root, text='Poisson:')
        output_label.grid(row=2, column=4, columnspan=2, padx=self.padxVal, pady=self.padyVal)
        output_entry = tk.Entry(self.root, width=self.withVal)
        output_entry.grid(row=2, column=6, columnspan=2, padx=self.padxVal, pady=self.padyVal)

        # Stress-True stress-strain options
        engState = tk.BooleanVar(value = True)
        trueState = tk.BooleanVar()

        engLabel = tk.Label(text='Engineering Curve', padx=self.padxVal, pady=self.padyVal)
        trueLabel = tk.Label(text='True Curve', padx=self.padxVal, pady=self.padyVal)

        engCheckBox = tk.Checkbutton(self.root, variable=engState, command=lambda: self.select_option(engState, trueState, 1))
        trueCheckBox = tk.Checkbutton(self.root, variable=trueState, command=lambda: self.select_option(engState, trueState, 2))

        engLabel.grid(row=3, column=0, padx=self.padxVal, pady=self.padyVal)
        trueLabel.grid(row=3, column=4, padx=self.padxVal, pady=self.padyVal)
        engCheckBox.grid(row=3, column=2, padx=self.padxVal, pady=self.padyVal)
        trueCheckBox.grid(row=3, column=6, padx=self.padxVal, pady=self.padyVal)

        # Strain variable options
        percState = tk.BooleanVar(value = True)
        adiState = tk.BooleanVar()

        percLabel = tk.Label(text='Strain(%)', padx=self.padxVal, pady=self.padyVal)
        adiLabel = tk.Label(text='Strain(-)', padx=self.padxVal, pady=self.padyVal)

        percCheckBox = tk.Checkbutton(self.root, variable=percState, command=lambda: self.select_option(percState, adiState, 1))
        adiCheckBox = tk.Checkbutton(self.root, variable=adiState, command=lambda: self.select_option(percState, adiState, 2))

        percLabel.grid(row=4, column=0, padx=self.padxVal, pady=self.padyVal)
        adiLabel.grid(row=4, column=4, padx=self.padxVal, pady=self.padyVal)
        percCheckBox.grid(row=4, column=2, padx=self.padxVal, pady=self.padyVal)
        adiCheckBox.grid(row=4, column=6, padx=self.padxVal, pady=self.padyVal)

        # Input/Output file Button 
        input_button = tk.Button(self.root, text='Select Input File', compound= 'left',command=self.select_input_file)
        input_button.grid(row=5 , column=2, padx=self.padxVal, pady=self.padyVal)
        self.input_entry = tk.Entry(self.root, width=(self.withVal*3))
        self.input_entry.grid(row=5, column=4,padx=self.padxVal, pady=self.padyVal)

        self.root.grid_rowconfigure([0, 1, 2, 3, 4, 5], weight=1)
        self.root.grid_columnconfigure([0, 1, 2, 3, 4, 5], weight=1)


        self.root.mainloop()

        
        