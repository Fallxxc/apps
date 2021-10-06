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

vitess = ''
@login_required(login_url = 'login')    
def vitess_p(request): #1
    vp= VitessePropagation.objects.all()
    if request.method == 'POST':
        var = request.POST.get('categorie')
        global vitess
        vitess = var 
    context={
        "vitessePropagation":vp }
    return render(request,'alerte/vitessepropa.html', context)

freq = ''
@login_required(login_url = 'login')    
def frequence(request): #2
    fr= Frequence.objects.all()
    if request.method == 'POST':
        var = request.POST.get('vitessePropagation')
        global freq
        freq = var
    context={
        "frequence":fr }
    return render(request,'alerte/frequence.html', context)

profond = ''
@login_required(login_url = 'login')    
def profondeur(request):#3
    pro= Profondeur.objects.all()
    if request.method == 'POST':
        var = request.POST.get('frequence')
        global profond
        profond = var
    context={
        'profondeur':pro,
    }
    return render(request,'alerte/profondeur.html', context)

niveaucon = ''
@login_required(login_url = 'login')    
def niveauControle(request):#4
    nc= NiveauControle.objects.all()
    if request.method == 'POST':
        var = request.POST.get('profondeur')
        global niveaucon
        niveaucon = var 
    context={
        'niveauControle':nc
            }
    return render(request,'alerte/nivocontrol.html', context)
nivopert = ''
@login_required(login_url = 'login')    
def niveauPerte(request):
    np= NiveauPerte.objects.all()
    if request.method == 'POST':
        var = request.POST.get('niveauControle')
        global nivopert
        nivopert = var
    context={
        'niveauPerte':np
    }
    return render(request,'alerte/nivoperte.html', context)


from collections import Iterable

def flatten(lis):
     for item in lis:
         if isinstance(item, Iterable) and not isinstance(item, str):
             for x in flatten(item):
                 yield x
         else:        
             yield item

