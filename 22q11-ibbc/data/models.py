# Core Django imports
from django.contrib.auth.models import User
from django.db import models

# Third-party app imports

# Local app imports

######################################################################################################
##  Site
######################################################################################################
"""
 Class to hold Site information
"""
class Site(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    group = models.CharField(max_length=255, blank=True)
    folder = models.CharField(max_length=255, null=True, blank=True)
    #Relationships
    site_pis = models.ManyToManyField(User, null=False, blank=True, related_name="%(app_label)s_%(class)s_site_pis")
    site_members = models.ManyToManyField(User, blank=True, related_name="%(app_label)s_%(class)s_site_members")
    allowed_users = models.ManyToManyField(User, blank=True, related_name="%(app_label)s_%(class)s_allowed_users")

    def __unicode__(self):
        return u"""{name}""".format(
            name=self.name,
        )

    def check_site_pis(self, username):
        if self.site_pis.filter(username=username).exists():
            return True
        return False

    def check_site_members(self, username):
        if self.site_members.filter(username=username).exists():
            return True
        return False

    def check_allowed_members(self, username):
        if self.allowed_members.filter(username=username).exists():
            return True
        return False


######################################################################################################
##  User Profile
######################################################################################################
"""
 Class to hold User Role information
"""
class UserRole(models.Model):
    role = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u"""{role}""".format(
            role=self.role,
        )

"""
 Class to hold User Profile information
"""
class UserProfile(models.Model):
    #Relationships
    user = models.ForeignKey(User, null=False, related_name="%(app_label)s_%(class)s_user")
    user_roles = models.ManyToManyField(UserRole, null=False, blank=True, related_name="%(app_label)s_%(class)s_user_roles")

    def __unicode__(self):
        return u"""{name}""".format(
            name=self.user,
        )


#####################################################################################################
#  Subject
#####################################################################################################
"""
 Class to hold Subject information
"""
class Subject(models.Model):
    genomic_db_id = models.IntegerField(primary_key=True)
    site_id = models.CharField(max_length=255, null=False, blank=False)
    alias = models.CharField(max_length=255, null=True, blank=True)
    project = models.CharField(max_length=255, null=True, blank=True)
    #Relationships
    owner_site = models.ForeignKey(Site, null=False, related_name="%(app_label)s_%(class)s_owner_site")

    def __unicode__(self):
        return u"""{site_id}""".format(
            genomic_db_id=self.genomic_db_id,
        )

    def get_absolute_url(self):
        return reverse('data:subject_detail', kwargs={'pk': self.genomic_db_id})

#####################################################################################################
#  Affymetrix
#####################################################################################################
"""
 Class to hold Affymetrix information
"""
class Affymetrix(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    cel_file = models.FileField(upload_to='.')
    #Relationships
    subject = models.ForeignKey(Subject, null=False, related_name="%(app_label)s_%(class)s_subject")

    def __unicode__(self):
        return u"""{name}""".format(
            name=self.name,
        )

    def get_absolute_url(self):
        return reverse('data:affymetrix_detail', kwargs={'pk': self.id})