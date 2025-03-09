from django.db import models
from django.contrib.auth.models import User

# Crea tus modelos aqui.
class RegistroUsuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    nombreUsuario = models.CharField(max_length=20, unique=True)
    direccion = models.CharField(max_length=80)
    telefono = models.CharField(max_length=10)
    correoElectronico = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=40)

    def __str__(self):
        return self.nombre + " " + self.apellido

class Articulos(models.Model):
    id_articulo = models.AutoField(primary_key=True)
    codigo = models.IntegerField()
    descripcion = models.CharField(max_length=100)
    talla = models.CharField(max_length=20)
    marca = models.CharField(max_length=20)
    referencia = models.CharField(max_length=80)
    ubicacion = models.CharField(max_length=20)
    costo = models.IntegerField()
    precio = models.IntegerField()
    itbis = models.IntegerField()
    cantidad = models.IntegerField()
    unidadMedida = models.CharField(max_length=8)
    margenBeneficio = models.IntegerField()
    usuario = models.ForeignKey(RegistroUsuario, on_delete=models.CASCADE) 

    def save(self):
        self.margenBeneficio = ((self.precio - self.costo) / self.precio) * 100
        super().save()

    def __str__(self):
        return self.descripcion

class Suplidores(models.Model):
    id_suplidor = models.AutoField(primary_key=True)
    codigo = models.IntegerField()
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=80)
    ciudad = models.CharField(max_length=20)
    telefono = models.CharField(max_length=10)
    limiteCredito = models.CharField(max_length=11)
    condiciones = models.CharField(max_length=50)
    rnc = models.IntegerField()
    descuento = models.CharField(max_length=4)
    usuario = models.ForeignKey(RegistroUsuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Clientes(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    codigo = models.IntegerField()
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=80)
    ciudad = models.CharField(max_length=20)
    telefono = models.CharField(max_length=10)
    cedula = models.CharField(max_length=11)
    correoElectronico = models.EmailField()
    rnc = models.IntegerField()
    descuento = models.CharField(max_length=4)
    usuario = models.ForeignKey(RegistroUsuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class EncargadosCompras(models.Model):
    id_encargadoCompra = models.AutoField(primary_key=True)
    codigo = models.IntegerField()
    encargadoCompra = models.CharField(max_length=50)
    usuario = models.ForeignKey(RegistroUsuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.encargadoCompra

class EncargadosVentas(models.Model):
    id_encargadoVenta = models.AutoField(primary_key=True)
    codigo = models.IntegerField()
    encargadoVenta = models.CharField(max_length=50)
    usuario = models.ForeignKey(RegistroUsuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.encargadoVenta

class Marcas(models.Model):
    id_marca = models.AutoField(primary_key=True)
    marca = models.CharField(max_length=50)
    usuario = models.ForeignKey(RegistroUsuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.marca

class Compras(models.Model):
    id_compra = models.AutoField(primary_key=True)
    horaCompra = models.TimeField(max_length=8)
    fechaCompra = models.DateField(auto_now_add=True)
    encargadoCompra = models.CharField(max_length=50)
    suplidor = models.CharField(max_length=50)
    codigo = models.IntegerField()
    descripcion = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    itbis = models.IntegerField()
    costo = models.IntegerField()
    totalCompra = models.IntegerField()
    usuario = models.ForeignKey(RegistroUsuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion

class Ventas(models.Model):
    id_venta = models.AutoField(primary_key=True)
    horaVenta = models.TimeField(max_length=8)
    fechaVenta = models.DateField(auto_now_add=True)
    encargadoVenta = models.CharField(max_length=50)
    cliente = models.CharField(max_length=50)
    codigo = models.IntegerField()
    descripcion = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    itbis = models.IntegerField()
    precio = models.IntegerField()
    totalVenta = models.IntegerField()
    usuario = models.ForeignKey(RegistroUsuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion