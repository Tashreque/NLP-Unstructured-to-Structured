# NLP-Unstructured-to-Structured
This tool reads in a .txt file containing medical test results in an unstructured format and exports a json containing a structured list of dictionaries which is easier to interpret.

### Steps to run the tool

- Make sure to navigate to the directory of the files in this repository
- Run the file named "form_structured.py" using the command "python form_structured.py <file_name>", where <file_name> should be replaced by the name of the actual text file obtained from OCR
- Once run, the output list of dictionaries will be displayed and will also be exported to the file "structured.json"


### How to run the program

- A class named Preprocess_text was defined, within which all necessary text preprocessing functions were defined. These included lowercasing, punctuation removal, stopwords removal, lemmatization. While removing punctuations, '/', '-' and ':' were not removed. This class was defined in the file "preprocess.py".
- Another file named "form_structured.py" contains all the functions necessary to read each OCR text file, read X1.json as well functions to validate parameters names and values.
- Initially, the analysis was done in a notebook file named "assessment.ipynb". The flow of the program can be understood easily by opening the ipynb file.


### Approach taken

For this, a simple parsing based or rule based technique is applied.

- For preprocessing, NLTK library is used.
- The OCR based text is read as a list of lines where any blank lines are removed.
- The lines are then preprocessed.
- Once this is done, each line is split based on the " " delimitter.
- For every line, each split is analyzed for parameters, values and units. For example, if a line is "ABC 123.8 121.8 60.2 nmol/l 50.5 - 65.5", the splits would be ['ABC', '123.8', '121.8', '60.2', 'nmol/l', '50.5', '-', '65.5'].
- Only the latest test result is considered from the splits.
- The splits are then analyzed using several manually constructed rules to determine whether the current split is a valid parameter (using X1.json), a valid value or a unit. Rules to determine whether a number is part of a range were also included so that a range value is not falsely identified as a test result value. If a valid value is not found, the parameter is avoided.


### Limitations

- This implementation only considers single worded parameter names since it is a split() based approach.
- This implementation would fail to parse test results placed in wrong positions since it's a rule based approach. The rules can always be made more robust to accommodate more variation in the data.
