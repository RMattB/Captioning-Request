from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms


class CaptioningService(models.Model):
    """
    A captioning service is both the particular turnaround time and 
    the lowest cost supplier who can provide that turnaround time.
    """
    turnaround_business_days = models.IntegerField("turnaround",
                                                   help_text="number of business days to fulfill the captioning request")
    price = models.DecimalField("price",
                                help_text="price in dollars per minute of video", 
                                max_digits=3, decimal_places=2)
    description = models.CharField("service description", max_length=128)
    name = models.CharField("service name", max_length=128)
    email = models.EmailField("email address")
    
    def __unicode__(self):
        return str(self.description)


class PublishingDestination(models.Model):
    """
    The publishing destinations are places where the captioned video will be published.
    This class is needed because different publishing destinations require different 
    formats of video files and caption files.
    """
    name = models.CharField(max_length=128)
    video_format = models.CharField(max_length=128)
    caption_format = models.CharField(max_length=128)
    publishing_instructions = models.TextField(help_text="Instructions for the user to perform.")
    
    def __unicode__(self):
        return self.name


class CaptioningRequest(models.Model):
    """
    A CaptioningRequest is the primary object of this application: 
    to request that a prerecorded video be captioned.
    """
    # We'll be using the built-in id as the captioning request number to show users.
    def __unicode__(self):
        return str(self.id) + ": " + self.video_title
    
#    todo: user relation
#    See https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#using-a-subset-of-fields-on-the-form
#    user = models.ForeignKey(User, related_name='+',blank=True, null=True)
    requester_email = models.EmailField("Your email address", blank=True, null=True)
    request_date_time = models.DateTimeField("date and time requested", auto_now_add=True)
    VIDEO_HAS_TRANSCRIPT_CHOICES = (
        ('True', 'Yes. (Captioning is *free* for 3 business day turnaround.)'),
        ('False', 'No. (Captioning is *billed*.)'),
    )
    video_has_transcript = models.BooleanField(choices=VIDEO_HAS_TRANSCRIPT_CHOICES, 
                                               help_text="Do you have a transcript for this video?", blank=True)
    video_transcript_file_URL = models.URLField(help_text="If you have a transcript, enter the URL of the video transcript file:", 
                                                blank=True)
    requester_agrees_to_billing = models.BooleanField(help_text="If you don't have a transcript, you must agree to be billed by the service provider.", 
                                                      blank=True)
    captioning_service = models.ForeignKey(CaptioningService, 
                                           verbose_name="the related captioning service", 
                                           help_text="How soon do you need this?")
    video_file_URL = models.URLField(help_text="Enter the URL of the video file:", blank=True)
    video_title = models.CharField(max_length=128, 
                                   help_text="Enter the title of this video (required).")
    video_description = models.TextField(help_text="Enter a short description of this video (lowers cost).", blank=True)
    video_speakers = models.TextField(help_text="Enter the names of speakers in the video, one per line (required).", blank=True)
    video_vocabulary = models.TextField(help_text="Enter special words or phrases, one per line (lowers cost). (Technical phrases, proper names, acronymns, other languages, etc.)", 
                                        blank=True)
    # For now, we're assuming approvers won't need to see all the videos they approved.
    other_approver_email = models.EmailField("Other approver's email address", 
                                             help_text="If someone other than you will be approving the captioning of this video, enter their email address.", 
                                             blank=True)
    publishing_destinations = models.ManyToManyField(PublishingDestination, 
                                                     verbose_name="the related publishing desintations", 
                                                     help_text="Choose the place you intend to publish the captioned video.", blank=True)
    other_notes = models.TextField(help_text="Other notes:", 
                                   blank=True)
    contact_special_request = models.BooleanField(help_text="Please contact me for special requests.", 
                                                  blank=True)
    # More computed values for future, some only used if we decide to store files locally.
#    video_file_checksum
#        video checksum hashlib.sha256().hexdigest()
#    video format
#    captioned video URL = models.CharField(max_length=2048)
#    captioned video transcript URL = models.CharField(max_length=2048, help_text="Given to user for editing and or reuse.")
#    is supplier done captioning?
#      what about whether the supplier is done?  that could be boolean, i spose
#    is approved & published?
#      this is basically a two-state workflow, so a boolean yes/no will be fine

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in CaptioningRequest._meta.fields]


# to do: try combining/reusing the admin form below for this purpose
class CaptioningRequestForm(ModelForm):
    class Meta:
        model = CaptioningRequest
        exclude = ["user"]
        # to do: needs adjustment
        yes_no = forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')])
        widgets = {'video_has_transcript': yes_no}


class AdminCaptioningRequestForm(ModelForm):
    class Meta:
        model = CaptioningRequest

