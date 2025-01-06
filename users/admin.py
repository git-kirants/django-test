from django.contrib import admin
from django.utils.html import format_html
from .models import User, ProviderProfile, ProviderApplication

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_approved', 'date_joined')
    list_filter = ('role', 'is_approved', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)

@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_profile_completed', 'service_radius')
    list_filter = ('is_profile_completed',)
    search_fields = ('user__username', 'user__email')

@admin.register(ProviderApplication)
class ProviderApplicationAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'applicant', 'status', 'experience_years', 
                   'submitted_at', 'action_buttons')
    list_filter = ('status', 'submitted_at')
    search_fields = ('business_name', 'user__username', 'user__email')
    readonly_fields = ('submitted_at',)
    ordering = ('-submitted_at',)

    def applicant(self, obj):
        return obj.user.get_full_name() or obj.user.username

    def action_buttons(self, obj):
        if obj.status == 'pending':
            return format_html(
                '<a class="button" href="{}?action=approve">Approve</a> '
                '<a class="button" href="{}?action=reject">Reject</a>',
                f'/admin/users/providerapplication/{obj.pk}/change/',
                f'/admin/users/providerapplication/{obj.pk}/change/'
            )
        return obj.get_status_display()

    action_buttons.short_description = 'Actions'

    def save_model(self, request, obj, form, change):
        action = request.GET.get('action')
        if action == 'approve':
            obj.status = 'approved'
            obj.user.role = 'PROVIDER'
            obj.user.is_approved = True
            obj.user.save()
        elif action == 'reject':
            obj.status = 'rejected'
        super().save_model(request, obj, form, change)

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
