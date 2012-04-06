from captioning_request.models import *
from django.contrib import admin


class CaptioningServiceAdmin(admin.ModelAdmin):
    list_display = ['turnaround_business_days', 'price', 'description', 'name', 'email']

admin.site.register(CaptioningService, CaptioningServiceAdmin)


class PublishingDestinationAdmin(admin.ModelAdmin):
    list_display = ['name', 'video_format', 'caption_format']

admin.site.register(PublishingDestination, PublishingDestinationAdmin)


class CaptioningRequestAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Lower cost with a transcript', {'fields': ['video_has_transcript', 
                                                     'video_transcript_file_URL', 
                                                     'requester_agrees_to_billing']}),
        ('Speed vs. cost (estimated)', {'fields': ['captioning_service']}),
        ('Upload video file', {'fields': ['video_file_URL']}),
        ('About this video content', {'fields': ['video_title', 
                                                 'video_description', 
                                                 'video_speakers', 
                                                 'video_vocabulary', 
                                                 'other_approver_email']}),
        ('Publishing destination', {'fields': ['publishing_destinations', 
                                               'other_notes', 
                                               'contact_special_request']}),
    ]
    form = AdminCaptioningRequestForm
    date_hierarchy = 'request_date_time'
    # to do
    # search_fields = ['requester']

admin.site.register(CaptioningRequest, CaptioningRequestAdmin)
