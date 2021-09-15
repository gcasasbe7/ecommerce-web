from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    list_display = ('name', 'surname', 'email',)
    # The fields to filter with
    list_filter = ('added_date',)
    # Displayed data within sections
    fieldsets = (
        ('Personal info', {'fields': ('name', 'surname', 'email','is_verified', 'is_active'),}),
        #('Details', {'fields': ('province', 'city', 'date_joined', 'dni')}),
        #('Payments', {'fields': ('stripe_customer_id',)}),
        ('Permissions', {'fields': ('is_admin',),}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'surname', 'email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    readonly_fields = ('is_verified', 'is_active','is_admin')
    ordering = ('name',)
    #ordering = ('date_joined', 'first_name', 'last_name', 'city')
    filter_horizontal = ()

class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]

    class Meta:
        model = Product

class ProductImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Brand)
admin.site.register(Order)