@login_required(login_url = 'login')    
def simulation(request):
    filename = '' 
    recup5, data = [],[]
    recup5.append(vitess)
    recup5.append(freq)
    recup5.append(profond)
    recup5.append(niveaucon)
    recup5.append(nivopert)
    if request.method == 'POST':
        nip  = request.POST.get('niveauPerte')
        recup5.append(nip)    
    data= list(flatten(recup5))
    sanit1 = ['Crise ou Catastrophe Sanitaire' , 'Maitrisée' , 'Récurrente', 'Locale', 'Sous Contrôle' , 'Pas de perte Humaine']
    sanit2 = ['Crise ou Catastrophe Sanitaire' , 'Maitrisée' , 'Récurrente', 'Nationale', 'Sous Contrôle' , 'Pas de perte Humaine']
    sanit3 = ['Crise ou Catastrophe Sanitaire' , 'Maitrisée' , 'Non récurrente', 'Locale', 'Sous Contrôle' , 'Pas de perte Humaine']
    sanit4 = ['Crise ou Catastrophe Sanitaire' , 'Maitrisée' , 'Non récurrente', 'Nationale', 'Sous Contrôle' , 'Pas de perte Humaine']
    sanit5 = ['Crise ou Catastrophe Sanitaire' , 'Lente' , 'Récurrente', 'Locale', 'Sous Contrôle' , 'Pas de perte Humaine']
    sanit6 = ['Crise ou Catastrophe Sanitaire' , 'Lente' , 'Récurrente', 'Locale', 'Hors Contrôle' , 'Perte humaine']
    sanit7 = ['Crise ou Catastrophe Sanitaire' , 'Lente' , 'Récurrente', 'Nationale', 'Sous Contrôle' , 'Pas de perte Humaine']
    sanit8 = ['Crise ou Catastrophe Sanitaire' , 'Lente' , 'Récurrente', 'Nationale', 'Hors Contrôle' , 'Perte humaine']
    sanit9 = ['Crise ou Catastrophe Sanitaire' , 'Lente' , 'Non récurrente', 'Locale', 'Sous Contrôle' , 'Pas de perte Humaine']
    sanit10= ['Crise ou Catastrophe Sanitaire' , 'Lente' , 'Non récurrente', 'Locale', 'Hors Contrôle' , 'Perte humaine']
    sanit11= ['Crise ou Catastrophe Sanitaire' , 'Lente' , 'Non récurrente', 'Nationale', 'Sous Contrôle' , 'Pas de perte Humaine']
    sanit12= ['Crise ou Catastrophe Sanitaire' , 'Lente' , 'Non récurrente', 'Nationale', 'Hors Contrôle' , 'Perte humaine']
    sanit13= ['Crise ou Catastrophe Sanitaire', 'Rapide', 'Récurrente' , 'Locale' , 'Sous Contrôle', 'Pas de perte Humaine']
    sanit14= ['Crise ou Catastrophe Sanitaire', 'Rapide', 'Récurrente' , 'Locale' , 'Hors Contrôle', 'Perte humaine']
    sanit15= ['Crise ou Catastrophe Sanitaire', 'Rapide', 'Récurrente' , 'Nationale' , 'Sous Contrôle', 'Pas de perte Humaine']
    sanit16= ['Crise ou Catastrophe Sanitaire', 'Rapide', 'Récurrente' , 'Nationale' , 'Hors Contrôle', 'Perte humaine']
    sanit17= ['Crise ou Catastrophe Sanitaire', 'Rapide', 'Non récurrente' , 'Locale' , 'Sous Contrôle', 'Pas de perte Humaine']
    sanit18= ['Crise ou Catastrophe Sanitaire', 'Rapide', 'Non récurrente' , 'Locale' , 'Hors Contrôle', 'Perte humaine']
    sanit19= ['Crise ou Catastrophe Sanitaire', 'Rapide', 'Non récurrente' , 'Nationale' , 'Sous Contrôle', 'Pas de perte Humaine']
    sanit20= ['Crise ou Catastrophe Sanitaire', 'Rapide', 'Non récurrente' , 'Nationale' , 'Hors Contrôle', 'Perte humaine']

    # CATASTROPHE NATURELLE 
    nat1=['Crise ou Catastrophe Naturelle', 'Maitrisée', 'Récurrente', 'Locale' , 'Sous Contrôle', 'Matériel']
    nat2=['Crise ou Catastrophe Naturelle', 'Maitrisée', 'Récurrente', 'Nationale' , 'Sous Contrôle' , 'Matériel']
    nat3=['Crise ou Catastrophe Naturelle', 'Maitrisée', 'Non récurrente' , 'Locale'     , 'Sous Contrôle' , 'Matériel']
    nat4=['Crise ou Catastrophe Naturelle', 'Maitrisée', 'Non récurrente', 'Nationale' , 'Sous Contrôle', 'Matériel']
    nat5=['Crise ou Catastrophe Naturelle', 'Lente', 'Récurrente'    , 'Locale'    , 'Sous Contrôle', 'Matériel']
    nat6=['Crise ou Catastrophe Naturelle', 'Lente', 'Récurrente' , 'Locale' , 'Hors Contrôle' , 'Matériel & Humain']
    nat7=['Crise ou Catastrophe Naturelle', 'Lente', 'Récurrente' , 'Locale' , 'Hors Contrôle' , 'Matériel & Humain']
    nat8=['Crise ou Catastrophe Naturelle', 'Lente', 'Récurrente'     ,'Nationale'  ,'Sous Contrôle' ,'Matériel']
    nat9=['Crise ou Catastrophe Naturelle', 'Lente', 'Récurrente'     ,'Nationale'  ,'Hors Contrôle' ,'Matériel & Humain']
    nat10=['Crise ou Catastrophe Naturelle','Lente', 'Non récurrente' ,'Locale'     ,'Sous Contrôle' ,'Matériel']
    nat11=['Crise ou Catastrophe Naturelle','Lente', 'Non récurrente' ,'Locale'     ,'Hors Contrôle' ,'Matériel & Humain']
    nat12=['Crise ou Catastrophe Naturelle','Rapide', 'Non récurrente' ,'Nationale'  ,'Hors Contrôle' ,'Matériel & Humain']
    nat13=['Crise ou Catastrophe Naturelle','Rapide', 'Non récurrente' ,'Nationale'  ,'Hors Contrôle' ,'Matériel & Humain']
    nat14=['Crise ou Catastrophe Naturelle','Rapide', 'Récurrente'     ,'Locale'     ,'Hors Contrôle' ,'Matériel & Humain']
    nat15=['Crise ou Catastrophe Naturelle','Rapide', 'Récurrente'     ,'Nationale'  ,'Sous Contrôle' ,'Matériel']
    nat16=['Crise ou Catastrophe Naturelle','Rapide', 'Récurrente'     ,'Nationale'  ,'Hors Contrôle' ,'Matériel & Humain']
    nat17=['Crise ou Catastrophe Naturelle','Rapide', 'Non récurrente' ,'Locale'     ,'Sous Contrôle' ,'Matériel']
    nat18=['Crise ou Catastrophe Naturelle','Rapide', 'Non récurrente' ,'Locale'     ,'Hors Contrôle' ,'Matériel & Humain']
    nat19=['Crise ou Catastrophe Naturelle','Rapide', 'Non récurrente' ,'Nationale'  ,'Sous Contrôle' ,'Matériel']
    nat20=['Crise ou Catastrophe Naturelle','Rapide', 'Non récurrente' ,'Nationale'  ,'Hors Contrôle' ,'Matériel & Humain']
    
    # CATASTROPHE SECURITAIRE
    sec1=['Crise ou Catastrophe Sécuritaire', 'Maitrisée', 'Récurrente', 'Locale', 'Sous Contrôle', 'Matériel'] 
    sec2=['Crise ou Catastrophe Sécuritaire', 'Maitrisée', 'Récurrente', 'Nationale', 'Sous Contrôle', 'Matériel']
    sec3=['Crise ou Catastrophe Sécuritaire', 'Maitrisée', 'Non récurrente', 'Locale', 'Sous Contrôle', 'Matériel']
    sec4=['Crise ou Catastrophe Sécuritaire', 'Maitrisée', 'Non récurrente', 'Nationale', 'Sous Contrôle', 'Matériel']
    sec5=['Crise ou Catastrophe Sécuritaire', 'Lente', 'Récurrente', 'Locale', 'Sous Contrôle', 'Matériel']
    sec6=['Crise ou Catastrophe Sécuritaire', 'Lente', 'Récurrente', 'Locale', 'Hors Contrôle' ,'Matériel & Humain' ]
    sec7=['Crise ou Catastrophe Sécuritaire', 'Lente', 'Récurrente', 'Nationale', 'Sous Contrôle', 'Matériel']
    sec8=['Crise ou Catastrophe Sécuritaire', 'Lente', 'Récurrente', 'Nationale', 'Hors Contrôle' ,'Matériel & Humain']
    sec9=['Crise ou Catastrophe Sécuritaire', 'Lente', 'Non récurrente', 'Locale', 'Sous Contrôle', 'Matériel']
    sec10=['Crise ou Catastrophe Sécuritaire', 'Lente', 'Non récurrente', 'Locale', 'Hors Contrôle' ,'Matériel & Humain']
    sec11=['Crise ou Catastrophe Sécuritaire', 'Lente', 'Non récurrente', 'Nationale', 'Sous Contrôle', 'Matériel']
    sec12=['Crise ou Catastrophe Sécuritaire', 'Lente',  'Non récurrente','Nationale','Hors Contrôle' ,'Matériel & Humain']
    sec13=['Crise ou Catastrophe Sécuritaire', 'Rapide', 'Récurrente', 'Locale', 'Sous Contrôle', 'Matériel']
    sec14=['Crise ou Catastrophe Sécuritaire', 'Rapide', 'Récurrente', 'Locale','Hors Contrôle' ,'Matériel & Humain' ]
    sec15=['Crise ou Catastrophe Sécuritaire', 'Rapide', 'Récurrente', 'Nationale', 'Sous Contrôle', 'Matériel']
    sec16=['Crise ou Catastrophe Sécuritaire', 'Rapide', 'Récurrente','Nationale','Hors Contrôle' ,'Matériel & Humain' ]
    sec17=['Crise ou Catastrophe Sécuritaire', 'Rapide', 'Non récurrente', 'Locale', 'Sous Contrôle', 'Matériel']
    sec18=['Crise ou Catastrophe Sécuritaire', 'Rapide', 'Non récurrente', 'Locale', 'Hors Contrôle' ,'Matériel & Humain']
    sec19=['Crise ou Catastrophe Sécuritaire', 'Rapide', 'Non récurrente', 'Nationale','Sous Contrôle', 'Matériel']   
    sec20=['Crise ou Catastrophe Sécuritaire', 'Rapide', 'Non récurrente', 'Nationale','Hors Contrôle' ,'Matériel & Humain']

    # la gestion des catastroph sanitaire 
    if data==sanit1:
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
        filename = "Aucune fiche de décision ne correspond aux choix effectués"
    
    context={
        'recup':data,
        'filename':filename
    }
    return render (request, 'alerte/simulation.html', context) 


                ############################################################################
                #                            LA GESTION DES ATTAQUE                        #
                ############################################################################    
