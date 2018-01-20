
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.gis.db import models as geomodels

from .bases import GDSEModel


class CaseStudy(GDSEModel):
    name = models.TextField()
    geom = geomodels.MultiPolygonField(null=True)
    focusarea = geomodels.MultiPolygonField(null=True)

    @property
    def solution_categories(self):
        """
        look for all solution categories created by the users of the casestudy
        """
        solution_categories = set()
        for uic in self.userincasestudy_set.all():
            for solution_category in uic.solutioncategory_set.all():
                solution_categories.add(solution_category)
        return solution_categories

    @property
    def stakeholder_categories(self):
        """
        look for all stakeholder categories created by the users of the casestudy
        """
        stakeholder_categories = set()
        for uic in self.userincasestudy_set.all():
            for stakeholder_category in uic.stakeholdercategory_set.all():
                stakeholder_categories.add(stakeholder_category)
        return stakeholder_categories

    @property
    def implementations(self):
        """
        look for all stakeholder categories created by the users of the casestudy
        """
        implementations = set()
        for uic in self.userincasestudy_set.all():
            for implementation in uic.implementation_set.all():
                implementations.add(implementation)
        return implementations


class Profile(GDSEModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    casestudies = models.ManyToManyField(CaseStudy, through='UserInCasestudy')
    organization = models.TextField(default='', blank=True)

    @property
    def name(self):
        return self.user.username

    def get_casestudies(self):
        return "\n".join([c.name for c in self.casestudies.all()])


@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, created, instance, **kwargs):
    if created:
        try:
            instance.profile
        except Profile.DoesNotExist:
            profile = Profile(id=instance.id, user=instance)
            profile.save()
        else:
            print(instance.profile)


class UserInCasestudy(GDSEModel):
    user = models.ForeignKey(Profile)
    casestudy = models.ForeignKey(CaseStudy)
    role = models.TextField(default='', blank=True)

    @property
    def name(self):
        return self.user.name

    def __str__(self):
        text = '{u} ({c})'
        return text.format(u=self.user, c=self.casestudy,)