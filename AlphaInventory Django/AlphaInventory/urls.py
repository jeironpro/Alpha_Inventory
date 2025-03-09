from django.urls import path
from AlphaInventory import views
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetDoneView

urlpatterns = [
    path('', views.index, name="index"),
    path('registro_usuario/', views.registro_usuario, name="registro_usuario"),
    path('activador/<uidb64>/<token>', views.activador, name='activador'),
    path('olvidar_contrasena/', views.olvidar_usuario_contrasena, name="recuperar_contrasena"),
    path('password_reset/', PasswordResetView.as_view(), {'template_name':'registration/password_reset_form.html', 'email_template_name':'registration/password_reset_email.html'}, name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), {'template_name':'registration/password_reset_done.html'}, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), {'template_name':'registration/password_reset_confirm.html'}, name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), {'template_name':'registration/password_reset_complete.html'}, name='password_reset_complete'),
    path('inicio_inventario/', views.inicio_inventario, name="inicio_inventario"),
    path('inicio_inventario/encargado_compras/', views.encargado_compras_inicio_inventario, name="inicio_inventario/encargado_compras/"),
    path('inicio_inventario/encargado_ventas/', views.encargado_ventas_inicio_inventario, name="inicio_inventario/encargado_ventas/"),
    path('cerrar_sesion/', views.cerrar_sesion, name="cerrar_sesion"),
    path('registrodearticulos/', views.registro_articulos, name="registrodearticulos"),
    path('editararticulo/<int:id_articulo>/', views.editar_articulo, name="editararticulo"),
    path('eliminar_articulo/<int:id_articulo>/', views.eliminar_articulo, name="eliminar_articulo"),
    path('registrodearticulos/editar_marca/<int:id_marca>/', views.editar_marca, name="editar_marca"),
    path('eliminar_marca/<int:id_marca>/', views.eliminar_marca, name="eliminar_marca"),
    path('registrodearticulos/encargado_compras/', views.encargado_compras_registro_articulos, name="registrodearticulos/encargado_compras/"),
    path('registrodearticulos/encargado_ventas/', views.encargado_ventas_registro_articulos, name="registrodearticulos/encargado_ventas/"),
    path('registrodesuplidores/', views.registro_suplidores, name="registrodesuplidores"),
    path('editarsuplidor/<int:id_suplidor>/', views.editar_suplidor, name="editarsuplidor"),
    path('eliminar_suplidor/<int:id_suplidor>/', views.eliminar_suplidor, name="eliminar_suplidor"),
    path('registrodesuplidores/encargado_compras/', views.encargado_compras_registro_suplidores, name="registrodesuplidores/encargado_compras/"),
    path('registrodesuplidores/encargado_ventas/', views.encargado_ventas_registro_suplidores, name="registrodesuplidores/encargado_ventas/"),
    path('registrodeclientes/', views.registro_clientes, name="registrodeclientes"),
    path('eliminar_cliente/<int:id_cliente>/', views.eliminar_cliente, name="eliminar_cliente"),
    path('registrodeclientes/encargado_compras/', views.encargado_compras_registro_clientes, name="registrodeclientes/encargado_compras/"),
    path('registrodeclientes/encargado_ventas/', views.encargado_ventas_registro_clientes, name="registrodeclientes/encargado_ventas/"),
    path('editarcliente/<int:id_cliente>/', views.editar_cliente, name="editarcliente"),
    path('compras/', views.compras, name="compras"),
    path('compras/encargado_compras/', views.encargado_compras_compras, name="compras/encargado_compras/"),
    path('editar_encargado_compra/<int:id_encargadoCompra>/', views.editar_encargado_compra, name="editar_encargado_compra"),
    path('compras/encargado_ventas/', views.encargado_ventas_compras, name="compras/encargado_ventas/"),
    path('eliminar_encargadoCompra/<int:id_encargadoCompra>', views.eliminar_encargadoCompra, name="eliminar_encargadoCompra"),
    path('ventas/', views.ventas, name="ventas"),
    path('ventas/encargado_ventas/', views.encargado_ventas_ventas, name="ventas/encargado_ventas/"),
    path('editar_encargado_venta/<int:id_encargadoVenta>/', views.editar_encargado_venta, name="editar_encargado_venta"),
    path('ventas/encargado_compras/', views.encargado_compras_ventas, name="ventas/encargado_compras/"),
    path('eliminar_encargadoVenta/<int:id_encargadoVenta>', views.eliminar_encargadoVenta, name="eliminar_encargadoVenta"),
    path('movimientosdiariocompras/', views.movimientos_diario_compra, name="movimientosdiariocompras"),
    path('movimientosdiariocompras/encargado_compras/', views.encargado_compras_movimientos_diario_compra, name="movimientosdiariocompras/encargado_compras/"),
    path('movimientosdiariocompras/encargado_ventas/', views.encargado_ventas_movimientos_diario_compra, name="movimientosdiariocompras/encargado_ventas/"),
    path('movimientosdiarioventas/', views.movimientos_diario_venta, name="movimientosdiarioventas"),
    path('movimientosdiarioventas/encargado_compras/', views.encargado_compras_movimientos_diario_venta, name="movimientosdiarioventas/encargado_compras/"),
    path('movimientosdiarioventas/encargado_ventas/', views.encargado_ventas_movimientos_diario_venta, name="movimientosdiarioventas/encargado_ventas/"),
    path('movimientoporarticulocompras/', views.movimiento_por_articulo_compras, name="movimientoporarticulocompras"),
    path('movimientoporarticulocompras/encargado_compras/', views.encargado_compras_movimiento_por_articulo_compras, name="movimientoporarticulocompras/encargado_compras/"),
    path('movimientoporarticulocompras/encargado_ventas/', views.encargado_ventas_movimiento_por_articulo_compras, name="movimientoporarticulocompras/encargado_ventas/"),
    path('movimientoporarticuloventas/', views.movimiento_por_articulo_ventas, name="movimientoporarticuloventas"),
    path('movimientoporarticuloventas/encargado_compras/', views.encargado_compras_movimiento_por_articulo_ventas, name="movimientoporarticuloventas/encargado_compras/"),
    path('movimientoporarticuloventas/encargado_ventas/', views.encargado_ventas_movimiento_por_articulo_ventas, name="movimientoporarticuloventas/encargado_ventas/"),
    path('listadodearticulos/', views.listado_articulos, name="listadodearticulos"),
    path('listadodearticulos/encargado_compras/', views.encargado_compras_listado_articulos, name="listadodearticulos/encargado_compras/"),
    path('listadodearticulos/encargado_ventas/', views.encargado_ventas_listado_articulos, name="listadodearticulos/encargado_ventas/"),
    path('listadodesuplidores/', views.listado_suplidores, name="listadodesuplidores"),
    path('listadodesuplidores/encargado_compras/', views.encargado_compras_listado_suplidores, name="listadodesuplidores/encargado_compras/"),
    path('listadodesuplidores/encargado_ventas/', views.encargado_ventas_listado_suplidores, name="listadodesuplidores/encargado_ventas/"),
    path('listadodeclientes/', views.listado_clientes, name="listadodeclientes"),
    path('listadodeclientes/encargado_compras/', views.encargado_compras_listado_clientes, name="listadodeclientes/encargado_compras/"),
    path('listadodeclientes/encargado_ventas/', views.encargado_ventas_listado_clientes, name="listadodeclientes/encargado_ventas/"),
    path('listadodecompras/', views.listado_compras, name="listadodecompras" ),
    path('listadodecompras/encargado_compras/', views.encargado_compras_listado_compras, name="listadodecompras/encargado_compras/"),
    path('listadodecompras/encargado_ventas/', views.encargado_ventas_listado_compras, name="listadodecompras/encargado_ventas/"),
    path('listadodeventas/', views.listado_ventas, name="listadodeventas"),
    path('listadodeventas/encargado_compras/', views.encargado_compras_listado_ventas, name="listadodeventas/encargado_compras/"),
    path('listadodeventas/encargado_ventas/', views.encargado_ventas_listado_ventas, name="listadodeventas/encargado_ventas/"),
    path('perfil/', views.perfil, name="perfil"),
    path('editarperfil/', views.editar_perfil, name="editarperfil"),
    path('perfil/encargado_compras/', views.encargado_compras_perfil, name="perfil/encargado_compras/"),
    path('perfil/encargado_ventas/', views.encargado_ventas_perfil, name="perfil/encargado_ventas/"),
    path('cambiarcontrasena/', views.cambiar_contrasena, name="cambiarcontrasena"),
    path('cambiarcontrasena/encargado_compras/', views.encargado_compras_cambiar_contrasena, name="cambiarcontrasena/encargado_compras/"),
    path('cambiarcontrasena/encargado_ventas/', views.encargado_ventas_cambiar_contrasena, name="cambiarcontrasena/encargado_ventas/"),
    path('terminosycondiciones/', views.terminos_condiciones, name="terminosycondiciones"),
    path('terminosycondiciones/encargado_compras/', views.encargado_compras_terminos_condiciones, name="terminosycondiciones/encargado_compras/"),
    path('terminosycondiciones/encargado_ventas/', views.encargado_ventas_terminos_condiciones, name="terminosycondiciones/encargado_ventas/"),
    path('eliminar_cuenta/', views.eliminar_cuenta, name="eliminar_cuenta"),
    path('manualdeuso/', views.manual_uso, name="manualdeuso"),
]