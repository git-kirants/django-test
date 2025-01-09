from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ProviderApplication

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('role', 'email')}),
    )

@admin.register(ProviderApplication)
class ProviderApplicationAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'username', 'email', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('business_name', 'username', 'email')
    readonly_fields = ('created_at',)
    
    actions = ['approve_applications']

    def approve_applications(self, request, queryset):
        for application in queryset:
            if application.status == ProviderApplication.STATUS_PENDING:
                # Create user account
                User.objects.create(
                    username=application.username,
                    email=application.email,
                    password=application.password,
                    role=User.PROVIDER
                )
                # Update application status
                application.status = ProviderApplication.STATUS_APPROVED
                application.save()
        
        self.message_user(request, f"Selected applications have been approved.")
    approve_applications.short_description = "Approve selected applications"
