from .models import *
import re

def MathExpressions_3(Correction_txt):
    print(f"[DEBUG] MathExpressions_3 called")
    print(f"[DEBUG] Input length: {len(Correction_txt)}")
    print(f"[DEBUG] Input first 200 chars: {Correction_txt[:200]}...")
    
    # Try to evaluate the string as Python code first
    try:
        # Clean and evaluate the response
        cleaned_string = Correction_txt.replace('```python', '').replace('```', '').strip()
        print(f"[DEBUG] Cleaned string length: {len(cleaned_string)}")
        
        # Try to evaluate as Python array
        import ast
        parsed_array = ast.literal_eval(cleaned_string)
        print(f"[DEBUG] Successfully parsed as Python array: {len(parsed_array)} items")
        
        def clean_array(arr):
            for sublist in arr:
                for item in sublist:
                    if len(item) >= 2:
                        # Remove extra backslashes
                        item[1] = re.sub(r"\\\\", r"\\", item[1])
                        # Remove newline characters
                        item[1] = item[1].replace('\\n', ' ')
            return arr
        
        clean_parsed_array = clean_array(parsed_array)
        print(f"[DEBUG] Cleaned array has {len(clean_parsed_array)} items")
        
        return clean_parsed_array
        
    except Exception as e:
        print(f"[DEBUG] Failed to parse as Python array: {e}")
        
        # Fallback to original parsing method
        cleaned_string = Correction_txt.replace('```python', '').replace('```', '').strip()

        def parse_complex_string(s):
            # Remove unnecessary characters and clean the string
            s = s.strip()

            # Define a pattern to match each question block
            block_pattern = re.compile(r'\[\[\s*(.*?)\s*\]\]')

            def parse_block(block):
                # Split by '], [' to separate question and choices
                parts = re.split(r'\], \[', block.strip('[]'))

                # Parse the question
                question = parts[0].strip('[]').split(', ', 1)
                question_id = question[0].strip()
                question_text = question[1].strip("'")

                # Parse the choices
                choices = []
                for part in parts[1:]:
                    choice_parts = re.split(r',\s*', part.strip('[]'), 1)
                    choice_id = choice_parts[0].strip()
                    choice_text = choice_parts[1].strip("'")
                    choices.append([choice_id, choice_text])

                return [[question_id, question_text]] + choices

            # Process each block to extract the questions and choices
            result = []
            for match in block_pattern.finditer(s):
                block = match.group(1)
                result.append(parse_block(block))

            return result

        parsed_array = parse_complex_string(cleaned_string)
        print(f"[DEBUG] Parsed {len(parsed_array)} items from LaTeX response")

        def clean_array(arr):
            for sublist in arr:
                for item in sublist:
                    # Remove extra backslashes
                    item[1] = re.sub(r"\\\\", r"\\", item[1])
                    # Remove newline characters
                    item[1] = item[1].replace('\\n', ' ')
            return arr
        
        clean_parsed_array = clean_array(parsed_array)
        print(f"[DEBUG] Cleaned array has {len(clean_parsed_array)} items")
        
        return clean_parsed_array


def MathExpressions_4(Correction):
    print(f"[DEBUG] MathExpressions_4 called")
    Correction_Parse = MathExpressions_3(Correction)
    print(f"[DEBUG] Processing {len(Correction_Parse)} items for database update")
    
    total_questions_updated = 0
    total_choices_updated = 0
    
    for i, data in enumerate(Correction_Parse):
        print(f"[DEBUG] Processing item {i}: Question ID {data[0][0]}")
        try:
            question = Question.objects.get(id=int(data[0][0]))
            old_content = question.Content
            question.Content = data[0][1]
            question.save()
            total_questions_updated += 1
            print(f"[DEBUG] Updated question {data[0][0]}: Content updated")
            
            for j, elements in enumerate(data[1:]):
                choice = Choice.objects.get(id=int(elements[0]))
                old_choice_content = choice.Content
                choice.Content = elements[1]
                choice.save()
                total_choices_updated += 1
                print(f"[DEBUG] Updated choice {elements[0]}: Content updated")
        except Exception as e:
            print(f"[DEBUG] Error processing item {i}: {e}")
    
    print(f"[DEBUG] LaTeX update completed: {total_questions_updated} questions, {total_choices_updated} choices updated")
