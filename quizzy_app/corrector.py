import google.generativeai as genai
from .models import *
from django.db.models import IntegerField
from django.db.models.functions import Cast
import re

# Function to create the initial array from the database
def create_exam_array(quizz_id):
    print(f"[DEBUG] create_exam_array called with quizz_id: {quizz_id}")
    
    # Fetch questions and sort them
    Questions = Question.objects.filter(Quizz_id=quizz_id).annotate(order_as_int=Cast('Order', IntegerField())).order_by('order_as_int')
    print(f"[DEBUG] Found {Questions.count()} questions")

    # Create the array of questions and choices
    Exam = []
    for question in Questions:
        tmp = []
        tmp.append([question.id, question.Content])
        print(f"[DEBUG] Processing question {question.id}: {question.Content[:50]}...")
        
        Choices = Choice.objects.filter(Question_id=question.id)
        print(f"[DEBUG] Found {Choices.count()} choices for question {question.id}")
        
        for choice in Choices:
            tmp.append([choice.id, choice.Content, 'null'])
        Exam.append(tmp)

    print(f"[DEBUG] Final Exam array length: {len(Exam)}")
    print(f"[DEBUG] Exam array structure: {Exam}")
    return Exam
