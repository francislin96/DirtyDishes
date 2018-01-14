### Import necessary libraries
import numpy as np
import RPi.GPIO as GPIO
import time
import sys
from hx711 import HX711
import tkinter as tk
import tkinter.font
import cv2

### Helper functions

def measure_sink(hx):
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

#def load_faces(num_people):
        # Returns an array of faces as templates for future face detection

def person_is_detected(n):
    # Returns a boolean indicating whether a person is detected or not
    if(n == 1 or n == 2 or n == 3 or n == 4):
        return TRUE
    else:
        return FALSE

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

    # Read the camera
    ret, im =cam.read()
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.2,5)
    for(x,y,w,h) in faces:

        # Create rectangle around the face
        cv2.rectangle(im, (x-20,y-20), (x+w+20,y+h+20), (0,255,0), 4)
        # Recognize the face belongs to which ID
        Id = recognizer.predict(gray[y:y+h,x:x+w])

        # Check the ID if exist
        if(Id[0] == 1):
            Id = "Brooke"
        elif(Id[0] == 2):
            Id = "Eric"
        elif(Id[0] == 3):
            Id = "Francis"
        elif(Id[0] == 4):
            Id = "Nithin"
        #If not exist, then it is Unknown
        else:
            Id = "Unknown"

        # Put text describe who is in the picture
        cv2.rectangle(im, (x-22,y-90), (x+w+22, y-22), (0,255,0), -1)
        cv2.putText(im, str(Id), (x,y-40), font, 2, (255,255,255), 3)

    # Display the video frame with the bounded rectangle
    cv2.imshow('im',im) 
    if cv2.waitKey(10) & 0xFF == ord('q'): sys.exit()
    
    if person_is_detected(Id[0]):
        person_index = Id[0] - 1							# Find the index of weight_array that belongs to person detected
        weight_after = measure_sink(hx)							# Takes measurement from load cell
        delta_weight = weight_after - weight_before					# Calculate the change in weight
        weight_array = change_array(person_index, weight_array, delta_weight)		# Update the weight array accordingly
        global weight_before
        weight_before = weight_after							# Update weight_before for next iteration

def update_display():
    # Iterates for t > 0, updates display
    global weight_array
    weight_array = update_data(weight_array)
    tk.Label(window, text="Dish Scoreboard", bg="black", fg="white", font="none 75 bold").grid(row=0, column=0)
    for i in range(0, len(names)):
        tk.Label(window, text="%s" % names[i], bg="black", fg="white", font="none 50 bold").grid(row=i+2, column=0)
    tk.Label(window, text="%d" % weight_array[i], bg="black", fg="white", font="none 50 bold").grid(row=i+2, column=1)
    window.after(2000, update_display)

# MAIN FUNCTION
def main():
	# Initialize load cell
	hx = HX711(5, 6)
	hx.set_reading_format("LSB", "MSB")
	hx.set_reference_unit(92)       # Calibrate reference unit to 1g
	hx.reset()
	hx.tare()

	# Initialize parameters at t = 0
	num_people = 4						# Initialize number of people
	global weight_array
	weight_array = np.zeros(num_people)		        # Store weights in an array
	global weight_before
	weight_before = measure_sink(hx)			# Initial weight in sink
	#faces = load_faces(num_people)			    	# Stores template faces for each person
	names = ["Brooke", "Eric", "Francis", "Nithin"]		# Stores names of each person

	# Initialize Display
	window = tk.Tk()
	window.title("Dirty dishes")
	window.configure(background="black")
	myFont = tkinter.font.Font(family='Helvetica', size = 25, weight = "bold")

	# Initialize Face Recognition
	recognizer = cv2.face.LBPHFaceRecognizer_create()
	recognizer.read('trainer/trainer.yml')
	cascadePath = "haarcascade_frontalface_default.xml"
	faceCascade = cv2.CascadeClassifier(cascadePath);
	font = cv2.FONT_HERSHEY_SIMPLEX
	global cam
	cam = cv2.VideoCapture(0)

	# Iterate for t > 0
	update_display()		# calls update_data as well
	window.mainloop()

	# Stop the camera
	global cam
	cam.release()

	# Close all windows
	cv2.destroyAllWindows()


#######
if __name__ == "__main__":
	main()
