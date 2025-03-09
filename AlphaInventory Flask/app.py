# IMPORTACIONES
from flask import Flask, render_template, request, redirect, session, flash, send_file, url_for
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
from datetime import datetime
from authlib.integrations.flask_client import OAuth
from itsdangerous import URLSafeTimedSerializer
import secrets

# INICIALIZACION DE LA APLICACION EN FLASK
app = Flask(__name__)

# CLAVE SECRETA
# app.secret_key = secrets.token_hex(32)

# CONFIGURACION BASE DE DATOS
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'alphainventory'

# INICIALIZACION DE LA BASE DE DATOS EN LA APLICACION
mysql = MySQL(app)

# CONFIGURACION CORREOS (SMTP)
app.config['MAIL_SERVER']= 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'jeironprogrammer@gmail.com'
app.config['MAIL_PASSWORD'] = 'kemhhnyiejhcortp'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# INICIALIZACION DE CORREOS EN LA APLICACION
mail = Mail(app)

# TOKEN PARA RECUPERAR CONTRASEÑA
serializer = URLSafeTimedSerializer(app.secret_key)

# RUTA MODALES
@app.route('/modales.html')
def modales():
    id_usuario = session.get('id_usuario')
    usuario = obtener_usuario(id_usuario)
    articulos = obtener_articulos(id_usuario)
    marcas = obtener_marcas(id_usuario)
    suplidores = obtener_suplidores(id_usuario)
    clientes = obtener_clientes(id_usuario)
    encargados_compras = obtener_encargados_compras(id_usuario)
    encargados_ventas = obtener_encargados_ventas(id_usuario)

    return render_template('modales.html', usuario=usuario, articulos=articulos, marcas=marcas, suplidores=suplidores, clientes=clientes, encargados_compras=encargados_compras, encargados_ventas=encargados_ventas)

@app.route('/menu')
def menu():
    return render_template('menu.html')

# FUNCION OBTENER USUARIOS
def obtener_usuario(id_usuario):
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM registro_usuario WHERE id_usuario = %s", (id_usuario,))
        usuario = cur.fetchall()
    return usuario

# FUNCION VERIFICAR EL CODIGO DE LA MARCA
def verificar_codigo_marca(codigo_marca, id_usuario):
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT codigo FROM marcas WHERE codigo = %s AND id_usuario = %s", (codigo_marca, id_usuario))
        codigo_marca = cur.fetchone()
    return codigo_marca

# FUNCION VERIFICAR EL NOMBRE DE LA MARCA
def verificar_nombre_marca(nombre_marca, id_usuario):
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT nombre FROM marcas WHERE nombre = %s AND id_usuario = %s", (nombre_marca, id_usuario))
        nombre_marca = cur.fetchone()
    return nombre_marca

# FUNCION CREAR LA MARCA EN LA BASE DE DATOS
def crear_marca(codigo_marca, nombre_marca, id_usuario):
    sql = ("INSERT INTO marcas (id_marca, codigo, nombre, id_usuario) VALUES (NULL, %s, %s, %s)")
    datos = (codigo_marca, nombre_marca, id_usuario)

    with mysql.connection.cursor() as cur:
        cur.execute(sql, datos)
        mysql.connection.commit()
    return flash('Enviando datos de la marca')

# RUTA CREAR MARCAS
@app.route('/crear_marca', methods=['POST'])
def creador_marca():
    id_usuario = session.get('id_usuario')
    codigo_marca = request.form.get('codigo_marca')
    nombre_marca = request.form.get('nombre_marca')

    referer_url = request.headers.get('Referer')

    if not referer_url:
        flash('Algo salio mal, al intentar crear el encargado de compras')
        referer_url = '/'
    if id_usuario:
        codigo_marca_existente = verificar_codigo_marca(codigo_marca, id_usuario)
        nombre_marca_existente = verificar_nombre_marca(nombre_marca, id_usuario)
        if codigo_marca_existente or nombre_marca_existente:
            flash(f'Este codigo {codigo_marca_existente} o nombre {nombre_marca_existente} de marca ya está registrado')
            return redirect(referer_url)
        else:
            crear_marca(nombre_marca, id_usuario)
            flash('Marca creada correctamente')
            return redirect(referer_url)
    else:
        return redirect(referer_url)

# FUNCION VERIFICAR EL CODIGO DEL ENCARGADO DE COMPRAS
def verificar_codigo_encargado_compras(codigo_encargado_compras, id_usuario):
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT codigo FROM encargados_compras WHERE codigo = %s AND id_usuario = %s", (codigo_encargado_compras, id_usuario,))
        codigo_encargado_compras = cur.fetchone()
    return codigo_encargado_compras

# FUNCION VERIFICAR EL NOMBRE DEL ENCARGADO DE COMPRAS
def verificar_nombre_encargado_compras(nombre_encargado_compras, id_usuario):
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT nombre FROM encargados_compras WHERE nombre = %s AND id_usuario = %s", (nombre_encargado_compras, id_usuario,))
        nombre_encargado_compras = cur.fetchone()
    return nombre_encargado_compras

# FUNCION CREAR EL ENCARGADO DE COMPRAS EN LA BASE DE DATOS
def crear_encargado_compras(codigo_encargado_compras, nombre_encargado_compras, id_usuario):
    sql = ("INSERT INTO encargados_compras (id_encargado_compras, codigo, nombre, id_usuario) VALUES (NULL, %s, %s, %s)")
    datos = (codigo_encargado_compras, nombre_encargado_compras, id_usuario)

    with mysql.connection.cursor() as cur:
        cur.execute(sql, datos)
        mysql.connection.commit()
    return flash('Enviando datos de encargado de compras')

# RUTA CREAR ENCARGADO DE COMPRAS EN LA BASE DE DATOS
@app.route('/crear_encargado_compras', methods=['POST'])
def creador_encargado_compras():
    codigo_encargado_compras = request.form.get('codigo_encargado_compras')
    nombre_encargado_compras = request.form.get('nombre_encargado_compras')
    id_usuario = session.get('id_usuario')

    referer_url = request.headers.get('Referer')

    if not referer_url:
        flash('Algo salio mal, al intentar crear el encargado de compras')
        referer_url = '/'
    if id_usuario:
        codigo_existente = verificar_codigo_encargado_compras(codigo_encargado_compras, id_usuario)
        nombre_existente = verificar_nombre_encargado_compras(nombre_encargado_compras, id_usuario)
        if codigo_existente:
            flash('Este código de encargado de compras ya está registrado')
            return redirect(referer_url)
        elif nombre_existente:
            flash('Este nombre de encargado de compras ya está registrado')
            return redirect(referer_url)
        else:
            crear_encargado_compras(codigo_encargado_compras, nombre_encargado_compras, id_usuario)
            flash('Encargado de compras creado correctamente')
            return redirect(referer_url)
    else:
        return redirect(referer_url)

# FUNCION VERIFICAR EL CODIGO DEL ENCARGADO DE VENTAS
def verificar_codigo_encargado_ventas(codigo_encargado_ventas, id_usuario):
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT codigo FROM encargados_ventas WHERE codigo = %s AND id_usuario = %s", (codigo_encargado_ventas, id_usuario,))
        codigo_encargado_ventas = cur.fetchone()
    return codigo_encargado_ventas

# FUNCION VERIFICAR EL NOMBRE DEL ENCARGADO DE VENTAS
def verificar_nombre_encargado_ventas(nombre_encargado_ventas, id_usuario):
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT nombre FROM encargados_ventas WHERE nombre = %s AND id_usuario = %s", (nombre_encargado_ventas, id_usuario,))
        nombre_encargado_ventas = cur.fetchone()
    return nombre_encargado_ventas

# FUNCION CREAR EL ENCARGADO DE VENTAS EN LA BASE DE DATOS
def crear_encargado_ventas(codigo_encargado_ventas, nombre_encargado_ventas, id_usuario):
    sql = ("INSERT INTO encargados_ventas (id_encargado_compras, codigo, nombre, id_usuario) VALUES (NULL, %s, %s, %s)")
    datos = (codigo_encargado_ventas, nombre_encargado_ventas, id_usuario)

    with mysql.connection.cursor() as cur:
        cur.execute(sql, datos)
        mysql.connection.commit()
    return flash('Enviando datos de encargado de ventas')

# RUTA CREAR ENCARGADO DE VENTAS EN LA BASE DE DATOS
@app.route('/crear_encargado_ventas', methods=['POST'])
def creador_encargado_ventas():
    codigo_encargado_ventas = request.form.get('codigo_encargado_ventas')
    nombre_encargado_ventas = request.form.get('nombre_encargado_ventas')
    id_usuario = session.get('id_usuario')

    referer_url = request.headers.get('Referer')

    if not referer_url:
        flash('Algo salio mal, al intentar crear el encargado de ventas')
        referer_url = '/'
    if id_usuario:
        codigo_existente = verificar_codigo_encargado_ventas(codigo_encargado_ventas, id_usuario)
        nombre_existente = verificar_nombre_encargado_ventas(nombre_encargado_ventas, id_usuario)
        if codigo_existente:
            flash('Este código de encargado de ventas ya está registrado')
            return redirect(referer_url)
        elif nombre_existente:
            flash('Este nombre de encargado de ventas ya está registrado')
            return redirect(referer_url)
        else:
            crear_encargado_compras(codigo_encargado_ventas, nombre_encargado_ventas, id_usuario)
            flash('Encargado de ventas creado correctamente')
            return redirect(referer_url)
    else:
        return redirect(referer_url)

# FUNCION OBTENER ARTICULOS
def obtener_articulos(id_usuario):
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM articulos WHERE id_usuario = %s", (id_usuario,))
        articulos = cur.fetchall()
    return articulos

# FUNCION PARA EDITAR ARTICULOS
def obtener_articulo_id(id):
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM articulos WHERE id_articulo = %s", (id,))
        articulo = cur.fetchall()
    return articulo

