from django.shortcuts import render

# Create your views here.

from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from django.http import FileResponse, Http404
from collections import Iterable

# Create your views here.
import sys
from simulation.form import  CreateUserForm 
from .models import * 


# @unauthenticated_user
def registrationPage(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, 'Account was created for ' + username)
			return redirect('login')
	context = {'form':form}
	return render(request, 'accounts/registration.html', context)

# @unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request,'Username or password is incorrect')
    context = {}            
    return render(request,'accounts/login.html')  

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url = 'login')    
def home(request):
    return render(request,'accounts/home.html')



                ############################################################################
                #                            LA GESTION DES ALERTE                         #
                ############################################################################    



@login_required(login_url = 'login')        
def cate(request): 
    cat= Categorie.objects.all()
    context={
            "categorie":cat
          }
    return render(request,'alerte/cate.html', context)


@login_required(login_url = 'login')    
def vitess_p(request): #1
    categorie = ''
    vp= VitessePropagation.objects.all()
    if request.method == 'POST':
        categorie = request.POST.get('categorie')
    request.session['categorie'] = categorie       
    context={
        "vitessePropagation":vp }
    return render(request,'alerte/vitessepropa.html', context)


@login_required(login_url = 'login')    
def frequence(request): #2
    vitesspro =''
    fr= Frequence.objects.all()
    if request.method == 'POST':
        vitesspro = request.POST.get('vitessePropagation')
    request.session['vitesspro'] = vitesspro 
    context={
        "frequence":fr }
    return render(request,'alerte/frequence.html', context)


@login_required(login_url = 'login')    
def profondeur(request):#3
    frequence = ''
    pro= Profondeur.objects.all()
    if request.method == 'POST':
        frequence = request.POST.get('frequence')
    request.session['frequence'] = frequence       
    context={
        'profondeur':pro,
    }
    return render(request,'alerte/profondeur.html', context)


@login_required(login_url = 'login')    
def niveauControle(request):#4
    profondeur = '' 
    nc= NiveauControle.objects.all()
    if request.method == 'POST':
        profondeur = request.POST.get('profondeur')
    request.session['profondeur'] = profondeur       
    context={
        'niveauControle':nc
            }
    return render(request,'alerte/nivocontrol.html', context)

@login_required(login_url = 'login')    
def niveauPerte(request):
    nivocnt = ''
    np= NiveauPerte.objects.all()
    if request.method == 'POST':
        nivocnt = request.POST.get('niveauControle')
    request.session['nivocnt'] = nivocnt       
    context={
        'niveauPerte':np
    }
    return render(request,'alerte/nivoperte.html', context)


# def flatten(lis):
#      for item in lis:
#          if isinstance(item, Iterable) and not isinstance(item, str):
#              for x in flatten(item):
#                  yield x
#          else:        
#              yield item


