from django import forms
from .models import RegistroUsuario, Articulos, Marcas, Suplidores, Clientes, EncargadosCompras, EncargadosVentas, Compras, Ventas

class RegistroUsuarioForm(forms.ModelForm):
    class Meta:
        model = RegistroUsuario
        fields = [
            'nombre',
            'apellido',
            'nombreUsuario',
            'direccion',
            'telefono',
            'correoElectronico',
            'contrasena'
        ]

class ArticulosForm(forms.ModelForm):
    class Meta:
        model = Articulos
        fields = [
            'codigo',
            'descripcion',
            'talla',
            'marca',
            'referencia',
            'ubicacion',
            'costo',
            'precio',
            'itbis',
            'cantidad',
            'unidadMedida',
            'usuario'
        ]
    
class EditarArticulosForm(forms.ModelForm):
    class Meta:
        model = Articulos
        fields = [
            'codigo',
            'descripcion',
            'talla',
            'marca',
            'referencia',
            'ubicacion',
            'costo',
            'precio',
            'itbis',
            'cantidad',
            'unidadMedida',
            'margenBeneficio',
            'usuario'
        ]

class MarcasForm(forms.ModelForm):
    class Meta:
        model = Marcas
        fields = [
            'marca',
            'usuario'
        ]

class EditarMarcasForm(forms.ModelForm):
    class Meta:
        model = Marcas
        fields = [
            'marca'
        ]

class SuplidoresForm(forms.ModelForm):
    class Meta:
        model = Suplidores
        fields = [
            'codigo',
            'nombre',
            'direccion',
            'ciudad',
            'telefono',
            'limiteCredito',
            'condiciones',
            'rnc',
            'descuento',
            'usuario'
        ]

class ClientesForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = [
            'codigo',
            'nombre',
            'direccion',
            'ciudad',
            'telefono',
            'cedula',
            'correoElectronico',
            'rnc',
            'descuento',
            'usuario'
        ]

class EncargadoComprasForm(forms.ModelForm):
    class Meta:
        model = EncargadosCompras
        fields = [
            'codigo',
            'encargadoCompra',
            'usuario'
        ]

class EditarEncargadoComprasForm(forms.ModelForm):
    class Meta:
        model = EncargadosCompras
        fields = [
            'encargadoCompra'
        ]

class EncargadoVentasForm(forms.ModelForm):
    class Meta:
        model = EncargadosVentas
        fields = [
            'codigo',
            'encargadoVenta',
            'usuario'
        ]

class EditarEncargadoVentasForm(forms.ModelForm):
    class Meta:
        model = EncargadosVentas
        fields = [
            'encargadoVenta'
        ]

class ComprasForm(forms.ModelForm):
    class Meta:
        model = Compras
        fields = [
            'horaCompra',
            'encargadoCompra',
            'suplidor',
            'codigo',
            'descripcion',
            'cantidad',
            'itbis',
            'costo',
            'usuario'
        ]

class VentasForm(forms.ModelForm):
    class Meta:
        model = Ventas
        fields = [
            'horaVenta',
            'encargadoVenta',
            'cliente',
            'codigo',
            'descripcion',
            'cantidad',
            'itbis',
            'precio',
            'usuario'
        ]

class PerfilForm(forms.ModelForm):
    class Meta:
        model = RegistroUsuario
        fields = [
            'nombreUsuario',
            'correoElectronico',
            'direccion',
            'telefono'
        ]