from django.contrib import admin
from .models import Product, Category, Review


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price',
        'image',
    )

    ordering = ('category',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'approved', 'created_at')
    list_filter = ('approved', 'created_at')
    search_fields = ('user__username', 'product__name', 'comment')

    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        """ Custom action to approve selected reviews """
        queryset.update(approved=True)
        self.message_user(request, "Selected reviews have been approved successfully.")
    approve_reviews.short_description = "Approve selected reviews"

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
