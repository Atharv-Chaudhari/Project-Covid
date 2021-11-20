from django.shortcuts import render,HttpResponse

# Create your views here.
def index(request):
    return render(request,'index.html')

def riskpredictor(request):
    return render(request,'riskpredictor.html')