from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Message


@login_required
def messages_list_view(request):
    message_list = Message.objects.filter(item__parent=request.user)
    return render(request, 'messages_list.html', {'message_list': message_list})


@login_required
def message_detail_view(request, pk):
    message = get_object_or_404(Message, pk=pk, item__parent=request.user)
    
    # Mark as read when viewing
    if not message.is_read:
        message.is_read = True
        message.save()
    
    return render(request, 'message_detail.html', {'message': message})
