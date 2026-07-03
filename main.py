import tkinter as tk        
from gui import TicTacToeApp 
def main():
    root = tk.Tk()          
    app = TicTacToeApp(root)
    root.mainloop()      
if __name__ == "__main__":
    main()
    