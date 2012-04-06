from django.shortcuts import render_to_response
from captioning_request.models import *
from django.contrib.auth.decorators import login_required
from django.forms.models import modelform_factory
from django.template import RequestContext
from django.core import serializers
from django.http import Http404
# to do: tests

@login_required
def index(request):
    CaptioningRequestForm = modelform_factory(CaptioningRequest)
    form = CaptioningRequestForm()
    return render_to_response('captioning-request/index.html', 
                              {
                               'form': form,
                              }, 
                              context_instance=RequestContext(request)
                            )

@login_required
def my_requests(request):
    thanks_message = ''
    error_message = ''
    # If this is a post of a new captioning request, save the new captioning request first
    if request.method == 'POST':
        captioning_request_model_instance = CaptioningRequest()
        # For django docs, make an illustration of this
        captioning_request_form_instance = CaptioningRequestForm(request.POST, 
                                                       instance=captioning_request_model_instance)
        error_message = captioning_request_form_instance.errors
        if captioning_request_form_instance.is_valid():
            thanks_message = "Thank you for your captioning request. You can now see it in the list of captioning requests below."
            saved_captioning_request = captioning_request_form_instance.save(commit=False)
            saved_captioning_request.user = request.user
            saved_captioning_request.requester_email = request.user.username + "@site.com"
            saved_captioning_request.save()
            captioning_request_form_instance.save_m2m()
    # Then show all of the captioning requests
    # to do: use request.user
    user_captioning_requests = CaptioningRequest.objects.all().order_by('-request_date_time')[:200]
    return render_to_response('captioning-request/my-requests.html', 
                              {
                                'user_captioning_requests': user_captioning_requests, 
                                'user': request.user, 
                                'thanks_message': thanks_message, 
                                'error_message': error_message, 
                              } 
                             )

@login_required
def detail(request, captioning_request_id):
    try:
        captioning_request = CaptioningRequest.objects.get(pk=captioning_request_id)
    except CaptioningRequest.DoesNotExist:
        raise Http404
    return render_to_response('captioning-request/detail.html', 
                              {
                               'captioning_request': captioning_request, 
                              }
                             )
