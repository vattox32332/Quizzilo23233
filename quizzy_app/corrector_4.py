from .models import *

def upload_correction_to_db(corrections):
    print(f"[DEBUG] upload_correction_to_db called with {len(corrections)} corrections")
    total_updates = 0
    
    # Save the corrections to the database
    for i, correction in enumerate(corrections):
        print(f"[DEBUG] Processing correction {i}: {correction}")
        if isinstance(correction, list) and len(correction) > 1:
            for j, choices in enumerate(correction[1:]):
                print(f"[DEBUG] Processing choice {j}: {choices}")
                try:
                    if isinstance(choices, list) and len(choices) >= 3:
                        choice = Choice.objects.get(id=int(choices[0]))
                        old_value = choice.Correction
                        choice.Correction = choices[2] == 'true'
                        choice.save()
                        total_updates += 1
                        print(f"[DEBUG] Updated choice {choices[0]}: {old_value} -> {choice.Correction}")
                    else:
                        print(f"[DEBUG] Invalid choice format: {choices}")
                except Choice.DoesNotExist:
                    print(f"[DEBUG] Choice with id {choices[0]} does not exist.")
                except Exception as e:
                    print(f"[DEBUG] Error processing choice: {e}")
    
    print(f"[DEBUG] Total database updates completed: {total_updates}")