# FUNCION PARA ELIMINAR ARTICULOS
def eliminar_articulo(id_articulo, id_usuario):
    with mysql.connection.cursor() as cur:
        cur.execute("DELETE FROM articulos WHERE id_articulo = %s AND id_usuario = %s", (id_articulo, id_usuario,))
        mysql.connection.commit()
    return flash('Eliminando datos de la base de datos')

# FUNCION OBTENER SUPLIDORES
def obtener_suplidores(id_usuario):
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM suplidores WHERE id_usuario = %s", (id_usuario,))
        suplidores = cur.fetchall()
    return suplidores

# FUNCION PARA EDITAR SUPLIDORES
def obtener_suplidor_id(id):
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM suplidores WHERE id_suplidor = %s", (id,))
        suplidor = cur.fetchall()
    return suplidor

# FUNCION PARA ELIMINAR SUPLIDORES
def eliminar_suplidor(id_suplidor, id_usuario):
    with mysql.connection.cursor() as cur:
        cur.execute("DELETE FROM suplidores WHERE id_suplidor = %s AND id_usuario = %s", (id_suplidor, id_usuario,))
        mysql.connection.commit()
    return flash('Eliminando datos de la base de datos')

# FUNCION OBTENER CLIENTES
def obtener_clientes(id_usuario):
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM clientes WHERE id_usuario = %s", (id_usuario,))
        clientes = cur.fetchall()
    return clientes

# FUNCION PARA EDITAR CLIENTES
def obtener_cliente_id(id):
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM clientes WHERE id_cliente = %s", (id,))
        cliente = cur.fetchall()
    return cliente

# FUNCION PARA ELIMINAR CLIENTES
def eliminar_cliente(id_cliente, id_usuario):
    with mysql.connection.cursor() as cur:
        cur.execute("DELETE FROM clientes WHERE id_cliente = %s AND id_usuario = %s", (id_cliente, id_usuario,))
        mysql.connection.commit()
    return flash('Eliminando datos de la base de datos')

# FUNCION OBTENER MARCAS
def obtener_marcas(id_usuario):
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM marcas WHERE id_usuario = %s", (id_usuario,))
        marcas = cur.fetchall()
    return marcas

# FUNCION OBTENER ENCARGADOS DE COMPRAS
def obtener_encargados_compras(id_usuario):
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM encargados_compras WHERE id_usuario = %s",(id_usuario,))
        encargados_compras = cur.fetchall()
    return encargados_compras

# FUNCION OBTENER ENCARGADOS DE VENTAS
def obtener_encargados_ventas(id_usuario):
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM encargados_ventas WHERE id_usuario = %s", (id_usuario,))
        encargados_ventas = cur.fetchall()
    return encargados_ventas

# FUNCION OBTENER COMPRAS
def obtener_compras(id_usuario):
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM compras WHERE id_usuario = %s", (id_usuario,))
        compras = cur.fetchall()
    return compras

# FUNCION OBTENER VENTAS
def obtener_ventas(id_usuario):
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM ventas WHERE id_usuario = %s", (id_usuario,))
        ventas = cur.fetchall()
    return ventas

# FUNCION PARA FILTROS DE COMPRAS DIARIAS
def filtros_compras_diarias(fecha_compra, id_usuario):
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM compras WHERE fecha_compra = %s AND id_usuario = %s", (fecha_compra, id_usuario,))
        filtro_compra_diaria = cur.fetchall()
    return filtro_compra_diaria

# FUNCION PARA FILTROS DE VENTAS DIARIAS
def filtros_ventas_diarias(fecha_venta, id_usuario):
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM ventas WHERE fecha_venta = %s AND id_usuario = %s", (fecha_venta, id_usuario,))
        filtro_venta_diaria = cur.fetchall()
    return filtro_venta_diaria

# FUNCION PARA FILTROS DE COMPRAS POR ARTICULOS
def filtros_compras_articulos(id_usuario, codigo_desde, codigo_hasta):
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM compras WHERE id_usuario = %s AND codigo BETWEEN %s AND %s", (id_usuario, codigo_desde, codigo_hasta))
        filtro_compra_articulo = cur.fetchall()
    return filtro_compra_articulo

# FUNCION PARA FILTROS DE VENTAS POR ARTICULOS
def filtros_ventas_articulos(id_usuario, codigo_desde, codigo_hasta):
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM ventas WHERE id_usuario = %s AND codigo BETWEEN %s AND %s", (id_usuario, codigo_desde, codigo_hasta))
        filtro_venta_articulo = cur.fetchall()
    return filtro_venta_articulo

# FUNCION PARA FILTROS DE LISTADO DE ARTICULOS
def filtros_articulos(id_usuario, codigo_desde, codigo_hasta):
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM articulos WHERE id_usuario = %s AND codigo BETWEEN %s AND %s", (id_usuario, codigo_desde, codigo_hasta))
        filtro_articulo = cur.fetchall()
    return filtro_articulo

# FUNCION PARA FILTROS DE LISTADO DE CLIENTES
def filtros_clientes(id_usuario, codigo_cliente, nombre_cliente):
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM clientes WHERE id_usuario = %s AND codigo = %s OR nombre = %s", (id_usuario, codigo_cliente, nombre_cliente))
        filtro_cliente = cur.fetchall()
    return filtro_cliente

# FUNCION PARA FILTROS DE LISTADO DE SUPLIDORES
def filtros_suplidores(id_usuario, codigo_suplidor, nombre_suplidor):
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM suplidores WHERE id_usuario = %s AND codigo = %s OR nombre = %s", (id_usuario, codigo_suplidor, nombre_suplidor))
        filtro_suplidor = cur.fetchall()
    return filtro_suplidor

# FUNCION PARA FILTROS DE LISTADO DE MARCAS
def filtros_marcas(id_usuario, codigo_desde, codigo_hasta):
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM marcas WHERE id_usuario = %s AND codigo BETWEEN %s AND %s", (id_usuario, codigo_desde, codigo_hasta))
        filtro_marca = cur.fetchall()
    return filtro_marca

# FUNCION PARA FILTROS DE LISTADO DE ENCARGADOS DE COMPRAS
def filtros_encargados_compras(id_usuario, codigo_desde, codigo_hasta):
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM encargados_compras WHERE id_usuario = %s AND codigo BETWEEN %s AND %s", (id_usuario, codigo_desde, codigo_hasta))
        filtro_encargado_compra = cur.fetchall()
    return filtro_encargado_compra

# FUNCION PARA FILTROS DE LISTADO DE ENCARGADOS DE VENTAS
def filtros_encargados_ventas(id_usuario, codigo_desde, codigo_hasta):
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM encargados_ventas WHERE id_usuario = %s AND codigo BETWEEN %s AND %s", (id_usuario, codigo_desde, codigo_hasta))
        filtro_encargado_venta = cur.fetchall()
    return filtro_encargado_venta

# FUNCION ELIMINAR CUENTA
def eliminar_mi_cuenta(id_usuario):
    with mysql.connection.cursor() as cur:
        cur.execute("DELETE FROM registro_usuario WHERE id_usuario = %s", (id_usuario,))
        mysql.connection.commit()
    return flash('Cuenta eliminada correctamente')

# RUTA ELIMINAR CUENTA
@app.route('/eliminar_cuenta', methods=['POST'])
def eliminar_cuenta():
    id_usuario = session.get('id_usuario')

    if id_usuario:
        eliminar_mi_cuenta(id_usuario)
        session.pop('id_usuario', None)
        return redirect(url_for('index'))
    else:
        return flash('Autenticacion no encontrada')

# INICIO DE SESION (GOOGLE)
oauth = OAuth(app)
google = oauth.register(
    name = 'google',
    authorize_url = 'https://accounts.google.com/o/oauth2/auth',
    authorize_params = None,
    access_token_url = 'https://accounts.google.com/o/oauth2/token',
    access_token_params = None,
    refresh_token_url = None,
    redirect_uri = 'http://127.0.0.1:5000/login/authorized',
    client_kwargs = {
        'scope':'openid email profile',
    },
    userinfo_endpoint = 'https://www.googleapis.com/oauth2/v3/userinfo',
    jwks_uri = 'https://www.googleapis.com/oauth2/v3/certs'
)

# RUTA AL REDIRECCIONAMIENTO PARA VERIFICAR LA AUTORIZACION DE GOOGLE
@app.route('/login/google')
def login_google():
    redirect_uri = url_for('google_authorized', _external=True)
    return google.authorize_redirect(redirect_uri)

# RUTA DE AUTORIZACION DE GOOGLE Y CREACION DE LA CUENTA EN LA BASE DE DATOS
@app.route('/login/google/authorized')
def google_authorized():
    try:
        token = google.authorize_access_token()
        session['google_token'] = token
        resp = google.get('https://www.googleapis.com/oauth2/v3/userinfo')
        resp.raise_for_status()
        user_info = resp.json()
        session['user'] = user_info
        
        with mysql.connection.cursor() as cur:
            cur.execute("SELECT id_usuario, correo_electronico FROM registro_usuario WHERE correo_electronico = %s", (user_info['email'],))
            usuario_existente = cur.fetchone()

        if usuario_existente:
            session['logueado'] = True
            session['id_usuario'] = usuario_existente[0]
            return redirect(url_for('inicio_inventario'))
        else:
            with mysql.connection.cursor() as cur:
                cur.execute("INSERT INTO registro_usuario (id_usuario, nombre, apellido, direccion, telefono, correo_electronico, contrasena) VALUES (NULL, %s, %s, %s, %s, %s, %s)", (user_info.get('given_name', ''), user_info.get('family_name', ''), 'NA', 'NA', user_info['email'], 'NA'))
                mysql.connection.commit()
            return redirect(url_for('inicio_inventario'))
    except Exception:
        flash('Error al iniciar sesion con Google')
        return redirect(url_for('index'))