@login_required(login_url = 'login')    
def Natureinformation(request): 
    natureinfo= NatureInformation.objects.all()
    context={
            "natureinfo":natureinfo
          }
    return render(request,'attaque/naturinfo.html', context)

nature_info = ''
@login_required(login_url = 'login')    
def Parutioninfo(request): #1
    nat =''
    paruinfo= Parution.objects.all()
    if request.method == 'POST':
        natinf = request.POST.get('natureinfo')
        global nature_info
        nature_info = natinf
    request.session['natinf'] = natinf   
    context={
        "paruinfo":paruinfo }
    return render(request,'attaque/paruinfo.html', context)

paru_info = ''
@login_required(login_url = 'login')    
def Perceptsupport(request): #2
    percepsupport= Perceptionsupport.objects.all()
    if request.method == 'POST':
        paruinf = request.POST.get('paruinfo')
        global paru_info
        paru_info = paruinf   
    request.session['paruinf'] = paruinf   
     
    context={
        "percepsupport":percepsupport}
    return render(request,'attaque/perceptionsupport.html', context)

rebond_info = ''
@login_required(login_url = 'login')    
def Rebondinfo(request):#3
    rebond= Rebond.objects.all()
    if request.method == 'POST':
        perc_sup = request.POST.get('percepsupport')
        global rebond_info
        rebond_info = perc_sup
    request.session['perc_sup'] = perc_sup   
    context={
        'rebond':rebond,
        # 'nat':nat
    }
    return render(request,'attaque/rebond.html', context)

