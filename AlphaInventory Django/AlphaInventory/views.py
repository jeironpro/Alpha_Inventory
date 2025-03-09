from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import RegistroUsuario, Articulos, Suplidores, Clientes, EncargadosCompras, EncargadosVentas, Marcas, Compras, Ventas
from .forms import RegistroUsuarioForm, ArticulosForm, EditarArticulosForm, MarcasForm, SuplidoresForm, ClientesForm, EncargadoComprasForm, EncargadoVentasForm, ComprasForm, VentasForm, PerfilForm, EditarMarcasForm, EditarEncargadoComprasForm, EditarEncargadoVentasForm
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str
from django.utils.encoding import force_bytes
from .tokens import generate_token
from django.urls import reverse_lazy

def index(request):
    if request.method == "POST":
        nombreUsuario = request.POST['nombreUsuario']
        contrasena = request.POST['contrasena']

        usuario = authenticate(username=nombreUsuario, password=contrasena)

        if usuario is not None:
            login(request, usuario)
            return redirect('inicio_inventario')
        else:
            messages.error(request, "Usuario o contrasena incorrecto")
            return redirect('index')
    return render(request, 'AlphaInventory/index.html')

def registro_usuario(request):
    if request.method == "POST":
        usuario = RegistroUsuarioForm(request.POST)
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        nombreUsuario = request.POST['nombreUsuario']
        correoElectronico = request.POST['correoElectronico']
        contrasena = request.POST['contrasena']
        contrasena_ = request.POST['contrasena-']

        if User.objects.filter(email=correoElectronico).exists():
            messages.error(request, "El correo electronico esta registrado")
            return redirect('registro_usuario')

        if User.objects.filter(username=nombreUsuario).exists():
            messages.error(request, "Este nombre de usuario esta registrado")
            return redirect('registro_usuario')

        if RegistroUsuario.objects.filter(correoElectronico=correoElectronico):
            messages.error(request, "El correo electronico esta registrado")
            return redirect('registro_usuario')

        if RegistroUsuario.objects.filter(nombreUsuario=nombreUsuario):
            messages.error(request, "Este nombre de usuario esta registrado")
            return redirect('registro_usuario')
        
        if len(nombreUsuario) > 20:
            messages.error(request, "El nombre de usuario debe tener maximo 20 caracteres ")
            return redirect('registro_usuario')
        
        if not nombreUsuario.isalnum():
            messages.error(request, "El nombre de usuario debe ser alfanumerico")
            return redirect('registro_usuario') 

        if nombreUsuario == (contrasena or contrasena_):
            messages.error(request, "El nombre de usuario no puede ser igual a la contrasena")
            return redirect('registro_usuario')

        if contrasena != contrasena_:
            messages.error(request, "Las contrasena no coinciden")
            return redirect('registro_usuario')

        if usuario.is_valid():
            usuario.save()
        
        usuario_auth = User.objects.create_user(nombreUsuario, correoElectronico, contrasena)
        usuario_auth.first_name = nombre
        usuario_auth.last_name = apellido
        usuario_auth.is_active = False
        usuario_auth.save()

        messages.success(request, "Tu cuenta se ha creado sastifactoriamente!!! Por favor, revise su correo electronico para poder activar su cuenta.")

        subject = "Bienvend@ a Alpha Inventory!!!"
        message = "Hola " + usuario_auth.first_name + "!!! \n" + "Bienvenid@ a Alpha Invetory. \nGracias por registrarse en nuestra aplicacion.\nLe hemos enviado un correo electrónico de confirmación, por favor confirme su dirección de correo electrónico. \n\nAlpha Inventory"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [usuario_auth.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        current_site = get_current_site(request)
        email_subject = "Confirma tu correo!!!"
        message2 = render_to_string('email_confirmacion.html',{
            
            'name': usuario_auth.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(usuario_auth.pk)),
            'token': generate_token.make_token(usuario_auth)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [usuario_auth.email],
        )
        email.fail_silently = True
        email.send()
        return redirect('index')
    return render(request, 'AlphaInventory/registrousuario.html')

def activador(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        usuario_auth = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        usuario_auth = None

    if usuario_auth is not None and generate_token.check_token(usuario_auth,token):
        usuario_auth.is_active = True
        usuario_auth.is_staff = True
        usuario_auth.is_superuser = True
        usuario_auth.save()
        login(request,usuario_auth)
        messages.success(request, "Tu cuenta ha sido activada!!!")
        return redirect('index')
    else:
        messages.success(request, "Su cuenta no esta activada. Asegurese de activarla antes de iniciar sesion.")
        return render(request,'activation_failed.html')

def olvidar_usuario_contrasena(request):
    if request.method == 'POST':
        correoElectronico = request.POST['correo_rc']
        usuario = RegistroUsuario.objects.filter(correoElectronico=correoElectronico).exists()

        if not usuario:
            messages.error(request, "EL correo electronico no esta registrado")
            return redirect('index')
        else:
            usuario_rc = User.objects.get(email=correoElectronico)
            current_site = get_current_site(request)
            email_subject = "Restablecer contraseña"
            message2 = render_to_string('restablecer_contrasena.html',{
                
                'name': usuario_rc.first_name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(usuario_rc.pk)),
                'token': generate_token.make_token(usuario_rc)
            })
            email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [usuario_rc.email],
            )
            email.fail_silently = True
            email.send()
            return redirect('index')
    return render(request, 'AlphaInventory/index.html', {'usuario':usuario})

@login_required()
def inicio_inventario(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    return render(request, 'AlphaInventory/inicio_inventario.html', {'usuario':usuario})

def encargado_compras_inicio_inventario(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoCompra = request.POST['encargadoCompra']
        if EncargadosCompras.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de compras ya esta registrado")
            return redirect('inicio_inventario')
        if EncargadosCompras.objects.filter(encargadoCompra=encargadoCompra).exists():
            messages.error(request, "Este encargado de compras ya esta registrado")
            return redirect('inicio_inventario')
        else:
            encargado_compra = EncargadoComprasForm(request.POST)
            if encargado_compra.is_valid():
                encargado_compra.save()
                return redirect('inicio_inventario')
    return render(request, 'AlphaInventory/inicio_inventario.html',{'usuario':usuario})

def encargado_ventas_inicio_inventario(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoVenta = request.POST['encargadoVenta']
        if EncargadosVentas.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de ventas ya esta registrado")
            return redirect('inicio_inventario')
        if EncargadosVentas.objects.filter(encargadoVenta=encargadoVenta).exists():
            messages.error(request, "Este encargado de ventas ya esta registrado")
            return redirect('inicio_inventario')
        else:
            encargado_venta = EncargadoVentasForm(request.POST)
            if encargado_venta.is_valid():
                encargado_venta.save()
                return redirect('inicio_inventario')
    return render(request, 'AlphaInventory/inicio_inventario.html', {'usuario':usuario})

@login_required()
def cerrar_sesion(request):
    logout(request)
    return redirect('index')

def registro_articulos(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    marcas = Marcas.objects.filter(usuario_id=request.user.id)
    if request.method == "POST":
        costo = request.POST['costo']
        precio = request.POST['precio']
        codigo = request.POST['codigo']
        itbis = request.POST['itbis']
        unidadMedida = request.POST['unidadMedida']

        if Articulos.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de articulo esta registrado")
            return redirect('registrodearticulos')
        if costo >= precio:
            messages.error(request, "El costo no puede ser mayor al precio")
            return redirect('registrodearticulos')
        if itbis != ('18' or '16' or '0'):
            messages.error(request, "Debe seleccionar el itbis")
            return redirect('registrodearticulos')
        if unidadMedida != ('docenas' or 'unidades'):
            messages.error(request, "Dede seleccionar la unidad de medida")
            return redirect('registrodearticulos')
        else:
            articulo = ArticulosForm(request.POST)
            if articulo.is_valid():
                articulo.save()
                if articulo.save():
                    marca = MarcasForm(request.POST)
                    marcaV = request.POST['marca']
                    verificarMarca = Marcas.objects.filter(marca=marcaV).exists()
                    if not verificarMarca and marca.is_valid():
                        marca.save()
                return redirect('registrodearticulos')
    else:
        articulo = ArticulosForm()
        marca = MarcasForm()
    return render(request, 'AlphaInventory/registrodearticulos.html',{'usuario':usuario, 'marcas':marcas})

def editar_articulo(request, id_articulo):
    articulo = Articulos.objects.get(id_articulo=id_articulo)
    marcas = Marcas.objects.filter(usuario_id=request.user.id)
    if request.method == "POST":
        articuloform = EditarArticulosForm(request.POST, instance=articulo)
        if articuloform.is_valid():
            articuloform.save()
            return redirect('listadodearticulos')
    else:
        articuloform = EditarArticulosForm(instance=articulo)
    return render(request, 'AlphaInventory/editararticulo.html', {'articulo':articulo, 'marcas':marcas,'articuloform':articuloform}) 

def eliminar_articulo(request, id_articulo):
    articulo = Articulos.objects.filter(id_articulo=id_articulo)
    if request.method == "POST" or "GET":
        articulo.delete()
        return redirect('listadodearticulos')

def editar_marca(request, id_marca):
    marcaE = get_object_or_404(Marcas, id_marca=id_marca)
    if request.method == "POST":
        marcaform = EditarMarcasForm(request.POST, instance=marcaE)
        if marcaform.is_valid():
            marcaform.save()
            return redirect('registrodearticulos')
    else:
        marcaform = EditarMarcasForm(instance=marcaE)
    return render(request, 'AlphaInventory/registrodearticulos.html', {'marcaE':marcaE, 'marcaform':marcaform})

def eliminar_marca(request, id_marca):
    marca = Marcas.objects.filter(id_marca=id_marca)
    if request.method == "POST" or "GET":
        marca.delete()
        return redirect('registrodearticulos')
    
def encargado_compras_registro_articulos(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoCompra = request.POST['encargadoCompra']
        if EncargadosCompras.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de compras ya esta registrado")
            return redirect('registrodearticulos')
        if EncargadosCompras.objects.filter(encargadoCompra=encargadoCompra).exists():
            messages.error(request, "Este encargado de compras ya esta registrado")
            return redirect('registrodearticulos')
        else:
            encargado_compra = EncargadoComprasForm(request.POST)
            if encargado_compra.is_valid():
                encargado_compra.save()
                return redirect('registrodearticulos')
    return render(request, 'AlphaInventory/registrodearticulos.html',{'usuario':usuario})

def encargado_ventas_registro_articulos(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoVenta = request.POST['encargadoVenta']
        if EncargadosVentas.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de ventas ya esta registrado")
            return redirect('registrodearticulos')
        if EncargadosVentas.objects.filter(encargadoVenta=encargadoVenta).exists():
            messages.error(request, "Este encargado de ventas ya esta registrado")
            return redirect('registrodearticulos')
        else:
            encargado_venta = EncargadoVentasForm(request.POST)
            if encargado_venta.is_valid():
                encargado_venta.save()
                return redirect('registrodearticulos')
    return render(request, 'AlphaInventory/registrodearticulos.html', {'usuario':usuario})

@login_required()
def registro_suplidores(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        nombre = request.POST['nombre']
        if Suplidores.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de suplidor ya esta registrado")
            return redirect('registrodesuplidores')
        if Suplidores.objects.filter(nombre=nombre).exists():
            messages.error(request, "Este suplidor ya esta registrado")
            return redirect('registrodesuplidores')
        else:
            suplidor = SuplidoresForm(request.POST)
            if suplidor.is_valid():
                suplidor.save()
                return redirect('registrodesuplidores')
    return render(request, 'AlphaInventory/registrodesuplidores.html', {'usuario':usuario})

def editar_suplidor(request, id_suplidor):
    suplidor = Suplidores.objects.get(id_suplidor=id_suplidor)
    if request.method == "POST":
        suplidorform = SuplidoresForm(request.POST, instance=suplidor)
        if suplidorform.is_valid():
            suplidorform.save()
            return redirect('listadodesuplidores')
    else:
        suplidorform = SuplidoresForm(instance=suplidor)
    return render(request, 'AlphaInventory/editarsuplidor.html', {'suplidor':suplidor,'suplidorform':suplidorform}) 

def eliminar_suplidor(request, id_suplidor):
    suplidor = Suplidores.objects.filter(id_suplidor=id_suplidor)
    if request.method == "POST" or "GET":
        suplidor.delete()
        return redirect('listadodesuplidores')

def encargado_compras_registro_suplidores(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoCompra = request.POST['encargadoCompra']
        if EncargadosCompras.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de compras ya esta registrado")
            return redirect('registrodesuplidores')
        if EncargadosCompras.objects.filter(encargadoCompra=encargadoCompra).exists():
            messages.error(request, "Este encargado de compras ya esta registrado")
            return redirect('registrodesuplidores')
        else:
            encargado_compra = EncargadoComprasForm(request.POST)
            if encargado_compra.is_valid():
                encargado_compra.save()
                return redirect('registrodesuplidores')
    return render(request, 'AlphaInventory/registrodesuplidores.html',{'usuario':usuario})

def encargado_ventas_registro_suplidores(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoVenta = request.POST['encargadoVenta']
        if EncargadosVentas.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de ventas ya esta registrado")
            return redirect('registrodesuplidores')
        if EncargadosVentas.objects.filter(encargadoVenta=encargadoVenta).exists():
            messages.error(request, "Este encargado de ventas ya esta registrado")
            return redirect('registrodesuplidores')
        else:
            encargado_venta = EncargadoVentasForm(request.POST)
            if encargado_venta.is_valid():
                encargado_venta.save()
                return redirect('registrodesuplidores')
    return render(request, 'AlphaInventory/registrodesuplidores.html', {'usuario':usuario})

# Ready
@login_required()
def registro_clientes(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        nombre = request.POST['nombre']
        if Clientes.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de cliente ya esta registrado")
            return redirect('registrodeclientes')
        if Clientes.objects.filter(nombre=nombre).exists():
            messages.error(request, "Este cliente ya esta registrado")
            return redirect('registrodeclientes')
        else:
            cliente = ClientesForm(request.POST)
            if cliente.is_valid():
                cliente.save()
                return redirect('registrodeclientes')
    return render(request, 'AlphaInventory/registrodeclientes.html', {'usuario':usuario})

def editar_cliente(request, id_cliente):
    cliente = Clientes.objects.get(id_cliente=id_cliente)
    if request.method == "POST":
        clienteform = ClientesForm(request.POST, instance=cliente)
        if clienteform.is_valid():
            clienteform.save()
            return redirect('listadodeclientes')
    else:
        clienteform = ClientesForm(instance=cliente)
    return render(request, 'AlphaInventory/editarcliente.html', {'cliente':cliente,'clienteform':clienteform}) 

def eliminar_cliente(request, id_cliente):
    cliente = Clientes.objects.filter(id_cliente=id_cliente)
    if request.method == "POST" or "GET":
        cliente.delete()
        return redirect('listadodeclientes')

def encargado_compras_registro_clientes(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoCompra = request.POST['encargadoCompra']
        if EncargadosCompras.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de compras ya esta registrado")
            return redirect('registrodeclientes')
        if EncargadosCompras.objects.filter(encargadoCompra=encargadoCompra).exists():
            messages.error(request, "Este encargado de compras ya esta registrado")
            return redirect('registrodeclientes')
        else:
            encargado_compra = EncargadoComprasForm(request.POST)
            if encargado_compra.is_valid():
                encargado_compra.save()
                return redirect('registrodeclientes')
    return render(request, 'AlphaInventory/registrodeclientes.html',{'usuario':usuario})

def encargado_ventas_registro_clientes(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoVenta = request.POST['encargadoVenta']
        if EncargadosVentas.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de ventas ya esta registrado")
            return redirect('registrodeclientes')
        if EncargadosVentas.objects.filter(encargadoVenta=encargadoVenta).exists():
            messages.error(request, "Este encargado de ventas ya esta registrado")
            return redirect('registrodeclientes')
        else:
            encargado_venta = EncargadoVentasForm(request.POST)
            if encargado_venta.is_valid():
                encargado_venta.save()
                return redirect('registrodeclientes')
    return render(request, 'AlphaInventory/registrodeclientes.html', {'usuario':usuario})

def compras(request):
    compra = Compras.objects.filter(usuario_id=request.user.id)
    usuario = RegistroUsuario.objects.filter(id_usuario=request.user.id)
    usuarioC = RegistroUsuario.objects.get(id_usuario=request.user.id)
    suplidores = Suplidores.objects.filter(usuario_id=request.user.id)
    encargadoCompras = EncargadosCompras.objects.filter(usuario_id=request.user.id)
    articulos = Articulos.objects.filter(usuario_id=request.user.id)
    hora = datetime.now()
    horaCompra = hora.strftime("%H:%M:%S")
    if request.method == "POST":
        suplidor = request.POST['suplidor']
        encargado_compra = request.POST['encargadoCompra']
        codigo = request.POST['codigo']
        descripcion = request.POST['descripcion']
        itbis = request.POST['itbis']
        cantidad = request.POST['cantidad']
        costo = request.POST['costo']

        codigo_ = request.POST['codigo_']
        descripcion_ = request.POST['descripcion_']
        itbis_ = request.POST['itbis_']
        cantidad_ = request.POST['cantidad_']
        costo_ = request.POST['costo_']

        codigo__ = request.POST['codigo__']
        descripcion__ = request.POST['descripcion__']
        itbis__ = request.POST['itbis__']
        cantidad__ = request.POST['cantidad__']
        costo__ = request.POST['costo__']

        codigo___ = request.POST['codigo___']
        descripcion___ = request.POST['descripcion___']
        itbis___ = request.POST['itbis___']
        cantidad___ = request.POST['cantidad___']
        costo___ = request.POST['costo___']

        codigo____ = request.POST['codigo____']
        descripcion____ = request.POST['descripcion____']
        itbis____ = request.POST['itbis____']
        cantidad____ = request.POST['cantidad____']
        costo____ = request.POST['costo____']

        codigo_____ = request.POST['codigo_____']
        descripcion_____ = request.POST['descripcion_____']
        itbis_____ = request.POST['itbis_____']
        cantidad_____ = request.POST['cantidad_____']
        costo_____ = request.POST['costo_____']

        codigo______ = request.POST['codigo______']
        descripcion______ = request.POST['descripcion______']
        itbis______ = request.POST['itbis______']
        cantidad______ = request.POST['cantidad______']
        costo______ = request.POST['costo______'] 

        compra = ComprasForm(request.POST)

        if not Suplidores.objects.filter(nombre=suplidor).exists():
            messages.error(request, "Este suplidor no existe")
            return redirect('compras')
        if not EncargadosCompras.objects.filter(encargadoCompra=encargado_compra).exists():
            messages.error(request, "Este encargado de compras no existe")
            return redirect('compras')
        if not Articulos.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de la casilla 1 de articulo no existe")
            return redirect('compras')
        if not Articulos.objects.filter(descripcion=descripcion, codigo=codigo):
            messages.error(request, "Esta no es la descripcion de la casilla 1 del articulo")
            return redirect('compras')
        if not Articulos.objects.filter(itbis=itbis, codigo=codigo):
            messages.error(request, "Este no es el itbis de la casilla 1 del articulo")
            return redirect('compras')
        if not Articulos.objects.filter(costo=costo, codigo=codigo):
            messages.error(request, "Este no es el costo de la casilla 1 del articulo")
            return redirect('compras')
        
        if codigo_ != "" and Articulos.objects.exclude(codigo=codigo_):
            messages.error(request, "Este codigo de la casiila 2 de articulo no existe")
            return redirect('compras')
        if (descripcion_ != "" and codigo_ != "") and Articulos.objects.exclude(descripcion=descripcion_, codigo=codigo_):
            messages.error(request, "Esta no es la descripcion de la casiila 2 del articulo")
            return redirect('compras')
        if (itbis_ != "" and codigo_ != "") and Articulos.objects.exclude(itbis=itbis_, codigo=codigo_):
            messages.error(request, "Este no es el itbis de la casiila 2 del articulo")
            return redirect('compras')
        if (costo_ != "" and codigo_ != "") and Articulos.objects.exclude(costo=costo_, codigo=codigo_):
            messages.error(request, "Este no es el costo de la casiila 2 del articulo")
            return redirect('compras')
        
        if (codigo__ != "") and Articulos.objects.exclude(codigo=codigo__):
            messages.error(request, "Este codigo de la casilla 3 de articulo no existe")
            return redirect('compras')
        if (descripcion__ != "" and codigo__ != "") and Articulos.objects.exclude(descripcion=descripcion__, codigo=codigo__):
            messages.error(request, "Esta no es la descripcion de la casilla 3 del articulo")
            return redirect('compras')
        if (itbis__ != "" and codigo__ != "") and Articulos.objects.exclude(itbis=itbis__, codigo_=codigo__):
            messages.error(request, "Este no es el itbis de la casilla 3 del articulo")
            return redirect('compras')
        if (costo__ != "" and codigo__ != "") and Articulos.objects.exclude(costo=costo__, codigo=codigo__):
            messages.error(request, "Este no es el costo de la casilla 3 del articulo")
            return redirect('compras')
        
        if (codigo___ != "") and Articulos.objects.exclude(codigo=codigo___):
            messages.error(request, "Este codigo de la casilla 4 de articulo no existe")
            return redirect('compras')
        if (descripcion___ and codigo___ != "") and Articulos.objects.exclude(descripcion=descripcion___, codigo=codigo___):
            messages.error(request, "Esta no es la descripcion de la casilla 4 del articulo")
            return redirect('compras')
        if (itbis___ != "" and codigo___ != "") and Articulos.objects.exclude(itbis=itbis___, codigo_=codigo___):
            messages.error(request, "Este no es el itbis de la casilla 4 del articulo")
            return redirect('compras')
        if (costo___ != "" and codigo___ != "") and Articulos.objects.exclude(costo=costo___, codigo=codigo___):
            messages.error(request, "Este no es el costo de la casilla 4 del articulo")
            return redirect('compras')
        
        if (codigo____ != "") and Articulos.objects.exclude(codigo=codigo____):
            messages.error(request, "Este codigo de la casilla 5 de articulo no existe")
            return redirect('compras')
        if (descripcion____ != "" and codigo____ != "") and Articulos.objects.exclude(descripcion=descripcion____, codigo=codigo____):
            messages.error(request, "Esta no es la descripcion de la casilla 5 del articulo")
            return redirect('compras')
        if (itbis____ != "" and codigo____ != "") and Articulos.objects.exclude(itbis=itbis____, codigo_=codigo____):
            messages.error(request, "Este no es el itbis de la casilla 5 del articulo")
            return redirect('compras')
        if (costo____ != "" and codigo____ != "") and Articulos.objects.exclude(costo=costo____, codigo=codigo____):
            messages.error(request, "Este no es el costo de la casilla 5 del articulo")
            return redirect('compras')
        
        if (codigo_____ != "") and Articulos.objects.exclude(codigo=codigo_____):
            messages.error(request, "Este codigo de la casilla 6 de articulo no existe")
            return redirect('compras')
        if (descripcion_____ != "" and codigo_____ != "") and Articulos.objects.exclude(descripcion=descripcion_____, codigo=codigo_____):
            messages.error(request, "Esta no es la descripcion de la casilla 6 del articulo")
            return redirect('compras')
        if (itbis_____ != "" and codigo_____ != "") and Articulos.objects.exclude(itbis=itbis_____, codigo_=codigo_____):
            messages.error(request, "Este no es el itbis de la casilla 6 del articulo")
            return redirect('compras')
        if (costo_____ != "" and codigo_____ != "") and Articulos.objects.exclude(costo=costo_____, codigo=codigo_____):
            messages.error(request, "Este no es el costo de la casilla 6 del articulo")
            return redirect('compras')
        
        if (codigo______ != "") and Articulos.objects.exclude(codigo=codigo______):
            messages.error(request, "Este codigo de la casilla 7 de articulo no existe")
            return redirect('compras')
        if (descripcion______ != "" and codigo______ != "") and Articulos.objects.exclude(descripcion=descripcion______, codigo=codigo______):
            messages.error(request, "Esta no es la descripcion de la casilla 7 del articulo")
            return redirect('compras')
        if (itbis______ != "" and codigo______ != "") and Articulos.objects.exclude(itbis=itbis______, codigo_=codigo______):
            messages.error(request, "Este no es el itbis de la casilla 7 del articulo")
            return redirect('compras')
        if (costo______ != "" and codigo______ != "") and Articulos.objects.exclude(costo=costo______, codigo=codigo______):
            messages.error(request, "Este no es el costo de la casilla 7 del articulo")
            return redirect('compras')
        
        if compra.is_valid():

            if codigo and descripcion and cantidad and itbis and costo and codigo_ and descripcion_ and cantidad_ and itbis_ and costo_ and codigo__ and descripcion__ and cantidad__ and itbis__ and costo__ and codigo___ and descripcion___ and cantidad___ and itbis___ and costo___ and codigo____ and descripcion____ and cantidad____ and itbis____ and costo____ and codigo____ and descripcion_____ and cantidad_____ and itbis_____ and costo_____ and codigo______ and descripcion______ and cantidad______ and itbis______ and costo______:
                itbisC = int(itbis) / 100
                itbisC_ = int(itbis_) / 100
                itbisC__ = int(itbis__) / 100
                itbisC___ = int(itbis___) / 100
                itbisC____ = int(itbis____) / 100
                itbisC_____ = int(itbis_____) / 100
                itbisC______ = int(itbis______) / 100
                compraG = [
                    Compras(horaCompra=horaCompra,encargadoCompra=encargado_compra, suplidor=suplidor, codigo=codigo, descripcion=descripcion, cantidad=cantidad, itbis=itbis, costo=costo, totalCompra=(int(cantidad)*int(costo)) * itbisC + (int(cantidad)*int(costo)), usuario=usuarioC),
                    Compras(horaCompra=horaCompra,encargadoCompra=encargado_compra, suplidor=suplidor, codigo=codigo_, descripcion=descripcion_, cantidad=cantidad_, itbis=itbis_, costo=costo_, totalCompra=(int(cantidad_)*int(costo_)) * itbisC_ + (int(cantidad_)*int(costo_)), usuario=usuarioC),
                    Compras(horaCompra=horaCompra,encargadoCompra=encargado_compra, suplidor=suplidor, codigo=codigo__, descripcion=descripcion__, cantidad=cantidad__, itbis=itbis__, costo=costo__, totalCompra=(int(cantidad__)*int(costo__)) * itbisC__ + (int(cantidad__)*int(costo__)), usuario=usuarioC),
                    Compras(horaCompra=horaCompra,encargadoCompra=encargado_compra, suplidor=suplidor, codigo=codigo___, descripcion=descripcion___, cantidad=cantidad___, itbis=itbis___, costo=costo___, totalCompra=(int(cantidad___)*int(costo___)) * itbisC___ + (int(cantidad___)*int(costo___)), usuario=usuarioC),
                    Compras(horaCompra=horaCompra,encargadoCompra=encargado_compra, suplidor=suplidor, codigo=codigo____, descripcion=descripcion____, cantidad=cantidad____, itbis=itbis____, costo=costo____, totalCompra=(int(cantidad____)*int(costo____)) * itbisC____ + (int(cantidad____)*int(costo____)), usuario=usuarioC),
                    Compras(horaCompra=horaCompra,encargadoCompra=encargado_compra, suplidor=suplidor, codigo=codigo_____, descripcion=descripcion_____, cantidad=cantidad_____, itbis=itbis_____, costo=costo_____, totalCompra=(int(cantidad_____)*int(costo_____)) * itbisC_____ + (int(cantidad_____)*int(costo_____)), usuario=usuarioC),
                    Compras(horaCompra=horaCompra,encargadoCompra=encargado_compra, suplidor=suplidor, codigo=codigo______, descripcion=descripcion______, cantidad=cantidad______, itbis=itbis______, costo=costo______, totalCompra=(int(cantidad______)*int(costo______)) * itbisC______ + (int(cantidad______)*int(costo______)), usuario=usuarioC)
                ]
                Compras.objects.bulk_create(compraG)

                articulo = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo)
                articulo.cantidad = (int(articulo.cantidad) + int(cantidad))
                articulo.save()

                articulo_ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo_)
                articulo_.cantidad = (int(articulo.cantidad) + int(cantidad_))
                articulo_.save()

                articulo__ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo__)
                articulo__.cantidad = (int(articulo.cantidad) + int(cantidad__))
                articulo__.save()

                articulo___ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo___)
                articulo___.cantidad = (int(articulo.cantidad) + int(cantidad___))
                articulo___.save()

                articulo____ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo____)
                articulo____.cantidad = (int(articulo.cantidad) + int(cantidad____))
                articulo____.save()

                articulo_____ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo_____)
                articulo_____.cantidad = (int(articulo.cantidad) + int(cantidad_____))
                articulo_____.save()

                articulo______ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo______)
                articulo______.cantidad = (int(articulo.cantidad) + int(cantidad______))
                articulo______.save()

            elif codigo and descripcion and cantidad and itbis and costo and codigo_ and descripcion_ and cantidad_ and itbis_ and costo_ and codigo__ and descripcion__ and cantidad__ and itbis__ and costo__ and codigo___ and descripcion___ and cantidad___ and itbis___ and costo___ and codigo____ and descripcion____ and cantidad____ and itbis____ and costo____ and codigo____ and descripcion_____ and cantidad_____ and itbis_____ and costo_____:
                itbisC = int(itbis) / 100
                itbisC_ = int(itbis_) / 100
                itbisC__ = int(itbis__) / 100
                itbisC___ = int(itbis___) / 100
                itbisC____ = int(itbis____) / 100
                itbisC_____ = int(itbis_____) / 100
                compraF = [
                    Compras(horaCompra=horaCompra,encargadoCompra=encargado_compra, suplidor=suplidor, codigo=codigo, descripcion=descripcion, cantidad=cantidad, itbis=itbis, costo=costo, totalCompra=(int(cantidad)*int(costo)) * itbisC + (int(cantidad)*int(costo)), usuario=usuarioC),
                    Compras(horaCompra=horaCompra,encargadoCompra=encargado_compra, suplidor=suplidor, codigo=codigo_, descripcion=descripcion_, cantidad=cantidad_, itbis=itbis_, costo=costo_, totalCompra=(int(cantidad_)*int(costo_)) * itbisC_ + (int(cantidad_)*int(costo_)), usuario=usuarioC),
                    Compras(horaCompra=horaCompra,encargadoCompra=encargado_compra, suplidor=suplidor, codigo=codigo__, descripcion=descripcion__, cantidad=cantidad__, itbis=itbis__, costo=costo__, totalCompra=(int(cantidad__)*int(costo__)) * itbisC__ + (int(cantidad__)*int(costo__)), usuario=usuarioC),
                    Compras(horaCompra=horaCompra,encargadoCompra=encargado_compra, suplidor=suplidor, codigo=codigo___, descripcion=descripcion___, cantidad=cantidad___, itbis=itbis___, costo=costo___, totalCompra=(int(cantidad___)*int(costo___)) * itbisC___ + (int(cantidad___)*int(costo___)), usuario=usuarioC),
                    Compras(horaCompra=horaCompra,encargadoCompra=encargado_compra, suplidor=suplidor, codigo=codigo____, descripcion=descripcion____, cantidad=cantidad____, itbis=itbis____, costo=costo____, totalCompra=(int(cantidad____)*int(costo____)) * itbisC____ + (int(cantidad____)*int(costo____)), usuario=usuarioC),
                    Compras(horaCompra=horaCompra,encargadoCompra=encargado_compra, suplidor=suplidor, codigo=codigo_____, descripcion=descripcion_____, cantidad=cantidad_____, itbis=itbis_____, costo=costo_____, totalCompra=(int(cantidad_____)*int(costo_____)) * itbisC_____ + (int(cantidad_____)*int(costo_____)), usuario=usuarioC)
                ]
                Compras.objects.bulk_create(compraF)

                articulo = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo)
                articulo.cantidad = (int(articulo.cantidad) + int(cantidad))
                articulo.save()

                articulo_ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo_)
                articulo_.cantidad = (int(articulo.cantidad) + int(cantidad_))
                articulo_.save()

                articulo__ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo__)
                articulo__.cantidad = (int(articulo.cantidad) + int(cantidad__))
                articulo__.save()

                articulo___ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo___)
                articulo___.cantidad = (int(articulo.cantidad) + int(cantidad___))
                articulo___.save()

                articulo____ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo____)
                articulo____.cantidad = (int(articulo.cantidad) + int(cantidad____))
                articulo____.save()

                articulo_____ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo_____)
                articulo_____.cantidad = (int(articulo.cantidad) + int(cantidad_____))
                articulo_____.save()

            elif codigo and descripcion and cantidad and itbis and costo and codigo_ and descripcion_ and cantidad_ and itbis_ and costo_ and codigo__ and descripcion__ and cantidad__ and itbis__ and costo__ and codigo___ and descripcion___ and cantidad___ and itbis___ and costo___ and codigo____ and descripcion____ and cantidad____ and itbis____ and costo____:
                itbisC = int(itbis) / 100
                itbisC_ = int(itbis_) / 100
                itbisC__ = int(itbis__) / 100
                itbisC___ = int(itbis___) / 100
                itbisC____ = int(itbis____) / 100
                compraE = [
                    Compras(horaCompra=horaCompra,encargadoCompra=encargado_compra, suplidor=suplidor, codigo=codigo, descripcion=descripcion, cantidad=cantidad, itbis=itbis, costo=costo, totalCompra=(int(cantidad)*int(costo)) * itbisC + (int(cantidad)*int(costo)), usuario=usuarioC),
                    Compras(horaCompra=horaCompra,encargadoCompra=encargado_compra, suplidor=suplidor, codigo=codigo_, descripcion=descripcion_, cantidad=cantidad_, itbis=itbis_, costo=costo_, totalCompra=(int(cantidad_)*int(costo_)) * itbisC_ + (int(cantidad_)*int(costo_)), usuario=usuarioC),
                    Compras(horaCompra=horaCompra,encargadoCompra=encargado_compra, suplidor=suplidor, codigo=codigo__, descripcion=descripcion__, cantidad=cantidad__, itbis=itbis__, costo=costo__, totalCompra=(int(cantidad__)*int(costo__)) * itbisC__ + (int(cantidad__)*int(costo__)), usuario=usuarioC),
                    Compras(horaCompra=horaCompra,encargadoCompra=encargado_compra, suplidor=suplidor, codigo=codigo___, descripcion=descripcion___, cantidad=cantidad___, itbis=itbis___, costo=costo___, totalCompra=(int(cantidad___)*int(costo___)) * itbisC___ + (int(cantidad___)*int(costo___)), usuario=usuarioC),
                    Compras(horaCompra=horaCompra,encargadoCompra=encargado_compra, suplidor=suplidor, codigo=codigo____, descripcion=descripcion____, cantidad=cantidad____, itbis=itbis____, costo=costo____, totalCompra=(int(cantidad____)*int(costo____)) * itbisC____ + (int(cantidad____)*int(costo____)), usuario=usuarioC)
                ]
                Compras.objects.bulk_create(compraE)

                articulo = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo)
                articulo.cantidad = (int(articulo.cantidad) + int(cantidad))
                articulo.save()

                articulo_ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo_)
                articulo_.cantidad = (int(articulo.cantidad) + int(cantidad_))
                articulo_.save()

                articulo__ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo__)
                articulo__.cantidad = (int(articulo.cantidad) + int(cantidad__))
                articulo__.save()

                articulo___ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo___)
                articulo___.cantidad = (int(articulo.cantidad) + int(cantidad___))
                articulo___.save()

                articulo____ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo____)
                articulo____.cantidad = (int(articulo.cantidad) + int(cantidad____))
                articulo____.save()

            elif codigo and descripcion and cantidad and itbis and costo and codigo_ and descripcion_ and cantidad_ and itbis_ and costo_ and codigo__ and descripcion__ and cantidad__ and itbis__ and costo__ and codigo___ and descripcion___ and cantidad___ and itbis___ and costo___:
                itbisC = int(itbis) / 100
                itbisC_ = int(itbis_) / 100
                itbisC__ = int(itbis__) / 100
                itbisC___ = int(itbis___) / 100
                compraD = [
                    Compras(horaCompra=horaCompra,encargadoCompra=encargado_compra, suplidor=suplidor, codigo=codigo, descripcion=descripcion, cantidad=cantidad, itbis=itbis, costo=costo, totalCompra=(int(cantidad)*int(costo)) * itbisC + (int(cantidad)*int(costo)), usuario=usuarioC),
                    Compras(horaCompra=horaCompra,encargadoCompra=encargado_compra, suplidor=suplidor, codigo=codigo_, descripcion=descripcion_, cantidad=cantidad_, itbis=itbis_, costo=costo_, totalCompra=(int(cantidad_)*int(costo_)) * itbisC_ + (int(cantidad_)*int(costo_)), usuario=usuarioC),
                    Compras(horaCompra=horaCompra,encargadoCompra=encargado_compra, suplidor=suplidor, codigo=codigo__, descripcion=descripcion__, cantidad=cantidad__, itbis=itbis__, costo=costo__, totalCompra=(int(cantidad__)*int(costo__)) * itbisC__ + (int(cantidad__)*int(costo__)), usuario=usuarioC),
                    Compras(horaCompra=horaCompra,encargadoCompra=encargado_compra, suplidor=suplidor, codigo=codigo___, descripcion=descripcion___, cantidad=cantidad___, itbis=itbis___, costo=costo___, totalCompra=(int(cantidad___)*int(costo___)) * itbisC___ + (int(cantidad___)*int(costo___)), usuario=usuarioC)
                ]
                Compras.objects.bulk_create(compraD)

                articulo = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo)
                articulo.cantidad = (int(articulo.cantidad) + int(cantidad))
                articulo.save()

                articulo_ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo_)
                articulo_.cantidad = (int(articulo.cantidad) + int(cantidad_))
                articulo_.save()

                articulo__ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo__)
                articulo__.cantidad = (int(articulo.cantidad) + int(cantidad__))
                articulo__.save()

                articulo___ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo___)
                articulo___.cantidad = (int(articulo.cantidad) + int(cantidad___))
                articulo___.save()

            elif codigo and descripcion and cantidad and itbis and costo and codigo_ and descripcion_ and cantidad_ and itbis_ and costo_ and codigo__ and descripcion__ and cantidad__ and itbis__ and costo__:
                itbisC = int(itbis) / 100
                itbisC_ = int(itbis_) / 100
                itbisC__ = int(itbis__) / 100
                compraC = [
                    Compras(horaCompra=horaCompra,encargadoCompra=encargado_compra, suplidor=suplidor, codigo=codigo, descripcion=descripcion, cantidad=cantidad, itbis=itbis, costo=costo, totalCompra=(int(cantidad)*int(costo)) * itbisC + (int(cantidad)*int(costo)), usuario=usuarioC),
                    Compras(horaCompra=horaCompra,encargadoCompra=encargado_compra, suplidor=suplidor, codigo=codigo_, descripcion=descripcion_, cantidad=cantidad_, itbis=itbis_, costo=costo_, totalCompra=(int(cantidad_)*int(costo_)) * itbisC_ + (int(cantidad_)*int(costo_)), usuario=usuarioC),
                    Compras(horaCompra=horaCompra,encargadoCompra=encargado_compra, suplidor=suplidor, codigo=codigo__, descripcion=descripcion__, cantidad=cantidad__, itbis=itbis__, costo=costo__, totalCompra=(int(cantidad__)*int(costo__)) * itbisC__ + (int(cantidad__)*int(costo__)), usuario=usuarioC)
                ]
                Compras.objects.bulk_create(compraC)

                articulo = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo)
                articulo.cantidad = (int(articulo.cantidad) + int(cantidad))
                articulo.save()

                articulo_ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo_)
                articulo_.cantidad = (int(articulo.cantidad) + int(cantidad_))
                articulo_.save()

                articulo__ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo__)
                articulo__.cantidad = (int(articulo.cantidad) + int(cantidad__))
                articulo__.save()

            elif codigo and descripcion and cantidad and itbis and costo and codigo_ and descripcion_ and cantidad_ and itbis_ and costo_ :
                itbisC = int(itbis) / 100
                itbisC_ = int(itbis_) / 100
                compraB = [
                    Compras(horaCompra=horaCompra,encargadoCompra=encargado_compra, suplidor=suplidor, codigo=codigo, descripcion=descripcion, cantidad=cantidad, itbis=itbis, costo=costo, totalCompra=(int(cantidad)*int(costo)) * itbisC + (int(cantidad)*int(costo)), usuario=usuarioC),
                    Compras(horaCompra=horaCompra,encargadoCompra=encargado_compra, suplidor=suplidor, codigo=codigo_, descripcion=descripcion_, cantidad=cantidad_, itbis=itbis_, costo=costo_, totalCompra=(int(cantidad_)*int(costo_)) * itbisC_ + (int(cantidad_)*int(costo_)), usuario=usuarioC)
                ]
                Compras.objects.bulk_create(compraB)

                articulo = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo)
                articulo.cantidad = (int(articulo.cantidad) + int(cantidad))
                articulo.save()

                articulo_ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo_)
                articulo_.cantidad = (int(articulo.cantidad) + int(cantidad_))
                articulo_.save()

            elif codigo and descripcion and cantidad and itbis and costo:
                itbisC = int(itbis) / 100
                compraA = [
                    Compras(horaCompra=horaCompra,encargadoCompra=encargado_compra, suplidor=suplidor, codigo=codigo, descripcion=descripcion, cantidad=cantidad, itbis=itbis, costo=costo, totalCompra=(int(cantidad)*int(costo)) * itbisC + (int(cantidad)*int(costo)), usuario=usuarioC)
                ]
                Compras.objects.bulk_create(compraA)

                articulo = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo)
                articulo.cantidad = (int(articulo.cantidad) + int(cantidad))
                articulo.save()
                
            return redirect('compras')
    else:
        compra = ComprasForm()
    return render(request, 'AlphaInventory/compras.html', {'compra':compra, 'usuario':usuario, 'suplidores':suplidores, 'encargadoCompras':encargadoCompras, 'articulos':articulos, 'horaCompra':horaCompra})

