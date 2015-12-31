# Core Django imports
from django.contrib import messages
from django.shortcuts import redirect, render

# Third-party app imports

# Local app imports

###################################################
# About Page
"""
 About Page defintion
"""
def About(request):
    template = '22q11-ibbc/about.html'
    return render(request, template)


###################################################
# Announcement Page
"""
 Announcement Page defintion
"""
def Announcement(request):
    template = '22q11-ibbc/announcement.html'
    return render(request, template)


###################################################
# Contact Page
"""
 Contact Page defintion
"""
def Contact(request):
    template = '22q11-ibbc/contact.html'
    return render(request, template)


###################################################
# Home page
"""
 Home Page definition
"""
def Home(request):
    template = '22q11-ibbc/home.html'
    return render(request, template)


###################################################
# Member Site Page
"""
 Member Site Page defintion
"""
def Member_Site(request):
    template = '22q11-ibbc/member_site.html'
    return render(request, template)


###################################################
# Publication Page
"""
 Publication Page defintion
"""
def Publication(request):
    template = '22q11-ibbc/publication.html'
    return render(request, template)