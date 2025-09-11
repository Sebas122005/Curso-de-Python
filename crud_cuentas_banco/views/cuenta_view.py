"""
Vista para la gestión de cuentas bancarias.
Permite realizar operaciones CRUD sobre cuentas.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from views.base_view import BaseView
from controllers.cuenta_controller import CuentaController
from controllers.cliente_controller import ClienteController
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class CuentaView(BaseView):
    """Vista para la gestión de cuentas bancarias."""
    
    def __init__(self, parent, controller: CuentaController):
        super().__init__(parent, "Gestión de Cuentas Bancarias")
        self.controller = controller
        self.cliente_controller = ClienteController()
        self.cuenta_actual = None
        self.clientes = []
        self.productos = []
        
        # Cargar datos iniciales
        self._cargar_datos_iniciales()
        
        # Crear interfaz
        self._crear_interfaz()
    
    def _cargar_datos_iniciales(self):
        """Carga los datos iniciales necesarios."""
        try:
            # Cargar clientes
            exito, _, self.clientes = self.cliente_controller.listar()
            if not exito:
                messagebox.showwarning("Advertencia", "No se pudieron cargar los clientes")
            
            # Cargar productos de cuenta (hardcoded por ahora)
            self.productos = [
                {'id_producto': 1, 'nombre_producto': 'Cuenta de Ahorros Clásica'},
                {'id_producto': 2, 'nombre_producto': 'Cuenta Sueldo'},
                {'id_producto': 3, 'nombre_producto': 'Cuenta Corriente Empresarial'},
                {'id_producto': 4, 'nombre_producto': 'Ahorro Programado'}
            ]
                
        except Exception as e:
            logger.error(f"Error al cargar datos iniciales: {str(e)}")
            messagebox.showerror("Error", f"Error al cargar datos iniciales: {str(e)}")
    
    def _crear_interfaz(self):
        """Crea la interfaz de gestión de cuentas."""
        # Título
        self.crear_titulo("Gestión de Cuentas Bancarias", 0, 0, 2)
        
        # Frame para formulario
        self._crear_formulario()
        
        # Frame para botones
        self._crear_botones()
        
        # Frame para tabla
        self._crear_tabla()
        
        # Cargar datos iniciales
        self._cargar_cuentas()
    
    def _crear_formulario(self):
        """Crea el formulario de cuenta."""
        frame_formulario = self.crear_frame_grupo("Datos de la Cuenta", 1, 0, 2)
        
        # Variables del formulario
        self.variables_formulario = {
            'numero_cuenta': tk.StringVar(),
            'cci': tk.StringVar(),
            'cliente': tk.StringVar(),
            'producto': tk.StringVar(),
            'saldo': tk.StringVar(),
            'fecha_apertura': tk.StringVar(),
            'estado': tk.StringVar()
        }
        
        # Fila 0: Número de cuenta y CCI
        ttk.Label(frame_formulario, text="Número de Cuenta:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        ttk.Entry(frame_formulario, textvariable=self.variables_formulario['numero_cuenta'], width=30).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(0, 10))
        
        ttk.Label(frame_formulario, text="CCI:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10), pady=5)
        ttk.Entry(frame_formulario, textvariable=self.variables_formulario['cci'], width=30).grid(row=0, column=3, sticky=(tk.W, tk.E), pady=5, padx=(0, 10))
        
        # Fila 1: Cliente
        ttk.Label(frame_formulario, text="Cliente:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        valores_clientes = [f"{c['id_cliente']} - {c['apellido_paterno']} {c['apellido_materno']}, {c['nombre']}" 
                           for c in self.clientes]
        ttk.Combobox(frame_formulario, textvariable=self.variables_formulario['cliente'], 
                    values=valores_clientes, width=50, state='readonly').grid(row=1, column=1, columnspan=3, sticky=(tk.W, tk.E), pady=5, padx=(0, 10))
        
        # Fila 2: Producto y Saldo
        ttk.Label(frame_formulario, text="Producto:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        valores_productos = [f"{p['id_producto']} - {p['nombre_producto']}" for p in self.productos]
        ttk.Combobox(frame_formulario, textvariable=self.variables_formulario['producto'], 
                    values=valores_productos, width=30, state='readonly').grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(0, 10))
        
        ttk.Label(frame_formulario, text="Saldo Inicial:").grid(row=2, column=2, sticky=tk.W, padx=(0, 10), pady=5)
        ttk.Entry(frame_formulario, textvariable=self.variables_formulario['saldo'], width=30).grid(row=2, column=3, sticky=(tk.W, tk.E), pady=5, padx=(0, 10))
        
        # Fila 3: Fecha de apertura y Estado
        ttk.Label(frame_formulario, text="Fecha Apertura:").grid(row=3, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        ttk.Entry(frame_formulario, textvariable=self.variables_formulario['fecha_apertura'], width=30).grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(0, 10))
        
        ttk.Label(frame_formulario, text="Estado:").grid(row=3, column=2, sticky=tk.W, padx=(0, 10), pady=5)
        estados = ['Activa', 'Inactiva', 'Suspendida', 'Cerrada']
        ttk.Combobox(frame_formulario, textvariable=self.variables_formulario['estado'], 
                    values=estados, width=30, state='readonly').grid(row=3, column=3, sticky=(tk.W, tk.E), pady=5, padx=(0, 10))
        
        # Configurar grid del formulario
        for i in range(4):
            frame_formulario.rowconfigure(i, weight=1)
        for i in range(4):
            frame_formulario.columnconfigure(i, weight=1)
    
    def _crear_botones(self):
        """Crea los botones de acción."""
        frame_botones = ttk.Frame(self.frame_principal)
        frame_botones.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Botones principales
        ttk.Button(frame_botones, text="Nuevo", command=self._nueva_cuenta).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(frame_botones, text="Guardar", command=self._guardar_cuenta).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame_botones, text="Editar", command=self._editar_cuenta).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(frame_botones, text="Eliminar", command=self._eliminar_cuenta).grid(row=0, column=3, padx=5, pady=5)
        ttk.Button(frame_botones, text="Limpiar", command=self._limpiar_formulario).grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(frame_botones, text="Generar Número", command=self._generar_numero_cuenta).grid(row=0, column=5, padx=5, pady=5)
    
    def _crear_tabla(self):
        """Crea la tabla de cuentas."""
        frame_tabla = self.crear_frame_grupo("Lista de Cuentas", 3, 0, 2)
        
        # Columnas de la tabla
        columnas = ['ID', 'Número', 'Cliente', 'Producto', 'Saldo', 'Estado', 'Fecha Apertura']
        
        # Crear Treeview directamente en el frame
        self.treeview = ttk.Treeview(frame_tabla, columns=columnas, show='headings', height=10)
        
        # Configurar columnas
        for col in columnas:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=100, anchor=tk.CENTER)
        
        # Crear scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar widgets
        self.treeview.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configurar selección
        self.treeview.bind('<<TreeviewSelect>>', self._on_seleccion_cuenta)
        
        # Configurar grid
        frame_tabla.rowconfigure(0, weight=1)
        frame_tabla.columnconfigure(0, weight=1)
    
    def _cargar_cuentas(self):
        """Carga la lista de cuentas en la tabla."""
        try:
            exito, mensaje, cuentas = self.controller.listar()
            if exito:
                # Preparar datos para la tabla
                datos_tabla = []
                for cuenta in cuentas:
                    nombre_cliente = cuenta.get('nombre_cliente', '')
                    apellido_paterno = cuenta.get('apellido_paterno', '')
                    apellido_materno = cuenta.get('apellido_materno', '')
                    nombre_completo = f"{apellido_paterno} {apellido_materno}, {nombre_cliente}" if nombre_cliente else "N/A"
                    
                    datos_tabla.append([
                        cuenta['id_cuenta'],
                        cuenta['numero_cuenta'],
                        nombre_completo,
                        cuenta.get('producto', ''),
                        f"S/ {cuenta['saldo']:,.2f}",
                        cuenta['estado'],
                        cuenta['fecha_apertura']
                    ])
                
                # Poblar tabla directamente
                for item in self.treeview.get_children():
                    self.treeview.delete(item)
                
                for fila in datos_tabla:
                    self.treeview.insert("", "end", values=fila)
            else:
                messagebox.showerror("Error", f"Error al cargar cuentas: {mensaje}")
                
        except Exception as e:
            logger.error(f"Error al cargar cuentas: {str(e)}")
            messagebox.showerror("Error", f"Error al cargar cuentas: {str(e)}")
    
    def _nueva_cuenta(self):
        """Inicia la creación de una nueva cuenta."""
        self._limpiar_formulario()
        self.cuenta_actual = None
        self.treeview.selection_remove(self.treeview.selection())
        
        # Establecer valores por defecto
        from utils.helpers import obtener_fecha_actual
        self.variables_formulario['fecha_apertura'].set(obtener_fecha_actual())
        self.variables_formulario['estado'].set('Activa')
        self.variables_formulario['saldo'].set('0.00')
    
    def _guardar_cuenta(self):
        """Guarda la cuenta actual."""
        try:
            # Obtener datos del formulario
            datos = self._obtener_datos_formulario()
            
            if not datos:
                return
            
            if self.cuenta_actual:
                # Actualizar cuenta existente
                exito, mensaje = self.controller.actualizar_cuenta(self.cuenta_actual, datos)
            else:
                # Crear nueva cuenta
                exito, mensaje, id_nuevo = self.controller.crear_cuenta(datos)
                if exito:
                    self.cuenta_actual = id_nuevo
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self._cargar_cuentas()
                self._limpiar_formulario()
                self.cuenta_actual = None
            else:
                messagebox.showerror("Error", mensaje)
                
        except Exception as e:
            logger.error(f"Error al guardar cuenta: {str(e)}")
            messagebox.showerror("Error", f"Error al guardar cuenta: {str(e)}")
    
    def _editar_cuenta(self):
        """Edita la cuenta seleccionada."""
        if not self.cuenta_actual:
            messagebox.showwarning("Advertencia", "Seleccione una cuenta para editar")
            return
        
        try:
            exito, mensaje, datos_cuenta = self.controller.leer(self.cuenta_actual)
            if exito:
                self._llenar_formulario(datos_cuenta)
            else:
                messagebox.showerror("Error", mensaje)
                
        except Exception as e:
            logger.error(f"Error al editar cuenta: {str(e)}")
            messagebox.showerror("Error", f"Error al editar cuenta: {str(e)}")
    
    def _eliminar_cuenta(self):
        """Elimina la cuenta seleccionada."""
        if not self.cuenta_actual:
            messagebox.showwarning("Advertencia", "Seleccione una cuenta para eliminar")
            return
        
        if not self.mostrar_confirmacion("Confirmar", "¿Está seguro que desea eliminar esta cuenta?"):
            return
        
        try:
            exito, mensaje = self.controller.eliminar(self.cuenta_actual)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self._cargar_cuentas()
                self._limpiar_formulario()
                self.cuenta_actual = None
            else:
                messagebox.showerror("Error", mensaje)
                
        except Exception as e:
            logger.error(f"Error al eliminar cuenta: {str(e)}")
            messagebox.showerror("Error", f"Error al eliminar cuenta: {str(e)}")
    
    def _generar_numero_cuenta(self):
        """Genera un número de cuenta automáticamente."""
        try:
            numero_cuenta = self.controller.generar_numero_cuenta()
            self.variables_formulario['numero_cuenta'].set(numero_cuenta)
            self.variables_formulario['cci'].set(numero_cuenta)  # CCI igual al número de cuenta
        except Exception as e:
            logger.error(f"Error al generar número de cuenta: {str(e)}")
            messagebox.showerror("Error", f"Error al generar número de cuenta: {str(e)}")
    
    def _on_seleccion_cuenta(self, event):
        """Maneja la selección de una cuenta en la tabla."""
        seleccion = self.treeview.selection()
        if seleccion:
            item = self.treeview.item(seleccion[0])
            id_cuenta = item['values'][0]
            self.cuenta_actual = id_cuenta
    
    def _obtener_datos_formulario(self) -> Optional[Dict]:
        """Obtiene los datos del formulario."""
        try:
            # Validar campos requeridos
            campos_requeridos = ['numero_cuenta', 'cci', 'cliente', 'producto', 'saldo', 'estado']
            
            for campo in campos_requeridos:
                if not self.variables_formulario[campo].get().strip():
                    messagebox.showerror("Error", f"El campo {campo.replace('_', ' ').title()} es requerido")
                    return None
            
            # Obtener datos
            datos = {
                'numero_cuenta': self.variables_formulario['numero_cuenta'].get().strip(),
                'cci': self.variables_formulario['cci'].get().strip(),
                'fecha_apertura': self.variables_formulario['fecha_apertura'].get().strip(),
                'estado': self.variables_formulario['estado'].get().strip()
            }
            
            # Obtener saldo
            try:
                datos['saldo'] = float(self.variables_formulario['saldo'].get())
            except ValueError:
                messagebox.showerror("Error", "El saldo debe ser un número válido")
                return None
            
            # Obtener IDs de los comboboxes
            cliente_texto = self.variables_formulario['cliente'].get()
            if cliente_texto:
                datos['id_cliente'] = int(cliente_texto.split(' - ')[0])
            
            producto_texto = self.variables_formulario['producto'].get()
            if producto_texto:
                datos['id_producto'] = int(producto_texto.split(' - ')[0])
            
            return datos
            
        except Exception as e:
            logger.error(f"Error al obtener datos del formulario: {str(e)}")
            messagebox.showerror("Error", f"Error al obtener datos: {str(e)}")
            return None
    
    def _llenar_formulario(self, datos_cuenta: Dict):
        """Llena el formulario con los datos de la cuenta."""
        try:
            self.variables_formulario['numero_cuenta'].set(datos_cuenta.get('numero_cuenta', ''))
            self.variables_formulario['cci'].set(datos_cuenta.get('cci', ''))
            self.variables_formulario['saldo'].set(str(datos_cuenta.get('saldo', 0)))
            self.variables_formulario['fecha_apertura'].set(datos_cuenta.get('fecha_apertura', ''))
            self.variables_formulario['estado'].set(datos_cuenta.get('estado', ''))
            
            # Establecer valores de comboboxes
            if datos_cuenta.get('id_cliente'):
                # Buscar el cliente en la lista
                for cliente in self.clientes:
                    if cliente['id_cliente'] == datos_cuenta['id_cliente']:
                        cliente_texto = f"{cliente['id_cliente']} - {cliente['apellido_paterno']} {cliente['apellido_materno']}, {cliente['nombre']}"
                        self.variables_formulario['cliente'].set(cliente_texto)
                        break
            
            if datos_cuenta.get('id_producto'):
                # Buscar el producto en la lista
                for producto in self.productos:
                    if producto['id_producto'] == datos_cuenta['id_producto']:
                        producto_texto = f"{producto['id_producto']} - {producto['nombre_producto']}"
                        self.variables_formulario['producto'].set(producto_texto)
                        break
                
        except Exception as e:
            logger.error(f"Error al llenar formulario: {str(e)}")
            messagebox.showerror("Error", f"Error al llenar formulario: {str(e)}")
    
    def _limpiar_formulario(self):
        """Limpia el formulario."""
        for variable in self.variables_formulario.values():
            variable.set("")
        self.cuenta_actual = None
