import tkinter as tk
from tkinter import ttk
from relational import handleRelationalModel
from nonrelational import handleNonRelationalModel


def create_gui():
    root = tk.Tk()
    root.title("Home Screen")

    # Set the width and height of the window
    window_width = 300
    window_height = 200
    root.geometry(f"{window_width}x{window_height}")

    # Create Button 1 with lambda function and place it at (50, 50)
    button1 = tk.Button(root, text="Relational Model",
                        command=lambda: handleRelationalModel(root))
    button1.place(x=90, y=50)

    # Create Button 2 with lambda function and place it at (150, 150)
    button2 = tk.Button(root, text="non Relational Model",
                        command=lambda: handleNonRelationalModel(root))
    button2.place(x=90, y=120)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    create_gui()