# RUTA INDEX / SITIO
@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        correo_electronico = request.form.get('correo_electronico')
        contrasena = request.form.get('contrasena')

        with mysql.connection.cursor() as cur:
            cur.execute("SELECT contrasena FROM registro_usuario WHERE correo_electronico = %s", (correo_electronico,))
            login_google = cur.fetchone()
        
            if login_google and login_google[0] == 'NA':
                flash('El correo electronico esta registrado con google')
                return redirect(url_for('index'))
            
            cur.execute("SELECT id_usuario, correo_electronico, contrasena FROM registro_usuario WHERE correo_electronico = %s AND contrasena = %s", (correo_electronico, contrasena,))
            data = cur.fetchone()

        if data:
            session['logueado'] = True
            session['id_usuario'] = data[0]
            return redirect(url_for('inicio_inventario'))
        else:
            flash('El correo electronico o la contraseña son incorrectos')
            return redirect(url_for('index'))
    return render_template('sitio/index.html')
        
# RUTA OLVIDASTE TU CONTRASEÑA / BASE DE DATOS
@app.route('/olvidastetucontrasena', methods = ['POST'])
def olvidaste_tu_contrasena_bd():
    correo_recuperacion = request.form.get('correo_recuperacion')

    with mysql.connection.cursor() as cur:
        cur.execute("SELECT correo_electronico, nombre FROM registro_usuario WHERE correo_electronico = %s", (correo_recuperacion,))
        usuario = cur.fetchone()
    
    if usuario:
        token = serializer.dumps(correo_recuperacion, salt='password-recovery-salt')
        link = url_for('recuperar_contrasena', token=token, _external=True)
        msg = Message('AlphaInventory', sender = 'jeironprogrammer@gmail.com', recipients = [correo_recuperacion])
        msg.html = f"Hola {usuario[1]},<br>¡Hubo una solicitud para cambiar su contraseña!<br>Si no realizó esta solicitud, ignore este correo electrónico.<br>De lo contrario, ingrese a este enlace para cambiar su contraseña: <a href='{link}' target='blank'>Enlace</a>"
        mail.send(msg)
        flash('Correo enviado exitosamente')
        return redirect(url_for('index'))
    else:
        flash(f'Este correo electronico {correo_recuperacion} no esta registrado')
        return redirect(url_for('index'))
  
# RUTA CERRAR SESION
@app.route('/cerrar_sesion')
def cerrar_sesion():
    session.clear()
    session.pop('user', None)
    return redirect(url_for('index'))

# RUTA INICIO INVENTARIO
@app.route('/inicio_inventario')
def inicio_inventario():
    if not 'logueado' in session:
        return redirect(url_for('index'))

    user = session.get('user')
    id_usuario = session.get('id_usuario')
    usuario = obtener_usuario(id_usuario)
    marcas = obtener_marcas(id_usuario)
    encargados_compras = obtener_encargados_compras(id_usuario)
    encargados_ventas = obtener_encargados_ventas(id_usuario)

    return render_template('sitio/inicio_inventario.html', user=user, usuario=usuario, marcas=marcas, encargados_ventas=encargados_ventas, encargados_compras=encargados_compras)

# RUTA MOVIMIENTOS DIARIOS COMPRAS 
@app.route('/movimientosdiarioscompras', methods=['GET', 'POST'])
def movimientos_diarios_compras():
    if not 'logueado' in session:
        return redirect(url_for('index'))  
    
    id_usuario = session.get('id_usuario')
    marcas = obtener_marcas(id_usuario)
    encargados_compras = obtener_encargados_compras(id_usuario)
    encargados_ventas = obtener_encargados_ventas(id_usuario)
    
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT SUM(cantidad*costo) FROM compras WHERE id_usuario = %s", (id_usuario,))
        costo_total = cur.fetchone()

    costo_total = costo_total[0] if costo_total[0] is not None else 0

    if request.method == 'POST':
        if 'reiniciar' in request.form:
            compras = obtener_compras(id_usuario)
        else:
            fecha_compra = request.form.get('fecha_compra')
            if fecha_compra:
                fecha_compra_posterior = datetime.strptime(fecha_compra, '%Y-%m-%d')
                if fecha_compra_posterior > datetime.now():
                    flash('La fecha no puede ser posterior a la actual')
                    return redirect(url_for('movimientos_diarios_compras'))
                with mysql.connection.cursor() as cur:
                    cur.execute("SELECT fecha_compra FROM compras WHERE fecha_compra = %s AND id_usuario = %s", (fecha_compra, id_usuario,))
                    verificar_fecha_compra = cur.fetchone()
                if verificar_fecha_compra:
                    compras = filtros_compras_diarias(fecha_compra, id_usuario)
                else:
                    compras = obtener_compras(id_usuario)
                    flash('Este dia no se realizaron compras')
                    return redirect(url_for('movimientos_diarios_compras'))
            else:
                compras = obtener_compras(id_usuario)
    else:
        compras = obtener_compras(id_usuario)

    return render_template ('sitio/movimientosdiarioscompras.html', compras=compras, marcas=marcas, encargados_ventas=encargados_ventas, encargados_compras=encargados_compras, costo_total=costo_total)

# RUTA MOVIMIENTOS DIARIOS VENTAS
@app.route('/movimientosdiariosventas', methods=['GET', 'POST'])
def movimientos_diarios_ventas():
    if not 'logueado' in session:
        return redirect(url_for('index'))  
    
    id_usuario = session.get('id_usuario')
    marcas = obtener_marcas(id_usuario)
    encargados_compras = obtener_encargados_compras(id_usuario)
    encargados_ventas = obtener_encargados_ventas(id_usuario)

    with mysql.connection.cursor() as cur:
        cur.execute("SELECT SUM(cantidad*precio) FROM ventas WHERE id_usuario = %s", (id_usuario,))
        precio_total = cur.fetchone()
    
    precio_total = precio_total[0] if precio_total[0] is not None else 0

    if request.method == 'POST':
        if 'reiniciar' in request.form:
            ventas = obtener_ventas(id_usuario)
        else:
            fecha_venta = request.form.get('fecha_venta')
            if fecha_venta:
                fecha_venta_posterior = datetime.strptime(fecha_venta, '%Y-%m-%d')
                if fecha_venta_posterior > datetime.now():
                    flash('La fecha no puede ser posterior a la actual')
                    return redirect(url_for('movimientos_diarios_ventas'))
                with mysql.connection.cursor() as cur:
                    cur.execute("SELECT fecha_venta FROM ventas WHERE fecha_venta = %s AND id_usuario = %s", (fecha_venta, id_usuario,))
                    verificar_fecha_venta = cur.fetchone()
                
                if verificar_fecha_venta:
                    ventas = filtros_ventas_diarias(fecha_venta, id_usuario)
                else:
                    ventas = obtener_ventas(id_usuario)
                    flash('Este dia no se realizaron ventas')
                    return redirect(url_for('movimientos_diarios_ventas'))
            else:
                ventas = obtener_ventas(id_usuario)
    else:
        ventas = obtener_ventas(id_usuario)
    return render_template('sitio/movimientosdiariosventas.html', ventas=ventas, compras=compras, marcas=marcas, encargados_ventas=encargados_ventas, encargados_compras=encargados_compras, precio_total=precio_total)

# RUTA MOVIMEINTOS POR ARTICULOS COMPRAS
@app.route('/movimientosporarticuloscompras', methods=['GET', 'POST'])
def movimientos_articulos_compras():
    if not 'logueado' in session:
        return redirect(url_for('index'))
    
    id_usuario = session.get('id_usuario')
    marcas = obtener_marcas(id_usuario)
    encargados_compras = obtener_encargados_compras(id_usuario)
    encargados_ventas = obtener_encargados_ventas(id_usuario)

    if request.method == 'POST':
        if 'reiniciar' in request.form:
            compras = obtener_compras(id_usuario)
        else:
            codigo_desde = request.form.get('codigo_desde')
            codigo_hasta = request.form.get('codigo_hasta')
            if codigo_desde and codigo_hasta:
                with mysql.connection.cursor() as cur:
                    cur.execute("SELECT codigo FROM compras WHERE codigo = %s AND id_usuario = %s", (codigo_desde, id_usuario,))
                    verificar_codigo_desde = cur.fetchone()
                    cur.execute("SELECT codigo FROM compras WHERE codigo = %s AND id_usuario = %s", (codigo_hasta, id_usuario,))
                    verificar_codigo_hasta = cur.fetchone()
                    if verificar_codigo_desde and verificar_codigo_hasta:
                        compras = filtros_compras_articulos(id_usuario, codigo_desde, codigo_hasta)
                    else:
                        compras = obtener_compras(id_usuario)
                        flash('Uno o los dos codigos de articulos no estan registrados')
                        return redirect(url_for('movimientos_articulos_compras'))
            else:
                compras = obtener_compras(id_usuario)
    else:
        compras = obtener_compras(id_usuario)

    return render_template ('sitio/movimientosporarticuloscompras.html', compras=compras, marcas=marcas, encargados_ventas=encargados_ventas, encargados_compras=encargados_compras)

# RUTA MOVIMEINTOS POR ARTICULOS VENTAS
@app.route('/movimientosporarticulosventas', methods=['GET', 'POST'])
def movimientos_articulos_ventas():
    if not 'logueado' in session:
        return redirect(url_for('index'))

    id_usuario = session.get('id_usuario')
    marcas = obtener_marcas(id_usuario)
    encargados_compras = obtener_encargados_compras(id_usuario)
    encargados_ventas = obtener_encargados_ventas(id_usuario)

    if request.method == 'POST':
        if 'reiniciar' in request.form:
            ventas = obtener_ventas(id_usuario)
        else:
            codigo_desde = request.form.get('codigo_desde')
            codigo_hasta = request.form.get('codigo_hasta')
            if codigo_desde and codigo_hasta:
                with mysql.connection.cursor() as cur:
                    cur.execute("SELECT codigo FROM ventas WHERE codigo = %s AND id_usuario = %s", (codigo_desde, id_usuario,))
                    verificar_codigo_desde = cur.fetchone()
                    cur.execute("SELECT codigo FROM ventas WHERE codigo = %s AND id_usuario = %s", (codigo_hasta, id_usuario,))
                    verificar_codigo_hasta = cur.fetchone()               
                    if verificar_codigo_desde and verificar_codigo_hasta:
                        ventas = filtros_ventas_articulos(id_usuario, codigo_desde, codigo_hasta)
                    else:
                        ventas = obtener_ventas(id_usuario)
                        flash('Uno o los dos codigos de articulos no estan registrados')
                        return redirect(url_for('movimientos_articulos_ventas'))
            else:
                ventas = obtener_ventas(id_usuario)
    else:
        ventas = obtener_ventas(id_usuario)

    return render_template ('sitio/movimientosporarticulosventas.html', ventas=ventas, marcas=marcas, encargados_ventas=encargados_ventas, encargados_compras=encargados_compras)

