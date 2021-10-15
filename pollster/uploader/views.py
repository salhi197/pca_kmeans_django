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

def Concordance(a, bh):
    conc = 0.0
    for critere in Criteres:
        poids = Poids[critere]
        ga = Performances[a][critere]
        gbh, qbh, pbh, vbh = Seuils[bh][critere]
        if gbh - ga >= pbh:
            conc += 0.0 * poids
        elif gbh - ga <= qbh:
            conc += 1.0 * poids
        else:
            conc += ((pbh + ga - gbh) / (pbh - qbh)) * poids
    return conc


def Concordance2(bh, a):
    conc = 0.0
    for critere in Criteres:
        poids = Poids[critere]
        ga = Performances[a][critere]
        gbh, qbh, pbh, vbh = Seuils[bh][critere]
        if ga - gbh >= 0:
            conc += 0.0 * poids
        elif ga - gbh <= 0:
            conc += 1.0 * poids
    return conc


def DiscordanceCritere(a, bh, critere):
    ga = Performances[a][critere]
    gbh, qbh, pbh, vbh = Seuils[bh][critere]
    if ga <= gbh - pbh:
        return 0.0
    elif ga > gbh + vbh:
        return 1.0
    else:
        return ((gbh + pbh) - ga) / (pbh + vbh)


def DiscordanceCritere2(bh, a, critere):
    ga = Performances[a][critere]
    gbh, qbh, pbh, vbh = Seuils[bh][critere]
    if gbh <= ga - 0:
        return 0.0
    elif gbh > ga + 0:
        return 1.0


def crédibilité(a, bh):
    mult = 1
    for critere in Criteres:
        mult = mult * ((2 - DiscordanceCritere(a, bh, critere)) / (2 - Concordance(a, bh)))
    sigma_abh = Concordance(a, bh) * mult
    return sigma_abh


def crédibilité2(bh, a):
    mult = 1
    for critere in Criteres:
        mult = mult * ((2 - DiscordanceCritere2(bh, a, critere)) / (2 - Concordance2(bh, a)))
    sigma_abh = Concordance2(bh, a) * mult
    return sigma_abh


def electretri():
    PE = []
    PD = []
    PC = []
    PB = []
    PA = []
    OE = []
    OD = []
    OC = []
    OB = []
    OA = []
    for a in Actions:
        i = 0
        z = 0
        l = 0
        p = 0
        # ['A', 'B', 'C', 'd', 'E']
        for classe in Classes[:-1]:
            if crédibilité(a, classe) >= Lambda and crédibilité2(classe, a) >= Lambda:
                l = l + 1
                if classe == 'E' and i == 0:
                    PD.append(a)
                    l = l + 1
                    i = 1
                if classe == 'D' and i == 0:
                    PC.append(a)
                    l = l + 1
                    i = 1
                if classe == 'C' and i == 0:
                    PB.append(a)
                    l = l + 1
                    i = 1
                if classe == 'B' and i == 0:
                    PA.append(a)
                    l = l + 1
                    i = 1
                if classe == 'E' and z == 0:
                    OE.append(a)
                    z = z + 1
                    l = l + 1
                if classe == 'D' and z == 0:
                    OD.append(a)
                    z = z + 1
                    l = l + 1
                if classe == 'C' and z == 0:
                    OC.append(a)
                    z = z + 1
                    l = l + 1
                if classe == 'B' and z == 0:
                    OB.append(a)
                    z = z + 1
                    l = l + 1
                if l == 5 and i == 1 and z == 0:
                    OA.append(a)
                if l == 5 and i == 0 and z == 1:
                    PE.append(a)

            elif crédibilité(a, classe) >= Lambda and crédibilité2(classe, a) < Lambda:
                l = l + 1
                if classe == 'E' and i == 0:
                    PD.append(a)
                    i = i + 1
                    l = l + 1
                if classe == 'D' and i == 0:
                    PC.append(a)
                    i = i + 1
                    l = l + 1
                if classe == 'C' and i == 0:
                    PB.append(a)
                    i = i + 1
                    l = l + 1
                if classe == 'B' and i == 0:
                    PA.append(a)
                    i = i + 1
                    l = l + 1
                if l == 5:
                    OA.append(a)
            elif crédibilité(a, classe) < Lambda and crédibilité2(classe, a) >= Lambda:
                l = l + 1
                if classe == 'E' and z == 0:
                    OE.append(a)
                    z = z + 1
                    l = l + 1
                if classe == 'D' and z == 0:
                    OD.append(a)
                    z = z + 1
                    l = l + 1
                if classe == 'C' and z == 0:
                    OC.append(a)
                    z = z + 1
                    l = l + 1
                if classe == 'B' and z == 0:
                    OB.append(a)
                    z = z + 1
                    l = l + 1
                if l == 5:
                    PE.append(a)
            elif crédibilité(a, classe) < Lambda and crédibilité2(classe, a) < Lambda:

                if (i == 0 and z == 0) or (z == 1 and i == 1) and p == 0:
                    OA.append(a)
                    PE.append(a)
                    z = z + 1
                    i = i + 1
                    p = p + 1
                if i == 1 and z == 0 and p == 0:
                    OA.append(a)
                    z = z + 1
                if i == 0 and z == 1 and p == 0:
                    PE.append(a)
                    i = i + 1

    resulta = [PE, PD, PC, PB, PA, OE, OD, OC, OB, OA]
    return resulta

