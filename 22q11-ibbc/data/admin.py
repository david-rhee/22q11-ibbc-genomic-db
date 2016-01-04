# Core Django imports
from django.contrib import admin

# Third-party app imports

# Local app imports
from .models import UserRole, UserProfile, Site, Subject, Affymetrix

# Model registration
admin.site.register(UserRole)
admin.site.register(UserProfile)
admin.site.register(Site)
admin.site.register(Subject)
admin.site.register(Affymetrix)