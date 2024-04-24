from django.http import HttpResponseNotFound
from django.shortcuts import render
from ml_models.ml_model import ExecuteJobLib
def index(request):
    return render(request, 'index.html')

def form(request):
    if request.method == 'POST':
        companyName = request.POST.get('companyName')
        fundingRounds = request.POST.get('fundingRounds')
        fundingTotalUSD = request.POST.get('fundingTotalUSD')
        fundingPeriodYear = request.POST.get('fundingPeriodYear')
        businessDomain = request.POST.get('businessDomain')
        print(fundingRounds)
        print(fundingPeriodYear)
        print(fundingTotalUSD)
        print(businessDomain)
        prediction = ExecuteJobLib(fundingRounds, fundingPeriodYear, fundingTotalUSD, businessDomain)
        
        context = {}
        context['prediction'] = prediction
        return render(request, 'pred.html', context)
    return render(request, 'form.html')
  
