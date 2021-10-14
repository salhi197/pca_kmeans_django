from django.shortcuts import render
from uploader.models import UploadForm,Upload
from django.http import HttpResponseRedirect
from django.urls import reverse
from pandas import DataFrame, read_csv
import random
from numpy import random

from django.http import JsonResponse
import pandas as pd
from re import search


# Create your views here.
def home(request):
    if request.method=="POST":
        img = UploadForm(request.POST, request.FILES)       
        if img.is_valid():
            img.save()  
            return HttpResponseRedirect(reverse('imageupload'))
    else:
        img=UploadForm()
    files=Upload.objects.all().order_by('-upload_date')
    return render(request,'home.html',{'form':img,'files':files})


def showFile(request, id): 
    file=Upload.objects.get(pk=id)
    #try to dispaly file in html table
    df = pd.read_excel(file.pic.file)
    data=   df.to_json(orient='split')
    return render(request,'acp.html',{'file':file,'data':data})


def launchElectre(request,id):
    file=Upload.objects.get(pk=id)
    df = pd.read_excel(file.pic.file)
    number_of_lines = df.shape[0]
    number_of_cols = df.shape[1]

    actions = []
    for i in range(1, number_of_lines):
        if search("PDV", str(list(df.iloc[i])[0])):
            actions.append(list(df.iloc[i])[0])


    actions.sort()
    print(actions)
    classe1 = random.choice(actions,3)
    classe2 = random.choice(actions,3)
    classe3 = random.choice(actions,3)
    classe4 = random.choice(actions,3)
    classe5 = random.choice(actions,3)

    return render(request,'electre.html',
        {
            "actions":actions,
            "classe1":classe1, 
            "classe2":classe2, 
            "classe3":classe3, 
            "classe4":classe4, 
            "classe5":classe5 
        })
    
