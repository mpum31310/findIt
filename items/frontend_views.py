from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Item
from .forms import ItemForm


@login_required
def items_list_view(request):
    items = Item.objects.filter(parent=request.user).select_related('child')
    return render(request, 'items_list.html', {'items': items})


@login_required
def item_add_view(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            item = form.save(commit=False)
            item.parent = request.user
            item.save()
            item.generate_qr_code()
            item.save()
            messages.success(request, 'Item added and QR code generated successfully!')
            return redirect('item_detail', pk=item.pk)
    else:
        form = ItemForm(user=request.user)
    return render(request, 'item_add.html', {'form': form})


@login_required
def item_detail_view(request, pk):
    item = get_object_or_404(Item, pk=pk, parent=request.user)
    
    if request.method == 'POST':
        if 'delete' in request.POST:
            item.delete()
            messages.success(request, 'Item deleted successfully!')
            return redirect('items_list')
        else:
            form = ItemForm(request.POST, request.FILES, instance=item, user=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Item updated successfully!')
                return redirect('item_detail', pk=item.pk)
    else:
        form = ItemForm(instance=item, user=request.user)

    return render(request, 'item_detail.html', {'form': form, 'item': item})


def item_scan_view(request, qr_data):
    """Public view for scanning QR codes"""
    try:
        item = Item.objects.get(qr_code_data=qr_data)
        from item_messages.forms import MessageForm
        from item_messages.models import Message
        
        if request.method == 'POST':
            form = MessageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.item = item
                message.save()
                return render(request, 'scan.html', {'item': item, 'message_sent': True})
        else:
            form = MessageForm(initial={'item_qr_data': qr_data})
        
        return render(request, 'scan.html', {'form': form, 'item': item, 'qr_data': qr_data})
    except Item.DoesNotExist:
        return render(request, 'scan.html', {'item': None})
