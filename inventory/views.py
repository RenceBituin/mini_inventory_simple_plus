from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum, F, DecimalField
from .models import Item, Category
from .forms import ItemForm, CategoryForm, RegisterForm
from django.contrib.auth import login

@login_required
def item_list(request):
    q = request.GET.get('q', '').strip()
    cat = request.GET.get('cat', '').strip()
    items = Item.objects.select_related('category').all().order_by('-updated_at')

    if q:
        items = items.filter(Q(name__icontains=q) | Q(sku__icontains=q))
    if cat:
        items = items.filter(category__id=cat)

    total_value = items.aggregate(
        total=Sum(F('quantity') * F('price'), output_field=DecimalField(max_digits=12, decimal_places=2))
    )['total'] or 0
    total_qty = items.aggregate(total=Sum('quantity'))['total'] or 0

    paginator = Paginator(items, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all().order_by('name')

    return render(request, 'inventory/item_list.html', {
        'page_obj': page_obj,
        'q': q,
        'cat': cat,
        'categories': categories,
        'total_value': total_value,
        'total_qty': total_qty,
    })

@login_required
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid() and _ensure_category_exists(form):
            form.save()
            messages.success(request, 'Item created successfully.')
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'inventory/item_form.html', {'form': form, 'title': 'Add Item'})

@login_required
def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid() and _ensure_category_exists(form):
            form.save()
            messages.success(request, 'Item updated successfully.')
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'inventory/item_form.html', {'form': form, 'title': 'Edit Item'})

def _ensure_category_exists(form):
    return True

@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item deleted.')
        return redirect('item_list')
    return render(request, 'inventory/item_confirm_delete.html', {'item': item})

@login_required
def category_list_create(request):
    categories = Category.objects.all().order_by('name')
    form = CategoryForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Category added.')
        return redirect('category_list_create')
    return render(request, 'inventory/category_list_create.html', {'categories': categories, 'form': form})

# NEW — Registration View
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in immediately after registration
            messages.success(request, "Registration successful! You are now logged in.")
            return redirect('item_list')
    else:
        form = RegisterForm()
    return render(request, 'inventory/register.html', {'form': form})
