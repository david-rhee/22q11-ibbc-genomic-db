# Core Django imports
from django import forms
from django.forms import Form, ModelForm
from django.core.exceptions import ObjectDoesNotExist

# Third-party app imports

# Local app imports
from .models import Site

#####################################################################################################
#  Subject
"""
Class to hold SubjectListForm information
"""
class SubjectListForm(Form):
    genomic_db_id = forms.CharField(max_length=255, required=False)
    local_id = forms.CharField(max_length=255, required=False)
    alias = forms.CharField(max_length=255, required=False)
    site = forms.ChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        super(SubjectListForm, self).__init__(*args, **kwargs)

        self.fields['genomic_db_id'].initial = '0'
        self.fields['local_id'].initial = 'all'
        self.fields['alias'].initial = 'all'

        sites = Site.objects.values_list('id', 'name').order_by('name').distinct('name')
        site_choices = []
        site_choices.insert(0, ('all', 'all'))
        for site in sites:
            site_choices.append([site[0], site[1]])
        self.fields['site'].choices = site_choices

#####################################################################################################
#  Affymetrix
"""
Class to hold AffymetrixListForm information
"""
class AffymetrixListForm(Form):
    affymetrix_name = forms.CharField(max_length=255, required=False)

    def __init__(self, *args, **kwargs):
        super(AffymetrixListForm, self).__init__(*args, **kwargs)

        self.fields['affymetrix_name'].initial = 'all'