# RUTA LISTADO DE ARTICULOS
@app.route('/listadodearticulos', methods=['GET', 'POST'])
def listado_articulos():
    if not 'logueado' in session:
        return redirect(url_for('index'))
    
    id_usuario = session.get('id_usuario')
    marcas = obtener_marcas(id_usuario)
    encargados_compras = obtener_encargados_compras(id_usuario)
    encargados_ventas = obtener_encargados_ventas(id_usuario)

    with mysql.connection.cursor() as cur:
        cur.execute("SELECT SUM(cantidad*costo) FROM articulos WHERE id_usuario = %s", (id_usuario,))
        precio_total_articulos = cur.fetchone()

    precio_total_articulos = precio_total_articulos[0] if precio_total_articulos[0] is not None else 0

    if request.method == 'POST':
        id_articulo = request.form.get('id_articulo')
        if id_articulo:
            with mysql.connection.cursor() as cur:
                cur.execute("SELECT cantidad FROM articulos WHERE id_articulo = %s AND id_usuario = %s", (id_articulo, id_usuario,))
                cantidad_articulo = cur.fetchone()
                if cantidad_articulo[0] != 0:
                    flash(f'No puedes eliminar este articulos porque todavia hay {cantidad_articulo[0]} disponibles')
                    return redirect(url_for('listado_articulos'))
                else:
                    eliminar_articulo(id_articulo, id_usuario)
                    return redirect(url_for('listado_articulos'))
        if 'reiniciar' in request.form:
            articulos = obtener_articulos(id_usuario)
        else:
            codigo_desde = request.form.get('codigo_desde')
            codigo_hasta = request.form.get('codigo_hasta')
            if codigo_desde and codigo_hasta:
                with mysql.connection.cursor() as cur:
                    cur.execute("SELECT codigo FROM articulos WHERE codigo = %s AND id_usuario = %s", (codigo_desde, id_usuario,))
                    verificar_codigo_desde = cur.fetchone()
                    cur.execute("SELECT codigo FROM articulos WHERE codigo = %s AND id_usuario = %s", (codigo_hasta, id_usuario,))
                    verificar_codigo_hasta = cur.fetchone()
                    if verificar_codigo_desde and verificar_codigo_hasta:
                        articulos = filtros_articulos(id_usuario, codigo_desde, codigo_hasta)
                    else:
                        articulos = obtener_articulos(id_usuario)
                        flash('Uno o los dos codigos de articulos no estan registrados')
                        return redirect(url_for('listado_articulos'))
            else:
                articulos = obtener_articulos(id_usuario)
    else:
        articulos = obtener_articulos(id_usuario)

    return render_template('sitio/listadodearticulos.html', articulos=articulos, marcas=marcas, encargados_ventas=encargados_ventas, encargados_compras=encargados_compras, precio_total_articulos=precio_total_articulos)

# RUTA EDITAR ARTICULO / BASE DE DATOS
@app.route('/editararticulo/<int:id>', methods=['GET', 'POST'])
def editar_articulo_bd(id):
    articulo = obtener_articulo_id(id)
    if articulo is None:
        flash('Articulo no encontrado')
        return redirect(url_for('listado_articulos'))
    
    if request.method == 'POST':
        codigo = request.form.get('codigo')
        descripcion = request.form.get('descripcion')
        talla = request.form.get('talla')
        marca = request.form.get('marca')
        referencia = request.form.get('referencia')
        ubicacion = request.form.get('direccion')
        costo = float(request.form.get('costo'))
        precio = float(request.form.get('precio'))
        itbis = request.form.get('itbis')
        unidad_medida = request.form.get('medida')
        margen_beneficio = round(((precio - costo) / precio) * 100, 2)

        if not id:
            flash('Ocurrio un error al intentar verificar el id del articulo')
            return redirect(url_for('editar_articulo_bd', articulo=articulo))
        else:
            with mysql.connection.cursor() as cur:
                cur.execute("UPDATE articulos SET codigo = %s, descripcion = %s, talla = %s, marca = %s, referencia = %s, ubicacion = %s, costo = %s, precio = %s, itbis = %s, unidad_medida = %s, margen_beneficio = %s WHERE id_articulo = %s",(codigo, descripcion, talla, marca, referencia, ubicacion, costo, precio, itbis, unidad_medida, margen_beneficio, id))
                mysql.connection.commit()
            flash('Articulo actualizado exitosamente')
            return redirect(url_for('listado_articulos'))
    return render_template('admin/editararticulo.html', articulo=articulo)

# RUTA LISTADO DE COMPRAS
@app.route('/listadodecompras', methods=['GET', 'POST'])
def listado_compras():
    if not 'logueado' in session:
        return redirect(url_for('index'))
    
    id_usuario = session.get('id_usuario')
    suplidores = obtener_suplidores(id_usuario)
    marcas = obtener_marcas(id_usuario)
    encargados_compras = obtener_encargados_compras(id_usuario)
    encargados_ventas = obtener_encargados_ventas(id_usuario)
    compras = obtener_compras(id_usuario)

    with mysql.connection.cursor() as cur:
        cur.execute("SELECT SUM(total_compra) FROM compras WHERE id_usuario = %s", (id_usuario,))
        costo_total = cur.fetchone()
    costo_total = costo_total[0] if costo_total[0] is not None else 0
    if request.method == 'POST':
        if 'reiniciar' in request.form:
            compras = obtener_compras(id_usuario)
        else:
            codigo_desde = request.form.get('codigo_desde')
            codigo_hasta = request.form.get('codigo_hasta')
            if codigo_desde and codigo_hasta:
                with mysql.connection.cursor() as cur:
                    cur.execute("SELECT codigo FROM compras WHERE codigo = %s AND id_usuario = %s", (codigo_desde, id_usuario,))
                    verificar_codigo_desde = cur.fetchone()
                    cur.execute("SELECT codigo FROM compras WHERE codigo = %s AND id_usuario = %s", (codigo_hasta, id_usuario,))
                    verificar_codigo_hasta = cur.fetchone()
                    if verificar_codigo_desde and verificar_codigo_hasta:
                        compras = filtros_compras_articulos(id_usuario, codigo_desde, codigo_hasta)
                    else:
                        compras = obtener_compras(id_usuario)
                        flash('Uno o los dos codigos de articulos no estan registrados')
                        return redirect(url_for('/listado_compras'))
            else:
                compras = obtener_compras(id_usuario)
    else:
        compras = obtener_compras(id_usuario)
    return render_template('sitio/listadodecompras.html', compras=compras, suplidores=suplidores, marcas=marcas, encargados_ventas=encargados_ventas, encargados_compras=encargados_compras, costo_total=costo_total)

# RUTA LISTADO DE VENTAS
@app.route('/listadodeventas', methods=['GET', 'POST'])
def listado_ventas():
    if not 'logueado' in session:
        return redirect(url_for('index'))
    
    id_usuario = session.get('id_usuario')
    clientes = obtener_clientes(id_usuario)
    marcas = obtener_marcas(id_usuario)
    encargados_compras = obtener_encargados_compras(id_usuario)
    encargados_ventas = obtener_encargados_ventas(id_usuario)

    with mysql.connection.cursor() as cur:
        cur.execute("SELECT SUM(total_venta) FROM ventas WHERE id_usuario = %s", (id_usuario,))
        precio_total = cur.fetchone()
    precio_total = precio_total[0] if precio_total[0] is not None else 0
    if request.method == 'POST':
        if 'reiniciar' in request.form:
            ventas = obtener_ventas(id_usuario)
        else:
            codigo_desde = request.form.get('codigo_desde')
            codigo_hasta = request.form.get('codigo_hasta')
            if codigo_desde and codigo_hasta:
                with mysql.connection.cursor() as cur:
                    cur.execute("SELECT codigo FROM ventas WHERE codigo = %s AND id_usuario = %s", (codigo_desde, id_usuario,))
                    verificar_codigo_desde = cur.fetchone()
                    cur.execute("SELECT codigo FROM ventas WHERE codigo = %s AND id_usuario = %s", (codigo_hasta, id_usuario,))
                    verificar_codigo_hasta = cur.fetchone()   
                    if verificar_codigo_desde and verificar_codigo_hasta:
                        ventas = filtros_ventas_articulos(id_usuario, codigo_desde, codigo_hasta)
                    else:
                        ventas = obtener_ventas(id_usuario)
                        flash('Uno o los dos codigos de articulos no estan registrados')
                        return redirect(url_for('listado_ventas'))
            else:
                ventas = obtener_ventas(id_usuario)
    else:
        ventas = obtener_ventas(id_usuario)
    return render_template('sitio/listadodeventas.html', ventas=ventas, clientes=clientes, marcas=marcas, encargados_ventas=encargados_ventas, encargados_compras=encargados_compras, precio_total=precio_total)