@login_required(login_url = 'login')    
def simulation(request):
    filename = '' 
    nivoperte = '' 
    recup_data, data, data2 = [],[],[]
    if request.method == 'POST':
        nivoperte  = request.POST.get('niveauPerte')

        request.session['nivoperte'] = nivoperte   
    categorie  = request.session.get('categorie', None)            
    vitesspro  = request.session.get('vitesspro', None)            
    frequence  = request.session.get('frequence', None)            
    profondeur  = request.session.get('profondeur', None)            
    nivocnt  = request.session.get('nivocnt', None)            
    nivoperte  = request.session.get('nivoperte', None)   

    data.append(categorie)
    data.append(vitesspro)
    data.append(frequence)
    data.append(profondeur)
    data.append(nivocnt)
    data.append(nivoperte)

    sanit1 = ['Crise ou Catastrophe Sanitaire' , 'Maitris??e' , 'R??currente', 'Locale', 'Sous Contr??le' , 'Pas de perte Humaine']
    sanit2 = ['Crise ou Catastrophe Sanitaire' , 'Maitris??e' , 'R??currente', 'Nationale', 'Sous Contr??le' , 'Pas de perte Humaine']
    sanit3 = ['Crise ou Catastrophe Sanitaire' , 'Maitris??e' , 'Non r??currente', 'Locale', 'Sous Contr??le' , 'Pas de perte Humaine']
    sanit4 = ['Crise ou Catastrophe Sanitaire' , 'Maitris??e' , 'Non r??currente', 'Nationale', 'Sous Contr??le' , 'Pas de perte Humaine']
    sanit5 = ['Crise ou Catastrophe Sanitaire' , 'Lente' , 'R??currente', 'Locale', 'Sous Contr??le' , 'Pas de perte Humaine']
    sanit6 = ['Crise ou Catastrophe Sanitaire' , 'Lente' , 'R??currente', 'Locale', 'Hors Contr??le' , 'Perte humaine']
    sanit7 = ['Crise ou Catastrophe Sanitaire' , 'Lente' , 'R??currente', 'Nationale', 'Sous Contr??le' , 'Pas de perte Humaine']
    sanit8 = ['Crise ou Catastrophe Sanitaire' , 'Lente' , 'R??currente', 'Nationale', 'Hors Contr??le' , 'Perte humaine']
    sanit9 = ['Crise ou Catastrophe Sanitaire' , 'Lente' , 'Non r??currente', 'Locale', 'Sous Contr??le' , 'Pas de perte Humaine']
    sanit10= ['Crise ou Catastrophe Sanitaire' , 'Lente' , 'Non r??currente', 'Locale', 'Hors Contr??le' , 'Perte humaine']
    sanit11= ['Crise ou Catastrophe Sanitaire' , 'Lente' , 'Non r??currente', 'Nationale', 'Sous Contr??le' , 'Pas de perte Humaine']
    sanit12= ['Crise ou Catastrophe Sanitaire' , 'Lente' , 'Non r??currente', 'Nationale', 'Hors Contr??le' , 'Perte humaine']
    sanit13= ['Crise ou Catastrophe Sanitaire', 'Rapide', 'R??currente' , 'Locale' , 'Sous Contr??le', 'Pas de perte Humaine']
    sanit14= ['Crise ou Catastrophe Sanitaire', 'Rapide', 'R??currente' , 'Locale' , 'Hors Contr??le', 'Perte humaine']
    sanit15= ['Crise ou Catastrophe Sanitaire', 'Rapide', 'R??currente' , 'Nationale' , 'Sous Contr??le', 'Pas de perte Humaine']
    sanit16= ['Crise ou Catastrophe Sanitaire', 'Rapide', 'R??currente' , 'Nationale' , 'Hors Contr??le', 'Perte humaine']
    sanit17= ['Crise ou Catastrophe Sanitaire', 'Rapide', 'Non r??currente' , 'Locale' , 'Sous Contr??le', 'Pas de perte Humaine']
    sanit18= ['Crise ou Catastrophe Sanitaire', 'Rapide', 'Non r??currente' , 'Locale' , 'Hors Contr??le', 'Perte humaine']
    sanit19= ['Crise ou Catastrophe Sanitaire', 'Rapide', 'Non r??currente' , 'Nationale' , 'Sous Contr??le', 'Pas de perte Humaine']
    sanit20= ['Crise ou Catastrophe Sanitaire', 'Rapide', 'Non r??currente' , 'Nationale' , 'Hors Contr??le', 'Perte humaine']

    # CATASTROPHE NATURELLE 
    nat1=['Crise ou Catastrophe Naturelle', 'Maitris??e', 'R??currente', 'Locale' , 'Sous Contr??le', 'Mat??riel']
    nat2=['Crise ou Catastrophe Naturelle', 'Maitris??e', 'R??currente', 'Nationale' , 'Sous Contr??le' , 'Mat??riel']
    nat3=['Crise ou Catastrophe Naturelle', 'Maitris??e', 'Non r??currente' , 'Locale'     , 'Sous Contr??le' , 'Mat??riel']
    nat4=['Crise ou Catastrophe Naturelle', 'Maitris??e', 'Non r??currente', 'Nationale' , 'Sous Contr??le', 'Mat??riel']
    nat5=['Crise ou Catastrophe Naturelle', 'Lente', 'R??currente'    , 'Locale'    , 'Sous Contr??le', 'Mat??riel']
    nat6=['Crise ou Catastrophe Naturelle', 'Lente', 'R??currente' , 'Locale' , 'Hors Contr??le' , 'Mat??riel & Humain']
    nat7=['Crise ou Catastrophe Naturelle', 'Lente', 'R??currente' , 'Locale' , 'Hors Contr??le' , 'Mat??riel & Humain']
    nat8=['Crise ou Catastrophe Naturelle', 'Lente', 'R??currente'     ,'Nationale'  ,'Sous Contr??le' ,'Mat??riel']
    nat9=['Crise ou Catastrophe Naturelle', 'Lente', 'R??currente'     ,'Nationale'  ,'Hors Contr??le' ,'Mat??riel & Humain']
    nat10=['Crise ou Catastrophe Naturelle','Lente', 'Non r??currente' ,'Locale'     ,'Sous Contr??le' ,'Mat??riel']
    nat11=['Crise ou Catastrophe Naturelle','Lente', 'Non r??currente' ,'Locale'     ,'Hors Contr??le' ,'Mat??riel & Humain']
    nat12=['Crise ou Catastrophe Naturelle','Rapide', 'Non r??currente' ,'Nationale'  ,'Hors Contr??le' ,'Mat??riel & Humain']
    nat13=['Crise ou Catastrophe Naturelle','Rapide', 'Non r??currente' ,'Nationale'  ,'Hors Contr??le' ,'Mat??riel & Humain']
    nat14=['Crise ou Catastrophe Naturelle','Rapide', 'R??currente'     ,'Locale'     ,'Hors Contr??le' ,'Mat??riel & Humain']
    nat15=['Crise ou Catastrophe Naturelle','Rapide', 'R??currente'     ,'Nationale'  ,'Sous Contr??le' ,'Mat??riel']
    nat16=['Crise ou Catastrophe Naturelle','Rapide', 'R??currente'     ,'Nationale'  ,'Hors Contr??le' ,'Mat??riel & Humain']
    nat17=['Crise ou Catastrophe Naturelle','Rapide', 'Non r??currente' ,'Locale'     ,'Sous Contr??le' ,'Mat??riel']
    nat18=['Crise ou Catastrophe Naturelle','Rapide', 'Non r??currente' ,'Locale'     ,'Hors Contr??le' ,'Mat??riel & Humain']
    nat19=['Crise ou Catastrophe Naturelle','Rapide', 'Non r??currente' ,'Nationale'  ,'Sous Contr??le' ,'Mat??riel']
    nat20=['Crise ou Catastrophe Naturelle','Rapide', 'Non r??currente' ,'Nationale'  ,'Hors Contr??le' ,'Mat??riel & Humain']
    
    # CATASTROPHE SECURITAIRE
    sec1=['Crise ou Catastrophe S??curitaire', 'Maitris??e', 'R??currente', 'Locale', 'Sous Contr??le', 'Mat??riel'] 
    sec2=['Crise ou Catastrophe S??curitaire', 'Maitris??e', 'R??currente', 'Nationale', 'Sous Contr??le', 'Mat??riel']
    sec3=['Crise ou Catastrophe S??curitaire', 'Maitris??e', 'Non r??currente', 'Locale', 'Sous Contr??le', 'Mat??riel']
    sec4=['Crise ou Catastrophe S??curitaire', 'Maitris??e', 'Non r??currente', 'Nationale', 'Sous Contr??le', 'Mat??riel']
    sec5=['Crise ou Catastrophe S??curitaire', 'Lente', 'R??currente', 'Locale', 'Sous Contr??le', 'Mat??riel']
    sec6=['Crise ou Catastrophe S??curitaire', 'Lente', 'R??currente', 'Locale', 'Hors Contr??le' ,'Mat??riel & Humain' ]
    sec7=['Crise ou Catastrophe S??curitaire', 'Lente', 'R??currente', 'Nationale', 'Sous Contr??le', 'Mat??riel']
    sec8=['Crise ou Catastrophe S??curitaire', 'Lente', 'R??currente', 'Nationale', 'Hors Contr??le' ,'Mat??riel & Humain']
    sec9=['Crise ou Catastrophe S??curitaire', 'Lente', 'Non r??currente', 'Locale', 'Sous Contr??le', 'Mat??riel']
    sec10=['Crise ou Catastrophe S??curitaire', 'Lente', 'Non r??currente', 'Locale', 'Hors Contr??le' ,'Mat??riel & Humain']
    sec11=['Crise ou Catastrophe S??curitaire', 'Lente', 'Non r??currente', 'Nationale', 'Sous Contr??le', 'Mat??riel']
    sec12=['Crise ou Catastrophe S??curitaire', 'Lente',  'Non r??currente','Nationale','Hors Contr??le' ,'Mat??riel & Humain']
    sec13=['Crise ou Catastrophe S??curitaire', 'Rapide', 'R??currente', 'Locale', 'Sous Contr??le', 'Mat??riel']
    sec14=['Crise ou Catastrophe S??curitaire', 'Rapide', 'R??currente', 'Locale','Hors Contr??le' ,'Mat??riel & Humain']
    sec15=['Crise ou Catastrophe S??curitaire', 'Rapide', 'R??currente', 'Nationale', 'Sous Contr??le', 'Mat??riel']
    sec16=['Crise ou Catastrophe S??curitaire', 'Rapide', 'R??currente','Nationale','Hors Contr??le' ,'Mat??riel & Humain']
    sec17=['Crise ou Catastrophe S??curitaire', 'Rapide', 'Non r??currente', 'Locale', 'Sous Contr??le', 'Mat??riel']
    sec18=['Crise ou Catastrophe S??curitaire', 'Rapide', 'Non r??currente', 'Locale', 'Hors Contr??le' ,'Mat??riel & Humain']
    sec19=['Crise ou Catastrophe S??curitaire', 'Rapide', 'Non r??currente', 'Nationale','Sous Contr??le', 'Mat??riel']   
    sec20=['Crise ou Catastrophe S??curitaire', 'Rapide', 'Non r??currente', 'Nationale','Hors Contr??le' ,'Mat??riel & Humain']

    # la gestion des catastroph sanitaire 
    if data == sanit1:
        filename = 'SANIT1.pdf'

    elif data==sanit2:
        filename = 'SANIT2.pdf'

    elif data==sanit3:
        filename = 'SANIT3.pdf' 

    elif data==sanit4:
        filename = 'SANIT4.pdf'

    elif data==sanit5:
        filename = 'SANIT5.pdf' 

    elif data==sanit6:
        filename = 'SANIT6.pdf'  

    elif data==sanit7:
        filename = 'SANIT7.pdf'  

    elif data==sanit8:
        filename = 'SANIT8.pdf' 

    elif data==sanit9:
        filename = 'SANIT9.pdf'

    elif data==sanit10:
        filename = 'SANIT10.pdf'

    elif data==sanit11:
        filename = 'SANIT11.pdf'

    elif data==sanit12:
        filename = 'SANIT12.pdf'

    elif data==sanit13:
        filename = 'SANIT13.pdf'

    elif data==sanit14:
        filename = 'SANIT14.pdf'

    elif data==sanit15:
        filename = 'SANIT15.pdf'

    elif data==sanit16:
        filename = 'SANIT16.pdf'
    
    elif data==sanit17:
        filename = 'SANIT17.pdf' 
        
    elif data==sanit18:
        filename = 'SANIT18.pdf'
    
    elif data==sanit19:
        filename = 'SANIT19.pdf' 
    
    elif data==sanit20:
        filename = 'SANIT20.pdf'

    # gestion des Catastrophe naturelles
    elif data==nat1:
        filename = 'NATUREL1.pdf'
    elif data==nat2:
        filename = 'NATUREL2.pdf'
    elif data==nat3:
        filename = 'NATUREL3.pdf' 
    elif data==nat4:
        filename = 'NATUREL4.pdf'
    elif data==nat5:
        filename = 'NATUREL5.pdf'  
    elif data==nat6:
        filename = 'NATUREL6.pdf'  
    elif data==nat7:
        filename = 'NATUREL7.pdf'  
    elif data==nat8:
        filename = 'NATUREL8.pdf'  
    elif data==nat9:
        filename = 'NATUREL9.pdf'  
    elif data==nat10:
        filename = 'NATUREL10.pdf'
    elif data==nat11:
        filename = 'NATUREL11.pdf'
   
    elif data==nat12:
        filename = 'NATUREL12.pdf'

    elif data==nat13:
        filename = 'NATUREL13.pdf'

    elif data==nat14:
        filename = 'NATUREL14.pdf'

    elif data==nat15:
        filename = 'NATUREL15.pdf'

    elif data==nat16:
        filename = 'NATUREL16.pdf'
    
    elif data==nat17:
        filename = 'NATUREL17.pdf' 
        
    elif data==nat18:
        filename = 'NATUREL18.pdf'
    
    elif data==nat19:
        filename = 'NATUREL19.pdf' 
    
    elif data==nat20:
        filename = 'NATUREL20.pdf'

    # la gestion des Catastrophe securitaire

    elif data==sec1:
        filename = 'SECUR1.pdf'
    elif data==sec2:
        filename = 'SECUR2.pdf'
    elif data==sec3:
        filename = 'SECUR3.pdf' 
    elif data==sec4:
        filename = 'SECUR4.pdf'
    elif data==sec5:
        filename = 'SECUR5.pdf'  
    elif data==sec6:
        filename = 'SECUR6.pdf'  
    elif data==sec7:
        filename = 'SECUR7.pdf'  
    elif data==sec8:
        filename = 'SECUR8.pdf'  
    elif data==sec9:
        filename = 'SECUR9.pdf'  
    elif data==sec10:
        filename = 'SECUR10.pdf'
    elif data==sec11:
        filename = 'SECUR11.pdf'
   
    elif data==sec12:
        filename = 'SECUR12.pdf'

    elif data==sec13:
        filename = 'SECUR13.pdf'

    elif data==sec14:
        filename = 'SECUR14.pdf'

    elif data==sec15:
        filename = 'SECUR15.pdf'

    elif data==sec16:
        filename = 'SECUR16.pdf'
    
    elif data==sec17:
        filename = 'SECUR17.pdf' 
        
    elif data==sec18:
        filename = 'SECUR18.pdf'
    
    elif data==sec19:
        filename = 'SECUR19.pdf' 
    
    elif data==sec20:
        filename = 'SECUR20.pdf'
    else:
        filename = "Aucune fiche de d??cision ne correspond aux choix effectu??s"
    context={
        'recup':data,
        'filename':filename,
    }
    return render (request, 'alerte/simulation.html', context) 


                ############################################################################
                #                            LA GESTION DES ATTAQUES                       #
                ############################################################################    
