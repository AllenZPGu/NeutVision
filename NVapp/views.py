from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Images, Scores
import json
import time
import random

def index(request):
	return render(request, 'NVapp/home.html')

@login_required
def score(request):
	fields = {"Quality":{"heading":"Image/staining quality", "buttons":["Good: nucleus visible", "Out of focus nucleus", "Nucleus not visible", "Other"], "optional":False},
		"Degree":{"heading":"Degree of segmentation", "buttons":["Unsegmented","Segmented","Hypersegmented","Unknown","Other"], "optional":False},
		"Lobe":{"heading":"Number of lobes (optional)", "buttons":["1","2","3","4","5","6", "Unknown", "Other"], "optional":True},
		"Shape":{"heading":"Nuclear shape (optional)", "buttons":["Pancake","Croissant","Donut","Unknown","Other"], "optional":True},
		}

	selectedImg = None
	n = 2
	while selectedImg == None and n > 0:
		n-= 1
		rawPossibleImgs = Images.objects.filter(count=n)
		rawPossibleImgs2 = [i for i in rawPossibleImgs]
		random.shuffle(rawPossibleImgs2)

		for posImg in rawPossibleImgs2:
			if len(Scores.objects.filter(scorer=request.user, img=posImg))==0:
				selectedImg = posImg
				break

	if selectedImg == None:
		toPass = {"neutsToScore":False}
	else:
		toPass = {"neutsToScore":True,
				"neutImagePath":"NVapp/cells/{}/{}".format(selectedImg.source, selectedImg.name,), 
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
		newScore.date = time.strftime("20%y-%m-%d")
		newScore.save()

		img.count+=1
		img.save()

		return JsonResponse({'success':True})
	else:
		return JsonResponse({'success':False})

@login_required
def history(request):
	allScores = Scores.objects.filter(scorer=request.user)
	history = []
	for score in allScores:
		scoreDict = {}
		scoreDict["Image Quality"] = score.quality
		scoreDict["Segmentation"] = score.degree
		scoreDict["Lobes"] = score.lobe if len(score.lobe)>0 else '-'
		scoreDict["Shape"] = score.shape if len(score.shape)>0 else '-'
		scoreDict["All Other Comments"] = score.allothercomments if len(score.allothercomments) > 0 else "-"
		scoreDict["Date"] = score.date.strftime("%d / %m / 20%y")
		scoreDict["Image"] = score.img.id
		history.append(scoreDict)

	columns = ["Date",
			"Image",
			"Image Quality", 
			"Segmentation", 
			"Lobes", 
			"Shape", 
			"All Other Comments",]
	imgPath = "NVapp/cells/"

	toPass = {"history":history, "columns":columns, "imgPath":imgPath, "anyHistory":bool(len(history))}
	return render(request, 'NVapp/history.html', toPass)

def examples(request):
	return render(request, 'NVapp/examples.html')

def leaderboard(request):
	allPeople = User.objects.all()
	unsortedList = []
	for person in allPeople:
		if person.username == 'gu.a':
			continue
		personDict = {}
		allScores = Scores.objects.filter(scorer=person)
		personDict['Person'] = person.username
		personDict['Total Scores'] = len(allScores)
		if len(allScores) == 0:
			continue
		personDict['Last Score Date'] = max([i.date for i in allScores]).strftime("%d / %m / 20%y")
		unsortedList.append(personDict)
	sortedList = sorted(unsortedList, key = lambda x: -x['Total Scores'])

	return render(request, 'NVapp/leaderboard.html', {'sortedList':sortedList, 'columns':['Person', 'Total Scores', 'Last Score Date']})











