import json
from django.shortcuts import render 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Student, LoginAuthentication, ClassSection


@csrf_exempt
def webhook(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body.decode('utf-8'))
            intent = data['queryResult']['intent']['displayName']
            print(intent)
            response_text = ''
            reg_num=0
            if intent == 'loginintent':
                reg_num = int(data['queryResult']['parameters']['register_number'])
                password = str(data['queryResult']['parameters']['password'])
                try:
                    student = Student.objects.get(register_number=reg_num)
                    auth = LoginAuthentication.objects.get(student=student)
                    if auth.password == password:
                        response_text = f"Welcome {student.name}!"
                    else:
                        response_text = "Invalid password. Please try again."
                except Student.DoesNotExist:
                    response_text = "Invalid register number. Please try again."

            elif intent == 'todayclass':
                try:
                    student = Student.objects.get(register_number=reg_num) # get the logged-in student object using their register number
                    section = ClassSection.objects.get(students=student)
                    
                    if section:
                        response_text = f"Today's class for {section.section_name} section is {section}."
                    else:
                        response_text = f"No classes scheduled for {student.name} today."
                except Student.DoesNotExist:
                    
                    response_text = "Invalid register number. Please try again."
                    # student = Student.objects.get(register_number=reg_num) # get the logged-in student object using their register number
                    # section = ClassSection.objects.get(students=student)
                    # print(student,section)

            else:
                response_text = "Sorry, I didn't understand that. Please try again."

            return JsonResponse({'fulfillmentText': response_text})

        else:
            return JsonResponse({'fulfillmentText': 'Invalid request method'})

    except Exception as e:
        return JsonResponse({'fulfillmentText': 'Error: ' + str(e)})