# RUTA LISTADO DE SUPLIDORES
@app.route('/listadodesuplidores', methods=['GET', 'POST'])
def listado_suplidores():
    if not 'logueado' in session:
        return redirect(url_for('index'))
    
    id_usuario = session.get('id_usuario')
    marcas = obtener_marcas(id_usuario)
    encargados_compras = obtener_encargados_compras(id_usuario)
    encargados_ventas = obtener_encargados_ventas(id_usuario)

    if request.method == 'POST':
        id_suplidor = request.form.get('id_suplidor')
        if id_suplidor:
            eliminar_suplidor(id_suplidor, id_usuario)
            return redirect(url_for('listado_suplidores'))
        if 'reiniciar' in request.form:
            suplidores = obtener_suplidores(id_usuario)
        else:
            codigo_suplidor = request.form.get('codigo_suplidor')
            nombre_suplidor = request.form.get('nombre_suplidor')
            if codigo_suplidor or nombre_suplidor:
                with mysql.connection.cursor() as cur:
                    cur.execute("SELECT codigo FROM suplidores WHERE codigo = %s AND id_usuario = %s", (codigo_suplidor, id_usuario,))
                    verificar_codigo_suplidor = cur.fetchone()
                    cur.execute("SELECT nombre FROM suplidores WHERE nombre = %s AND id_usuario = %s", (nombre_suplidor, id_usuario,))
                    verificar_nombre_suplidor = cur.fetchone()
                    if verificar_codigo_suplidor or verificar_nombre_suplidor:
                        suplidores = filtros_suplidores(id_usuario, codigo_suplidor, nombre_suplidor)
                    else:
                        suplidores = obtener_suplidores(id_usuario)
                        flash('El codigo o nombre no esta registrados')
                        return redirect(url_for('listado_suplidores'))
            else:
                suplidores = obtener_suplidores(id_usuario)
    else:
        suplidores = obtener_suplidores(id_usuario)
    return render_template('sitio/listadodesuplidores.html', suplidores=suplidores, marcas=marcas, encargados_ventas=encargados_ventas, encargados_compras=encargados_compras)

# RUTA EDITAR SUPLIDOR / BASE DE DATOS
@app.route('/editarsuplidor/<int:id>', methods=['GET', 'POST'])
def editar_suplidor_bd(id):
    suplidor = obtener_suplidor_id(id)
    if suplidor is None:
        flash('Suplidor no encontrado')
        return redirect(url_for('listado_suplidores'))
    
    if request.method == 'POST':
        codigo = request.form.get('codigo')
        nombre = request.form.get('nombre')
        direccion = request.form.get('direccion')
        ciudad = request.form.get('ciudad')
        telefono = request.form.get('telefono')
        limite_credito = request.form.get('limite_credito')
        condiciones = request.form.get('condiciones')
        rnc = request.form.get('rnc')
        descuentos = request.form.get('descuento')

        if not id:
            flash('Ocurrio un error al intentar verificar el id del suplidor')
            return redirect(url_for('editar_suplidor_bd', suplidor=suplidor))
        else:
            with mysql.connection.cursor() as cur:
                cur.execute("UPDATE suplidores SET codigo = %s, nombre = %s, direccion = %s, ciudad = %s, telefono = %s, limite_credito = %s, condiciones = %s, rnc = %s, descuentos = %s WHERE id_suplidor = %s",(codigo, nombre, direccion, ciudad, telefono, limite_credito, condiciones, rnc, descuentos, id))
                mysql.connection.commit()
            flash('Suplidor actualizado exitosamente')
            return redirect(url_for('listado_suplidores'))
    return render_template('admin/editarsuplidor.html', suplidor=suplidor)

# RUTA LISTADO DE CLIENTES
@app.route('/listadodeclientes', methods=['GET', 'POST'])
def listado_clientes():
    if not 'logueado' in session:
        return redirect(url_for('index'))
    
    id_usuario = session.get('id_usuario')
    marcas = obtener_marcas(id_usuario)
    encargados_compras = obtener_encargados_compras(id_usuario)
    encargados_ventas = obtener_encargados_ventas(id_usuario)

    if request.method == 'POST':
        id_cliente = request.form.get('id_cliente')
        if id_cliente:
            eliminar_cliente(id_cliente, id_usuario)
            return redirect(url_for('listado_clientes'))
        if 'reiniciar' in request.form:
            clientes = obtener_clientes(id_usuario)
        else:
            codigo_cliente = request.form.get('codigo_cliente')
            nombre_cliente = request.form.get('nombre_cliente')
            if codigo_cliente or nombre_cliente:
                with mysql.connection.cursor() as cur:
                    cur.execute("SELECT codigo FROM clientes WHERE codigo = %s AND id_usuario = %s", (codigo_cliente, id_usuario,))
                    verificar_codigo_cliente = cur.fetchone()
                    cur.execute("SELECT nombre FROM clientes WHERE nombre = %s AND id_usuario = %s", (nombre_cliente, id_usuario,))
                    verificar_nombre_cliente = cur.fetchone()
                    if verificar_codigo_cliente or verificar_nombre_cliente:
                        clientes = filtros_clientes(id_usuario, codigo_cliente, nombre_cliente)
                    else:
                        clientes = obtener_clientes(id_usuario)
                        flash('El codigo o nombre no esta registrados')
                        return redirect(url_for('listado_clientes'))
            else:
                clientes = obtener_clientes(id_usuario)
    else:
        clientes = obtener_clientes(id_usuario)
    return render_template('sitio/listadodeclientes.html', clientes=clientes, marcas=marcas, encargados_ventas=encargados_ventas, encargados_compras=encargados_compras)

# RUTA EDITAR CLIENTE / BASE DE DATOS
@app.route('/editarcliente/<int:id>', methods=['GET', 'POST'])
def editar_cliente_bd(id):
    cliente = obtener_cliente_id(id)
    if cliente is None:
        flash('Cliente no encontrado')
        return redirect(url_for('listado_clientes'))
    
    if request.method == 'POST':
        codigo = request.form.get('codigo')
        nombre = request.form.get('nombre')
        direccion = request.form.get('direccion')
        ciudad = request.form.get('ciudad')
        telefono = request.form.get('telefono')
        cedula = request.form.get('cedula')
        correo_electronico = request.form.get('correo_electronico')
        rnc = request.form.get('rnc')
        descuentos = request.form.get('descuento')

        if not id:
            flash('Ocurrio un error al intentar verificar el id del cliente')
            return redirect(url_for('editar_cliente_bd', cliente=cliente))
        else:
            with mysql.connection.cursor() as cur:
                cur.execute("UPDATE clientes SET codigo = %s, nombre = %s, direccion = %s, ciudad = %s, telefono = %s, cedula = %s, correo_electronico = %s, rnc = %s, descuentos = %s WHERE id_cliente = %s",(codigo, nombre, direccion, ciudad, telefono, cedula, correo_electronico, rnc, descuentos, id))
                mysql.connection.commit()
            flash('Cliente actualizado exitosamente')
            return redirect(url_for('listado_clientes'))
    return render_template('admin/editarcliente.html', cliente=cliente)

@app.route('/listadodemarcas', methods=['GET', 'POST'])
def listado_marcas():
    if not 'logueado' in session:
        return redirect(url_for('index'))
    
    id_usuario = session.get('id_usuario')
    marcas = obtener_marcas(id_usuario)

    if request.method == 'POST':
        if 'reiniciar' in request.form:
            marcas = obtener_marcas(id_usuario)
        else:
            codigo_desde = request.form.get('codigo_desde')
            codigo_hasta = request.form.get('codigo_hasta')
            if codigo_desde and codigo_hasta:
                with mysql.connection.cursor() as cur:
                    cur.execute("SELECT codigo FROM marcas WHERE codigo = %s AND id_usuario = %s", (codigo_desde, id_usuario,))
                    verificar_codigo_desde = cur.fetchone()
                    cur.execute("SELECT codigo FROM marcas WHERE codigo = %s AND id_usuario = %s", (codigo_hasta, id_usuario,))
                    verificar_codigo_hasta = cur.fetchone()
                    if verificar_codigo_desde and verificar_codigo_hasta:
                        marcas = filtros_marcas(id_usuario, codigo_desde, codigo_hasta)
                    else:
                        marcas = obtener_marcas(id_usuario)
                        flash('Uno o los dos codigos de marcas no estan registrados')
                        return redirect(url_for('listado_articulos'))
            else:
                marcas = obtener_marcas(id_usuario)
    else:
        marcas = obtener_marcas(id_usuario)
    return render_template('sitio/listadodemarcas.html', marcas=marcas)

# RUTA EDITAR MARCA / BASE DE DATOS
@app.route('/editarmarca/<int:id>', methods=['POST'])
def editar_marca_bd(id):

    codigo_marca = request.form.get('codigo_marca_editar')
    nombre_marca = request.form.get('nombre_marca_editar')

    with mysql.connection.cursor() as cur:
        cur.execute("UPDATE marcas SET codigo = %s, nombre = %s WHERE id_marca = %s", (codigo_marca, nombre_marca, id))
        mysql.connection.commit()
    return redirect(url_for('listado_marcas'))

# RUTA ELIMINAR MARCA / BASE DE DATOS
@app.route('/eliminarmarca', methods=['POST'])
def eliminar_marca_bd():

    id_marca = request.form['id_marca']

    with mysql.connection.cursor() as cur:
        cur.execute("DELETE FROM marcas WHERE id_marca = %s", (id_marca,))
        mysql.connection.commit()
    
    return redirect(url_for('listado_marcas'))

@app.route('/listadodeencargadoscompras', methods=['GET', 'POST'])
def listado_encargados_compras():
    if not 'logueado' in session:
        return redirect(url_for('index'))
    
    id_usuario = session.get('id_usuario')
    encargados_compras = obtener_encargados_compras(id_usuario)

    if request.method == 'POST':
        if 'reiniciar' in request.form:
            encargados_compras = obtener_encargados_compras(id_usuario)
        else:
            codigo_desde = request.form.get('codigo_desde')
            codigo_hasta = request.form.get('codigo_hasta')
            if codigo_desde and codigo_hasta:
                with mysql.connection.cursor() as cur:
                    cur.execute("SELECT codigo FROM encargados_compras WHERE codigo = %s AND id_usuario = %s", (codigo_desde, id_usuario,))
                    verificar_codigo_desde = cur.fetchone()
                    cur.execute("SELECT codigo FROM encargados_compras WHERE codigo = %s AND id_usuario = %s", (codigo_hasta, id_usuario,))
                    verificar_codigo_hasta = cur.fetchone()
                    if verificar_codigo_desde and verificar_codigo_hasta:
                        encargados_compras = filtros_encargados_compras(id_usuario, codigo_desde, codigo_hasta)
                    else:
                        encargados_compras = obtener_encargados_compras(id_usuario)
                        flash('Uno o los dos codigos de encargados de compras no estan registrados')
                        return redirect(url_for('listado_encargados_compras'))
            else:
                encargados_compras = obtener_encargados_compras(id_usuario)
    else:
        encargados_compras = obtener_encargados_compras(id_usuario)
    return render_template('sitio/listadodeencargadoscompras.html', encargados_compras=encargados_compras)

