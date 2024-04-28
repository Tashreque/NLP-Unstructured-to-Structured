import json
import sys
from preprocess import Preprocess_text

'''
This function reads an OCR obtained .txt file and returns a list of the
lines in the file. It also gets rid of any blank lines.
'''
def read_file(file_name):
    lines = []
    with open(file_name, 'r') as file:
        for line in file:
            # Remove whitespaces on either end
            stripped_line = line.strip()

            # Only append lines which are not blank
            if len(stripped_line) > 0:
                lines.append(stripped_line)

    return lines

'''
This function reads the X1.json file and forms a dictionary where the keys
are the abbreviations and the values are sets of synonyms.
'''
def load_x1(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

    parameter_dictionary = {}

    for item in data:
        abb = item["Abbreviation"].lower()

        # Conversion to set so that searching is more efficient (constant time).
        syns = set([each.lower() for each in item["Synonyms"]])

        if abb not in parameter_dictionary:
            parameter_dictionary[abb] = syns

    return parameter_dictionary

'''
This function checks whether a given parameter is valid by using the X1.json
file.
'''
def is_valid_parameter(param, parameter_dict):
    # Check if parameter is a key in the dictionary formed from X1.
    if param in parameter_dict:
        return True
    else:
        # Check if parameter is in the set of synonyms for each key.
        for key in parameter_dict:
            if (param in parameter_dict[key]):
                return True
        return False
    
'''
This function checks whether a number is a valid value.
'''
def validate_number(item, splits, index):
    try:
        # If number is valid or if the number is part of a range
        number = float(item)
        if index == len(splits) - 1:
            if "-" in splits[index - 1][-1]:
                return False
        elif index == 0:
            if "-" in splits[index + 1][0]:
                return False
        elif ("(" in splits[index - 1][-1]) and (")" in splits[index + 1][0]):
                return False
        else:
            if ("-" in splits[index - 1][-1]) or ("-" in splits[index + 1][0]):
                return False
            else:
                return True
    except:
        # If number cannot be parsed
        return False

'''
Function to extract data from the unstructured text.
'''
def extract_data(lines, parameter_dict):
    lod = []
    for line in lines:
        splits = line.split()
        if len(splits) > 0:
            if is_valid_parameter(splits[0], parameter_dict):

                # Obtaining parameter
                parameter = splits[0]

                # Choosing the latest value
                value = ""
                i = len(splits) - 1
                for item in reversed(splits):
                    if validate_number(item, splits, i):
                        value = item
                        break
                    i -= 1

                # Initialize unit to ""
                unit = ""
                for split in splits:
                    if '/' in split:
                        unit = split

                # Add dictionary to list if a value exists
                if value != "":
                    lod.append({"parameter": parameter,
                                "value": value,
                                "unit": unit})
    return lod

def make_structured(file_name):
    # Obtain lines from file
    lines = read_file(file_name)

    # Retrieve the parameter dictionary from X1.json
    param_dict = load_x1("X1.json")

    # Perform preprocessing like lowercasing, punctuation and stopword removal etc. 
    preprocessed_lines = Preprocess_text(lines).preprocessed

    # Obtain list of dictionaries
    lod = extract_data(preprocessed_lines, param_dict)
    return lod

# Parse parameters from command line and obtain list of dictionaries
cl_params = sys.argv
file_name = cl_params[1]
lod = make_structured(file_name)

# Export list of dictionaries to a JSON file
with open('structured', 'w') as output_file:
    json.dump(lod, output_file)

# Display the list of dictionaries
print(lod)
                