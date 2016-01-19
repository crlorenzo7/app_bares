from django.contrib import admin

from rango.models import Bares,Tapas,PerfilUsuario, MeGustaTapa

class BaresAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('nombre',)}

admin.site.register(Bares,BaresAdmin)
admin.site.register(Tapas,BaresAdmin)
admin.site.register(PerfilUsuario)
admin.site.register(MeGustaTapa)