# RUTA EDITAR ENCARCADOS DE COMPRAS / BASE DE DATOS
@app.route('/editarencargadocompras/<int:id>', methods=['POST'])
def editar_encargado_compras_bd(id):

    codigo_encargado_compras = request.form.get('codigo_encargado_compras_editar')
    nombre_encargado_compras = request.form.get('nombre_encargado_compras_editar')

    with mysql.connection.cursor() as cur:
        cur.execute("UPDATE encargados_compras SET codigo = %s, nombre = %s WHERE id_encargado_compras = %s", (codigo_encargado_compras, nombre_encargado_compras, id))
        mysql.connection.commit()

    return redirect(url_for('listado_encargados_compras'))

# RUTA ELIMINAR ENCARGADO DE COMPRA
@app.route('/eliminarencargadocompras', methods=['POST'])
def eliminar_encargado_compras_bd():

    id_encargado_compras = request.form['id_encargado_compras']

    with mysql.connection.cursor() as cur:
        cur.execute("DELETE FROM encargados_compras WHERE id_encargado_compras = %s", (id_encargado_compras,))
        mysql.connection.commit()

    return redirect(url_for('listado_encargados_compras'))

@app.route('/listadodeencargadosventas', methods=['GET', 'POST'])
def listado_encargados_ventas():
    if not 'logueado' in session:
        return redirect(url_for('index'))
    
    id_usuario = session.get('id_usuario')
    encargados_ventas = obtener_encargados_ventas(id_usuario)

    if request.method == 'POST':
        if 'reiniciar' in request.form:
            encargados_ventas = obtener_encargados_ventas(id_usuario)
        else:
            codigo_desde = request.form.get('codigo_desde')
            codigo_hasta = request.form.get('codigo_hasta')
            if codigo_desde and codigo_hasta:
                with mysql.connection.cursor() as cur:
                    cur.execute("SELECT codigo FROM encargados_ventas WHERE codigo = %s AND id_usuario = %s", (codigo_desde, id_usuario,))
                    verificar_codigo_desde = cur.fetchone()
                    cur.execute("SELECT codigo FROM encargados_ventas WHERE codigo = %s AND id_usuario = %s", (codigo_hasta, id_usuario,))
                    verificar_codigo_hasta = cur.fetchone()
                    if verificar_codigo_desde and verificar_codigo_hasta:
                        encargados_ventas = filtros_encargados_ventas(id_usuario, codigo_desde, codigo_hasta)
                    else:
                        encargados_ventas = obtener_encargados_ventas(id_usuario)
                        flash('Uno o los dos codigos de encargados de ventas no estan registrados')
                        return redirect(url_for('listado_articulos'))
            else:
                encargados_ventas = obtener_encargados_ventas(id_usuario)
    else:
        encargados_ventas = obtener_encargados_ventas(id_usuario)
    return render_template('sitio/listadodeencargadosventas.html', encargados_ventas=encargados_ventas)

# RUTA EDITAR ENCARCADOS DE VENTAS / BASE DE DATOS
@app.route('/editarencargadoventas/<int:id>', methods=['POST'])
def editar_encargado_ventas_bd(id):

    codigo_encargado_ventas = request.form.get('codigo_encargado_ventas_editar')
    nombre_encargado_ventas = request.form.get('nombre_encargado_ventas_editar')

    with mysql.connection.cursor() as cur:
        cur.execute("UPDATE encargados_ventas SET codigo = %s, nombre = %s WHERE id_encargado_ventas = %s", (codigo_encargado_ventas, nombre_encargado_ventas, id))
        mysql.connection.commit()

    return redirect(url_for('listado_encargados_ventas'))

# RUTA ELIMINAR ENCARGADO DE VENTA
@app.route('/eliminarencargadoventas', methods=['POST'])
def eliminar_encargado_ventas_bd():

    id_encargado_ventas = request.form['id_encargado_ventas']

    with mysql.connection.cursor() as cur:
        cur.execute("DELETE FROM encargados_ventas WHERE id_encargado_ventas = %s", (id_encargado_ventas,))
        mysql.connection.commit()

    return redirect(url_for('listado_encargados_ventas'))

# RUTA PERFIL
@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    if not 'logueado' in session:
        return redirect(url_for('index'))

    id_usuario = session.get('id_usuario')
    usuario = obtener_usuario(id_usuario)
    marcas = obtener_marcas(id_usuario)
    encargados_compras = obtener_encargados_compras(id_usuario)
    encargados_ventas = obtener_encargados_ventas(id_usuario)

    if request.method == "POST":
        correo_electronico = request.form.get('correo_electronico')
        direccion = request.form.get('direccion')
        telefono = request.form.get('telefono')

        with mysql.connection.cursor() as cur:
            cur.execute("UPDATE registro_usuario SET direccion = %s, telefono = %s, correo_electronico = %s WHERE id_usuario = %s", (direccion, telefono, correo_electronico, id_usuario,))
            mysql.connection.commit()
        usuario = obtener_usuario(id_usuario)

    return render_template('sitio/perfil.html', usuario=usuario, marcas=marcas, encargados_ventas=encargados_ventas, encargados_compras=encargados_compras)

# RUTA TERMINOS Y CONDICIONES
@app.route('/terminosycondiciones')
def terminos_condiciones():
    if not 'logueado' in session:
        return redirect(url_for('index'))

    id_usuario = session.get('id_usuario')
    marcas = obtener_marcas(id_usuario)
    encargados_compras = obtener_encargados_compras(id_usuario)
    encargados_ventas = obtener_encargados_ventas(id_usuario)

    return render_template ('sitio/terminosycondiciones.html', marcas=marcas, encargados_ventas=encargados_ventas, encargados_compras=encargados_compras)

# RUTA MANUAL DE USO
@app.route('/manualdeuso')
def manualdeuso():
    path = "manualdeuso_alphainventory.pdf"
    return send_file(path, as_attachment=True)

# RUTA ADMIN
@app.route('/admin/')
def admin():
    if not 'logueado' in session:
        return redirect(url_for('index'))
    return render_template('/admin/')

# RUTA REGISTRO USUARIO
@app.route('/registro_usuario')
def registro_usuario():
    return render_template('admin/registrousuario.html')

# RUTA REGISTRO USUARIO / BASE DE DATOS
@app.route('/registro_usuario', methods=['POST'])
def registro_usuario_bd():
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    direccion = request.form.get('direccion')
    telefono = request.form.get('telefono')
    correo_electronico = request.form.get('correo_electronico')
    contrasena = request.form.get('contrasena')
    contrasena_ = request.form.get('contrasena_')

    with mysql.connection.cursor() as cur:
        cur.execute("SELECT correo_electronico FROM registro_usuario WHERE correo_electronico = %s", (correo_electronico,))
        data = cur.fetchone()
        if data:
            flash('Correo electronico registrado')
            return redirect(url_for('registro_usuario'))
    if contrasena != contrasena_:
        flash('Las contraseñas no coinciden')
        return redirect(url_for('registro_usuario'))
    if contrasena or contrasena_ == nombre or apellido:
        flash('La contraseña no puede ser igual al nombre o apellido')
        return redirect(url_for('registro_usuario'))
    if contrasena == contrasena_:
        with mysql.connection.cursor() as cur:
            cur.execute("INSERT INTO registro_usuario (id_usuario, nombre, apellido, direccion, telefono, correo_electronico, contrasena) VALUES (NULL, %s, %s, %s, %s, %s, %s)", (nombre, apellido, direccion, telefono, correo_electronico, contrasena,))
            mysql.connection.commit()   
        flash('Cuenta creada exitosamente')
        return redirect(url_for('index'))
    else:
        return redirect(url_for('registro_usuario'))
    
# RUTA RECUPERAR CONTRASEÑA
@app.route('/recuperarcontrasena/<token>', methods=['GET', 'POST'])
def recuperar_contrasena(token):
    try:
        correo_electronico = serializer.loads(token, salt='password-recovery-salt', max_age=3600)
    except Exception:
        flash('Este enlace ha expirado')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        contrasena = request.form.get('contrasena')
        contrasena_ = request.form.get('contrasena_')
        with mysql.connection.cursor() as cur:
            cur.execute("SELECT contrasena FROM registro_usuario WHERE correo_electronico = %s", (correo_electronico,))
            verificar_contrasena = cur.fetchone()

            if verificar_contrasena == contrasena:
                flash('La contrasena introducida es tu actual')
                return redirect(url_for('recuperar_contrasena', token=token))
            
        if contrasena != contrasena_:
            flash('Las contrasenas no coinciden')
            return redirect(url_for('recuperar_contrasena', token=token))
        else:
            with mysql.connection.cursor() as cur:
                cur.execute("UPDATE registro_usuario SET contrasena = %s WHERE correo_electronico = %s", (contrasena, correo_electronico,))
                mysql.connection.commit()
            flash('Contraseña recuperada con exito')
            return redirect(url_for('index'))
    return render_template('admin/recuperarcontrasena.html', token=token)