def encargado_compras_compras(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoCompra = request.POST['encargadoCompra']
        if EncargadosCompras.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de compras ya esta registrado")
            return redirect('compras')
        if EncargadosCompras.objects.filter(encargadoCompra=encargadoCompra).exists():
            messages.error(request, "Este encargado de compras ya esta registrado")
            return redirect('compras')
        else:
            encargado_compra = EncargadoComprasForm(request.POST)
            if encargado_compra.is_valid():
                encargado_compra.save()
                return redirect('compras')
    return render(request, 'AlphaInventory/compras.html',{'usuario':usuario})

def editar_encargado_compra(request, id_encargadoCompra):
    encargado_compraE = get_object_or_404(EncargadosCompras, id_encargadoCompra=id_encargadoCompra)
    if request.method == "POST":
        encargadocompraform = EditarEncargadoComprasForm(request.POST, instance=encargado_compraE)
        if encargadocompraform.is_valid():
            encargadocompraform.save()
            return redirect('compras')
    else:
        encargadocompraform = EditarEncargadoComprasForm(instance=encargado_compraE)
    return render(request, 'AlphaInventory/compras.html', {'encargado_compraE':encargado_compraE, 'encargadocompraform':encargadocompraform})

def eliminar_encargadoCompra(request, id_encargadoCompra):
    encargadoCompra = EncargadosCompras.objects.filter(id_encargadoCompra=id_encargadoCompra)
    if request.method == "POST" or "GET":
        encargadoCompra.delete()
        return redirect('compras')

def encargado_ventas_compras(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoVenta = request.POST['encargadoVenta']
        if EncargadosVentas.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de ventas ya esta registrado")
            return redirect('compras')
        if EncargadosVentas.objects.filter(encargadoVenta=encargadoVenta).exists():
            messages.error(request, "Este encargado de ventas ya esta registrado")
            return redirect('compras')
        else:
            encargado_venta = EncargadoVentasForm(request.POST)
            if encargado_venta.is_valid():
                encargado_venta.save()
                return redirect('compras')
    return render(request, 'AlphaInventory/compras.html', {'usuario':usuario})

def ventas(request):
    venta = Ventas.objects.filter(usuario_id=request.user.id)
    usuario = RegistroUsuario.objects.filter(id_usuario=request.user.id)
    usuarioV = RegistroUsuario.objects.get(id_usuario=request.user.id)
    clientes = Clientes.objects.filter(usuario_id=request.user.id)
    encargadoVentas = EncargadosVentas.objects.filter(usuario_id=request.user.id)
    articulos = Articulos.objects.filter(usuario_id=request.user.id)
    hora = datetime.now()
    horaVenta = hora.strftime("%H:%M:%S")
    if request.method == "POST":
        cliente = request.POST['cliente']
        encargado_venta = request.POST['encargadoVenta']
        codigo = request.POST['codigo']
        descripcion = request.POST['descripcion']
        itbis = request.POST['itbis']
        cantidad = request.POST['cantidad']
        precio = request.POST['precio']

        codigo_ = request.POST['codigo_']
        descripcion_ = request.POST['descripcion_']
        itbis_ = request.POST['itbis_']
        cantidad_ = request.POST['cantidad_']
        precio_ = request.POST['precio_']

        codigo__ = request.POST['codigo__']
        descripcion__ = request.POST['descripcion__']
        itbis__ = request.POST['itbis__']
        cantidad__ = request.POST['cantidad__']
        precio__ = request.POST['precio__']

        codigo___ = request.POST['codigo___']
        descripcion___ = request.POST['descripcion___']
        itbis___ = request.POST['itbis___']
        cantidad___ = request.POST['cantidad___']
        precio___ = request.POST['precio___']

        codigo____ = request.POST['codigo____']
        descripcion____ = request.POST['descripcion____']
        itbis____ = request.POST['itbis____']
        cantidad____ = request.POST['cantidad____']
        precio____ = request.POST['precio____']

        codigo_____ = request.POST['codigo_____']
        descripcion_____ = request.POST['descripcion_____']
        itbis_____ = request.POST['itbis_____']
        cantidad_____ = request.POST['cantidad_____']
        precio_____ = request.POST['precio_____']

        codigo______ = request.POST['codigo______']
        descripcion______ = request.POST['descripcion______']
        itbis______ = request.POST['itbis______']
        cantidad______ = request.POST['cantidad______']
        precio______ = request.POST['precio______'] 

        venta = VentasForm(request.POST)

        if not Clientes.objects.filter(nombre=cliente).exists():
            messages.error(request, "Este cliente no existe")
            return redirect('ventas')
        if not EncargadosVentas.objects.filter(encargadoVenta=encargado_venta).exists():
            messages.error(request, "Este encargado de compras no existe")
            return redirect('ventas')
        if not Articulos.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de la casilla 1 de articulo no existe")
            return redirect('ventas')
        if not Articulos.objects.filter(descripcion=descripcion, codigo=codigo):
            messages.error(request, "Esta no es la descripcion de la casilla 1 del articulo")
            return redirect('ventas')
        if not Articulos.objects.filter(itbis=itbis, codigo=codigo):
            messages.error(request, "Este no es el itbis de la casilla 1 del articulo")
            return redirect('ventas')
        if not Articulos.objects.filter(precio=precio, codigo=codigo):
            messages.error(request, "Este no es el precio de la casilla 1 del articulo")
            return redirect('ventas')
        
        if codigo_ != "" and Articulos.objects.exclude(codigo=codigo_):
            messages.error(request, "Este codigo de la casiila 2 de articulo no existe")
            return redirect('ventas')
        if (descripcion_ != "" and codigo_ != "") and Articulos.objects.exclude(descripcion=descripcion_, codigo=codigo_):
            messages.error(request, "Esta no es la descripcion de la casiila 2 del articulo")
            return redirect('ventas')
        if (itbis_ != "" and codigo_ != "") and Articulos.objects.exclude(itbis=itbis_, codigo=codigo_):
            messages.error(request, "Este no es el itbis de la casiila 2 del articulo")
            return redirect('ventas')
        if (precio_ != "" and codigo_ != "") and Articulos.objects.exclude(costo=precio_, codigo=codigo_):
            messages.error(request, "Este no es el precio de la casiila 2 del articulo")
            return redirect('ventas')
        
        if (codigo__ != "") and Articulos.objects.exclude(codigo=codigo__):
            messages.error(request, "Este codigo de la casilla 3 de articulo no existe")
            return redirect('ventas')
        if (descripcion__ != "" and codigo__ != "") and Articulos.objects.exclude(descripcion=descripcion__, codigo=codigo__):
            messages.error(request, "Esta no es la descripcion de la casilla 3 del articulo")
            return redirect('ventas')
        if (itbis__ != "" and codigo__ != "") and Articulos.objects.exclude(itbis=itbis__, codigo_=codigo__):
            messages.error(request, "Este no es el itbis de la casilla 3 del articulo")
            return redirect('ventas')
        if (precio__ != "" and codigo__ != "") and Articulos.objects.exclude(precio=precio__, codigo=codigo__):
            messages.error(request, "Este no es el precio de la casilla 3 del articulo")
            return redirect('ventas')
        
        if (codigo___ != "") and Articulos.objects.exclude(codigo=codigo___):
            messages.error(request, "Este codigo de la casilla 4 de articulo no existe")
            return redirect('ventas')
        if (descripcion___ and codigo___ != "") and Articulos.objects.exclude(descripcion=descripcion___, codigo=codigo___):
            messages.error(request, "Esta no es la descripcion de la casilla 4 del articulo")
            return redirect('ventas')
        if (itbis___ != "" and codigo___ != "") and Articulos.objects.exclude(itbis=itbis___, codigo_=codigo___):
            messages.error(request, "Este no es el itbis de la casilla 4 del articulo")
            return redirect('ventas')
        if (precio___ != "" and codigo___ != "") and Articulos.objects.exclude(precio=precio___, codigo=codigo___):
            messages.error(request, "Este no es el precio de la casilla 4 del articulo")
            return redirect('ventas')
        
        if (codigo____ != "") and Articulos.objects.exclude(codigo=codigo____):
            messages.error(request, "Este codigo de la casilla 5 de articulo no existe")
            return redirect('ventas')
        if (descripcion____ != "" and codigo____ != "") and Articulos.objects.exclude(descripcion=descripcion____, codigo=codigo____):
            messages.error(request, "Esta no es la descripcion de la casilla 5 del articulo")
            return redirect('ventas')
        if (itbis____ != "" and codigo____ != "") and Articulos.objects.exclude(itbis=itbis____, codigo_=codigo____):
            messages.error(request, "Este no es el itbis de la casilla 5 del articulo")
            return redirect('ventas')
        if (precio____ != "" and codigo____ != "") and Articulos.objects.exclude(precio=precio____, codigo=codigo____):
            messages.error(request, "Este no es el precio de la casilla 5 del articulo")
            return redirect('ventas')
        
        if (codigo_____ != "") and Articulos.objects.exclude(codigo=codigo_____):
            messages.error(request, "Este codigo de la casilla 6 de articulo no existe")
            return redirect('ventas')
        if (descripcion_____ != "" and codigo_____ != "") and Articulos.objects.exclude(descripcion=descripcion_____, codigo=codigo_____):
            messages.error(request, "Esta no es la descripcion de la casilla 6 del articulo")
            return redirect('ventas')
        if (itbis_____ != "" and codigo_____ != "") and Articulos.objects.exclude(itbis=itbis_____, codigo_=codigo_____):
            messages.error(request, "Este no es el itbis de la casilla 6 del articulo")
            return redirect('ventas')
        if (precio_____ != "" and codigo_____ != "") and Articulos.objects.exclude(precio=precio_____, codigo=codigo_____):
            messages.error(request, "Este no es el precio de la casilla 6 del articulo")
            return redirect('ventas')
        
        if (codigo______ != "") and Articulos.objects.exclude(codigo=codigo______):
            messages.error(request, "Este codigo de la casilla 7 de articulo no existe")
            return redirect('ventas')
        if (descripcion______ != "" and codigo______ != "") and Articulos.objects.exclude(descripcion=descripcion______, codigo=codigo______):
            messages.error(request, "Esta no es la descripcion de la casilla 7 del articulo")
            return redirect('ventas')
        if (itbis______ != "" and codigo______ != "") and Articulos.objects.exclude(itbis=itbis______, codigo_=codigo______):
            messages.error(request, "Este no es el itbis de la casilla 7 del articulo")
            return redirect('ventas')
        if (precio______ != "" and codigo______ != "") and Articulos.objects.exclude(precio=precio______, codigo=codigo______):
            messages.error(request, "Este no es el precio de la casilla 7 del articulo")
            return redirect('ventas')
        
        if venta.is_valid():

            if codigo and descripcion and cantidad and itbis and precio and codigo_ and descripcion_ and cantidad_ and itbis_ and precio_ and codigo__ and descripcion__ and cantidad__ and itbis__ and precio__ and codigo___ and descripcion___ and cantidad___ and itbis___ and precio___ and codigo____ and descripcion____ and cantidad____ and itbis____ and precio____ and codigo____ and descripcion_____ and cantidad_____ and itbis_____ and precio_____ and codigo______ and descripcion______ and cantidad______ and itbis______ and precio______:
                itbisV = int(itbis) / 100
                itbisV_ = int(itbis_) / 100
                itbisV__ = int(itbis__) / 100
                itbisV___ = int(itbis___) / 100
                itbisV____ = int(itbis____) / 100
                itbisV_____ = int(itbis_____) / 100
                itbisV______ = int(itbis______) / 100
                ventaG = [
                    Ventas(horaVenta=horaVenta,encargadoVenta=encargado_venta, cliente=cliente, codigo=codigo, descripcion=descripcion, cantidad=cantidad, itbis=itbis, precio=precio, totalVenta=(int(cantidad)*int(precio)) * itbisV + (int(cantidad)*int(precio)), usuario=usuarioV),
                    Ventas(horaVenta=horaVenta,encargadoVenta=encargado_venta, cliente=cliente, codigo=codigo_, descripcion=descripcion_, cantidad=cantidad_, itbis=itbis_, precio=precio_, totalVenta=(int(cantidad_)*int(precio_)) * itbisV_ + (int(cantidad_)*int(precio_)), usuario=usuarioV),
                    Ventas(horaVenta=horaVenta,encargadoVenta=encargado_venta, cliente=cliente, codigo=codigo__, descripcion=descripcion__, cantidad=cantidad__, itbis=itbis__, precio=precio__, totalVenta=(int(cantidad__)*int(precio__)) * itbisV__ + (int(cantidad__)*int(precio__)), usuario=usuarioV),
                    Ventas(horaVenta=horaVenta,encargadoVenta=encargado_venta, cliente=cliente, codigo=codigo___, descripcion=descripcion___, cantidad=cantidad___, itbis=itbis___, precio=precio___, totalVenta=(int(cantidad___)*int(precio___)) * itbisV___ + (int(cantidad___)*int(precio___)), usuario=usuarioV),
                    Ventas(horaVenta=horaVenta,encargadoVenta=encargado_venta, cliente=cliente, codigo=codigo____, descripcion=descripcion____, cantidad=cantidad____, itbis=itbis____, precio=precio____, totalVenta=(int(cantidad____)*int(precio____)) * itbisV____ + (int(cantidad____)*int(precio____)), usuario=usuarioV),
                    Ventas(horaVenta=horaVenta,encargadoVenta=encargado_venta, cliente=cliente, codigo=codigo_____, descripcion=descripcion_____, cantidad=cantidad_____, itbis=itbis_____, precio=precio_____, totalVenta=(int(cantidad_____)*int(precio_____)) * itbisV_____ + (int(cantidad_____)*int(precio_____)), usuario=usuarioV),
                    Ventas(horaVenta=horaVenta,encargadoVenta=encargado_venta, cliente=cliente, codigo=codigo______, descripcion=descripcion______, cantidad=cantidad______, itbis=itbis______, precio=precio______, totalVenta=(int(cantidad______)*int(precio______)) * itbisV______ + (int(cantidad______)*int(precio______)), usuario=usuarioV)
                ]
                Ventas.objects.bulk_create(ventaG)

                articulo = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo)
                articulo.cantidad = (int(articulo.cantidad) - int(cantidad))
                articulo.save()

                articulo_ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo_)
                articulo_.cantidad = (int(articulo.cantidad) - int(cantidad_))
                articulo_.save()

                articulo__ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo__)
                articulo__.cantidad = (int(articulo.cantidad) - int(cantidad__))
                articulo__.save()

                articulo___ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo___)
                articulo___.cantidad = (int(articulo.cantidad) - int(cantidad___))
                articulo___.save()

                articulo____ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo____)
                articulo____.cantidad = (int(articulo.cantidad) - int(cantidad____))
                articulo____.save()

                articulo_____ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo_____)
                articulo_____.cantidad = (int(articulo.cantidad) - int(cantidad_____))
                articulo_____.save()

                articulo______ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo______)
                articulo______.cantidad = (int(articulo.cantidad) - int(cantidad______))
                articulo______.save()

            elif codigo and descripcion and cantidad and itbis and precio and codigo_ and descripcion_ and cantidad_ and itbis_ and precio_ and codigo__ and descripcion__ and cantidad__ and itbis__ and precio__ and codigo___ and descripcion___ and cantidad___ and itbis___ and precio___ and codigo____ and descripcion____ and cantidad____ and itbis____ and precio____ and codigo____ and descripcion_____ and cantidad_____ and itbis_____ and precio_____:
                itbisV = int(itbis) / 100
                itbisV_ = int(itbis_) / 100
                itbisV__ = int(itbis__) / 100
                itbisV___ = int(itbis___) / 100
                itbisV____ = int(itbis____) / 100
                itbisV_____ = int(itbis_____) / 100
                ventaF = [
                    Compras(horaVenta=horaVenta,encargadoVenta=encargado_venta, cliente=cliente, codigo=codigo, descripcion=descripcion, cantidad=cantidad, itbis=itbis, precio=precio, totalVenta=(int(cantidad)*int(precio)) * itbisV + (int(cantidad)*int(precio)), usuario=usuarioV),
                    Compras(horaVenta=horaVenta,encargadoVenta=encargado_venta, cliente=cliente, codigo=codigo_, descripcion=descripcion_, cantidad=cantidad_, itbis=itbis_, precio=precio_, totalVenta=(int(cantidad_)*int(precio_)) * itbisV_ + (int(cantidad_)*int(precio_)), usuario=usuarioV),
                    Ventas(horaVenta=horaVenta,encargadoVenta=encargado_venta, cliente=cliente, codigo=codigo__, descripcion=descripcion__, cantidad=cantidad__, itbis=itbis__, precio=precio__, totalVenta=(int(cantidad__)*int(precio__)) * itbisV__ + (int(cantidad__)*int(precio__)), usuario=usuarioV),
                    Ventas(horaVenta=horaVenta,encargadoVenta=encargado_venta, cliente=cliente, codigo=codigo___, descripcion=descripcion___, cantidad=cantidad___, itbis=itbis___, precio=precio___, totalVenta=(int(cantidad___)*int(precio___)) * itbisV___ + (int(cantidad___)*int(precio___)), usuario=usuarioV),
                    Ventas(horaVenta=horaVenta,encargadoVenta=encargado_venta, cliente=cliente, codigo=codigo____, descripcion=descripcion____, cantidad=cantidad____, itbis=itbis____, precio=precio____, totalVenta=(int(cantidad____)*int(precio____)) * itbisV____ + (int(cantidad____)*int(precio____)), usuario=usuarioV),
                    Ventas(horaVenta=horaVenta,encargadoVenta=encargado_venta, cliente=cliente, codigo=codigo_____, descripcion=descripcion_____, cantidad=cantidad_____, itbis=itbis_____, precio=precio_____, totalVenta=(int(cantidad_____)*int(precio_____)) * itbisV_____ + (int(cantidad_____)*int(precio_____)), usuario=usuarioV)
                ]
                Ventas.objects.bulk_create(ventaF)

                articulo = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo)
                articulo.cantidad = (int(articulo.cantidad) - int(cantidad))
                articulo.save()

                articulo_ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo_)
                articulo_.cantidad = (int(articulo.cantidad) - int(cantidad_))
                articulo_.save()

                articulo__ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo__)
                articulo__.cantidad = (int(articulo.cantidad) - int(cantidad__))
                articulo__.save()

                articulo___ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo___)
                articulo___.cantidad = (int(articulo.cantidad) - int(cantidad___))
                articulo___.save()

                articulo____ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo____)
                articulo____.cantidad = (int(articulo.cantidad) - int(cantidad____))
                articulo____.save()

                articulo_____ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo_____)
                articulo_____.cantidad = (int(articulo.cantidad) - int(cantidad_____))
                articulo_____.save()

            elif codigo and descripcion and cantidad and itbis and precio and codigo_ and descripcion_ and cantidad_ and itbis_ and precio_ and codigo__ and descripcion__ and cantidad__ and itbis__ and precio__ and codigo___ and descripcion___ and cantidad___ and itbis___ and precio___ and codigo____ and descripcion____ and cantidad____ and itbis____ and precio____:
                itbisV = int(itbis) / 100
                itbisV_ = int(itbis_) / 100
                itbisV__ = int(itbis__) / 100
                itbisV___ = int(itbis___) / 100
                itbisV____ = int(itbis____) / 100
                ventaE = [
                    Ventas(horaVenta=horaVenta,encargadoVenta=encargado_venta, cliente=cliente, codigo=codigo, descripcion=descripcion, cantidad=cantidad, itbis=itbis, precio=precio, totalVenta=(int(cantidad)*int(precio)) * itbisV + (int(cantidad)*int(precio)), usuario=usuarioV),
                    Ventas(horaVenta=horaVenta,encargadoVenta=encargado_venta, cliente=cliente, codigo=codigo_, descripcion=descripcion_, cantidad=cantidad_, itbis=itbis_, precio=precio_, totalVenta=(int(cantidad_)*int(precio_)) * itbisV_ + (int(cantidad_)*int(precio_)), usuario=usuarioV),
                    Ventas(horaVenta=horaVenta,encargadoVenta=encargado_venta, cliente=cliente, codigo=codigo__, descripcion=descripcion__, cantidad=cantidad__, itbis=itbis__, precio=precio__, totalVenta=(int(cantidad__)*int(precio__)) * itbisV__ + (int(cantidad__)*int(precio__)), usuario=usuarioV),
                    Ventas(horaVenta=horaVenta,encargadoVenta=encargado_venta, cliente=cliente, codigo=codigo___, descripcion=descripcion___, cantidad=cantidad___, itbis=itbis___, precio=precio___, totalVenta=(int(cantidad___)*int(precio___)) * itbisV___ + (int(cantidad___)*int(precio___)), usuario=usuarioV),
                    Ventas(horaVenta=horaVenta,encargadoVenta=encargado_venta, cliente=cliente, codigo=codigo____, descripcion=descripcion____, cantidad=cantidad____, itbis=itbis____, precio=precio____, totalVenta=(int(cantidad____)*int(precio____)) * itbisV____ + (int(cantidad____)*int(precio____)), usuario=usuarioV)
                ]
                Ventas.objects.bulk_create(ventaE)

                articulo = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo)
                articulo.cantidad = (int(articulo.cantidad) - int(cantidad))
                articulo.save()

                articulo_ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo_)
                articulo_.cantidad = (int(articulo.cantidad) - int(cantidad_))
                articulo_.save()

                articulo__ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo__)
                articulo__.cantidad = (int(articulo.cantidad) - int(cantidad__))
                articulo__.save()

                articulo___ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo___)
                articulo___.cantidad = (int(articulo.cantidad) - int(cantidad___))
                articulo___.save()

                articulo____ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo____)
                articulo____.cantidad = (int(articulo.cantidad) - int(cantidad____))
                articulo____.save()

            elif codigo and descripcion and cantidad and itbis and precio and codigo_ and descripcion_ and cantidad_ and itbis_ and precio_ and codigo__ and descripcion__ and cantidad__ and itbis__ and precio__ and codigo___ and descripcion___ and cantidad___ and itbis___ and precio___:
                itbisV = int(itbis) / 100
                itbisV_ = int(itbis_) / 100
                itbisV__ = int(itbis__) / 100
                itbisV___ = int(itbis___) / 100
                ventaD = [
                    Ventas(horaVenta=horaVenta,encargadoVenta=encargado_venta, cliente=cliente, codigo=codigo, descripcion=descripcion, cantidad=cantidad, itbis=itbis, precio=precio, totalVenta=(int(cantidad)*int(precio)) * itbisV + (int(cantidad)*int(precio)), usuario=usuarioV),
                    Ventas(horaVenta=horaVenta,encargadoVenta=encargado_venta, cliente=cliente, codigo=codigo_, descripcion=descripcion_, cantidad=cantidad_, itbis=itbis_, precio=precio_, totalVenta=(int(cantidad_)*int(precio_)) * itbisV_ + (int(cantidad_)*int(precio_)), usuario=usuarioV),
                    Ventas(horaVenta=horaVenta,encargadoVenta=encargado_venta, cliente=cliente, codigo=codigo__, descripcion=descripcion__, cantidad=cantidad__, itbis=itbis__, precio=precio__, totalVenta=(int(cantidad__)*int(precio__)) * itbisV__ + (int(cantidad__)*int(precio__)), usuario=usuarioV),
                    Ventas(horaVenta=horaVenta,encargadoVenta=encargado_venta, cliente=cliente, codigo=codigo___, descripcion=descripcion___, cantidad=cantidad___, itbis=itbis___, precio=precio___, totalVenta=(int(cantidad___)*int(precio___)) * itbisV___ + (int(cantidad___)*int(precio___)), usuario=usuarioV)
                ]
                Ventas.objects.bulk_create(ventaD)

                articulo = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo)
                articulo.cantidad = (int(articulo.cantidad) - int(cantidad))
                articulo.save()

                articulo_ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo_)
                articulo_.cantidad = (int(articulo.cantidad) - int(cantidad_))
                articulo_.save()

                articulo__ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo__)
                articulo__.cantidad = (int(articulo.cantidad) - int(cantidad__))
                articulo__.save()

                articulo___ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo___)
                articulo___.cantidad = (int(articulo.cantidad) - int(cantidad___))
                articulo___.save()

            elif codigo and descripcion and cantidad and itbis and precio and codigo_ and descripcion_ and cantidad_ and itbis_ and precio_ and codigo__ and descripcion__ and cantidad__ and itbis__ and precio__:
                itbisV = int(itbis) / 100
                itbisV_ = int(itbis_) / 100
                itbisV__ = int(itbis__) / 100
                ventaC = [
                    Ventas(horaVenta=horaVenta,encargadoVenta=encargado_venta, cliente=cliente, codigo=codigo, descripcion=descripcion, cantidad=cantidad, itbis=itbis, precio=precio, totalVenta=(int(cantidad)*int(precio)) * itbisV + (int(cantidad)*int(precio)), usuario=usuarioV),
                    Ventas(horaVenta=horaVenta,encargadoVenta=encargado_venta, cliente=cliente, codigo=codigo_, descripcion=descripcion_, cantidad=cantidad_, itbis=itbis_, precio=precio_, totalVenta=(int(cantidad_)*int(precio_)) * itbisV_ + (int(cantidad_)*int(precio_)), usuario=usuarioV),
                    Ventas(horaVenta=horaVenta,encargadoVenta=encargado_venta, cliente=cliente, codigo=codigo__, descripcion=descripcion__, cantidad=cantidad__, itbis=itbis__, precio=precio__, totalVenta=(int(cantidad__)*int(precio__)) * itbisV__ + (int(cantidad__)*int(precio__)), usuario=usuarioV)
                ]
                Ventas.objects.bulk_create(ventaC)

                articulo = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo)
                articulo.cantidad = (int(articulo.cantidad) - int(cantidad))
                articulo.save()

                articulo_ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo_)
                articulo_.cantidad = (int(articulo.cantidad) - int(cantidad_))
                articulo_.save()

                articulo__ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo__)
                articulo__.cantidad = (int(articulo.cantidad) - int(cantidad__))
                articulo__.save()

            elif codigo and descripcion and cantidad and itbis and precio and codigo_ and descripcion_ and cantidad_ and itbis_ and precio_ :
                itbisV = int(itbis) / 100
                itbisV_ = int(itbis_) / 100
                ventaB = [
                    Ventas(horaVenta=horaVenta,encargadoVenta=encargado_venta, cliente=cliente, codigo=codigo, descripcion=descripcion, cantidad=cantidad, itbis=itbis, precio=precio, totalVenta=(int(cantidad)*int(precio)) * itbisV + (int(cantidad)*int(precio)), usuario=usuarioV),
                    Ventas(horaVenta=horaVenta,encargadoVenta=encargado_venta, cliente=cliente, codigo=codigo_, descripcion=descripcion_, cantidad=cantidad_, itbis=itbis_, precio=precio_, totalVenta=(int(cantidad_)*int(precio_)) * itbisV_ + (int(cantidad_)*int(precio_)), usuario=usuarioV)
                ]
                Ventas.objects.bulk_create(ventaB)

                articulo = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo)
                articulo.cantidad = (int(articulo.cantidad) - int(cantidad))
                articulo.save()

                articulo_ = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo_)
                articulo_.cantidad = (int(articulo.cantidad) - int(cantidad_))
                articulo_.save()

            elif codigo and descripcion and cantidad and itbis and precio:
                itbisC = int(itbis) / 100
                ventaA = [
                    Ventas(horaVenta=horaVenta,encargadoVenta=encargado_venta, cliente=cliente, codigo=codigo, descripcion=descripcion, cantidad=cantidad, itbis=itbis, precio=precio, totalVenta=(int(cantidad)*int(precio)) * itbisC + (int(cantidad)*int(precio)), usuario=usuarioV)
                ]
                Ventas.objects.bulk_create(ventaA)

                articulo = Articulos.objects.get(usuario_id=request.user.id, codigo=codigo)
                articulo.cantidad = (int(articulo.cantidad) - int(cantidad))
                articulo.save()
                
            return redirect('ventas')
    else:
        ventaform = VentasForm()
    return render(request, 'AlphaInventory/ventas.html', {'venta':venta, 'usuario':usuario, 'horaVenta':horaVenta, 'clientes':clientes, 'encargadoVentas':encargadoVentas, 'articulos':articulos})