@login_required(login_url = 'login')    
def Natureinformation(request): 
    natureinfo= NatureInformation.objects.all()
    context={
            "natureinfo":natureinfo
          }
    return render(request,'attaque/naturinfo.html', context)

@login_required(login_url = 'login')    
def Parutioninfo(request): #1
    natinf =''
    paruinfo= Parution.objects.all()
    if request.method == 'POST':
        natinf = request.POST.get('natureinfo')
    request.session['natinf'] = natinf   
    context={
        "paruinfo":paruinfo }
    return render(request,'attaque/paruinfo.html', context)


@login_required(login_url = 'login')    
def Perceptsupport(request): #2
    paruinf =''
    percepsupport= Perceptionsupport.objects.all()
    if request.method == 'POST':
        paruinf = request.POST.get('paruinfo')
    request.session['paruinf'] = paruinf   
     
    context={
        "percepsupport":percepsupport}
    return render(request,'attaque/perceptionsupport.html', context)



@login_required(login_url = 'login')    
def Rebondinfo(request):#3
    perceptsup = ''
    rebond= Rebond.objects.all()
    if request.method == 'POST':
        perceptsup = request.POST.get('percepsupport')
    request.session['perceptsup'] = perceptsup   
    context={
        'rebond':rebond,
    }
    return render(request,'attaque/rebond.html', context)



