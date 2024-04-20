from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import *
from .forms import *
# Create your views here.


def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, "User does not exisit. Try registering yourself first!")
            return redirect('login-page')
          #validating credentials
        user = authenticate(request, username = username , password = password )
        if user == None:
          messages.error(request, "Incorrect Username or Password!")
        else:
          user = login(request,user)
          return redirect('home')

    return render(request , 'main/login_register.html' , context={'page' : page})

def register_page(request):
    page = 'register'
    form = UserCreationForm()
    if request.method == 'POST':
        #get data from frontend
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            print(user.username)
            if User.objects.filter(username = user.username).exists():
                print(User.objects.filter(username = user.username).exists())
                messages.error(request , "User with this username already exsist")
                return redirect('register-page')
            else:
                user.save()
                login(request,user)
                return redirect('home')
        else:
            messages.error(request , "Something went wrong, try again")
            redirect('register-page')        
        
    return render(request, 'main/login_register.html' , context={'page' : page , 'form' : form})
'''    print("HEllo")
    page = 'register'
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username = username)
            messages.error(request , "User with this username already exsist")
            redirect('register-page')
        except:
            User.objects.create_user(username=username, password=password)
            redirect('login-page')'''


def logout_page(request):
    logout(request)
    return redirect('login-page')


@login_required(login_url = 'login-page')
def home(request):
    name = request.GET.get('name')
    if request.GET.get('name') == None:
        name = ""
    print(name)
    if name == None:
        all_rooms = Room.objects.all()
    else:
        all_rooms = Room.objects.filter(Q(topic__name__icontains = name) | Q(host__username__icontains = name) | Q(name__icontains = name) | Q(description__icontains = name))
    
    all_topics = Topic.objects.all() 
    rooms_count = all_rooms.count()
    total_count = Room.objects.all().count()
    recent_messages = Message.objects.filter(Q(room__topic__name__icontains = name)).order_by('-updated_at')[:5]
    return render(request,'main/home.html' , context={'rooms' : all_rooms, 'topics' : all_topics, 'rooms_count' : rooms_count , 'total_count' : total_count , 'recent_messages' : recent_messages})

def room(request,pk):
    room = Room.objects.get(id = pk)
    room_msgs = room.message_set.all().order_by('-created_at')
    members = room.members.all()
    if request.method == "POST":
        Message.objects.create(sender = request.user , room = room , matter = request.POST.get('matter')  )
        sender = request.user
        if not (room.members.filter(username = sender.username).exists()):
            room.members.add(request.user)
        
    
    return render(request,'main/room.html' , context={'room' : room , 'room_msgs' : room_msgs , 'members' : members})

@login_required(login_url = 'login-page')
def delete_message(request,pk):
    page = "msg"
    deleting_msg = Message.objects.get(id = pk)
    if request.user != deleting_msg.sender:
        return HttpResponse("Access denied!")
    if request.method == 'POST':
        deleting_msg.delete()
        return redirect('home') 
    return render(request , 'main/delete.html' , context={'obj' : deleting_msg , 'page' : page})






@login_required(login_url = 'login-page')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name) # This simple creates a topic object if a new topic is typed else return an exsisting topic
        obj = Room.objects.create(host = request.user ,topic = topic , name = request.POST.get('name') , description = request.POST.get('description'))
        user_obj = User.objects.get(id = request.user.id)
        obj.members.add(user_obj)
        return redirect('home')

    return render(request, 'main/room_form.html' , context={'form' : form , 'topics' : topics})

@login_required(login_url = 'login-page')
def update_room(request, pk):
    updating_room = Room.objects.get(id = pk)
    form = RoomForm(instance=updating_room)
    topics = Topic.objects.all()
    if request.user != updating_room.host:
        return HttpResponse("Access denied!")

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name) # This simple creates a topic object if a new topic is typed else return an exsisting topic
        Room.objects.update(topic = topic , name = request.POST.get('name') , description = request.POST.get('description'))
        return redirect('home')

    return render(request, 'main/room_form.html' , context={'form' : form , 'topics' : topics , 'updating_room' : updating_room })

#iss function say bhi proper delete ho raha hai, but no confirmation wala scn
@login_required(login_url = 'login-page')
def delete_room(request , pk):
    deleting_room = Room.objects.get(id = pk).delete()
    return redirect('home')

#iss function say delete ho raha hai with confirmation wala scn
@login_required(login_url = 'login-page')
def delete_room_confirm(request,pk):
    deleting_room = Room.objects.get(id = pk)
    if request.user != deleting_room.host:
        return HttpResponse("Access denied!")
    if request.method == 'POST':
        deleting_room.delete()
        return redirect('home')
    return render(request , 'main/delete.html' , context={'obj' : deleting_room})
    
@login_required(login_url = 'login-page')
def user_profile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    recent_messages = user.message_set.all().order_by('-updated_at')[:5]
    return render(request,'main/user_profile.html' , context={'user' : user , 'rooms' : rooms , 'topics' : topics , 'recent_messages' : recent_messages})

@login_required(login_url = 'login-page')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == "POST":
        form  = UserForm(request.POST , instance=user)
        form.save()
        return redirect('user-profile' , pk = user.id)

    return render(request , 'main/update_user.html' , context={'form' : form})

def topics(request):
    searched_topic = request.GET.get('searched_topic')
    if searched_topic == None:
        all_topics = Topic.objects.all()
    else:
        all_topics = Topic.objects.filter(Q(name__icontains = searched_topic))
    

    return render(request , 'main/topics.html' , context={'all_topics' : all_topics})

def activity(request):

    recent_messages = Message.objects.all().order_by('-updated_at')[:5]
    return render(request , 'main/activity.html' , context={'recent_messages' : recent_messages , })