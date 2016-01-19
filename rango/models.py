from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class  Bares(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    direccion = models.CharField(max_length=150)
    numero_visitas = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super(Bares, self).save(*args, **kwargs)
    
    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return self.nombre+", "+self.direccion+", "+str(self.numero_visitas)
    
class Tapas(models.Model):
    bar = models.ForeignKey(Bares, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=60, unique=True)
    votos = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    imagen = models.ImageField(upload_to='img_tapas', blank=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super(Tapas, self).save(*args, **kwargs)
    
    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return self.nombre+", "+str(self.votos)

class PerfilUsuario(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    web = models.URLField(blank=True)
    imagen = models.ImageField(upload_to='img_perfil', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username

class MeGustaTapa(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tapa = models.ForeignKey(Tapas, on_delete=models.CASCADE)
    identificador=models.CharField(max_length=100,unique=True)
    
    def __unicode__(self):
        return str(self.identificador)+". "+str(self.usuario)+". "+str(self.tapa)