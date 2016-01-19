from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from rango.models import Bares, Tapas, PerfilUsuario, MeGustaTapa
from rango.forms import UserForm,UserProfileForm,FormularioTapas
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify



def index(request):
    lista_bares=Bares.objects.order_by('-numero_visitas')
    contexto={'bares':lista_bares}
    return render(request,'rango/index.html',contexto)

def bar(request,nombre_bar):
    
        
    contexto={}
    try:
        bar = Bares.objects.get(slug=nombre_bar)
        bar.numero_visitas=int(bar.numero_visitas)+1
        bar.save()
        contexto['nombre_bar']=nombre_bar
        lista_tapas=Tapas.objects.filter(bar=bar)
        if request.user:
            user=request.user
            if user.is_active:
                lista_gustas=MeGustaTapa.objects.filter(usuario=request.user)
                lmg=[]
                i=0
                for k in lista_gustas:
                    lmg.append(k.tapa)
                contexto['gustas']=lmg
        contexto['tapas']=lista_tapas
        contexto['bar']=bar
        contexto['form']=FormularioTapas()
    except:
        pass
    return render(request,'rango/bar-extend.html',contexto)

def registro(request):
    registrado=False
    contexto={}
    if request.method=='POST':
        dato=request.POST
        datos={}
        datos['username']=dato['username']
        datos['password']=dato['pass1']
        datos['email']=dato['email']

        user_form=UserForm(data=datos)
        if user_form.is_valid():
            password1=request.POST['pass1']
            password2=request.POST['pass2']
            
            if password1==password2:
                usuario= User.objects.get_or_create(username=request.POST['username'])[0]
                usuario.set_password(password1)
                usuario.email=request.POST['email']
                usuario.save()
                registrado=True
            
                user = authenticate(username=datos['username'], password=password1)
                login(request,user)
                return HttpResponseRedirect('/rango/')
            
    user_form=UserForm()
    return render(request,'rango/registrar.html',{'user_form':user_form,'registrado':registrado})

@login_required
def salir(request):
    logout(request)

    return HttpResponseRedirect('/rango/')

def entrar(request):
    if request.method=='POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/rango/')
        return HttpResponse("invalid password or username")
    return HttpResponseRedirect('/rango/')
    
def about(request):
    return HttpResponse("pagina de about")

def add_tapa(request):
    if request.method=='POST':
        dato=request.POST
        datos={}
        nbar=dato['nombre_bar']
        datos['nombre']=dato['nombre']
        datos['votos']=dato['votos']
        form = FormularioTapas(data=datos)
        bar = Bares.objects.get(slug=slugify(nbar))
        if form.is_valid():
            if Tapas.objects.filter(bar=bar,nombre=datos['nombre']).count()>0:
                contexto={}
                bar = Bares.objects.get(slug=slugify(nbar))
                bar.numero_visitas=int(bar.numero_visitas)+1
                bar.save()
                contexto['nombre_bar']=nbar
                lista_tapas=Tapas.objects.filter(bar=bar)
                if request.user:
                    user=request.user
                    if user.is_active:
                        lista_gustas=MeGustaTapa.objects.filter(usuario=request.user)
                        lmg=[]
                        i=0
                        for k in lista_gustas:
                            lmg.append(k.tapa)
                        contexto['gustas']=lmg
                contexto['tapas']=lista_tapas
                contexto['bar']=bar
                contexto['form']=form
                return render(request,'rango/bar-extend.html',contexto)
            else:
                tapa=Tapas.objects.get_or_create(bar=bar,nombre=datos['nombre'])[0]
                tapa.votos=datos['votos']
                if 'imagen' in request.FILES:
                    tapa.imagen=request.FILES['imagen']
                tapa.save()
                return HttpResponseRedirect('/rango/bar/'+slugify(nbar)+'/')
        else:
            contexto={}
            bar = Bares.objects.get(slug=slugify(nbar))
            bar.numero_visitas=int(bar.numero_visitas)+1
            bar.save()
            contexto['nombre_bar']=nbar
            lista_tapas=Tapas.objects.filter(bar=bar)
            if request.user:
                user=request.user
                if user.is_active:
                    lista_gustas=MeGustaTapa.objects.filter(usuario=request.user)
                    lmg=[]
                    i=0
                    for k in lista_gustas:
                        lmg.append(k.tapa)
                    contexto['gustas']=lmg
            contexto['tapas']=lista_tapas
            contexto['bar']=bar
            contexto['form']=form
            return render(request,'rango/bar-extend.html',contexto)
    else:
        return HttpResponseRedirect('/rango/')
    
def reclamar_datos(request):
    datos=Bares.objects.order_by('-numero_visitas')
    bares={};
    for k in range(len(datos)):
        bar={}
        datos_bar=str(datos[k]).split(',')
        bar['nombre']=datos_bar[0]
        bar['visitas']=datos_bar[len(datos_bar)-1]
        bares[k]=bar
    
  
   
    return JsonResponse(bares, safe=False)

def me_gusta(request):
    opcion=int(request.GET['opcion'])
    slug=str(request.GET['slug'])
    tapa=Tapas.objects.get(slug=slugify(slug))
    user=request.user
    iden=user.username+tapa.slug
    if opcion==1:
        tapa.votos=int(tapa.votos)+1
        tapa.save()
        
        megusta=MeGustaTapa.objects.get_or_create(usuario=user,tapa=tapa,identificador=iden)
       
    else:
        if(int(tapa.votos)!=0):
            tapa.votos=int(tapa.votos)-1
            tapa.save()
           
            megusta=MeGustaTapa.objects.get(identificador=iden)
            megusta.delete()
            
    return JsonResponse(tapa.votos,safe=False)
