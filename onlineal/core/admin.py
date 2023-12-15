from django.contrib import admin
from .models import (
    Contact,
    FAQ,
)

# Register your models here.


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'full_name',
        'phone_number',
        'message',
        'created_at',
        'updated_at',
    )
    list_display_links = (
        'id',
        'full_name',
        "phone_number",
    )


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'question',
        'display_order',
        'is_active',
        'created_at',
        'updated_at',
    )
    list_display_links = (
        'id',
        'question',
    )
