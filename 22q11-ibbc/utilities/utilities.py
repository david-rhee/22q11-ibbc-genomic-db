# Core Django imports
from django.template.defaulttags import register

# Third-party app imports

# Local app imports

#####################################################################################################
# For string concat
@register.filter
def addstr(arg1, arg2):
    return str(arg1) + str(arg2)

#####################################################################################################
# For 
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

#####################################################################################################
# For
@register.filter
def split(value, arg):
    return value.split(arg)