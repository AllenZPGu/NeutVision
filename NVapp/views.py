from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Images, Scores
import json
import random

def index(request):
	return render(request, 'NVapp/home.html')

@login_required
def score(request):
	fields = {"Quality":{"heading":"Image/staining quality", "buttons":["Good: nucleus visible","Poor: nucleus not visible","Poor staining","Other"]},
		"Degree":{"heading":"Degree of segmentation", "buttons":["Unsegmented","Segmented","Hypersegmented","Unknown","Other"]},
		"Lobe":{"heading":"Number of lobes", "buttons":["1","2","3","4","5","6", "Unknown", "Other"]},
		"Shape":{"heading":"Nuclear shape", "buttons":["Pancake","Croissant","Donut","Unknown","Other"]},
		}

	selectedImg = None
	possibleImgs = Images.objects.filter(count__lt=2)
	
	for posImg in possibleImgs:
		if len(Scores.objects.filter(scorer=request.user, img=posImg))==0:
			selectedImg = posImg
			break

	if selectedImg == None:
		toPass = {"neutsToScore":False}
	else:
		toPass = {"neutsToScore":True,
				"neutImagePath":"NVapp/cells/%s"%selectedImg.name, 
				"neutImageName":selectedImg.name,
				"myData":json.dumps(fields)}

	return render(request, 'NVapp/score.html', toPass)

def submit_score(request):
	if request.method == "POST":
		results = request.POST
		
		img = Images.objects.filter(name=results["Image"])[0]

		newScore = Scores()
		newScore.scorer = request.user
		newScore.img = img
		newScore.quality = results["Quality"]
		newScore.degree = results["Degree"]
		newScore.lobe = results["Lobe"]
		newScore.shape = results["Shape"]
		newScore.allothercomments = results["AllOtherComments"]
		newScore.save()

		img.count+=1
		img.save()

		return JsonResponse({'success':True})
	else:
		return JsonResponse({'success':False})

def history(request):
	return render(request, 'NVapp/home.html')