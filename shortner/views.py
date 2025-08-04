from django.shortcuts import render,get_object_or_404,redirect
from .models import ShortURL,encode_base62,generate_shortcode
from .form import URLForm
from django.contrib import messages
import string
import random

# Create your views here.
def index(request):
    return render(request,'index.html')




def home(request):
    short_url=None
    if request.method=='POST':
        form=URLForm(request.POST)
        if form.is_valid():
            url=form.cleaned_data['original_url']
            existing = ShortURL.objects.filter(user=request.user, original_url=url).first()
            if existing:
                short_code=existing.short_code
                messages.info(request, "You already generated a shortcode for this URL.")
            else:
                
                short_obj=ShortURL.objects.create(user=request.user,original_url=url)
                short_obj.short_code=generate_shortcode(short_obj.id)
                short_obj.save()
                messages.success(request,"Short URL generated Successfully")
                short_code=short_obj.short_code
            short_url = request.build_absolute_uri(f'/{short_code}')
    else:
        form=URLForm()

    return render(request, 'home.html', {'form': form, 'short_url': short_url})

def redirect_url(request,short_code):
    short_url=get_object_or_404(ShortURL,short_code=short_code)
    return redirect(short_url.original_url)