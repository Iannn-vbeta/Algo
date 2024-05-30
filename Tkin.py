from tkinter import *

window = Tk()
window.title("Tanilogi")
lebar = 800
tinggi = 500
x = 400
y = 200

window.resizable(False, False)

screenWidth = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()

newWindow = int((screenWidth/2) - (lebar/2))
newHeight = int((screenHeight/2) - (tinggi/2))

window.geometry(f'{lebar}x{tinggi}+{x}+{y}')

window.mainloop()