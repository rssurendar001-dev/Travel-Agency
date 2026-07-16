from django.contrib import admin
from .models import CurrencyConverter, Package, Destination, Enquiry, TravelBuddy, TravelCost, TravelGoal, Blog, Memory, BudgetPlanner

admin.site.register(Package)

admin.site.register(Destination)

admin.site.register(Enquiry)

admin.site.register(TravelGoal)

admin.site.register(Blog)

admin.site.register(Memory)

admin.site.register(BudgetPlanner)

admin.site.register(TravelCost)

admin.site.register(TravelBuddy)

admin.site.register(CurrencyConverter)