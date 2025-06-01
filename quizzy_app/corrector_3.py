
from .models import *
import re

# Function to upload the corrected array into the database
def parse_correction_into_array(cleaned_string):
    print(f"[DEBUG] parse_correction_into_array called")
    print(f"[DEBUG] Input string length: {len(cleaned_string)}")
    print(f"[DEBUG] Input string first 300 chars: {cleaned_string[:300]}...")
    
    # Clean the string by removing '```python' and '```'
    cleaned_string = cleaned_string.replace('```python', '').replace('```', '').strip()
    print(f"[DEBUG] After cleaning, string length: {len(cleaned_string)}")
    
    # Initialize empty lists
    corrections = []
    current_question = None
    current_question_id = None

    # Use regex to match the patterns
    lines = cleaned_string.splitlines()
    print(f"[DEBUG] Number of lines to process: {len(lines)}")

    for i, line in enumerate(lines):
        print(f"[DEBUG] Processing line {i}: {line}")
        try:
            if "$1/1$" in line:  # It's a question
                print(f"[DEBUG] Found question line: {line}")
                # Extract the question ID
                question_match = re.search(r'\$1/1\$\s*(.*?)\s*\$1/1\$', line)
                if question_match:
                    current_question_id = question_match.group(1).strip()
                    current_question = [[current_question_id]]  # Create a new question array with the ID
                    corrections.append(current_question)  # Add it to the main list
                    print(f"[DEBUG] Added question {current_question_id}, corrections now has {len(corrections)} items")
                else:
                    print(f"[DEBUG] Question regex didn't match for line: {line}")
            elif "$2/2$" in line:  # It's a choice
                print(f"[DEBUG] Found choice line: {line}")
                # Extract the choice ID
                choice_match = re.search(r'\$2/2\$\s*(.*?)\s*\$2/2\$', line)
                if choice_match and current_question is not None:
                    choice_id = choice_match.group(1).strip()
                    current_question.append([choice_id])  # Add the choice ID to the current question array
                    print(f"[DEBUG] Added choice {choice_id} to current question")
                else:
                    print(f"[DEBUG] Choice regex didn't match or no current question")
            elif "$3/3$" in line:  # It's a 0 or 1 indicator
                print(f"[DEBUG] Found value line: {line}")
                # Extract the 0 or 1 value
                value_match = re.search(r'\$3/3\$\s*(.*?)\s*\$3/3\$', line)
                if value_match and current_question is not None and len(current_question) > 1:
                    value = value_match.group(1).strip()
                    # Convert to boolean string for database compatibility
                    bool_value = 'true' if value == '1' else 'false'
                    current_question[-1].append(bool_value)  # Add the true/false value to the last choice
                    print(f"[DEBUG] Added value {bool_value} to last choice")
                else:
                    print(f"[DEBUG] Value regex didn't match or no current question/choices")
        except Exception as e:
            print(f"[DEBUG] Error encountered on line {i}: {e}")
            print(f"[DEBUG] Line content: {line}")
            # Return the already parsed corrections when an error occurs
            print(f"[DEBUG] Corrections so far: {corrections}")
            return corrections
   
    print(corrections)

    # Output the parsed array
    return corrections
