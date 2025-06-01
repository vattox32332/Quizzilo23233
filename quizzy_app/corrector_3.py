
from .models import *
import re

# Function to upload the corrected array into the database
def parse_correction_into_array(cleaned_string):
    # Clean the string by removing '```python' and '```'
    cleaned_string = cleaned_string.replace('```python', '').replace('```', '').strip()
    
    # Initialize empty lists
    corrections = []
    current_question = None

    # Use regex to match the patterns
    lines = cleaned_string.splitlines()

    for line in lines:
        try:
            if "$1/1$" in line:  # It's a question
                # Extract the question text
                question_match = re.search(r'\$1/1\$\s*(.*?)\s*\$1/1\$', line)
                if question_match:
                    question = question_match.group(1)
                    current_question = [[question]]  # Create a new question array wrapped in an array
                    corrections.append(current_question)  # Add it to the main list
            elif "$2/2$" in line:  # It's a choice
                # Extract the choice text
                choice_match = re.search(r'\$2/2\$\s*(.*?)\s*\$2/2\$', line)
                if choice_match and current_question is not None:
                    choice = choice_match.group(1)
                    current_question.append([choice])  # Add the choice to the current question array
            elif "$3/3$" in line:  # It's a 0 or 1 indicator
                # Extract the 0 or 1 value
                value_match = re.search(r'\$3/3\$\s*(.*?)\s*\$3/3\$', line)
                if value_match and current_question is not None and len(current_question) > 1:
                    value = value_match.group(1).strip()
                    # Convert to boolean string for database compatibility
                    bool_value = 'true' if value == '1' else 'false'
                    current_question[-1].append(bool_value)  # Add the true/false value to the last choice
        except Exception as e:
            print(f"Error encountered: {e}")
            # Return the already parsed corrections when an error occurs
            print(corrections)
            return corrections
   
    print(corrections)

    # Output the parsed array
    return corrections
