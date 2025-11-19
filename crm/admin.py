from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Company, Customer, Interaction, User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'created_at', 'updated_at')
    fieldsets = UserAdmin.fieldsets + (
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'company', 'representative', 'birthday')
    list_filter = ('company', 'representative')
    search_fields = ('first_name', 'last_name', 'company__name', 'representative__username')


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ('customer', 'interaction_type', 'date')
    list_filter = ('interaction_type', 'date')
    search_fields = ('customer__first_name', 'customer__last_name')
