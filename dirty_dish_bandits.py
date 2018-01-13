### Import necessary libraries
import numpy as np


### Initialize at t = 0
num_people = 100									# Initialize number of people
weight_array = np.zeros(num_people)					# Store weights in an array
weight_before = measure_sink()						# Initial weight in sink
faces = load_faces(num_people)						# Stores template faces for each person
names = ["Brooke", "Eric", "Francis", "Nithin"]		# Stores names of each person


### Iterate for t > 0
while True:
	if person_is_detected():
		person_index = identify_person()											# Find the index of weight_array that belongs to person detected
		weight_after = measure_sink()												# Takes measurement from load cell
		delta_weight = weight_after - weight_before									# Calculate the change in weight
		weight_array = change_array(person_index, weight_array, delta_weight)		# Update the weight array accordingly
		weight_before = weight_after												# Update weight_before for next iteration

	display_results(faces, num_people, weight_array)								# Continuously display weight_array




### Helper functions

def measure_sink():
	# Returns a double corresponding with how much weight is in the sink

def load_faces(num_people):
	# Returns an array of faces as templates for future face detection

def person_is_detected():
	# Returns a boolean indicating whether a person is detected or not

def identify_person():
	# Returns an int corresponding with that person's index in weight_array

def change_array(person_index, delta_weight):
	# Updates weight_array based on how the sink changed

def display_results(faces, weight_array):
	# Updates the continuous display with the weight of each person
	for i in names:
		print "%s: %dg" % (name[i], weight_array[i])

def change_array(person_index, weight_array, delta_weight,):
	# Recalculates weight_array
	#weight_array(person_index) = weight_array(person_index) + delta_weight
	#if weight_array(person_index) < 0:
		# redistribute the extra weight amongst the others
		# change the person's weight to 0
