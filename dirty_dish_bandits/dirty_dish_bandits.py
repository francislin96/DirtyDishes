### Import necessary libraries
import numpy as np
import RPi.GPIO as GPIO
import time
import sys
from hx711 import HX711
import tkinter as tk
import tkinter.font

### Helper functions

def measure_sink():
    # Returns a double corresponding with how much weight is in the sink
    try:
        val = hx.get_weight(5)
        #print(val)
        hx.power_down()
        hx.power_up()
        time.sleep(.01)
    except (KeyboardInterrupt, SystemExit):
        GPIO.cleanup()
        print("Exiting..")
        sys.exit()
    return val

"""
def load_faces(num_people):
    # Returns an array of faces as templates for future face detection

def person_is_detected():
    # Returns a boolean indicating whether a person is detected or not

def identify_person():
    # Returns an int corresponding with that person's index in weight_array
"""

def change_array(person_index, weight_array, delta_weight,):
    # Updates weight_array based on how the sink changed

    # if person washes less than their weight, subtract it
    if weight_array[person_index] + delta_weight > 0:
        weight_array[person_index] = weight_array[person_index] + delta_weight

    # if person washes more than their weight, redistribute weight to other members
    else:
        # find how much each person contributes to the sink, and redistribute based on ratio
        sum_array = sum(weight_array) - weight_array[person_index]
        for i in range(0, len(weight_array)):
            if i != person_index:
                weight_array[i] = weight_array[i] + float(weight_array[i])/sum_array * (weight_array[person_index] + delta_weight)
        weight_array[person_index] = 0
    # return new weight_array
    return weight_array

def update_data(weight_array):
    # Updates weight_array
    if person_is_detected():
        person_index = identify_person()                                            # Find the index of weight_array that belongs to person detected
        weight_after = measure_sink()                                                # Takes measurement from load cell
        delta_weight = weight_after - weight_before                                    # Calculate the change in weight
        weight_array = change_array(person_index, weight_array, delta_weight)        # Update the weight array accordingly
        global weight_before
        weight_before = weight_after                                                # Update weight_before for next iteration

def update_display():
    # Iterates for t > 0, updates display
    weight_array = update_data(weight_array)
    tk.Label(window, text="Dish Scoreboard", bg="black", fg="white", font="none 75 bold").grid(row=0, column=0)
    for i in range(0, len(names)):
        tk.Label(window, text="%s" % names[i], bg="black", fg="white", font="none 50 bold").grid(row=i+2, column=0)
        tk.Label(window, text="%d" % weight_array[i], bg="black", fg="white", font="none 50 bold").grid(row=i+2, column=1)
    window.after(2000, update_display)

# MAIN FUNCTION
def main():
    # Initialize parameters at t = 0
    num_people = 4                                        # Initialize number of people
    weight_array = np.zeros(num_people)                    # Store weights in an array
    global weight_before
    weight_before = measure_sink()                        # Initial weight in sink
    faces = load_faces(num_people)                        # Stores template faces for each person
    names = ["Brooke", "Eric", "Francis", "Nithin"]        # Stores names of each person

    # Initialize load cell
    hx = HX711(5, 6)
    hx.set_reading_format("LSB", "MSB")
    hx.set_reference_unit(92)       # Calibrate reference unit to 1g
    hx.reset()
    hx.tare()

    # Initialize Display
    window = tk.Tk()
    window.title("Dirty dishes")
    window.configure(background="black")
    myFont = tkinter.font.Font(family='Helvetica', size = 25, weight = "bold")

    # Iterate for t > 0
    update_display()        # calls update_data as well
    window.mainloop()


#######
if __name__ == "__main__":
    main()