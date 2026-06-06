import tkinter as tk
from tkinter import ttk
from gui import ConcertModelApp

def main():
    root = tk.Tk()

    try:
        style = ttk.Style()
        if "clam" in style.theme_names():
            style.theme_use("clam")
    except tk.TclError:
        pass

    ConcertModelApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()