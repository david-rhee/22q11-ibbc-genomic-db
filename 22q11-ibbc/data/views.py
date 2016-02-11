# Python

# Core Django imports
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse
from django.shortcuts import redirect, render
from django.views.generic import DetailView, UpdateView, DeleteView, ListView

# Third-party app imports
from braces.views import LoginRequiredMixin

# Local app imports
from .models import Site, UserProfile, Subject, Affymetrix
from .forms import SubjectListForm, AffymetrixListForm
from utilities.utilities import get_item, split

#####################################################################################################
# Password Reset
"""
 Password Reset page.
"""
def reset(request):
    return password_reset(request, template_name='data/data_password_reset_form.html',
        email_template_name='data/data_password_reset_email.html',
        post_reset_redirect=reverse('data:22q11_ibbc_login'))

"""
 Password Reset change page.
"""
def reset_confirm(request, uidb64=None, token=None):
    return password_reset_confirm(request, template_name='data/data_password_reset_confirm.html',
        uidb64=uidb64, token=token, post_reset_redirect=reverse('data:reset_complete'))

"""
 Password Reset change complete page.
"""
def reset_complete(request):
    template = 'data/data_password_reset_complete.html'
    return render(request, template)


#####################################################################################################
# Home page
"""
 Home Page definition
"""
@login_required(login_url='data:22q11_ibbc_login')
def home(request):
    sites = Site.objects.all().order_by('name').exclude(name='Database').exclude(name='Genomics')
    
    subjects = {}
    for site in sites:
        subjects[site.name] = Subject.objects.all().filter(owner_site=site).count()

    affymetrixes = {}
    for site in sites:
        affymetrixes[site.name] = Affymetrix.objects.all().filter(subject__owner_site__id__exact=site.id).count()

    template = 'data/data_home.html'

    return render(request, template, {'sites': sites, 'subjects': subjects, 'affymetrixes': affymetrixes})


#####################################################################################################
#  Site
"""
 Site detail page.
"""
@login_required(login_url='data:22q11_ibbc_login')
def site_detail_view(request, **kwargs):
    site = Site.objects.get(id=kwargs['pk'])

    subjects = {}
    subjects[site.name] = Subject.objects.all().filter(owner_site=site).count()

    affymetrixes = {}
    affymetrixes[site.name] = Affymetrix.objects.all().filter(subject__owner_site__id__exact=site.id).count()

    template = 'data/data_site_detail.html'
    
    return render(request, template, {'site': site, 'subjects': subjects, 'affymetrixes': affymetrixes,})

