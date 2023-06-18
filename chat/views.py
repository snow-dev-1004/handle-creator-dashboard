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
    chats = models.Chat.objects.filter(user=request.user.id).order_by("-datetime")
    chat_list = list(chats)
    sorted_chats = sorted(chat_list, key=lambda chat: chat.datetime)
    
    if request.method=='POST': 
        message = request.POST.get('message')
        
        message_list = [chat.message for chat in sorted_chats]
        conversion_history = ''.join(message_list)
        if conversion_history == '':
            conversion_history = "You are Handlechat, a AI support of Handlechat company"
        
        ai_message = generate_response(conversion_history + message)
        
        new_user_chat = models.Chat(message=message,sender=0,user=request.user)
        new_user_chat.save()
        
        new_ai_chat = models.Chat(message=ai_message,sender=1,user=request.user)
        new_ai_chat.save()
        
        return JsonResponse({
            "message": "Add the text in the database successfully!", 
            "data": ai_message
        })
    notebook = models.Note.objects.filter(user=request.user.id).first()
    return render(request, 'chat/chat.html', {
        'chats': sorted_chats,
        'note': notebook
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