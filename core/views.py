from django.shortcuts import render

def home(request):
    """
    Public home page - accessible to everyone
    Shows features, chatbot, and insurance predictor
    """
    context = {
        'page': 'home',
    }
    return render(request, 'core/home.html', context)