#####################################################################################################
#  Affymetrix Folder
"""
 Download for Affymetrix Folder.
"""
@login_required(login_url='data:22q11_ibbc_login')
def affymetrix_folder_download(request, file_name, site_pk):
    flag = False    
    site = Site.objects.get(id=site_pk)

    # if user is one of PIs of owner site
    if site.site_pis.all().filter(username=request.user.username):
        flag = True
    # if user is one of members of owner site
    elif site.site_members.all().filter(username=request.user.username):
        flag = True
    # if user belongs to allowed users
    elif site.allowed_users.all().filter(username=request.user.username):
        flag = True

    if flag == True:
        response = HttpResponse(content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=%s' % (file_name, )
        response['X-Accel-Redirect'] = '/affymetrix_folder/%s' % (file_name, )    
        return response
 
    messages.error(request, 'You do NOT have permission to download, please contact the PI to gain access')
    return redirect('data:home')

#####################################################################################################
#  UserProfile
"""
 DetailView for UserProfile.
"""
class UserProfile_DetailView(DetailView, LoginRequiredMixin):
    model = UserProfile
    template_name = 'data/data_user_profile_detail.html'


#####################################################################################################
#  Subject
"""
 ListView for Subject.
"""
class Subject_all_ListView(ListView, LoginRequiredMixin):
    model = Subject
    template_name = 'data/data_subject_list_all.html'
    
    paginate_by = 25
    
    def get_queryset(self):
        queryset = Subject.objects.all().order_by('genomic_db_id')
        return queryset

"""
 Search for ListView for Subject.
"""
@login_required(login_url='data:22q11_ibbc_login')
def subject_search_view(request):
    if request.method == 'POST': # If the form has been submitted...
        form = SubjectListForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            genomic_db_id = form.cleaned_data['genomic_db_id']
            local_id = form.cleaned_data['local_id']
            alias = form.cleaned_data['alias']
            site = form.cleaned_data['site']
            return redirect(reverse('data:subject_search_list', kwargs={'g' : genomic_db_id, 'l' : local_id, 'a' : alias, 's' : site}))

        else :
            messages.error(request, 'Error. Please try again.')            

    form = SubjectListForm() # An unbound form
    template_name = 'data/data_subject_list_form_search.html'
    return render(request, template_name, {'form': form,})

"""
 ListView for Subject.
"""
class Subject_search_ListView(ListView, LoginRequiredMixin):
    model = Subject
    template_name = 'data/data_subject_list_search.html'
    
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super(Subject_search_ListView, self).get_context_data(**kwargs)
        context['g'] = self.kwargs['g']
        context['l'] = self.kwargs['l']
        context['a'] = self.kwargs['a']
        context['s'] = self.kwargs['s']
        return context

    def get_queryset(self):
        # set genomic id filter
        if self.kwargs['g'] == '0' :
            subjects_genomic_db_id = Subject.objects.all()
        else :
            subjects_genomic_db_id = Subject.objects.filter(genomic_db_id=int(self.kwargs['g']))

        # set site id filter
        if self.kwargs['l'] == 'all' :
            subjects_local_id = Subject.objects.all()
        else :
            subjects_local_id = Subject.objects.filter(site_id__icontains=self.kwargs['l'])

        # set alias filter
        if self.kwargs['a'] == 'all' :
            subjects_alias = Subject.objects.all()
        else :
            subjects_alias = Subject.objects.filter(alias__icontains=self.kwargs['a'])

        # set site filter
        if self.kwargs['s'] == 'all' :
            subjects_site = Subject.objects.all()
        else :
            subjects_site = Subject.objects.filter(owner_site__id__icontains=self.kwargs['s'])

        return subjects_genomic_db_id & subjects_local_id & subjects_alias & subjects_site

"""
 ListView for Subjects (For a particular site).
"""
class Subject_site_ListView(ListView, LoginRequiredMixin):
    model = Subject
    template_name = 'data/data_subject_list_site.html'
    
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super(Subject_site_ListView, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context

    def get_queryset(self, **kwargs):
        queryset = Subject.objects.all().filter(owner_site__id__exact=self.kwargs['pk']).order_by('genomic_db_id')
        return queryset

"""
 DetailView for Subject.
"""
class Subject_DetailView(DetailView, LoginRequiredMixin):
    model = Subject
    template_name = 'data/data_subject_detail.html'

    def get_context_data(self, **kwargs):
        context = super(Subject_DetailView, self).get_context_data(**kwargs) # Call the base implementation first to get a context
        context['affymetrixes'] = Affymetrix.objects.all().filter(subject__genomic_db_id__exact=self.object.genomic_db_id) # Add in the affymetrix
        return context


#####################################################################################################
#  Affymetrix
"""
 ListView for Affymetrix.
"""
class Affymetrix_all_ListView(ListView, LoginRequiredMixin):
    model = Affymetrix
    template_name = 'data/data_affymetrix_list_all.html'

    paginate_by = 25
    
    def get_queryset(self):
        queryset = Affymetrix.objects.all().order_by('name')
        return queryset

"""
 Search for ListView for Affymetrix.
"""
@login_required(login_url='data:22q11_ibbc_login')
def affymetrix_search_view(request):
    if request.method == 'POST': # If the form has been submitted...
        form = AffymetrixListForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            affymetrix_name = form.cleaned_data['affymetrix_name']
            return redirect(reverse('data:affymetrix_search_list', kwargs={'a' : affymetrix_name,}))

        else :
            messages.error(request, 'Error. Please try again.')            

    form = AffymetrixListForm() # An unbound form
    template_name = 'data/data_affymetrix_list_form_search.html'
    return render(request, template_name, {'form': form,})

"""
 ListView for Affymetrix.
"""
class Affymetrix_search_ListView(ListView, LoginRequiredMixin):
    model = Affymetrix
    template_name = 'data/data_affymetrix_list_search.html'

    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super(Affymetrix_search_ListView, self).get_context_data(**kwargs)
        context['a'] = self.kwargs['a']
        return context

    def get_queryset(self):
        # set name filter
        if self.kwargs['a'] == 'all' :
            return Affymetrix.objects.all()
        else :
            return Affymetrix.objects.filter(name__icontains=self.kwargs['a'])

"""
 ListView for Affymetrix (For a particular site).
"""
class Affymetrix_site_ListView(ListView, LoginRequiredMixin):
    model = Affymetrix
    template_name = 'data/data_affymetrix_list_site.html'

    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super(Affymetrix_site_ListView, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context

    def get_queryset(self, **kwargs):
        queryset = Affymetrix.objects.all().filter(subject__owner_site__id__exact=self.kwargs['pk']).order_by('name')
        return queryset

"""
 DetailView for Affymetrix.
"""
class Affymetrix_DetailView(DetailView, LoginRequiredMixin):
    model = Affymetrix
    template_name = 'data/data_affymetrix_detail.html'

"""
 Download for Affymetrix.
"""
@login_required(login_url='data:22q11_ibbc_login')
def affymetrix_download(request, **kwargs):
    flag = False    
    affymetrix = Affymetrix.objects.get(id=kwargs['pk'])

    # if user is one of PIs of owner site
    if affymetrix.subject.owner_site.site_pis.all().filter(username=request.user.username):
        flag = True
    # if user is one of members of owner site
    elif affymetrix.subject.owner_site.site_members.all().filter(username=request.user.username):
        flag = True
    # if user belongs to allowed users
    elif affymetrix.subject.owner_site.allowed_users.all().filter(username=request.user.username):
        flag = True

    if flag == True:
        cel_file = affymetrix.cel_file.name.split('/')[-1]
        response = StreamingHttpResponse(affymetrix.cel_file, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=%s' % cel_file
        return response
 
    messages.error(request, 'You do NOT have permission to download, please contact the PI to gain access')
    return redirect('data:home')

#####################################################################################################
# WGS
"""
 WGS definition
"""
@login_required(login_url='data:22q11_ibbc_login')
def wgs(request):
    template = 'data/data_wgs.html'
    return render(request, template)

"""
 Download for WGS.
"""
@login_required(login_url='data:22q11_ibbc_login')
def wgs_download(request, file_name):
    response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % (file_name, )
    response['X-Accel-Redirect'] = '/wgs/%s' % (file_name, )    
    return response


###################################################
# Documents
"""
 Documents 1 definition
"""
@login_required(login_url='data:22q11_ibbc_login')
def Documents_1(request):
    template = 'data/data_documents_1.html'
    return render(request, template)

"""
 Documents 2 definition
"""
@login_required(login_url='data:22q11_ibbc_login')
def Documents_2(request):
    template = 'data/data_documents_2.html'
    return render(request, template)

"""
 Documents 3 definition
"""
@login_required(login_url='data:22q11_ibbc_login')
def Documents_3(request):
    template = 'data/data_documents_3.html'
    return render(request, template)

"""
 Documents 4 definition
"""
@login_required(login_url='data:22q11_ibbc_login')
def Documents_4(request):
    template = 'data/data_documents_4.html'
    return render(request, template)

"""
 Documents 5 definition
"""
@login_required(login_url='data:22q11_ibbc_login')
def Documents_5(request):
    template = 'data/data_documents_5.html'
    return render(request, template)


###################################################
# Log in and out Pages
"""
 Logout
"""
@login_required(login_url='data:22q11_ibbc_login')
def logout_view(request):
    logout(request)
    messages.success(request, 'You are successfully logged out!')
    return redirect('data:home')