from django.shortcuts import render
from uploader.models import UploadForm,Upload
from django.http import HttpResponseRedirect
from django.urls import reverse
from pandas import DataFrame, read_csv
from django.http import JsonResponse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import interactive
from sklearn.datasets import load_breast_cancer
from sklearn.datasets import load_wine
from sklearn.datasets import load_boston
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

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


def launchPca(request,id):
    file=Upload.objects.get(pk=id)
    df = pd.read_excel(file.pic.file)
    #cancer=load_breast_cancer()
    #data = load_wine()
    # data= load_boston()
    # df=pd.DataFrame(data['data'],columns=data['feature_names'])
    # Standardize the data to have a mean of ~0 and a variance of 1
    X_std = StandardScaler().fit_transform(df)
    # Create a PCA instance: pca
    pca = PCA(n_components=df.shape[1])
    principalComponents = pca.fit_transform(X_std)
    # Plot the explained variances
    features = range(pca.n_components_)

    # Save components to a DataFrame
    PCA_components = pd.DataFrame(principalComponents)
    ks = range(1, 8)
    inertias = []
    for k in ks:
        model = KMeans(n_clusters=k)
        model.fit(PCA_components.iloc[:,:3])
        inertias.append(model.inertia_)
    return render(request,'chart.html',{
        'file':file,
        'pca_explained_variance_ratio_':pca.explained_variance_ratio_,
        'two_pca_components':principalComponents[:,0:2],
        'inertias':inertias
        })
    
