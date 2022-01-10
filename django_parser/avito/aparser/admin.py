from django.contrib import admin

from .forms import ProductForm
from .models import Product

from .forms import ProfileForm
from .models import Profile
from .models import Message

from .models import Rent
from .forms import RentForm

PRICE_FILTER_STEPS = 10


class PriceFilter(admin.SimpleListFilter):
    title = 'Цена'
    parameter_name = 'price'

    def lookups(self, request, model_admin):
        # Вытащить полный список цен
        prices = [c.price for c in model_admin.model.objects.all()]
        prices = list(filter(None, prices))
        if not prices:
            return

        # TODO: найти "кластера цен", то есть такие интервалы, внутри которых точно есть продукты!

        # Побить его на 10 интервалов
        max_price = max(prices)
        chunk = int(max_price / PRICE_FILTER_STEPS)
        print(f'max_price = {max_price}, chunk = {chunk}')

        intervals = [
            (f'{chunk * i},{chunk * (i + 1)}', f'{chunk * i} - {chunk * (i + 1)}')
            for i in range(PRICE_FILTER_STEPS)
        ]
        return intervals

    def queryset(self, request, queryset):
        choice = self.value() or ''
        if not choice:
            return queryset
        choice = choice.split(',')
        if not len(choice) == 2:
            return queryset
        price_from, price_to = choice
        return queryset.distinct().filter(price__gte=price_from, price__lt=price_to)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'address', 'published_date', 'url')
    list_filter = ('published_date', PriceFilter)
    form = ProductForm


@admin.register(Rent)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'srok', 'address', 'published_date', 'url')
    list_filter = ('published_date', PriceFilter)
    form = RentForm


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name')
    form = ProfileForm


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'text', 'created_at')