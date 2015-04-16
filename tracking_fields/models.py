from __future__ import unicode_literals

try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except ImportError:
    from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _, pgettext_lazy
from django.db import models

# Used for object modifications
CREATE = 'CREATE'
UPDATE = 'UPDATE'
DELETE = 'DELETE'
# Used for m2m modifications
ADD = 'ADD'
REMOVE = 'REMOVE'
CLEAR = 'CLEAR'


class TrackingEvent(models.Model):
    class Meta:
        verbose_name = _('Tracking event')
        verbose_name_plural = _('Tracking events')

    ACTIONS = (
        (CREATE, _('Create')),
        (UPDATE, _('Update')),
        (DELETE, _('Delete')),
        (ADD, _('Add')),
        (REMOVE, pgettext_lazy('Remove from something', 'Remove')),
        (CLEAR, _('Clear')),
    )
    date = models.DateTimeField(
        _("Date"), auto_now_add=True, editable=False
    )
    action = models.CharField(
        _('Action'), max_length=6, choices=ACTIONS, editable=False
    )

    object_content_type = models.ForeignKey(
        ContentType,
        related_name='tracking_object_content_type',
        editable=False
    )
    object_id = models.PositiveIntegerField(editable=False, null=True)
    object = GenericForeignKey('object_content_type', 'object_id')
    object_repr = models.CharField(
        _("Object representation"),
        help_text=_(
            "Object representation, useful if the object is deleted later."
        ),
        max_length=250,
        editable=False
    )

    user_content_type = models.ForeignKey(
        ContentType,
        related_name='tracking_user_content_type',
        editable=False,
        null=True,
    )
    user_id = models.PositiveIntegerField(editable=False, null=True)
    user = GenericForeignKey('user_content_type', 'user_id')
    user_repr = models.CharField(
        _("User representation"),
        help_text=_(
            "User representation, useful if the user is deleted later."
        ),
        max_length=250,
        editable=False
    )


class TrackedFieldModification(models.Model):
    class Meta:
        verbose_name = _('Tracking field modification')
        verbose_name_plural = _('Tracking field modifications')

    event = models.ForeignKey(
        TrackingEvent, verbose_name=_("Event"), related_name='fields',
        editable=False
    )
    field = models.CharField(_("Field"), max_length=40, editable=False)
    old_value = models.TextField(
        _("Old value"),
        help_text=_("JSON serialized"),
        null=True,
        editable=False,
    )
    new_value = models.TextField(
        _("New value"),
        help_text=_("JSON serialized"),
        null=True,
        editable=False,
    )
