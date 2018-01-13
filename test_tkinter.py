# Import necessary libraries
import tkinter as tk
import tkinter.font
import time

# Initialize
window = tk.Tk()
window.title("Dirty dishes")
window.configure(background="black")
myFont = tkinter.font.Font(family='Helvetica', size = 25, weight = "bold")
names = ['Brooke: ', 'Eric: ', 'Francis: ', 'Nithin: ']
dish = [0, 10, 0, 0]

def update():
	dish[2] = dish[2]+1
	tk.Label(window, text="Dish Scoreboard", bg="black", fg="white", font="none 75 bold").grid(row=0, column=0)
	for i in range(0, len(names)):
		tk.Label(window, text="%s" % names[i], bg="black", fg="white", font="none 50 bold").grid(row=i+2, column=0)
		tk.Label(window, text="%d" % dish[i], bg="black", fg="white", font="none 50 bold").grid(row=i+2, column=1)
	window.after(5, update)
update()
window.mainloop()

print('hi')