def encargado_ventas_ventas(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoVenta = request.POST['encargadoVenta']
        if EncargadosVentas.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de ventas ya esta registrado")
            return redirect('ventas')
        if EncargadosVentas.objects.filter(encargadoVenta=encargadoVenta).exists():
            messages.error(request, "Este encargado de ventas ya esta registrado")
            return redirect('ventas')
        else:
            encargado_venta = EncargadoVentasForm(request.POST)
            if encargado_venta.is_valid():
                encargado_venta.save()
                return redirect('ventas')
    return render(request, 'AlphaInventory/ventas.html', {'usuario':usuario})

def editar_encargado_venta(request, id_encargadoVenta):
    encargado_ventaE = get_object_or_404(EncargadosVentas, id_encargadoVenta=id_encargadoVenta)
    if request.method == "POST":
        encargadoventaform = EditarEncargadoVentasForm(request.POST, instance=encargado_ventaE)
        if encargadoventaform.is_valid():
            encargadoventaform.save()
            return redirect('compras')
    else:
        encargadoventaform = EditarEncargadoVentasForm(instance=encargado_ventaE)
    return render(request, 'AlphaInventory/ventas.html', {'encargado_ventaE':encargado_ventaE, 'encargadoventaform':encargadoventaform})

def encargado_compras_ventas(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoCompra = request.POST['encargadoCompra']
        if EncargadosCompras.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de compras ya esta registrado")
            return redirect('ventas')
        if EncargadosCompras.objects.filter(encargadoCompra=encargadoCompra).exists():
            messages.error(request, "Este encargado de compras ya esta registrado")
            return redirect('ventas')
        else:
            encargado_compra = EncargadoComprasForm(request.POST)
            if encargado_compra.is_valid():
                encargado_compra.save()
                return redirect('ventas')
    return render(request, 'AlphaInventory/ventas.html',{'usuario':usuario})

def eliminar_encargadoVenta(request, id_encargadoVenta):
    encargadoVenta = EncargadosVentas.objects.filter(id_encargadoVenta=id_encargadoVenta)
    if request.method == "POST" or "GET":
        encargadoVenta.delete()
        return redirect('ventas')

def movimientos_diario_compra(request):
    compra = Compras.objects.filter(usuario_id=request.user.id)
    costo_total = Compras.objects.filter(usuario_id=request.user.id).aggregate(costo_total_articulos=Sum('totalCompra'))
    return render(request, 'AlphaInventory/movimientosdiariocompras.html', {'compra':compra, 'costo_total':costo_total})

def encargado_compras_movimientos_diario_compra(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoCompra = request.POST['encargadoCompra']
        if EncargadosCompras.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de compras ya esta registrado")
            return redirect('movimientosdiariocompras')
        if EncargadosCompras.objects.filter(encargadoCompra=encargadoCompra).exists():
            messages.error(request, "Este encargado de compras ya esta registrado")
            return redirect('movimientosdiariocompras')
        else:
            encargado_compra = EncargadoComprasForm(request.POST)
            if encargado_compra.is_valid():
                encargado_compra.save()
                return redirect('movimientosdiariocompras')
    return render(request, 'AlphaInventory/movimientosdiariocompras.html',{'usuario':usuario})

def encargado_ventas_movimientos_diario_compra(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoVenta = request.POST['encargadoVenta']
        if EncargadosVentas.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de ventas ya esta registrado")
            return redirect('movimientosdiariocompras')
        if EncargadosVentas.objects.filter(encargadoVenta=encargadoVenta).exists():
            messages.error(request, "Este encargado de ventas ya esta registrado")
            return redirect('movimientosdiariocompras')
        else:
            encargado_venta = EncargadoVentasForm(request.POST)
            if encargado_venta.is_valid():
                encargado_venta.save()
                return redirect('movimientosdiariocompras')
    return render(request, 'AlphaInventory/movimientosdiariocompras.html', {'usuario':usuario})

def movimientos_diario_venta(request):
    venta = Ventas.objects.filter(usuario_id=request.user.id)
    precio_total = Ventas.objects.filter(usuario_id=request.user.id).aggregate(precio_total_articulos=Sum('totalVenta'))
    return render(request, 'AlphaInventory/movimientosdiarioventas.html', {'venta':venta, 'precio_total':precio_total})

def encargado_compras_movimientos_diario_venta(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoCompra = request.POST['encargadoCompra']
        if EncargadosCompras.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de compras ya esta registrado")
            return redirect('movimientosdiarioventas')
        if EncargadosCompras.objects.filter(encargadoCompra=encargadoCompra).exists():
            messages.error(request, "Este encargado de compras ya esta registrado")
            return redirect('movimientosdiarioventas')
        else:
            encargado_compra = EncargadoComprasForm(request.POST)
            if encargado_compra.is_valid():
                encargado_compra.save()
                return redirect('movimientosdiarioventas')
    return render(request, 'AlphaInventory/movimientosdiarioventas.html',{'usuario':usuario})

def encargado_ventas_movimientos_diario_venta(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoVenta = request.POST['encargadoVenta']
        if EncargadosVentas.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de ventas ya esta registrado")
            return redirect('movimientosdiarioventas')
        if EncargadosVentas.objects.filter(encargadoVenta=encargadoVenta).exists():
            messages.error(request, "Este encargado de ventas ya esta registrado")
            return redirect('movimientosdiarioventas')
        else:
            encargado_venta = EncargadoVentasForm(request.POST)
            if encargado_venta.is_valid():
                encargado_venta.save()
                return redirect('movimientosdiarioventas')
    return render(request, 'AlphaInventory/movimientosdiarioventas.html', {'usuario':usuario})

def movimiento_por_articulo_compras(request):
    compra = Compras.objects.all()
    return render(request, 'AlphaInventory/movimientoporarticulocompras.html', {'compra':compra})

def encargado_compras_movimiento_por_articulo_compras(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoCompra = request.POST['encargadoCompra']
        if EncargadosCompras.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de compras ya esta registrado")
            return redirect('movimientoporarticulocompras')
        if EncargadosCompras.objects.filter(encargadoCompra=encargadoCompra).exists():
            messages.error(request, "Este encargado de compras ya esta registrado")
            return redirect('movimientoporarticulocompras')
        else:
            encargado_compra = EncargadoComprasForm(request.POST)
            if encargado_compra.is_valid():
                encargado_compra.save()
                return redirect('movimientoporarticulocompras')
    return render(request, 'AlphaInventory/movimientoporarticulocompras.html',{'usuario':usuario})

def encargado_ventas_movimiento_por_articulo_compras(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoVenta = request.POST['encargadoVenta']
        if EncargadosVentas.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de ventas ya esta registrado")
            return redirect('movimientoporarticulocompras')
        if EncargadosVentas.objects.filter(encargadoVenta=encargadoVenta).exists():
            messages.error(request, "Este encargado de ventas ya esta registrado")
            return redirect('movimientoporarticulocompras')
        else:
            encargado_venta = EncargadoVentasForm(request.POST)
            if encargado_venta.is_valid():
                encargado_venta.save()
                return redirect('movimientoporarticulocompras')
    return render(request, 'AlphaInventory/movimientoporarticulocompras.html', {'usuario':usuario})

def movimiento_por_articulo_ventas(request):
    venta = Ventas.objects.all()
    return render(request, 'AlphaInventory/movimientoporarticuloventas.html', {'venta':venta})

def encargado_compras_movimiento_por_articulo_ventas(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoCompra = request.POST['encargadoCompra']
        if EncargadosCompras.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de compras ya esta registrado")
            return redirect('movimientoporarticuloventas')
        if EncargadosCompras.objects.filter(encargadoCompra=encargadoCompra).exists():
            messages.error(request, "Este encargado de compras ya esta registrado")
            return redirect('movimientoporarticuloventas')
        else:
            encargado_compra = EncargadoComprasForm(request.POST)
            if encargado_compra.is_valid():
                encargado_compra.save()
                return redirect('movimientoporarticuloventas')
    return render(request, 'AlphaInventory/movimientoporarticuloventas.html',{'usuario':usuario})

def encargado_ventas_movimiento_por_articulo_ventas(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoVenta = request.POST['encargadoVenta']
        if EncargadosVentas.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de ventas ya esta registrado")
            return redirect('movimeintoporarticuloventas')
        if EncargadosVentas.objects.filter(encargadoVenta=encargadoVenta).exists():
            messages.error(request, "Este encargado de ventas ya esta registrado")
            return redirect('movimeintoporarticuloventas')
        else:
            encargado_venta = EncargadoVentasForm(request.POST)
            if encargado_venta.is_valid():
                encargado_venta.save()
                return redirect('movimeintoporarticuloventas')
    return render(request, 'AlphaInventory/movimeintoporarticuloventas.html', {'usuario':usuario})

def listado_articulos(request):
    articulo = Articulos.objects.filter(usuario_id=request.user.id)
    precio_total = Articulos.objects.filter(usuario_id=request.user.id).aggregate(precio_total_articulos=Sum('precio') * Sum('cantidad'))
    return render(request, 'AlphaInventory/listadodearticulos.html', {'articulo':articulo, 'precio_total':precio_total})

def encargado_compras_listado_articulos(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoCompra = request.POST['encargadoCompra']
        if EncargadosCompras.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de compras ya esta registrado")
            return redirect('listadodearticulos')
        if EncargadosCompras.objects.filter(encargadoCompra=encargadoCompra).exists():
            messages.error(request, "Este encargado de compras ya esta registrado")
            return redirect('listadodearticulos')
        else:
            encargado_compra = EncargadoComprasForm(request.POST)
            if encargado_compra.is_valid():
                encargado_compra.save()
                return redirect('listadodearticulos')
    return render(request, 'AlphaInventory/listadodearticulos.html',{'usuario':usuario})

def encargado_ventas_listado_articulos(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoVenta = request.POST['encargadoVenta']
        if EncargadosVentas.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de ventas ya esta registrado")
            return redirect('listadodearticulos')
        if EncargadosVentas.objects.filter(encargadoVenta=encargadoVenta).exists():
            messages.error(request, "Este encargado de ventas ya esta registrado")
            return redirect('listadodearticulos')
        else:
            encargado_venta = EncargadoVentasForm(request.POST)
            if encargado_venta.is_valid():
                encargado_venta.save()
                return redirect('listadodearticulos')
    return render(request, 'AlphaInventory/listadodearticulos.html', {'usuario':usuario})

def listado_suplidores(request):
    suplidor = Suplidores.objects.filter(usuario_id=request.user.id)
    return render(request, 'AlphaInventory/listadodesuplidores.html', {'suplidor':suplidor})

def encargado_compras_listado_suplidores(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoCompra = request.POST['encargadoCompra']
        if EncargadosCompras.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de compras ya esta registrado")
            return redirect('listadodesuplidores')
        if EncargadosCompras.objects.filter(encargadoCompra=encargadoCompra).exists():
            messages.error(request, "Este encargado de compras ya esta registrado")
            return redirect('listadodesuplidores')
        else:
            encargado_compra = EncargadoComprasForm(request.POST)
            if encargado_compra.is_valid():
                encargado_compra.save()
                return redirect('listadodesuplidores')
    return render(request, 'AlphaInventory/listadodesuplidores.html',{'usuario':usuario})

def encargado_ventas_listado_suplidores(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoVenta = request.POST['encargadoVenta']
        if EncargadosVentas.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de ventas ya esta registrado")
            return redirect('listadodesuplidores')
        if EncargadosVentas.objects.filter(encargadoVenta=encargadoVenta).exists():
            messages.error(request, "Este encargado de ventas ya esta registrado")
            return redirect('listadodesuplidores')
        else:
            encargado_venta = EncargadoVentasForm(request.POST)
            if encargado_venta.is_valid():
                encargado_venta.save()
                return redirect('listadodesuplidores')
    return render(request, 'AlphaInventory/listadodesuplidores.html', {'usuario':usuario})

def listado_clientes(request):
    cliente = Clientes.objects.filter(usuario_id=request.user.id)
    return render(request, 'AlphaInventory/listadodeclientes.html', {'cliente':cliente})

def encargado_compras_listado_clientes(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoCompra = request.POST['encargadoCompra']
        if EncargadosCompras.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de compras ya esta registrado")
            return redirect('listadodeclientes')
        if EncargadosCompras.objects.filter(encargadoCompra=encargadoCompra).exists():
            messages.error(request, "Este encargado de compras ya esta registrado")
            return redirect('listadodeclientes')
        else:
            encargado_compra = EncargadoComprasForm(request.POST)
            if encargado_compra.is_valid():
                encargado_compra.save()
                return redirect('listadedeclientes')
    return render(request, 'AlphaInventory/listadodeclientes.html',{'usuario':usuario})

def encargado_ventas_listado_clientes(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoVenta = request.POST['encargadoVenta']
        if EncargadosVentas.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de ventas ya esta registrado")
            return redirect('listadodeclientes')
        if EncargadosVentas.objects.filter(encargadoVenta=encargadoVenta).exists():
            messages.error(request, "Este encargado de ventas ya esta registrado")
            return redirect('listadodeclientes')
        else:
            encargado_venta = EncargadoVentasForm(request.POST)
            if encargado_venta.is_valid():
                encargado_venta.save()
                return redirect('listadodeclientes')
    return render(request, 'AlphaInventory/listadodeclientes.html', {'usuario':usuario})

def listado_compras(request):
    compra = Compras.objects.filter(usuario_id=request.user.id)
    costo_total = Compras.objects.filter(usuario_id=request.user.id).aggregate(costo_total_articulos=Sum('totalCompra'))
    return render(request, 'AlphaInventory/listadodecompras.html', {'compra':compra, 'costo_total':costo_total})

def encargado_compras_listado_compras(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoCompra = request.POST['encargadoCompra']
        if EncargadosCompras.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de compras ya esta registrado")
            return redirect('listadodecompras')
        if EncargadosCompras.objects.filter(encargadoCompra=encargadoCompra).exists():
            messages.error(request, "Este encargado de compras ya esta registrado")
            return redirect('listadodecompras')
        else:
            encargado_compra = EncargadoComprasForm(request.POST)
            if encargado_compra.is_valid():
                encargado_compra.save()
                return redirect('listadodecompras')
    return render(request, 'AlphaInventory/listadodecompras.html',{'usuario':usuario})

def encargado_ventas_listado_compras(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoVenta = request.POST['encargadoVenta']
        if EncargadosVentas.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de ventas ya esta registrado")
            return redirect('listadodecompras')
        if EncargadosVentas.objects.filter(encargadoVenta=encargadoVenta).exists():
            messages.error(request, "Este encargado de ventas ya esta registrado")
            return redirect('listadodecompras')
        else:
            encargado_venta = EncargadoVentasForm(request.POST)
            if encargado_venta.is_valid():
                encargado_venta.save()
                return redirect('listadodecompras')
    return render(request, 'AlphaInventory/listadodecompras.html', {'usuario':usuario})

def listado_ventas(request):
    venta = Ventas.objects.filter(usuario_id=request.user.id)
    precio_total = Ventas.objects.filter(usuario_id=request.user.id).aggregate(precio_total_articulos=Sum('totalVenta'))
    return render(request, 'AlphaInventory/listadodeventas.html', {'venta':venta, 'precio_total':precio_total})

def encargado_compras_listado_ventas(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoCompra = request.POST['encargadoCompra']
        if EncargadosCompras.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de compras ya esta registrado")
            return redirect('listadodeventas')
        if EncargadosCompras.objects.filter(encargadoCompra=encargadoCompra).exists():
            messages.error(request, "Este encargado de compras ya esta registrado")
            return redirect('listadodeventas')
        else:
            encargado_compra = EncargadoComprasForm(request.POST)
            if encargado_compra.is_valid():
                encargado_compra.save()
                return redirect('listadodeventas')
    return render(request, 'AlphaInventory/listadodeventas.html',{'usuario':usuario})

def encargado_ventas_listado_ventas(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoVenta = request.POST['encargadoVenta']
        if EncargadosVentas.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de ventas ya esta registrado")
            return redirect('listadodeventas')
        if EncargadosVentas.objects.filter(encargadoVenta=encargadoVenta).exists():
            messages.error(request, "Este encargado de ventas ya esta registrado")
            return redirect('listadodeventas')
        else:
            encargado_venta = EncargadoVentasForm(request.POST)
            if encargado_venta.is_valid():
                encargado_venta.save()
                return redirect('listadodeventas')
    return render(request, 'AlphaInventory/listadodeventas.html', {'usuario':usuario})

def perfil(request):
    perfil = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    return render(request, 'AlphaInventory/perfil.html', {'perfil':perfil})

def encargado_compras_perfil(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoCompra = request.POST['encargadoCompra']
        if EncargadosCompras.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de compras ya esta registrado")
            return redirect('perfil')
        if EncargadosCompras.objects.filter(encargadoCompra=encargadoCompra).exists():
            messages.error(request, "Este encargado de compras ya esta registrado")
            return redirect('perfil')
        else:
            encargado_compra = EncargadoComprasForm(request.POST)
            if encargado_compra.is_valid():
                encargado_compra.save()
                return redirect('perfil')
    return render(request, 'AlphaInventory/perfil.html',{'usuario':usuario})

def encargado_ventas_perfil(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoVenta = request.POST['encargadoVenta']
        if EncargadosVentas.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de ventas ya esta registrado")
            return redirect('perfil')
        if EncargadosVentas.objects.filter(encargadoVenta=encargadoVenta).exists():
            messages.error(request, "Este encargado de ventas ya esta registrado")
            return redirect('perfil')
        else:
            encargado_venta = EncargadoVentasForm(request.POST)
            if encargado_venta.is_valid():
                encargado_venta.save()
                return redirect('perfil')
    return render(request, 'AlphaInventory/perfil.html', {'usuario':usuario})

def editar_perfil(request):
    perfil = RegistroUsuario.objects.get(nombreUsuario=request.user)
    if request.method == "POST":
        nombreUsuario = request.POST['nombreUsuario']
        perfilform = PerfilForm(request.POST, instance=perfil)
        usuario = User.objects.get(username=request.user.username)
        if perfilform.is_valid():
            usuario.username = nombreUsuario
            usuario.save()
            perfilform.save()
            return redirect('perfil')
    else:
        perfilform = PerfilForm(instance=perfil)
    return render(request, 'AlphaInventory/editarperfil.html', {'perfil':perfil, 'perfilform':perfilform}) 

def cambiar_contrasena(request):
    usuario = User.objects.get(username=request.user)

    if request.method == "POST":
        Acontrasena = request.POST['contrasena__']
        contrasena = request.POST['contrasena']
        contrasena_ = request.POST['contrasena_']

        usuario.set_password(contrasena)

        if contrasena != contrasena_:
            messages.error(request, "Las contrasenas no coinciden")
            return redirect(reverse_lazy('cambiarcontrasena'))
        if RegistroUsuario.objects.filter(nombreUsuario=request.user, contrasena=Acontrasena):
            if contrasena == contrasena_:
                usuario.save()
                messages.success(request, "Su contrasena se restablecio correctamente")
                return redirect('index')
        else:
            messages.error(request, "La contrasena introducida no es tu antigua contrasena")
            return redirect(reverse_lazy('cambiarcontrasena'))
    return render(request, 'AlphaInventory/cambiarcontrasena.html')

def encargado_compras_cambiar_contrasena(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoCompra = request.POST['encargadoCompra']
        if EncargadosCompras.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de compras ya esta registrado")
            return redirect('cambiarcontrasena')
        if EncargadosCompras.objects.filter(encargadoCompra=encargadoCompra).exists():
            messages.error(request, "Este encargado de compras ya esta registrado")
            return redirect('cambiarcontrasena')
        else:
            encargado_compra = EncargadoComprasForm(request.POST)
            if encargado_compra.is_valid():
                encargado_compra.save()
                return redirect('cambiarcontrasena')
    return render(request, 'AlphaInventory/cambiarcontrasena.html',{'usuario':usuario})

def encargado_ventas_cambiar_contrasena(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoVenta = request.POST['encargadoVenta']
        if EncargadosVentas.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de ventas ya esta registrado")
            return redirect('cambiarcontrasena')
        if EncargadosVentas.objects.filter(encargadoVenta=encargadoVenta).exists():
            messages.error(request, "Este encargado de ventas ya esta registrado")
            return redirect('cambiarcontrasena')
        else:
            encargado_venta = EncargadoVentasForm(request.POST)
            if encargado_venta.is_valid():
                encargado_venta.save()
                return redirect('cambiarcontrasena')
    return render(request, 'AlphaInventory/cambiarcontrasena.html', {'usuario':usuario})

def terminos_condiciones(request):
    return render(request, 'AlphaInventory/terminosycondiciones.html')

def encargado_compras_terminos_condiciones(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoCompra = request.POST['encargadoCompra']
        if EncargadosCompras.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de compras ya esta registrado")
            return redirect('terminosycondiciones')
        if EncargadosCompras.objects.filter(encargadoCompra=encargadoCompra).exists():
            messages.error(request, "Este encargado de compras ya esta registrado")
            return redirect('terminosycondiciones')
        else:
            encargado_compra = EncargadoComprasForm(request.POST)
            if encargado_compra.is_valid():
                encargado_compra.save()
                return redirect('terminosycondiciones')
    return render(request, 'AlphaInventory/terminosycondiciones.html',{'usuario':usuario})

def encargado_ventas_terminos_condiciones(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    if request.method == "POST":
        codigo = request.POST['codigo']
        encargadoVenta = request.POST['encargadoVenta']
        if EncargadosVentas.objects.filter(codigo=codigo).exists():
            messages.error(request, "Este codigo de encargado de ventas ya esta registrado")
            return redirect('terminosycondiciones')
        if EncargadosVentas.objects.filter(encargadoVenta=encargadoVenta).exists():
            messages.error(request, "Este encargado de ventas ya esta registrado")
            return redirect('terminosycondiciones')
        else:
            encargado_venta = EncargadoVentasForm(request.POST)
            if encargado_venta.is_valid():
                encargado_venta.save()
                return redirect('terminosycondiciones')
    return render(request, 'AlphaInventory/terminosycondiciones.html', {'usuario':usuario})

def manual_uso(request):
    pdf = open('manualdeuso_alphainventory.pdf', 'rb')

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="manualdeuso_alphainventory.pdf"'
    
    return response

def eliminar_cuenta(request):
    usuario = RegistroUsuario.objects.filter(nombreUsuario=request.user)
    user = User.objects.filter(username=request.user)
    if request.method == "POST":
        usuario.delete()
        user.delete()
        return redirect('index')