# RUTA REGISTRO DE ARTICULOS
@app.route('/registrodearticulos')
def registro_articulos():
    if not 'logueado' in session:
        return redirect(url_for('index'))
    
    id_usuario = session.get('id_usuario')
    articulos = obtener_articulos(id_usuario)
    encargados_compras = obtener_encargados_compras(id_usuario)
    encargados_ventas = obtener_encargados_ventas(id_usuario)

    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM marcas WHERE id_usuario = %s GROUP BY nombre", (id_usuario,))
        marcas = cur.fetchall()

    return render_template('admin/registrodearticulos.html', articulos=articulos, marcas=marcas, encargados_ventas=encargados_ventas, encargados_compras=encargados_compras)

# RUTA REGISTRO DE ARTICULOS / BASE DE DATOS
@app.route('/registrodearticulos', methods=['POST'])
def registro_articulos_bd():
    id_usuario = session.get('id_usuario')
    codigo = request.form.get('codigo')
    descripcion = request.form.get('descripcion')
    talla = request.form.get('talla')
    marca = request.form.get('marca')
    referencia = request.form.get('referencia')
    ubicacion = request.form.get('direccion')
    costo = float(request.form.get('costo'))
    precio = float(request.form.get('precio'))
    itbis = request.form.get('itbis')
    cantidad = 0
    unidad_medida = request.form.get('medida')
    margen_beneficio = round(((precio - costo) / precio) * 100, 2)
    
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT codigo FROM articulos WHERE codigo = %s AND id_usuario = %s", (codigo, id_usuario,))
        codigos = cur.fetchone()
        if codigos:
            flash('Este codigo de articulo esta registrado')
            return redirect(url_for('registro_articulos'))
        
        cur.execute("SELECT descripcion FROM articulos WHERE descripcion = %s", (descripcion,))
        descripciones = cur.fetchone()
        cur.execute("SELECT talla FROM articulos WHERE talla = %s", (talla,))
        tallas = cur.fetchone()
        if descripciones and tallas:
            flash('Ya hay un articulo con esta descripcion y talla')
            return redirect(url_for('registro_articulos'))

        cur.execute("SELECT referencia FROM articulos WHERE referencia = %s", (referencia,))
        referencias = cur.fetchone()
        if referencias:
            flash('Ya hay un articulo con esta referencia')
            return redirect(url_for('registro_articulos'))
        cur.execute("SELECT marca FROM marcas WHERE nombre = %s", (marca,))
        marcas = cur.fecthall()
        if not marcas:
            flash('Esta marca no existe')
            return redirect(url_for('registro_articulos'))
        
    if costo > precio:
        flash('El costo no puede ser mayor al precio')
        return redirect(url_for('registro_articulos'))
    else:
        with mysql.connection.cursor() as cur:
            cur.execute("INSERT INTO articulos (id_articulo, codigo, descripcion, talla, marca, referencia, ubicacion, costo, precio, itbis, cantidad, unidad_medida, margen_beneficio, id_usuario) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (codigo, descripcion, talla, marca, referencia, ubicacion, costo, precio, itbis, cantidad, unidad_medida, margen_beneficio, id_usuario,))
            mysql.connection.commit()

        return redirect('registro_articulos')

# RUTA REGISTRO DE SUPLIDORES
@app.route('/registrodesuplidores')
def registro_suplidores():
    if not 'logueado' in session:
        return redirect(url_for('index'))
    
    id_usuario = session.get('id_usuario')
    suplidores = obtener_suplidores(id_usuario)
    marcas = obtener_marcas(id_usuario)
    encargados_compras = obtener_encargados_compras(id_usuario)
    encargados_ventas = obtener_encargados_ventas(id_usuario)

    return render_template('admin/registrodesuplidores.html', suplidores=suplidores, marcas=marcas, encargados_ventas=encargados_ventas, encargados_compras=encargados_compras)

# RUTA REGISTRO DE SUPLIDORES / BASE DE DATOS
@app.route('/registrodesuplidores', methods=['POST'])
def registro_suplidores_bd():
    id_usuario = session.get('id_usuario')
    codigo = request.form.get('codigo')
    nombre = request.form.get('nombre')
    direccion = request.form.get('direccion')
    ciudad = request.form.get('ciudad')
    telefono = request.form.get('telefono')
    limite_credito = request.form.get('limite_credito')
    condiciones = request.form.get('condiciones')
    rnc = request.form.get('rnc')
    descuentos = request.form.get('descuento')

    with mysql.connection.cursor() as cur:
        cur.execute("SELECT codigo FROM suplidores WHERE codigo = %s AND id_usuario = %s", (codigo, id_usuario))
        codigos = cur.fetchone()
        if codigos:
            flash('Este codigo de suplidor esta registrado')
            return redirect(url_for('registro_suplidores'))

        cur.execute("SELECT nombre FROM suplidores WHERE nombre = %s", (nombre,))
        nombres = cur.fetchone()
        if nombres:
            flash('Este nombre de suplidor esta registrado')
            return redirect(url_for('registro_suplidores'))

        cur.execute("SELECT rnc FROM suplidores WHERE rnc = %s", (rnc,))
        rncs = cur.fetchone()

        if rncs:
            flash('Este rnc de suplidor esta registrado')
            return redirect(url_for('registro_suplidores'))
        else:
            with mysql.connection.cursor() as cur:
                cur.execute("INSERT INTO suplidores (id_suplidor, codigo, nombre, direccion, ciudad, telefono, limite_credito, condiciones, rnc, descuentos, id_usuario) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (codigo, nombre, direccion, ciudad, telefono, limite_credito, condiciones, rnc, descuentos, id_usuario))
                mysql.connection.commit()
    return redirect(url_for('registro_suplidores'))

# RUTA REGISTRO DE CLIENTES
@app.route('/registrodeclientes')
def registro_clientes():
    if not 'logueado' in session:
        return redirect(url_for('index'))

    id_usuario = session.get('id_usuario')
    clientes = obtener_clientes(id_usuario)
    marcas = obtener_marcas(id_usuario)
    encargados_compras = obtener_encargados_compras(id_usuario)
    encargados_ventas = obtener_encargados_ventas(id_usuario)

    return render_template('admin/registrodeclientes.html', clientes=clientes, marcas=marcas, encargados_ventas=encargados_ventas, encargados_compras=encargados_compras)

# RUTA REGISTRO DE CLIENTES / BASE DE DATOS
@app.route('/registrodeclientes', methods=['POST'])
def registro_clientes_bd():
    id_usuario = session.get('id_usuario')
    codigo = request.form.get('codigo')
    nombre = request.form.get('nombre')
    direccion = request.form.get('direccion')
    ciudad = request.form.get('ciudad')
    telefono = request.form.get('telefono')
    cedula = request.form.get('cedula')
    correo_electronico = request.form.get('correo_electronico')
    descuentos = request.form.get('descuento')

    with mysql.connection.cursor() as cur:
        cur.execute("SELECT codigo FROM clientes WHERE codigo = %s AND id_usuario = %s", (codigo, id_usuario))
        codigos = cur.fetchone()
        if codigos:
            flash('Este codigo de cliente esta registrado')
            return redirect(url_for('registro_clientes'))

        cur.execute("SELECT nombre FROM clientes WHERE nombre = %s", (nombre,))
        nombres = cur.fetchone()
        if nombres:
            flash('Este nombre de cliente esta registrado')
            return redirect(url_for('registro_clientes'))
        
        cur.execute("SELECT cedula FROM clientes WHERE cedula = %s", (cedula))
        cedulas = cur.fetchone()
        if cedulas:
            flash('Esta cedula de cliente esta registrado')
            return redirect(url_for('registro_clientes'))
        else:
            with mysql.connection.cursor() as cur:
                cur.execute("INSERT INTO clientes (id_cliente, codigo, nombre, direccion, ciudad, telefono, cedula, correo_electronico, descuentos, id_usuario) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (codigo, nombre, direccion, ciudad, telefono, cedula, correo_electronico, descuentos, id_usuario,))
                mysql.connection.commit()
    return redirect(url_for('registro_clientes'))

# RUTA COMPRAS
@app.route('/compras')
def compras():
    if not 'logueado' in session:
        return redirect(url_for('index'))
    
    id_usuario = session.get('id_usuario')
    articulos = obtener_articulos(id_usuario)
    suplidores = obtener_suplidores(id_usuario)
    marcas = obtener_marcas(id_usuario)
    encargados_compras = obtener_encargados_compras(id_usuario)
    encargados_ventas = obtener_encargados_ventas(id_usuario)
    compras = obtener_compras(id_usuario)

    return render_template ('admin/compras.html', compras=compras, articulos=articulos, suplidores=suplidores, marcas=marcas, encargados_ventas=encargados_ventas, encargados_compras=encargados_compras)

# RUTA COMPRAS / BASE DE DATOS
@app.route('/compras', methods=['POST'])
def compras_bd():
    id_usuario = session.get('id_usuario')
    tiempo = datetime.now()
    fecha_compra = tiempo.strftime('%Y-%m-%d')
    hora_compra = tiempo.strftime('%H:%M:%S') 
    suplidor = request.form.get('suplidor')
    encargado_compras = request.form.get('encargado_compras')
    numero_articulos = int(request.form.get('numero_articulos_compra'))

    with mysql.connection.cursor() as cur:
        cur.execute("SELECT nombre FROM suplidores WHERE nombre = %s", (suplidor,))
        verificar_suplidor = cur.fetchone()
        if not verificar_suplidor:
            flash(f'Este suplidor "{suplidor}" no existe')
            return redirect(url_for('compras'))
        
        cur.execute("SELECT nombre FROM encargados_compras WHERE nombre = %s", (encargado_compras,))
        verificar_encargado_compras = cur.fetchone()
        if not verificar_encargado_compras:
            flash(f'Este encargado de compras "{encargado_compras}" no existe')
            return redirect(url_for('compras'))

    for i in range(1, numero_articulos + 1):
        articulos = []
        codigo = request.form.get(f'codigo_{i}')
        descripcion = request.form.get(f'descripcion_{i}')
        cantidad = request.form.get(f'cantidad_{i}')
        itbis = request.form.get(f'itbis_{i}')
        costo = request.form.get(f'costo_{i}')
        itbis_compra = int(itbis) / 100
        total_compra = (int(cantidad) * int(costo)) * itbis_compra + (int(cantidad) * int(costo))
        
        articulo = (
           fecha_compra,
           hora_compra,
           suplidor,
           encargado_compras,
           codigo,
           descripcion,
           cantidad,
           itbis,
           costo,
           total_compra,
           id_usuario
        )
        articulos.append(articulo)
       
        with mysql.connection.cursor() as cur:
            cur.execute("SELECT codigo FROM articulos WHERE codigo = %s", (codigo,))
            verificar_codigo_articulo = cur.fetchone()
            if not verificar_codigo_articulo:
                flash(f'Este codigo "{codigo}" no existe')
                return redirect(url_for('compras'))
            
            cur.execute("SELECT descripcion FROM articulos WHERE codigo = %s AND descripcion = %s", (codigo, descripcion,))
            verificar_descripcion_articulo = cur.fetchone()
            if not verificar_descripcion_articulo:
                flash(f'Esta descripcion "{descripcion}" no es la del articulo')
                return redirect(url_for('compras'))
            
            cur.execute("SELECT itbis FROM articulos WHERE codigo = %s AND itbis = %s", (codigo, itbis,))
            verificar_itbis_articulo = cur.fetchone()
            if not verificar_itbis_articulo:
                flash(f'Este no es el itbis "{itbis}" del articulo')
                return redirect(url_for('compras'))
            
            cur.execute("SELECT costo FROM articulos WHERE codigo = %s AND costo = %s", (codigo, costo,))
            verificar_costo_articulo = cur.fetchone()
            if not verificar_costo_articulo:
                flash(f'Este no es el costo "{costo}" del articulo')
                return redirect(url_for('compras'))
            
        with mysql.connection.cursor() as cur:
            sql = ("INSERT INTO compras (id_compra, fecha_compra, hora_compra, suplidor, encargado_compras, codigo, descripcion, cantidad, itbis, costo, total_compra, id_usuario) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            cur.executemany(sql, articulos)
        for articulo in articulos:
            cantidad = articulo[6]
            codigo = articulo[4]
        with mysql.connection.cursor() as cur:
            cur.execute("UPDATE articulos SET cantidad = (cantidad + {0}) WHERE codigo = {1}".format(cantidad, codigo))
            mysql.connection.commit()
    return redirect(url_for('compras'))

# RUTA VENTAS
@app.route('/ventas')
def ventas():
    if not 'logueado' in session:
        return redirect(url_for('index'))

    id_usuario = session.get('id_usuario')
    articulos = obtener_articulos(id_usuario)
    clientes = obtener_clientes(id_usuario)
    marcas = obtener_marcas(id_usuario)
    encargados_compras = obtener_encargados_compras(id_usuario)
    encargados_ventas = obtener_encargados_ventas(id_usuario)
    ventas = obtener_ventas(id_usuario)

    return render_template ('admin/ventas.html', ventas=ventas, articulos=articulos, clientes=clientes, marcas=marcas, encargados_ventas=encargados_ventas, encargados_compras=encargados_compras)

# RUTA VENTAS / BASE DE DATOS
@app.route('/ventas', methods=['POST'])
def ventas_bd():

    id_usuario = session.get('id_usuario')
    tiempo = datetime.now()
    fecha_venta = tiempo.strftime('%Y-%m-%d')
    hora_venta = tiempo.strftime('%H:%M:%S') 
    cliente = request.form.get('cliente')
    encargado_ventas = request.form.get('encargado_ventas')
    numero_articulos = int(request.form.get('numero_articulos_venta'))

    with mysql.connection.cursor() as cur:
        cur.execute("SELECT nombre FROM clientes WHERE nombre = %s", (cliente,))
        verificar_cliente = cur.fetchone()
        if not verificar_cliente:
            flash(f'Este cliente "{cliente}" no existe')
            return redirect(url_for('ventas'))
        
        cur.execute("SELECT nombre FROM encargados_ventas WHERE nombre = %s", (encargado_ventas,))
        verificar_encargado_ventas = cur.fetchone()
        if not verificar_encargado_ventas:
            flash(f'Este encargado de ventas "{encargado_ventas}" no existe')
            return redirect(url_for('ventas'))

    for i in range(1, numero_articulos + 1):
        articulos = []
        codigo = request.form.get(f'codigo_{i}')
        descripcion = request.form.get(f'descripcion_{i}')
        cantidad = request.form.get(f'cantidad_{i}')
        itbis = request.form.get(f'itbis_{i}')
        precio = request.form.get(f'precio_{i}')
        itbis_venta = int(itbis) / 100
        total_venta = (int(precio) * int(cantidad)) * itbis_venta + (int(precio) * int(cantidad)),
        
        articulo = (
           fecha_venta,
           hora_venta,
           cliente,
           encargado_ventas,
           codigo,
           descripcion,
           cantidad,
           itbis,
           precio,
           total_venta,
           id_usuario
        )
        articulos.append(articulo)

        with mysql.connection.cursor() as cur:
            cur.execute("SELECT codigo FROM articulos WHERE codigo = %s", (codigo,))
            verificar_codigo_articulo = cur.fetchone()
            if not verificar_codigo_articulo:
                flash(f'Este codigo "{codigo}" no existe')
                return redirect(url_for('ventas'))
            
            cur.execute("SELECT descripcion FROM articulos WHERE codigo = %s AND descripcion = %s", (codigo, descripcion,))
            verificar_descripcion_articulo = cur.fetchone()
            if not verificar_descripcion_articulo:
                flash(f'Esta descripcion "{descripcion}" no es la del articulo')
                return redirect(url_for('ventas'))
            
            cur.execute("SELECT cantidad FROM articulos WHERE codigo = %s", (codigo,))
            verificar_cantidad_articulo = cur.fetchone()
            cantidades_articulos = verificar_cantidad_articulo[0]
            if int(cantidad) > cantidades_articulos:
                flash(f'La cantidad {cantidad} a vender es mayor a la cantidad {cantidades_articulos} disponible del articulo')
                return redirect(url_for('ventas'))
            
            cur.execute("SELECT itbis FROM articulos WHERE codigo = %s AND itbis = %s", (codigo, itbis,))
            verificar_itbis_articulo = cur.fetchone()
            if not verificar_itbis_articulo:
                flash(f'Este no es el itbis "{itbis}" del articulo')
                return redirect(url_for('ventas'))
            
            cur.execute("SELECT precio FROM articulos WHERE codigo = %s AND precio = %s", (codigo, precio,))
            verificar_precio_articulo = cur.fetchone()
            if not verificar_precio_articulo:
                flash(f'Este no es el precio "{precio}" del articulo')
                return redirect(url_for('ventas'))
        with mysql.connection.cursor() as cur:
            sql = ("INSERT INTO ventas (id_venta, fecha_venta, hora_venta, cliente, encargado_ventas, codigo, descripcion, cantidad, itbis, precio, total_venta, id_usuario) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            cur.executemany(sql, articulos)
        for articulo in articulos:
            cantidad = articulo[6]
            codigo = articulo[4]
        with mysql.connection.cursor() as cur:
            cur.execute("UPDATE articulos SET cantidad = (cantidad - {0}) WHERE codigo = {1}".format(cantidad, codigo))
            mysql.connection.commit()
    return redirect(url_for('ventas'))

# RUTA EDITAR PERFIL
@app.route('/editarperfil')
def editar_perfil():
    if not 'logueado' in session:
        return redirect(url_for('index'))

    id_usuario = session.get('id_usuario')
    usuario = obtener_usuario(id_usuario)
    marcas = obtener_marcas(id_usuario)
    encargados_compras = obtener_encargados_compras(id_usuario)
    encargados_ventas = obtener_encargados_ventas(id_usuario)
    
    return render_template('admin/editarperfil.html', usuario=usuario, marcas=marcas, encargados_ventas=encargados_ventas, encargados_compras=encargados_compras)

# RUTA CAMBIAR CONTRASEÑA
@app.route('/cambiarcontrasena')
def cambiar_contrasena():
    if not 'logueado' in session:
        return redirect(url_for('index'))

    id_usuario = session.get('id_usuario')
    usuario = obtener_usuario(id_usuario)
    marcas = obtener_marcas(id_usuario)
    encargados_compras = obtener_encargados_compras(id_usuario)
    encargados_ventas = obtener_encargados_ventas(id_usuario)

    with mysql.connection.cursor() as cur:
        cur.execute("SELECT id_usuario FROM registro_usuario WHERE id_usuario = %s AND contrasena = 'NA'", (id_usuario,))
        login_google = cur.fetchone()
    return render_template ('admin/cambiarcontrasena.html', login_google=login_google, usuario=usuario, marcas=marcas, encargados_ventas=encargados_ventas, encargados_compras=encargados_compras)

# RUTA CAMBIAR CONTRASEÑA / BASE DE DATOS
@app.route('/cambiarcontrasena', methods=['POST'])
def cambiar_contrasena_bd():
    id_usuario = session.get('id_usuario')
    contrasena_antigua = request.form.get('contrasena_antigua')
    contrasena = request.form.get('contrasena')
    contrasena_ = request.form.get('contrasena_')

    with mysql.connection.cursor() as cur:
        cur.execute("SELECT id_usuario FROM registro_usuario WHERE contrasena = %s AND id_usuario = %s", (contrasena_antigua, id_usuario,))
        contrasena_registro = cur.fetchone()
        if not contrasena_registro:
            flash('Esta no es tu antigua contraseña')
            return redirect(url_for('cambiar_contrasena'))
    if contrasena_antigua == contrasena or contrasena_antigua == contrasena_:
        flash('La nueva contrasena no puede ser la antigua')
        return redirect(url_for('cambiar_contrasena'))
    else:
        with mysql.connection.cursor() as cur:
            cur.execute("UPDATE registro_usuario SET contrasena = %s WHERE id_usuario = %s", (contrasena, id_usuario,))
            mysql.connection.commit()
    return redirect(url_for('inicio_inventario'))

if __name__ == '__main__':
    app.run(debug=True)