nip =''
@login_required(login_url = 'login')    
def simulationattack(request):
    action = '' 
    recup5, data = [],[]
    recup5.append(nature_info)
    recup5.append(paru_info)
    recup5.append(rebond_info)
    if request.method == 'POST':
        rebondinf  = request.POST.get('rebond')
        request.session['rebondinf'] = rebondinf   
        global nip
        nip = rebondinf
        recup5.append(rebondinf)   
    natinf  = request.session.get('natinf', None)        
    paruinf  = request.session.get('paruinf', None)        
    perc_sup  = request.session.get('perc_sup', None)        
    rebondinf  = request.session.get('rebondinf', None)        
    data= list(flatten(recup5))
    Action1 = ['Fausse (Fake news)',          	"Page RS de l'entreprise",   	"Image de l'entreprise",	"RAS"]   
    Action2 =['Fausse (Fake news)',          	"Page RS de l'entreprise",   	"Image de l'entreprise",	"Effectif"]      
    
    Action3 =['Fausse (Fake news)',          	"Fil de discussion RS / Blog",	"Crédible",             	"RAS"]	         
    Action4 =['Fausse (Fake news)',          	"Fil de discussion RS / Blog",	"Crédible",             	"Effectif"]    	 
    Action5 =['Fausse (Fake news)',          	"Fil de discussion RS / Blog",	"Pas crédible",	            "RAS"]       	 
    Action6 =['Fausse (Fake news)',          	"Fil de discussion RS / Blog",	"Pas crédible",	            "Effectif"]    	 
    Action7 =['Fausse (Fake news)',          	"Article Site d'actualité",	    "Crédible",             	"RAS"]       	 
    Action8 =['Fausse (Fake news)',          	"Article Site d'actualité",	    "Crédible",             	"Effectif"]    	 
    Action9 =['Fausse (Fake news)',          	"Article Site d'actualité",	    "Pas crédible",	            "RAS"]       	 
    Action10=['Fausse (Fake news)',          	"Article Site d'actualité",	    "Pas crédible",	            "Effectif"]    	  
    Action11=['Fausse (Fake news)',          	"Presse",                   	"Crédible",             	"RAS"]       	  
    Action12=['Fausse (Fake news)',          	"Presse",                   	"Crédible",             	"Effectif"]    	  
    Action13=['Fausse (Fake news)',          	"Presse",                   	"Pas crédible",	            "RAS"]       	 
    Action14=['Fausse (Fake news)',          	"Presse",                   	"Pas crédible",	            "Effectif"]    	  
    Action15=['Mi-figue Mi-raisin (bashing)',	"Page RS de l'entreprise",   	"Image de l'entreprise",	"RAS"]       	  
    Action16=['Mi-figue Mi-raisin (bashing)',	"Page RS de l'entreprise",   	"Image de l'entreprise",	"Effectif"]    	  
    Action17=['Mi-figue Mi-raisin (bashing)',	"Fil de discussion RS / Blog",	"Crédible",             	"RAS"]       	  
    Action18=['Mi-figue Mi-raisin (bashing)',	"Fil de discussion RS / Blog",	"Crédible",             	"Effectif"]    	  
    Action19=['Mi-figue Mi-raisin (bashing)',	"Fil de discussion RS / Blog",	"Pas crédible",	            "RAS"]       	  
    Action20=['Mi-figue Mi-raisin (bashing)',	"Fil de discussion RS / Blog",	"Pas crédible",	            "Effectif"]    	  
    Action21=['Mi-figue Mi-raisin (bashing)',	"Article Site d'actualité",	    "Crédible",             	"RAS"]       	  
    Action22=['Mi-figue Mi-raisin (bashing)',	"Article Site d'actualité",	    "Crédible",             	"Effectif"]    	  
    Action23=['Mi-figue Mi-raisin (bashing)',	"Article Site d'actualité",	    "Pas crédible",	            "RAS"]       	  
    Action24=['Mi-figue Mi-raisin (bashing)',	"Article Site d'actualité",	    "Pas crédible",	            "Effectif"]    	  
    Action25=['Mi-figue Mi-raisin (bashing)',	"Presse",                   	"Crédible",             	"RAS"]       	  
    Action26=['Mi-figue Mi-raisin (bashing)',	"Presse",                   	"Crédible",             	"Effectif"]    	  
    Action27=['Mi-figue Mi-raisin (bashing)',	"Presse",                   	"Pas crédible",	            "RAS"]       	  
    Action28=['Mi-figue Mi-raisin (bashing)',	"Presse",                   	"Pas crédible",	            "Effectif"]    	  
    Action29=['100% vrai (knocking)',         	"Page RS de l'entreprise",   	"Image de l'entreprise",	"RAS"]       	  
    Action30=['100% vrai (knocking)',         	"Page RS de l'entreprise",   	"Image de l'entreprise",	"Effectif"]    	  
    Action31=['100% vrai (knocking)',         	"Fil de discussion RS / Blog",	"Crédible",             	"RAS"]       	  
    Action32=['100% vrai (knocking)',         	"Fil de discussion RS / Blog",	"Crédible",             	"Effectif"]    	  
    Action33=['100% vrai (knocking)',         	"Fil de discussion RS / Blog",	"Pas crédible",	            "RAS"]       	  
    Action34=['100% vrai (knocking)',         	"Fil de discussion RS / Blog",	"Pas crédible",	            "Effectif"]    	  
    Action35=['100% vrai (knocking)',         	"Article Site d'actualité",	    "Crédible",              	"RAS"]       	  
    Action36=['100% vrai (knocking)',         	"Article Site d'actualité",	    "Crédible",              	"Effectif"]    	  
    Action37=['100% vrai (knocking)',         	"Article Site d'actualité",	    "Pas crédible",	            "RAS"]       	  
    Action38=['100% vrai (knocking)',         	"Article Site d'actualité",	    "Pas crédible",	            "Effectif"]    	  
    Action39=['100% vrai (knocking)',         	"Presse",                   	"Crédible",             	"RAS"]       	  
    Action40=['100% vrai (knocking)',         	"Presse",                   	"Crédible",             	"Effectif"]    	  
    Action41=['100% vrai (knocking)',         	"Presse",                   	"Pas crédible",	            "RAS"]       	  
    Action42=['100% vrai (knocking)',         	"Presse",                   	"Pas crédible",	            "Effectif"]  
    if data == Action1:
        action="Réponse directe argumentée"
    elif data == Action2:
        action="Démenti"
    elif data == Action3:
        action="Réponse directe argumentée"
    elif data == Action4: 
        action="Droit de réponse"
    elif data == Action5:
        action="Pas de réaction"
    elif data == Action6:
        action="Démenti"
    elif data == Action7: 
        action="Démenti"   
    elif data == Action8:
        action="Démenti"
    elif data == Action9:
        action="Pas de réaction"
    elif data == Action10:
        action="Démenti"
    elif data == Action11:
        action="Démenti"
    elif data == Action12:
        action="Démenti"        
    elif data == Action13:
        action="Pas de réaction"
    elif data == Action14:
        action="Démenti"
    elif data == Action15:
        action="Réponse directe argumentée"
    elif data == Action16:
        action="Capitalisation image"
    elif data == Action17:
        action="Pas de réaction"
    elif data == Action18:
        action="Capitalisation image / Canal influ..."
    elif data == Action19:
        action="Pas de réaction"
    elif data == Action20:
        action="Capitalisation image / Canal influ..."
    elif data == Action21:
        action="Pas de réaction"
    elif data == Action22:
        action="Capitalisation sur image (Exemple ..."
    elif data == Action23:
        action="Pas de réaction"
    elif data == Action24:
        action="Capitalisation sur image (Exemple R..."    
    elif data == Action25:
        action="Pas de réaction"
    elif data == Action26:
        action="Capitalisation sur image (Exemple ..."
    elif data == Action27:
        action="Pas de réaction"
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
        action="Pas de réaction"
    elif data == Action36:
        action="Reconnaissance + Perspective ou ré..."
    elif data == Action37:
        action="Pas de réaction"
    elif data == Action38:
        action="Capitalisation sur image (Exemple ..."
    elif data == Action39:
        action="Pas de réaction"
    elif data == Action40:
        action="Reconnaissance + Perspective ou ré..."
    elif data == Action41:
        action="Pas de réaction"
    elif data == Action42:
        action="Capitalisation sur image (Exemple ..."            
    else:
        action = "Aucun plan d'action ne correspond aux choix effectués"
    for i in range(0, len(data)):
        if data[i] == None:
            data[i]='Aucun choix'    
    context={
        'recup':data,
        'filename':action,
        'natinf': natinf, 
        'paruinf':paruinf,
        'perc_sup':perc_sup,
        'rebondinf':rebondinf    }
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

