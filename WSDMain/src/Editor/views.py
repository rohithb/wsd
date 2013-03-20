# Create your views here.


from django.shortcuts import render_to_response


def editor(request):

    return render_to_response('index.html')