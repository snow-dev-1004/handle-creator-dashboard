from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import models
from django.http import JsonResponse
from .utils import generate_response

@login_required
def dashboard_view(request):
    return render(request, 'chat/dashboard.html')

@login_required
def chat_view(request):
    # message = request.POST.get('message')
    if request.method=='POST': 
        ai_message = generate_response(message)
        
        new_user_chat = models.Chat(message=message,sender=0,user=request.user)
        new_user_chat.save()
        
        new_ai_chat = models.Chat(message=ai_message,sender=1,user=request.user)
        new_ai_chat.save()
        
        return JsonResponse({
            "message": "Add the text in the database successfully!", 
            "data": ai_message
        })
        
    chats = models.Chat.objects.filter(user=request.user.id).order_by("-datetime")[:3]
    chat_list = list(chats)
    sorted_chats = sorted(chat_list, key=lambda chat: chat.datetime)
    return render(request, 'chat/chat.html', {
        'chats': sorted_chats
    })

@login_required
def notebook_view(request):
    notebook = models.Note.objects.filter(user=request.user.id).first()
    if request.method=='POST': 
        content = request.POST.get('content')
        if notebook:
            notebook.message = content
            notebook.save()
        else:
            notebook = models.Note(message=content,user=request.user)
            notebook.save()
    
    return render(request, 'chat/notebook.html', {
        'note': notebook
    })