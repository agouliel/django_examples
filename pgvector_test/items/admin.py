from django.contrib import admin
from items.models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["content" , "price", "in_stock"]
    list_filter = ["price", "in_stock"]
    search_fields = ["content"]
    show_facets = admin.ShowFacets.ALWAYS

    def get_search_results(self, request, queryset, term):
      queryset, _ = super().get_search_results(request, queryset, term)
      if term:
        queryset |= self.model.search(term) # union
      return queryset, _