"""
Vista para la gestión de clientes del sistema bancario.
Permite realizar operaciones CRUD sobre clientes.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from views.base_view import BaseView
from controllers.cliente_controller import ClienteController
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class ClienteView(BaseView):
    """Vista para la gestión de clientes."""
    
    def __init__(self, parent, controller: ClienteController):
        super().__init__(parent, "Gestión de Clientes")
        self.controller = controller
        self.cliente_actual = None
        self.tipos_documento = []
        self.categorias = []
        
        # Cargar datos iniciales
        self._cargar_datos_iniciales()
        
        # Crear interfaz
        self._crear_interfaz()
    
    def _cargar_datos_iniciales(self):
        """Carga los datos iniciales necesarios."""
        try:
            # Cargar tipos de documento
            exito, _, self.tipos_documento = self.controller.obtener_tipos_documento()
            if not exito:
                messagebox.showwarning("Advertencia", "No se pudieron cargar los tipos de documento")
            
            # Cargar categorías
            exito, _, self.categorias = self.controller.obtener_categorias_cliente()
            if not exito:
                messagebox.showwarning("Advertencia", "No se pudieron cargar las categorías")
                
        except Exception as e:
            logger.error(f"Error al cargar datos iniciales: {str(e)}")
            messagebox.showerror("Error", f"Error al cargar datos iniciales: {str(e)}")
    
    def _crear_interfaz(self):
        """Crea la interfaz de gestión de clientes."""
        # Título
        self.crear_titulo("Gestión de Clientes", 0, 0, 2)
        
        # Frame para formulario
        self._crear_formulario()
        
        # Frame para botones
        self._crear_botones()
        
        # Frame para tabla
        self._crear_tabla()
        
        # Cargar datos iniciales
        self._cargar_clientes()
    
    def _crear_formulario(self):
        """Crea el formulario de cliente."""
        frame_formulario = self.crear_frame_grupo("Datos del Cliente", 1, 0, 2)
        
        # Variables del formulario
        self.variables_formulario = {
            'nombre': tk.StringVar(),
            'apellido_paterno': tk.StringVar(),
            'apellido_materno': tk.StringVar(),
            'tipo_documento': tk.StringVar(),
            'numero_documento': tk.StringVar(),
            'email': tk.StringVar(),
            'telefono': tk.StringVar(),
            'fecha_nacimiento': tk.StringVar(),
            'categoria': tk.StringVar()
        }
        
        # Fila 0: Nombre
        ttk.Label(frame_formulario, text="Nombre:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        ttk.Entry(frame_formulario, textvariable=self.variables_formulario['nombre'], width=30).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(0, 10))
        
        # Fila 1: Apellidos
        ttk.Label(frame_formulario, text="Apellido Paterno:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        ttk.Entry(frame_formulario, textvariable=self.variables_formulario['apellido_paterno'], width=30).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(0, 10))
        
        ttk.Label(frame_formulario, text="Apellido Materno:").grid(row=1, column=2, sticky=tk.W, padx=(0, 10), pady=5)
        ttk.Entry(frame_formulario, textvariable=self.variables_formulario['apellido_materno'], width=30).grid(row=1, column=3, sticky=(tk.W, tk.E), pady=5, padx=(0, 10))
        
        # Fila 2: Documento
        ttk.Label(frame_formulario, text="Tipo Documento:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        valores_tipo_doc = [f"{t['id_tipo_documento']} - {t['nombre_tipo']}" for t in self.tipos_documento]
        ttk.Combobox(frame_formulario, textvariable=self.variables_formulario['tipo_documento'], 
                    values=valores_tipo_doc, width=30, state='readonly').grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(0, 10))
        
        ttk.Label(frame_formulario, text="Número Documento:").grid(row=2, column=2, sticky=tk.W, padx=(0, 10), pady=5)
        ttk.Entry(frame_formulario, textvariable=self.variables_formulario['numero_documento'], width=30).grid(row=2, column=3, sticky=(tk.W, tk.E), pady=5, padx=(0, 10))
        
        # Fila 3: Email y Teléfono
        ttk.Label(frame_formulario, text="Email:").grid(row=3, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        ttk.Entry(frame_formulario, textvariable=self.variables_formulario['email'], width=30).grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(0, 10))
        
        ttk.Label(frame_formulario, text="Teléfono:").grid(row=3, column=2, sticky=tk.W, padx=(0, 10), pady=5)
        ttk.Entry(frame_formulario, textvariable=self.variables_formulario['telefono'], width=30).grid(row=3, column=3, sticky=(tk.W, tk.E), pady=5, padx=(0, 10))
        
        # Fila 4: Fecha de nacimiento y Categoría
        ttk.Label(frame_formulario, text="Fecha Nacimiento:").grid(row=4, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        ttk.Entry(frame_formulario, textvariable=self.variables_formulario['fecha_nacimiento'], width=30).grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5, padx=(0, 10))
        
        ttk.Label(frame_formulario, text="Categoría:").grid(row=4, column=2, sticky=tk.W, padx=(0, 10), pady=5)
        valores_categoria = [f"{c['id_categoria']} - {c['nombre_categoria']}" for c in self.categorias]
        ttk.Combobox(frame_formulario, textvariable=self.variables_formulario['categoria'], 
                    values=valores_categoria, width=30, state='readonly').grid(row=4, column=3, sticky=(tk.W, tk.E), pady=5, padx=(0, 10))
        
        # Configurar grid del formulario
        for i in range(5):
            frame_formulario.rowconfigure(i, weight=1)
        for i in range(4):
            frame_formulario.columnconfigure(i, weight=1)
    
    def _crear_botones(self):
        """Crea los botones de acción."""
        frame_botones = ttk.Frame(self.frame_principal)
        frame_botones.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Botones principales
        ttk.Button(frame_botones, text="Nuevo", command=self._nuevo_cliente).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(frame_botones, text="Guardar", command=self._guardar_cliente).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame_botones, text="Editar", command=self._editar_cliente).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(frame_botones, text="Eliminar", command=self._eliminar_cliente).grid(row=0, column=3, padx=5, pady=5)
        ttk.Button(frame_botones, text="Limpiar", command=self._limpiar_formulario).grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(frame_botones, text="Buscar", command=self._buscar_cliente).grid(row=0, column=5, padx=5, pady=5)
    
    def _crear_tabla(self):
        """Crea la tabla de clientes."""
        frame_tabla = self.crear_frame_grupo("Lista de Clientes", 3, 0, 2)
        
        # Columnas de la tabla
        columnas = ['ID', 'Nombre Completo', 'Documento', 'Email', 'Teléfono', 'Categoría']
        
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
        self.treeview.bind('<<TreeviewSelect>>', self._on_seleccion_cliente)
        
        # Configurar grid
        frame_tabla.rowconfigure(0, weight=1)
        frame_tabla.columnconfigure(0, weight=1)
    
    def _cargar_clientes(self):
        """Carga la lista de clientes en la tabla."""
        try:
            exito, mensaje, clientes = self.controller.listar()
            if exito:
                # Preparar datos para la tabla
                datos_tabla = []
                for cliente in clientes:
                    nombre_completo = self.controller.formatear_nombre_completo(cliente)
                    datos_tabla.append([
                        cliente['id_cliente'],
                        nombre_completo,
                        cliente['numero_documento'],
                        cliente['email'],
                        cliente['telefono'] or '',
                        cliente['categoria'] or ''
                    ])
                
                # Poblar tabla directamente
                for item in self.treeview.get_children():
                    self.treeview.delete(item)
                
                for fila in datos_tabla:
                    self.treeview.insert("", "end", values=fila)
            else:
                messagebox.showerror("Error", f"Error al cargar clientes: {mensaje}")
                
        except Exception as e:
            logger.error(f"Error al cargar clientes: {str(e)}")
            messagebox.showerror("Error", f"Error al cargar clientes: {str(e)}")
    
    def _nuevo_cliente(self):
        """Inicia la creación de un nuevo cliente."""
        self._limpiar_formulario()
        self.cliente_actual = None
        self.treeview.selection_remove(self.treeview.selection())
    
    def _guardar_cliente(self):
        """Guarda el cliente actual."""
        try:
            # Obtener datos del formulario
            datos = self._obtener_datos_formulario()
            
            if not datos:
                return
            
            if self.cliente_actual:
                # Actualizar cliente existente
                exito, mensaje = self.controller.actualizar_cliente(self.cliente_actual, datos)
            else:
                # Crear nuevo cliente
                exito, mensaje, id_nuevo = self.controller.crear_cliente(datos)
                if exito:
                    self.cliente_actual = id_nuevo
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self._cargar_clientes()
                self._limpiar_formulario()
                self.cliente_actual = None
            else:
                messagebox.showerror("Error", mensaje)
                
        except Exception as e:
            logger.error(f"Error al guardar cliente: {str(e)}")
            messagebox.showerror("Error", f"Error al guardar cliente: {str(e)}")
    
    def _editar_cliente(self):
        """Edita el cliente seleccionado."""
        if not self.cliente_actual:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para editar")
            return
        
        try:
            exito, mensaje, datos_cliente = self.controller.leer(self.cliente_actual)
            if exito:
                self._llenar_formulario(datos_cliente)
            else:
                messagebox.showerror("Error", mensaje)
                
        except Exception as e:
            logger.error(f"Error al editar cliente: {str(e)}")
            messagebox.showerror("Error", f"Error al editar cliente: {str(e)}")
    
    def _eliminar_cliente(self):
        """Elimina el cliente seleccionado."""
        if not self.cliente_actual:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para eliminar")
            return
        
        if not self.mostrar_confirmacion("Confirmar", "¿Está seguro que desea eliminar este cliente?"):
            return
        
        try:
            exito, mensaje = self.controller.eliminar(self.cliente_actual)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self._cargar_clientes()
                self._limpiar_formulario()
                self.cliente_actual = None
            else:
                messagebox.showerror("Error", mensaje)
                
        except Exception as e:
            logger.error(f"Error al eliminar cliente: {str(e)}")
            messagebox.showerror("Error", f"Error al eliminar cliente: {str(e)}")
    
    def _buscar_cliente(self):
        """Busca clientes por criterios."""
        # TODO: Implementar diálogo de búsqueda avanzada
        messagebox.showinfo("Búsqueda", "Funcionalidad de búsqueda en desarrollo")
    
    def _on_seleccion_cliente(self, event):
        """Maneja la selección de un cliente en la tabla."""
        seleccion = self.treeview.selection()
        if seleccion:
            item = self.treeview.item(seleccion[0])
            id_cliente = item['values'][0]
            self.cliente_actual = id_cliente
    
    def _obtener_datos_formulario(self) -> Optional[Dict]:
        """Obtiene los datos del formulario."""
        try:
            # Validar campos requeridos
            campos_requeridos = ['nombre', 'apellido_paterno', 'apellido_materno', 
                               'tipo_documento', 'numero_documento', 'email', 'categoria']
            
            for campo in campos_requeridos:
                if not self.variables_formulario[campo].get().strip():
                    messagebox.showerror("Error", f"El campo {campo.replace('_', ' ').title()} es requerido")
                    return None
            
            # Obtener datos
            datos = {
                'nombre': self.variables_formulario['nombre'].get().strip(),
                'apellido_paterno': self.variables_formulario['apellido_paterno'].get().strip(),
                'apellido_materno': self.variables_formulario['apellido_materno'].get().strip(),
                'numero_documento': self.variables_formulario['numero_documento'].get().strip(),
                'email': self.variables_formulario['email'].get().strip(),
                'telefono': self.variables_formulario['telefono'].get().strip(),
                'fecha_nacimiento': self.variables_formulario['fecha_nacimiento'].get().strip(),
                'id_agencia_apertura': 1  # Por defecto, agencia 1
            }
            
            # Obtener IDs de los comboboxes
            tipo_doc_texto = self.variables_formulario['tipo_documento'].get()
            if tipo_doc_texto:
                datos['id_tipo_documento'] = int(tipo_doc_texto.split(' - ')[0])
            
            categoria_texto = self.variables_formulario['categoria'].get()
            if categoria_texto:
                datos['id_categoria'] = int(categoria_texto.split(' - ')[0])
            
            return datos
            
        except Exception as e:
            logger.error(f"Error al obtener datos del formulario: {str(e)}")
            messagebox.showerror("Error", f"Error al obtener datos: {str(e)}")
            return None
    
    def _llenar_formulario(self, datos_cliente: Dict):
        """Llena el formulario con los datos del cliente."""
        try:
            self.variables_formulario['nombre'].set(datos_cliente.get('nombre', ''))
            self.variables_formulario['apellido_paterno'].set(datos_cliente.get('apellido_paterno', ''))
            self.variables_formulario['apellido_materno'].set(datos_cliente.get('apellido_materno', ''))
            self.variables_formulario['numero_documento'].set(datos_cliente.get('numero_documento', ''))
            self.variables_formulario['email'].set(datos_cliente.get('email', ''))
            self.variables_formulario['telefono'].set(datos_cliente.get('telefono', ''))
            self.variables_formulario['fecha_nacimiento'].set(datos_cliente.get('fecha_nacimiento', ''))
            
            # Establecer valores de comboboxes
            if datos_cliente.get('id_tipo_documento'):
                tipo_doc_texto = f"{datos_cliente['id_tipo_documento']} - {datos_cliente.get('tipo_documento', '')}"
                self.variables_formulario['tipo_documento'].set(tipo_doc_texto)
            
            if datos_cliente.get('id_categoria'):
                categoria_texto = f"{datos_cliente['id_categoria']} - {datos_cliente.get('categoria', '')}"
                self.variables_formulario['categoria'].set(categoria_texto)
                
        except Exception as e:
            logger.error(f"Error al llenar formulario: {str(e)}")
            messagebox.showerror("Error", f"Error al llenar formulario: {str(e)}")
    
    def _limpiar_formulario(self):
        """Limpia el formulario."""
        for variable in self.variables_formulario.values():
            variable.set("")
        self.cliente_actual = None