def launchElectre(request,id):
    file=Upload.objects.get(pk=id)
    df = pd.read_excel(file.pic.file)

    Classes = ['E', 'D', 'C', 'B', 'A']

    lenclasses = len(Classes)
    minus = lenclasses+3
    dimensions = df.shape
    x=dimensions[0]

    Poids=(df.iloc[-1]).to_dict()
    Poids.pop('Alternative')

    Criteres = list(Poids.keys())

    first_column = (df.iloc[:, 0]).to_dict()
    values = first_column.values()
    values_list = list(values)
    Actions = []
    for i in range(0,dimensions[0]-minus):
        Actions.append(values_list[i])

    per = (df.iloc[:dimensions[0]-minus, 1:]).to_dict('records')
    print(per)
    Performances = {}
    for i in range(0,len(Actions)):
        Performances[Actions[i]] = per[i]


    Seuils = {
        # seuils (g,q,p,v) de Bon Ã  Moyen
        'E': {
            'Spend': (45, 20, 10, 50),
            'Activation': (60000, 20000, 10000, 50000),
            'Rechargement': (3000, 1000, 500, 3000),
            'Potenciel': (60, 20, 10, 50),
            'Stock initial': (30, 20, 10, 500)},
        'D': {
            'Spend': (70, 20, 10, 50),
            'Activation': (90000, 20000, 10000, 50000),
            'Rechargement': (5000, 1000, 500, 3000),
            'Potenciel': (80, 20, 10, 50),
            'Stock initial': (55, 20, 10, 500)},
        'C': {
            'Spend': (100, 20, 10, 50),
            'Activation': (120000, 20000, 10000, 50000),
            'Rechargement': (130000, 1000, 500, 3000),
            'Potenciel': (130, 20, 10, 50),
            'Stock initial': (85, 20, 10, 500)},
        'B': {
            'Spend': (500, 20, 10, 50),
            'Activation': (128000, 20000, 10000, 50000),
            'Rechargement': (200000, 1000, 500, 3000),
            'Potenciel': (520, 20, 10, 50),
            'Stock initial': (480, 20, 10, 500)},

    }


    Lambda = 0.75

    for classe in Classes[:-1]:
        resulta = electretri()

    print('\n\n****************optimiste******************')
    print('\n', resulta[0], 'E\n', resulta[1], 'D\n', resulta[2], 'C\n', resulta[3], 'B\n', resulta[4], 'A\n')
    print('****************optimiste******************\n\n\n\n\n')
    print('****************pessimiste******************')
    print('\n', resulta[5], 'E\n', resulta[6], 'D\n', resulta[7], 'C\n', resulta[8], 'B\n', resulta[9], 'A\n')
    print('****************pessimiste******************')

    return render(request,'electre.html')
    
