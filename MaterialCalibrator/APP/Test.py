import tkinter as tk
from tkinter import ttk
import clipboard

def add_row():
    tree.insert("", "end", values=("Value", "Stress", "Strain"))

def remove_row():
    selected_item = tree.selection()
    if selected_item:
        tree.delete(selected_item)

def paste_values():
    clipboard_content = clipboard.paste()
    values = clipboard_content.strip().split('\n')
    for value in values:
        tree.insert("", "end", values=(value, "Stress", "Strain"))

# Create the main window
root = tk.Tk()
root.title("Stress-Strain Table")

# Create a Treeview widget for the table
tree = ttk.Treeview(root, columns=("Value", "Stress", "Strain"), show="headings")
tree.heading("Value", text="Value")
tree.heading("Stress", text="Stress")
tree.heading("Strain", text="Strain")

# Create buttons to add, remove, and paste rows
add_button = tk.Button(root, text="Add Row", command=add_row)
remove_button = tk.Button(root, text="Remove Row", command=remove_row)
paste_button = tk.Button(root, text="Paste Values", command=paste_values)

# Pack the Treeview and buttons
tree.pack(padx=10, pady=10)
add_button.pack(side="left", padx=10)
remove_button.pack(side="left", padx=10)
paste_button.pack(side="right", padx=10)

# Start the main event loop
root.mainloop()
