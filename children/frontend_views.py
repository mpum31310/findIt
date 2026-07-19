from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Child
from .forms import ChildForm


@login_required
def children_list_view(request):
    children = Child.objects.filter(parent=request.user)
    return render(request, 'children_list.html', {'children': children})


@login_required
def child_add_view(request):
    if request.method == 'POST':
        form = ChildForm(request.POST)
        if form.is_valid():
            child = form.save(commit=False)
            child.parent = request.user
            child.save()
            messages.success(request, 'Child added successfully!')
            return redirect('children_list')
    else:
        form = ChildForm()
    return render(request, 'child_add.html', {'form': form})


@login_required
def child_detail_view(request, pk):
    child = get_object_or_404(Child, pk=pk, parent=request.user)
    
    if request.method == 'POST':
        if 'delete' in request.POST:
            child.delete()
            messages.success(request, 'Child deleted successfully!')
            return redirect('children_list')
        else:
            form = ChildForm(request.POST, instance=child)
            if form.is_valid():
                form.save()
                messages.success(request, 'Child updated successfully!')
                return redirect('child_detail', pk=child.pk)
    else:
        form = ChildForm(instance=child)
    
    items = child.items.all()
    return render(request, 'child_detail.html', {'form': form, 'child': child, 'items': items})

