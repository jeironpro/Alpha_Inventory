from django.contrib import admin
from .models import RegistroUsuario, Articulos, Suplidores, Clientes, EncargadosCompras, EncargadosVentas, Marcas, Compras, Ventas

# Registra tus modelos aqui.
admin.site.register(RegistroUsuario)
admin.site.register(Articulos)
admin.site.register(Suplidores)
admin.site.register(Clientes)
admin.site.register(EncargadosCompras)
admin.site.register(EncargadosVentas)
admin.site.register(Marcas)
admin.site.register(Compras)
admin.site.register(Ventas)