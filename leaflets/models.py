from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from base import util
from base.models import MediaRemovalMixin
from base.storage import OverwriteFileSystemStorage


# TODO: Remove once Python3 is required
def get_leaflet_path_global(model, name):
    return model.get_leaflet_path()


class Leaflet(MediaRemovalMixin, models.Model):
    '''
    Represents a given (generated) leaflet.
    '''

    def get_leaflet_path(self, *args):
        return "leaflets/{name}.pdf".format(name=unicode(self))

    def get_thumbnail_path(self):
        return "leaflets/thumbnails/{name}.jpg".format(name=unicode(self))

    def get_media_files(self):
        return [self.get_leaflet_path(), self.get_thumbnail_path()]

    # Define autocomplete fields for grapelli search in admin
    @staticmethod
    def autocomplete_search_fields():
        return (
            "competition__name__icontains",
            "year__iexact",
            "issue__iexact",
            )

    def __unicode__(self):
        return "{competition}-{year}-{issue}"\
               .format(competition=self.competition,
                       year=self.year,
                       issue=self.issue)

    competition = models.ForeignKey('competitions.Competition',
                                    verbose_name=_('competition'))
    year = models.IntegerField(verbose_name=_('year'))
    issue = models.IntegerField(verbose_name=_('issue'))
    leaflet = models.FileField(upload_to=get_leaflet_path_global,
                               storage=OverwriteFileSystemStorage(),
                               verbose_name=_('leaflet'))

    # Fields added via foreign keys:

    #  problemset_set

    # TODO: more than one problemset can point to given leaflet, is that a
    #       problem?

    class Meta:
        ordering = ['competition', '-year', 'issue']
        unique_together = ('competition', 'year', 'issue')
        verbose_name = _('leaflet')
        verbose_name_plural = _('leaflets')


@receiver(post_save, sender=Leaflet)
def generate_leaflet_thumbnail(sender, instance, created, **kwargs):
    source_path = instance.get_leaflet_path()
    dest_path = instance.get_thumbnail_path()

    util.generate_pdf_thumbnail(source=source_path,
                                destination=dest_path,
                                height=212,
                                width=150)