@login_required(login_url = 'login')    
def simulationattack(request):
    action = '' 
    rebondinf = ''
    if request.method == 'POST':
        rebondinf  = request.POST.get('rebond')
        request.session['rebondinf'] = rebondinf   
    natinf  = request.session.get('natinf', None)        
    paruinf  = request.session.get('paruinf', None)        
    perceptsup  = request.session.get('perceptsup', None)        
    rebondinf  = request.session.get('rebondinf', None)   
    data = [] 
    data.append(natinf)
    data.append(paruinf)
    data.append(perceptsup)
    data.append(rebondinf)

   
    Action1 = ['Fausse (Fake news)',          	"Page RS de l'entreprise",   	"Image de l'entreprise",	"RAS"]   # -
    Action2 =['Fausse (Fake news)',          	"Page RS de l'entreprise",   	"Image de l'entreprise",	"Effectif"] #     
    Action3 =['Fausse (Fake news)',          	"Fil de discussion RS / Blog",	"Cr??dible",             	"RAS"]	    #-     
    Action4 =['Fausse (Fake news)',          	"Fil de discussion RS / Blog",	"Cr??dible",             	"Effectif"] #-   	 
    Action5 =['Fausse (Fake news)',          	"Fil de discussion RS / Blog",	"Pas cr??dible",	            "RAS"]       #	 
    Action6 =['Fausse (Fake news)',          	"Fil de discussion RS / Blog",	"Pas cr??dible",	            "Effectif"]  #  	 
    Action7 =['Fausse (Fake news)',          	"Article Site d'actualit??",	    "Cr??dible",             	"RAS"]       #	 
    Action8 =['Fausse (Fake news)',          	"Article Site d'actualit??",	    "Cr??dible",             	"Effectif"]   # 	 
    Action9 =['Fausse (Fake news)',          	"Article Site d'actualit??",	    "Pas cr??dible",	            "RAS"]       	# 
    Action10=['Fausse (Fake news)',          	"Article Site d'actualit??",	    "Pas cr??dible",	            "Effectif"]    	 # 
    Action11=['Fausse (Fake news)',          	"Presse",                   	"Cr??dible",             	"RAS"]       	  
    Action12=['Fausse (Fake news)',          	"Presse",                   	"Cr??dible",             	"Effectif"]    	  
    Action13=['Fausse (Fake news)',          	"Presse",                   	"Pas cr??dible",	            "RAS"]       	 
    Action14=['Fausse (Fake news)',          	"Presse",                   	"Pas cr??dible",	            "Effectif"]    	  
    Action15=['Mi-figue Mi-raisin (bashing)',	"Page RS de l'entreprise",   	"Image de l'entreprise",	"RAS"]       	  
    Action16=['Mi-figue Mi-raisin (bashing)',	"Page RS de l'entreprise",   	"Image de l'entreprise",	"Effectif"]    	  
    Action17=['Mi-figue Mi-raisin (bashing)',	"Fil de discussion RS / Blog",	"Cr??dible",             	"RAS"]       	  
    Action18=['Mi-figue Mi-raisin (bashing)',	"Fil de discussion RS / Blog",	"Cr??dible",             	"Effectif"]    	  
    Action19=['Mi-figue Mi-raisin (bashing)',	"Fil de discussion RS / Blog",	"Pas cr??dible",	            "RAS"]       	  
    Action20=['Mi-figue Mi-raisin (bashing)',	"Fil de discussion RS / Blog",	"Pas cr??dible",	            "Effectif"]    	  
    Action21=['Mi-figue Mi-raisin (bashing)',	"Article Site d'actualit??",	    "Cr??dible",             	"RAS"]       	  
    Action22=['Mi-figue Mi-raisin (bashing)',	"Article Site d'actualit??",	    "Cr??dible",             	"Effectif"]    	  
    Action23=['Mi-figue Mi-raisin (bashing)',	"Article Site d'actualit??",	    "Pas cr??dible",	            "RAS"]       	  
    Action24=['Mi-figue Mi-raisin (bashing)',	"Article Site d'actualit??",	    "Pas cr??dible",	            "Effectif"]    	  
    Action25=['Mi-figue Mi-raisin (bashing)',	"Presse",                   	"Cr??dible",             	"RAS"]       	  
    Action26=['Mi-figue Mi-raisin (bashing)',	"Presse",                   	"Cr??dible",             	"Effectif"]    	  
    Action27=['Mi-figue Mi-raisin (bashing)',	"Presse",                   	"Pas cr??dible",	            "RAS"]       	  
    Action28=['Mi-figue Mi-raisin (bashing)',	"Presse",                   	"Pas cr??dible",	            "Effectif"]    	  
    Action29=['100% vrai (knocking)',         	"Page RS de l'entreprise",   	"Image de l'entreprise",	"RAS"]       	  
    Action30=['100% vrai (knocking)',         	"Page RS de l'entreprise",   	"Image de l'entreprise",	"Effectif"]    	  
    Action31=['100% vrai (knocking)',         	"Fil de discussion RS / Blog",	"Cr??dible",             	"RAS"]       	  
    Action32=['100% vrai (knocking)',         	"Fil de discussion RS / Blog",	"Cr??dible",             	"Effectif"]    	  
    Action33=['100% vrai (knocking)',         	"Fil de discussion RS / Blog",	"Pas cr??dible",	            "RAS"]       	  
    Action34=['100% vrai (knocking)',         	"Fil de discussion RS / Blog",	"Pas cr??dible",	            "Effectif"]    	  
    Action35=['100% vrai (knocking)',         	"Article Site d'actualit??",	    "Cr??dible",              	"RAS"]       	  
    Action36=['100% vrai (knocking)',         	"Article Site d'actualit??",	    "Cr??dible",              	"Effectif"]    	  
    Action37=['100% vrai (knocking)',         	"Article Site d'actualit??",	    "Pas cr??dible",	            "RAS"]       	  
    Action38=['100% vrai (knocking)',         	"Article Site d'actualit??",	    "Pas cr??dible",	            "Effectif"]    	  
    Action39=['100% vrai (knocking)',         	"Presse",                   	"Cr??dible",             	"RAS"]       	  
    Action40=['100% vrai (knocking)',         	"Presse",                   	"Cr??dible",             	"Effectif"]    	  
    Action41=['100% vrai (knocking)',         	"Presse",                   	"Pas cr??dible",	            "RAS"]       	  
    Action42=['100% vrai (knocking)',         	"Presse",                   	"Pas cr??dible",	            "Effectif"]  
    if data == Action1:
        action="R??ponse directe argument??e"
    elif data == Action2:
        action="D??menti"
    elif data == Action3:
        action="R??ponse directe argument??e"
    elif data == Action4: 
        action="Droit de r??ponse"
    elif data == Action5:
        action="Pas de r??action"
    elif data == Action6:
        action="D??menti"
    elif data == Action7: 
        action="D??menti"   
    elif data == Action8:
        action="D??menti"
    elif data == Action9:
        action="Pas de r??action"
    elif data == Action10:
        action="D??menti"
    elif data == Action11:
        action="D??menti"
    elif data == Action12:
        action="D??menti"        
    elif data == Action13:
        action="Pas de r??action"
    elif data == Action14:
        action="D??menti"
    elif data == Action15:
        action="R??ponse directe argument??e"
    elif data == Action16:
        action="Capitalisation image"
    elif data == Action17:
        action="Pas de r??action"
    elif data == Action18:
        action="Capitalisation image / Canal influ..."
    elif data == Action19:
        action="Pas de r??action"
    elif data == Action20:
        action="Capitalisation image / Canal influ..."
    elif data == Action21:
        action="Pas de r??action"
    elif data == Action22:
        action="Capitalisation sur image (Exemple ..."
    elif data == Action23:
        action="Pas de r??action"
    elif data == Action24:
        action="Capitalisation sur image (Exemple R..."    
    elif data == Action25:
        action="Pas de r??action"
    elif data == Action26:
        action="Capitalisation sur image (Exemple ..."
    elif data == Action27:
        action="Pas de r??action"
    elif data == Action28:
        action="Capitalisation sur image (Exemple ..."
    elif data == Action29:
        action="Prise en charge"
    elif data == Action30:
        action="Capitalisation sur image (Exemple ..."
    elif data == Action31:
        action="Prise en charge"
    elif data == Action32:
        action="Capitalisation sur image (Exemple ..."
    elif data == Action33:
        action="Prise en charge"
    elif data == Action34:
        action="Capitalisation sur image (Exemple ..."
    elif data == Action35:
        action="Pas de r??action"
    elif data == Action36:
        action="Reconnaissance + Perspective ou r??..."
    elif data == Action37:
        action="Pas de r??action"
    elif data == Action38:
        action="Capitalisation sur image (Exemple ..."
    elif data == Action39:
        action="Pas de r??action"
    elif data == Action40:
        action="Reconnaissance + Perspective ou r??..."
    elif data == Action41:
        action="Pas de r??action"
    elif data == Action42:
        action="Capitalisation sur image (Exemple ..."            
    else:
        action = "Aucun plan d'action ne correspond aux choix effectu??s"
    context={
        'recup':data,
        'filename':action,
         }
    return render (request, 'attaque/simulationattack.html', context)

@login_required(login_url = 'login')    
def custom_page_not_found_view(request, exception):
    return render(request, "errors/404.html", {})

@login_required(login_url = 'login')    
def custom_error_view(request, exception=None):
    return render(request, "errors/500.html", {})

@login_required(login_url = 'login')    
def custom_permission_denied_view(request, exception=None):
    return render(request, "errors/403.html", {})

@login_required(login_url = 'login')    
def custom_bad_request_view(request, exception=None):
    return render(request, "errors/400.html", {})

