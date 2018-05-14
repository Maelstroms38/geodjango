from django.shortcuts import render, render_to_response
from django.views.generic.edit import FormView
from .forms import LookupForm
from .models import Event
from django.utils import timezone
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.template.loader import render_to_string

class LookupView(FormView):
	form_class = LookupForm

	def get(self, request):
		return render(self.request, 'lookup.html')
    
	def form_valid(self, form):
		# Get data
		latitude = form.cleaned_data['latitude']
		longitude = form.cleaned_data['longitude']
		# Get today's date
		now = timezone.now()
		# Get next week's date
		next_week = now + timezone.timedelta(weeks=1)
		# Get Point
		location = Point(longitude, latitude, srid=4326)
		# Look up events
		events = Event.objects.filter(datetime__gte=now).filter(datetime__lte=next_week).annotate(distance=Distance('venue__location', location)).order_by('distance')[0:5]
		# Render the template
		return render_to_response('lookupresults.html', {
			'events': events
		})