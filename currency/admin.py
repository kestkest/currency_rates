from django.contrib import admin

from .models import Currency
from .utils import update_currency_rates


class CurrencyAdmin(admin.ModelAdmin):
    fields = ('nominal', 'title', 'rate', 'code')
    list_display = ('nominal', 'title', 'rate', 'code')
    actions = ['update_rates']

    def changelist_view(self, request, extra_context=None):
        if request.method == 'POST' and request.POST.get('action') == 'update_rates':
            post = request.POST.copy()
            post.setlist(admin.helpers.ACTION_CHECKBOX_NAME,
                         self.model.objects.values_list('id', flat=True))
            request.POST = post
            self.message_user(request, "Currency rates have been successfully updated!")

        return super().changelist_view(request, extra_context=None)

    def update_rates(self, request, queryset):
        update_currency_rates()

    update_rates.short_description = "Updates all currencies rates"


admin.site.register(Currency, CurrencyAdmin)
