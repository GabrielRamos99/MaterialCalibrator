import tkinter as tk

def increase_value():
    current_value = int(spinbox.get())
    spinbox.delete(0, tk.END)
    spinbox.insert(0, str(current_value + 1))

def decrease_value():
    current_value = int(spinbox.get())
    spinbox.delete(0, tk.END)
    spinbox.insert(0, str(current_value - 1))

# Create the main window
root = tk.Tk()
root.title("Increment/Decrement Value")

# Create a Spinbox widget with arrows to increase or decrease the value
spinbox = tk.Spinbox(root, from_=0, to=100)

# Create buttons to increase and decrease the value
increase_button = tk.Button(root, text="Increase", command=increase_value)
decrease_button = tk.Button(root, text="Decrease", command=decrease_value)

# Pack the Spinbox and buttons
spinbox.pack(padx=10, pady=10)
increase_button.pack(side="left", padx=5)
decrease_button.pack(side="right", padx=5)

# Start the main event loop
root.mainloop()
