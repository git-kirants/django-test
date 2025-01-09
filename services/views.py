# services/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Service
from .forms import ServiceForm, ServiceImageFormSet
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
import json
from django.db.models import Q
from django.template.loader import render_to_string

class ServiceListView(ListView):
    model = Service
    template_name = 'services/service_list.html'
    context_object_name = 'services'
    paginate_by = 12

    def get_queryset(self):
        queryset = Service.objects.filter(is_available=True)
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service_categories'] = Service.CATEGORY_CHOICES
        context['messages'] = list(messages.get_messages(self.request))
        return context

class ServiceDetailView(DetailView):
    model = Service
    template_name = 'services/service_detail.html'

class ServiceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'services/service_form.html'
    success_url = reverse_lazy('services:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = ServiceImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['image_formset'] = ServiceImageFormSet()
        return context

    def test_func(self):
        return self.request.user.role == 'PROVIDER'

    @transaction.atomic
    def form_valid(self, form):
        form.instance.gardener = self.request.user
        context = self.get_context_data()
        image_formset = context['image_formset']
        
        if image_formset.is_valid():
            self.object = form.save()
            image_formset.instance = self.object
            image_formset.save()
            messages.success(self.request, 'Service created successfully!')
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

class ServiceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'services/service_form.html'
    success_url = reverse_lazy('services:list')

    def test_func(self):
        service = self.get_object()
        return self.request.user == service.gardener

    def form_valid(self, form):
        messages.success(self.request, 'Service updated successfully!')
        return super().form_valid(form)

class ServiceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Service
    success_url = reverse_lazy('services:list')
    template_name = 'services/service_confirm_delete.html'

    def test_func(self):
        service = self.get_object()
        return self.request.user == service.gardener

def service_details(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    
    # Check permissions
    can_edit = request.user == service.gardener
    can_change_availability = can_edit or request.user.is_staff
    
    data = {
        'id': service.id,
        'title': service.title,
        'description': service.description,
        'price': str(service.price),
        'duration': service.duration,
        'category': service.get_category_display(),
        'is_available': service.is_available,
        'image': service.image.url if service.image else None,
        'additional_images': [img.image.url for img in service.additional_images.all()],
        'gardener': {
            'id': service.gardener.id,
            'name': service.gardener.get_full_name() or service.gardener.username,
            'business_name': getattr(service.gardener.providerprofile, 'business_name', ''),
            'description': getattr(service.gardener.providerprofile, 'description', ''),
            'phone': getattr(service.gardener.providerprofile, 'phone_number', ''),
        },
        'permissions': {
            'can_edit': can_edit,
            'can_change_availability': can_change_availability
        },
        'can_book': request.user.is_authenticated and request.user.role == 'CUSTOMER' and service.is_available,
        'average_rating': service.get_average_rating(),
        'total_ratings': service.get_total_ratings(),
    }
    
    return JsonResponse(data)

@login_required
@require_POST
def toggle_availability(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    
    # Check if user has permission to change availability
    if not (request.user == service.gardener or request.user.is_staff):
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    
    data = json.loads(request.body)
    service.is_available = data.get('is_available', False)
    service.save()
    
    return JsonResponse({'success': True})

def service_list(request):
    search_query = request.GET.get('search', '')
    
    services = Service.objects.all()
    
    if search_query:
        services = services.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__icontains=search_query) |
            Q(gardener__providerprofile__business_name__icontains=search_query)
        )
    
    service_categories = Service.CATEGORY_CHOICES
    
    context = {
        'services': services,
        'service_categories': service_categories,
    }
    return render(request, 'services/service_list.html', context)

def service_search(request):
    search_query = request.GET.get('search', '')
    
    services = Service.objects.all()
    
    if search_query:
        services = services.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__icontains=search_query) |
            Q(gardener__providerprofile__business_name__icontains=search_query)
        )
    
    html = render_to_string('services/partials/service_grid.html', {
        'services': services,
        'request': request
    })
    
    return HttpResponse(html)