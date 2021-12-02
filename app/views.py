from django.shortcuts import render,HttpResponse
print("##################################################################################################################################################################################################################")
# Create your views here.
def index(request):
    if request.method == 'POST':
        return render(request,'results.html')
    else:
        return render(request,'index.html')

def riskpredictor(request):
    return render(request,'riskpredictor.html')

def about(request):
    return render(request,'about.html')

def loading(request):
    return render(request,'loading.html')
    
def results(request):
    return render(request,'results.html')

def contact(request):
    return render(request,'contact.html')

def vaccine(request):
    if('message_frm' in request.POST):
        print("I got it")
    else:
        return render(request,'vaccine.html')