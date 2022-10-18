from django.http import HttpResponse
from django.shortcuts import render, redirect
import pymongo
import re
from DjangoCrudApp.models import Person
from django.views.decorators.csrf import csrf_exempt
from bson.objectid import ObjectId
from rest_framework.parsers import JSONParser
from django.contrib import messages


# Create your views here.

def home(request):
    persons = Person.objects.all()
    return render(request, 'index.html',{"persons": persons})

def add_person(request):
    index = get_last()
    name = request.POST['name']
    gender = request.POST['gender']
    age = request.POST['age']
    eyeColor = request.POST['eyeColor']
    balance = request.POST['balance']
    tags = validate_last_position(request.POST['tags'].split(';'))
    friends = generate_friends_object(validate_last_position(request.POST['friends'].split(';')))
    greeting = "Hello, "+name+"! You have "+ request.POST['greeting'] +" unread messages." 
    favoriteFruit = request.POST['favoriteFruit']
    person = Person(index = index, name = name, gender = gender, age = age, eyeColor = eyeColor, balance = balance,tags = tags,friends = friends, greeting = greeting, favoriteFruit=favoriteFruit)
    person.save()
    messages.success(request, 'Added Person!')
    return redirect("/")

def open_update_person(request, id):
    id = get_id(id)
    person = Person.objects.get(_id=ObjectId(id))
    person.greeting = re.findall(r'[0-9]+', person.greeting)[0]
    person.tags = ';'.join(person.tags)
    person.friends = ';'.join(get_friends(person.friends))
    return render(request, 'updatePerson.html', {"person": person})

def update_person(request, id):
    id = get_id(id)
    person = Person.objects.get(_id=ObjectId(id))
    person.name = request.POST['name']
    person.gender = request.POST['gender']
    person.age = request.POST['age']
    person.eyeColor = request.POST['eyeColor']
    person.balance = request.POST['balance']
    person.tags = validate_last_position(request.POST['tags'].split(';'))
    person.friends = generate_friends_object(validate_last_position(request.POST['friends'].split(';')))
    person.greeting = "Hello, "+request.POST['name']+"! You have "+ request.POST['greeting'] +" unread messages."
    person.favoriteFruit = request.POST['favoriteFruit']
    person.save()
    messages.success(request, 'Updated Person!')
    return redirect("/")

def delete_person(request, id):
    id = get_id(id)
    person = Person.objects.get(_id=ObjectId(id))
    person.delete()
    messages.success(request, 'Deleted Person!')
    return redirect("/")

def visualize_person(request, id):
    id = get_id(id)
    person = Person.objects.get(_id=ObjectId(id))
    return render(request, 'visualizePerson.html', {"person": person})

@csrf_exempt
def add_person_api(request):
    if(request.POST.dict() != {}):
        data = request.POST.dict()
        add_person_to_file(data)
    else:
        data = JSONParser().parse(request)
        for person in data:
            add_person_to_file(person)
    return HttpResponse("All Persons Inserted")

def add_person_to_file(data):
    index = get_last() if data.get('index') == None else data.get('index')
    name = data.get('name')
    gender = data.get('gender')
    age = data.get('age')
    eyeColor = data.get('eyeColor')
    balance = data.get('balance')
    tags = data.get('tags').split(',') if data.get('_id') == None else data.get('tags')
    friends = convert_to_dict(data.get('friends')) if data.get('_id') == None else data.get('friends')
    greeting = data.get('greeting')
    favoriteFruit = data.get('favoriteFruit')
    person = None
    if data.get('_id') == None and data.get('index') == None:
        person = Person(index = index, name = name, gender = gender, age = age, eyeColor = eyeColor, balance = balance, tags = tags, friends = friends, greeting = greeting, favoriteFruit=favoriteFruit)
    else:
        person = Person(_id = ObjectId(data.get('_id')),index = index, name = name, gender = gender, age = age, eyeColor = eyeColor, balance = balance, tags = tags, friends = friends, greeting = greeting, favoriteFruit=favoriteFruit)
    person.save()
    print("Person Inserted")
    
def get_last():
    try:
        client = pymongo.MongoClient('mongodb+srv://SebasMongoAdmin:sebasmongo@clusterpersons.nt5w8ge.mongodb.net/?retryWrites=true&w=majority')
        db = client.get_database('PersonsDB')
        collection = db.get_collection('DjangoCrudApp_person')
        last_person = collection.find().sort('index', pymongo.DESCENDING).limit(1)
        client.close()
        return last_person[0]['index'] + 1
    except Exception as e:
        return 0

def get_id(person_object):
    return person_object.split('(')[1].replace(')', '')

def convert_to_dict(json_str):
    list = json_str.split('},{')
    list_dict = []
    for object in list:
        object = object.replace('{', '')
        object = object.replace('}', '')
        object_list = object.split(',')
        new_dict = {}
        for data in object_list:
            data = data.split(':')
            new_dict[data[0]] = data[1]
        list_dict.append(new_dict)
    return list_dict

def validate_last_position(list):
    if list[len(list)-1] == '':
        list.pop()
    return list

def get_friends(friends_object):
    friends_list = []
    for friend in friends_object:
        friends_list.append(friend['name'])
    return friends_list

def generate_friends_object(friends_list):
    object_list = []
    for i in range(len(friends_list)):
        object_list.append({'id':i, 'name': friends_list[i]})
    return object_list