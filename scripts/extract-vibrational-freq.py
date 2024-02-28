import re
import json
import sys

# This script parses a vibrational calculation from VASP with the
#   diagonalized phonon stretches for atoms of interest. Results
#   are saved as a .json file for later analysis. Takes in OUTCAR
#   file path as input.

# Check if at least one argument is provided
if len(sys.argv) > 1:
    # Access the first argument (index 1)
    OUTCAR = sys.argv[1]

#Create array to store results
vib_modes_list = []

# Open the text file in read mode
with open(OUTCAR, 'r') as file:
    # Initialize a list to store the line indices
    line_indices = []

    # Iterate over each line in the file, find the lines with
    #    one vibrational mode

    for idx, line in enumerate(file):
        # Check if the line matches the desired pattern
        matches = re.findall(r' f  =', line) #re.findall(r'[-+]?\d*\.\d+|\d+', line)

        if matches:
            if matches[0] == ' f  =': #vibrational mode found

                #save frequency line and restart dictionary
                freq_line = idx
                mode_dict =  {
                    "frequency (cm)": None,
                    "N3": None,
                    "N10": None,
                    "N13": None,
                    "H114": None,
                    "H144": None,
                    "Cu157": None
                }

                #extract frequency
                freq_match = re.findall(r'\d+\.\d+', line)
                mode_dict["frequency (cm)"] = float(freq_match[2])

        if 'freq_line' in locals():
            #extract the atomic displacements with regex
            if idx == freq_line + 4:
                matches = re.findall(r'(-?\d+\.\d+)', line)
                array = [float(match) for match in matches[-3:]]
                mode_dict["N3"] = array

            if idx == freq_line + 11:
                matches = re.findall(r'(-?\d+\.\d+)', line)
                array = [float(match) for match in matches[-3:]]
                mode_dict["N10"] = array

            if idx == freq_line + 14:
                matches = re.findall(r'(-?\d+\.\d+)', line)
                array = [float(match) for match in matches[-3:]]
                mode_dict["N13"] = array

            if idx == freq_line + 115:
                matches = re.findall(r'(-?\d+\.\d+)', line)
                array = [float(match) for match in matches[-3:]]
                mode_dict["H114"] = array

            if idx == freq_line + 145:
                matches = re.findall(r'(-?\d+\.\d+)', line)
                array = [float(match) for match in matches[-3:]]
                mode_dict["H144"] = array

            if idx == freq_line + 158:
                matches = re.findall(r'(-?\d+\.\d+)', line)
                array = [float(match) for match in matches[-3:]]
                mode_dict["Cu157"] = array

            if idx == freq_line + 169:
                vib_modes_list.append(mode_dict)
                mode_dict =  {
                        "frequency (cm)": None,
                        "N3": None,
                        "N10": None,
                        "N13": None,
                        "C78": None,
                        "O144": None,
                        "Cu157": None
                    }

#save results in .json file 
with open(OUTCAR + "_vib-results.json", "w") as json_file:
    json.dump(vib_modes_list, json_file)
