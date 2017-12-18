from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import PageOneForm
from .utility import ml_algo, pred2, get_disease_info, get_names, getListFromString,  get_hospital_address
import numpy as np


def page_one(request):
	listlabel =[]
	if request.method == 'POST':		
		form = PageOneForm(request.POST)
		if form.is_valid():
			fever = int(request.POST.get('radio-set-1'))
			hyper = int(request.POST.get('radio-set-2'))
			lesio = int(request.POST.get('radio-set-3'))
			conju = int(request.POST.get('radio-set-4'))
			respi = int(request.POST.get('radio-set-5'))
			skin = int(request.POST.get('radio-set-6'))
			consti = int(request.POST.get('radio-set-7'))
			diarr = int(request.POST.get('radio-set-8'))
			cns = int(request.POST.get('radio-set-8'))
			wasting = int(request.POST.get('radio-set-10'))
			abort = int(request.POST.get('radio-set-11'))
			a = np.array([fever,hyper,lesio,conju,respi,skin,consti,diarr,cns,wasting,abort]).reshape(1,-1)
			pre1= ml_algo(a)

			for i in range(9):
				value = request.POST.get('chk'+str(i))
				if value is not None:
					listlabel.append(int(value))
			listlabel = list(set(listlabel))

			listString = form.cleaned_data['other_symptoms']
			other_symptoms = getListFromString(listString)
			pre2 = pred2(other_symptoms)

			if pre1 == 0:
				resa = get_disease_info(pre2[0])
			else:
				resa = get_disease_info(pre1)

			resb = get_names(listlabel)
			
			return render(request, 'page_two.html', {"disease":resa['name'], "desc":resa['description'],
			"steps":resa['steps'], "cont":resa['contacts'], "samples":resa['samples'], "tests":resa['tests'],
			"how_to_diagnose":resa['how_to_diagnose'], "resb":resb})
	else:
		form = PageOneForm()
	return render(request, 'page_one.html', {'form': form })

@csrf_exempt
def ajax_request(request):
    if request.method == 'POST' and request.is_ajax():
    	response_data = {}
    	if request.POST.get('user_address') == "":
    		response_data['header'] = "Address not selected!!!"
    		response_data['hospital'] = ""
    		response_data['phone'] = ""
	    	response_data['address'] = ""
	    	response_data['state'] = ""
	    	response_data['longitude'] = ""
	    	response_data['latitude'] = ""
    	else:
    		res = get_hospital_address(request.POST.get('user_address'))
    		response_data['header'] = "Nearest Vetenary Hospital"
    		response_data['hospital'] = res['hospital_name']
    		response_data['phone'] = res['phone_no']
	    	response_data['address'] = res['address']
	    	response_data['state'] = res['state']
	    	response_data['longitude'] = res['longitude']
	    	response_data['latitude'] = res['latitude']

    	return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
    	return render_to_response("page_two.html", locals())