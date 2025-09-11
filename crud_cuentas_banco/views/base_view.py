"""
Vista base para todas las ventanas del sistema bancario.
Proporciona funcionalidad común y componentes reutilizables.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Any, Optional, Callable
import logging

logger = logging.getLogger(__name__)


class BaseView:
    """Clase base para todas las vistas del sistema."""
    
    def __init__(self, parent, titulo: str = ""):
        """
        Inicializa la vista base.
        
        Args:
            parent: Widget padre
            titulo: Título de la ventana
        """
        self.parent = parent
        self.titulo = titulo
        self.frame_principal = None
        self.variables_formulario = {}
        self.widgets = {}
        
        # Configurar estilo
        self._configurar_estilo()
        
        # Crear frame principal
        self._crear_frame_principal()
    
    def _configurar_estilo(self):
        """Configura el estilo de los widgets."""
        self.style = ttk.Style()
        
        # Configurar tema
        self.style.theme_use('clam')
        
        # Configurar colores
        self.style.configure('TLabel', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('TEntry', font=('Arial', 10))
        self.style.configure('TCombobox', font=('Arial', 10))
        self.style.configure('Treeview', font=('Arial', 9))
        self.style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
    
    def _crear_frame_principal(self):
        """Crea el frame principal de la vista."""
        self.frame_principal = ttk.Frame(self.parent, padding="10")
        self.frame_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        self.frame_principal.columnconfigure(1, weight=1)
    
    def crear_titulo(self, texto: str, fila: int = 0, columna: int = 0, 
                    colspan: int = 2) -> ttk.Label:
        """
        Crea un título para la vista.
        
        Args:
            texto: Texto del título
            fila: Fila donde colocar el título
            columna: Columna donde colocar el título
            colspan: Número de columnas que abarca
            
        Returns:
            ttk.Label: Widget del título
        """
        titulo = ttk.Label(
            self.frame_principal, 
            text=texto, 
            font=('Arial', 14, 'bold')
        )
        titulo.grid(row=fila, column=columna, columnspan=colspan, 
                   pady=(0, 20), sticky=tk.W)
        
        return titulo
    
    def crear_label(self, texto: str, fila: int, columna: int = 0, 
                   sticky: str = tk.W) -> ttk.Label:
        """
        Crea una etiqueta.
        
        Args:
            texto: Texto de la etiqueta
            fila: Fila donde colocar la etiqueta
            columna: Columna donde colocar la etiqueta
            sticky: Posicionamiento
            
        Returns:
            ttk.Label: Widget de la etiqueta
        """
        label = ttk.Label(self.frame_principal, text=texto)
        label.grid(row=fila, column=columna, sticky=sticky, padx=(0, 10), pady=5)
        return label
    
    def crear_entry(self, fila: int, columna: int = 1, ancho: int = 30, 
                   variable: Optional[tk.StringVar] = None) -> ttk.Entry:
        """
        Crea un campo de entrada de texto.
        
        Args:
            fila: Fila donde colocar el campo
            columna: Columna donde colocar el campo
            ancho: Ancho del campo
            variable: Variable asociada al campo
            
        Returns:
            ttk.Entry: Widget del campo de entrada
        """
        if variable is None:
            variable = tk.StringVar()
            self.variables_formulario[f"entry_{fila}_{columna}"] = variable
        
        entry = ttk.Entry(self.frame_principal, textvariable=variable, width=ancho)
        entry.grid(row=fila, column=columna, sticky=(tk.W, tk.E), pady=5, padx=(0, 10))
        
        return entry
    
    def crear_combobox(self, fila: int, columna: int = 1, ancho: int = 30,
                      valores: List[str] = None, variable: Optional[tk.StringVar] = None) -> ttk.Combobox:
        """
        Crea un combobox.
        
        Args:
            fila: Fila donde colocar el combobox
            columna: Columna donde colocar el combobox
            ancho: Ancho del combobox
            valores: Lista de valores
            variable: Variable asociada al combobox
            
        Returns:
            ttk.Combobox: Widget del combobox
        """
        if variable is None:
            variable = tk.StringVar()
            self.variables_formulario[f"combobox_{fila}_{columna}"] = variable
        
        combobox = ttk.Combobox(
            self.frame_principal, 
            textvariable=variable, 
            width=ancho,
            values=valores or [],
            state='readonly'
        )
        combobox.grid(row=fila, column=columna, sticky=(tk.W, tk.E), pady=5, padx=(0, 10))
        
        return combobox
    
    def crear_boton(self, texto: str, comando: Callable, fila: int, columna: int = 0,
                   colspan: int = 1, sticky: str = tk.W) -> ttk.Button:
        """
        Crea un botón.
        
        Args:
            texto: Texto del botón
            comando: Función a ejecutar al hacer clic
            fila: Fila donde colocar el botón
            columna: Columna donde colocar el botón
            colspan: Número de columnas que abarca
            sticky: Posicionamiento
            
        Returns:
            ttk.Button: Widget del botón
        """
        boton = ttk.Button(
            self.frame_principal, 
            text=texto, 
            command=comando
        )
        boton.grid(row=fila, column=columna, columnspan=colspan, 
                  sticky=sticky, pady=5, padx=(0, 10))
        
        return boton
    
    def crear_treeview(self, columnas: List[str], fila: int, columna: int = 0,
                      colspan: int = 2, filas: int = 10) -> ttk.Treeview:
        """
        Crea una tabla (Treeview).
        
        Args:
            columnas: Lista de nombres de columnas
            fila: Fila donde colocar la tabla
            columna: Columna donde colocar la tabla
            colspan: Número de columnas que abarca
            filas: Número de filas visibles
            
        Returns:
            ttk.Treeview: Widget de la tabla
        """
        # Crear frame para la tabla y scrollbar
        frame_tabla = ttk.Frame(self.frame_principal)
        frame_tabla.grid(row=fila, column=columna, columnspan=colspan, 
                        sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Crear Treeview
        treeview = ttk.Treeview(frame_tabla, columns=columnas, show='headings', height=filas)
        
        # Configurar columnas
        for col in columnas:
            treeview.heading(col, text=col)
            treeview.column(col, width=100, anchor=tk.CENTER)
        
        # Crear scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=treeview.yview)
        treeview.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar widgets
        treeview.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configurar grid
        frame_tabla.columnconfigure(0, weight=1)
        frame_tabla.rowconfigure(0, weight=1)
        
        return treeview
    
    def crear_separador(self, fila: int, columna: int = 0, colspan: int = 2) -> ttk.Separator:
        """
        Crea un separador horizontal.
        
        Args:
            fila: Fila donde colocar el separador
            columna: Columna donde colocar el separador
            colspan: Número de columnas que abarca
            
        Returns:
            ttk.Separator: Widget del separador
        """
        separador = ttk.Separator(self.frame_principal, orient='horizontal')
        separador.grid(row=fila, column=columna, columnspan=colspan, 
                      sticky=(tk.W, tk.E), pady=10)
        
        return separador
    
    def mostrar_mensaje(self, titulo: str, mensaje: str, tipo: str = "info"):
        """
        Muestra un mensaje al usuario.
        
        Args:
            titulo: Título del mensaje
            mensaje: Contenido del mensaje
            tipo: Tipo de mensaje (info, warning, error, success)
        """
        if tipo == "error":
            messagebox.showerror(titulo, mensaje)
        elif tipo == "warning":
            messagebox.showwarning(titulo, mensaje)
        elif tipo == "success":
            messagebox.showinfo(titulo, mensaje)
        else:
            messagebox.showinfo(titulo, mensaje)
    
    def mostrar_confirmacion(self, titulo: str, mensaje: str) -> bool:
        """
        Muestra un diálogo de confirmación.
        
        Args:
            titulo: Título del diálogo
            mensaje: Contenido del mensaje
            
        Returns:
            bool: True si el usuario confirma, False en caso contrario
        """
        return messagebox.askyesno(titulo, mensaje)
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario."""
        for variable in self.variables_formulario.values():
            if isinstance(variable, tk.StringVar):
                variable.set("")
    
    def obtener_valor_campo(self, nombre_campo: str) -> str:
        """
        Obtiene el valor de un campo del formulario.
        
        Args:
            nombre_campo: Nombre del campo
            
        Returns:
            str: Valor del campo
        """
        variable = self.variables_formulario.get(nombre_campo)
        if variable:
            return variable.get()
        return ""
    
    def establecer_valor_campo(self, nombre_campo: str, valor: str):
        """
        Establece el valor de un campo del formulario.
        
        Args:
            nombre_campo: Nombre del campo
            valor: Valor a establecer
        """
        variable = self.variables_formulario.get(nombre_campo)
        if variable:
            variable.set(valor)
    
    def poblar_treeview(self, treeview: ttk.Treeview, datos: List[Dict], 
                       columnas: List[str]):
        """
        Pobla una tabla con datos.
        
        Args:
            treeview: Widget de la tabla
            datos: Lista de diccionarios con los datos
            columnas: Lista de nombres de columnas
        """
        # Limpiar tabla
        for item in treeview.get_children():
            treeview.delete(item)
        
        # Agregar datos
        for fila in datos:
            valores = [fila.get(col, "") for col in columnas]
            treeview.insert("", "end", values=valores)
    
    def obtener_fila_seleccionada(self, treeview: ttk.Treeview) -> Optional[Dict]:
        """
        Obtiene los datos de la fila seleccionada en una tabla.
        
        Args:
            treeview: Widget de la tabla
            
        Returns:
            dict: Datos de la fila seleccionada o None
        """
        seleccion = treeview.selection()
        if not seleccion:
            return None
        
        item = treeview.item(seleccion[0])
        return item['values']
    
    def configurar_grid_responsivo(self, filas_peso: List[int] = None, 
                                  columnas_peso: List[int] = None):
        """
        Configura el grid para que sea responsivo.
        
        Args:
            filas_peso: Lista de pesos para las filas
            columnas_peso: Lista de pesos para las columnas
        """
        if filas_peso:
            for i, peso in enumerate(filas_peso):
                self.frame_principal.rowconfigure(i, weight=peso)
        
        if columnas_peso:
            for i, peso in enumerate(columnas_peso):
                self.frame_principal.columnconfigure(i, weight=peso)
    
    def centrar_ventana(self, ancho: int = 800, alto: int = 600):
        """
        Centra la ventana en la pantalla.
        
        Args:
            ancho: Ancho de la ventana
            alto: Alto de la ventana
        """
        if hasattr(self.parent, 'winfo_screenwidth'):
            ancho_pantalla = self.parent.winfo_screenwidth()
            alto_pantalla = self.parent.winfo_screenheight()
            
            x = (ancho_pantalla - ancho) // 2
            y = (alto_pantalla - alto) // 2
            
            self.parent.geometry(f"{ancho}x{alto}+{x}+{y}")
    
    def crear_frame_grupo(self, titulo: str, fila: int, columna: int = 0, 
                         colspan: int = 2) -> ttk.LabelFrame:
        """
        Crea un frame de grupo con título.
        
        Args:
            titulo: Título del grupo
            fila: Fila donde colocar el frame
            columna: Columna donde colocar el frame
            colspan: Número de columnas que abarca
            
        Returns:
            ttk.LabelFrame: Widget del frame de grupo
        """
        frame_grupo = ttk.LabelFrame(self.frame_principal, text=titulo, padding="10")
        frame_grupo.grid(row=fila, column=columna, columnspan=colspan, 
                        sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        return frame_grupo
