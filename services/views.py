# services/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Service
from .forms import ServiceForm

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
        return context

class ServiceDetailView(DetailView):
    model = Service
    template_name = 'services/service_detail.html'

class ServiceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'services/service_form.html'
    success_url = reverse_lazy('services:list')

    def test_func(self):
        return self.request.user.role == 'PROVIDER' and self.request.user.is_approved

    def form_valid(self, form):
        form.instance.gardener = self.request.user
        messages.success(self.request, 'Service created successfully!')
        return super().form_valid(form)

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