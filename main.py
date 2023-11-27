import tkinter as tk
from gui import GitCredentialsManager

if __name__ == "__main__":
    root = tk.Tk()
    app = GitCredentialsManager(root)
    root.mainloop()
