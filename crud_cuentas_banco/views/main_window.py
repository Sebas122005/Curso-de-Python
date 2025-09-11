"""
Ventana principal del sistema bancario.
Contiene el menú principal y la navegación entre módulos.
"""

import py_compile
import tkinter as tk
from tkinter import ttk, messagebox
from views.base_view import BaseView
from views.cliente_view import ClienteView
from views.cuenta_view import CuentaView
from controllers.cliente_controller import ClienteController
from controllers.cuenta_controller import CuentaController
from controllers.usuario_controller import UsuarioController
import logging

logger = logging.getLogger(__name__)


class MainWindow:
    """Ventana principal del sistema bancario."""
    
    def __init__(self, root):
        """
        Inicializa la ventana principal.
        
        Args:
            root: Ventana raíz de Tkinter
        """
        self.root = root
        self.root.title("Sistema CRUD - Cuentas Bancarias")
        self.root.geometry("1000x700")
        
        # Configurar el cierre de la ventana
        self.root.protocol("WM_DELETE_WINDOW", self._cerrar_aplicacion)
        
        # Inicializar controladores
        self.cliente_controller = ClienteController()
        self.cuenta_controller = CuentaController()
        self.usuario_controller = UsuarioController()
        
        # Frame actual
        self.frame_actual = None
        
        # Crear interfaz
        self._crear_interfaz()
        
        # Centrar ventana
        self._centrar_ventana()
    
    def _crear_interfaz(self):
        """Crea la interfaz principal."""
        # Frame principal
        self.frame_principal = ttk.Frame(self.root)
        self.frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear barra de menú
        self._crear_barra_menu()
        
        # Crear área de contenido
        self._crear_area_contenido()
        
        # Mostrar pantalla de inicio
        self._mostrar_pantalla_inicio()
    
    def _crear_barra_menu(self):
        """Crea la barra de menú principal."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Sistema
        menu_sistema = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Sistema", menu=menu_sistema)
        menu_sistema.add_command(label="Inicio", command=self._mostrar_pantalla_inicio)
        menu_sistema.add_separator()
        menu_sistema.add_command(label="Salir", command=self._cerrar_aplicacion)
        
        # Menú Clientes
        menu_clientes = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Clientes", menu=menu_clientes)
        menu_clientes.add_command(label="Gestionar Clientes", command=self._abrir_clientes)
        menu_clientes.add_command(label="Buscar Cliente", command=self._buscar_cliente)
        
        # Menú Cuentas
        menu_cuentas = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Cuentas", menu=menu_cuentas)
        menu_cuentas.add_command(label="Gestionar Cuentas", command=self._abrir_cuentas)
        menu_cuentas.add_command(label="Buscar Cuenta", command=self._buscar_cuenta)
        
        # Menú Reportes
        menu_reportes = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Reportes", menu=menu_reportes)
        menu_reportes.add_command(label="Estadísticas Generales", command=self._mostrar_estadisticas)
        
        # Menú Ayuda
        menu_ayuda = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=menu_ayuda)
        menu_ayuda.add_command(label="Acerca de", command=self._mostrar_acerca_de)
    
    def _crear_area_contenido(self):
        """Crea el área de contenido principal."""
        # Frame para el contenido
        self.frame_contenido = ttk.Frame(self.frame_principal)
        self.frame_contenido.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Configurar grid
        self.frame_principal.columnconfigure(0, weight=1)
        self.frame_principal.rowconfigure(1, weight=1)
    
    def _mostrar_pantalla_inicio(self):
        """Muestra la pantalla de inicio."""
        self._limpiar_contenido()
        
        # Crear vista de inicio
        vista_inicio = InicioView(self.frame_contenido, self)
        self.frame_actual = vista_inicio.frame_principal
    
    def _abrir_clientes(self):
        """Abre el módulo de gestión de clientes."""
        self._limpiar_contenido()
        
        try:
            vista_clientes = ClienteView(self.frame_contenido, self.cliente_controller)
            self.frame_actual = vista_clientes.frame_principal
        except Exception as e:
            logger.error(f"Error al abrir módulo de clientes: {str(e)}")
            messagebox.showerror("Error", f"Error al abrir módulo de clientes: {str(e)}")
    
    def _abrir_cuentas(self):
        """Abre el módulo de gestión de cuentas."""
        self._limpiar_contenido()
        
        try:
            vista_cuentas = CuentaView(self.frame_contenido, self.cuenta_controller)
            self.frame_actual = vista_cuentas.frame_principal
        except Exception as e:
            logger.error(f"Error al abrir módulo de cuentas: {str(e)}")
            messagebox.showerror("Error", f"Error al abrir módulo de cuentas: {str(e)}")
    
    def _buscar_cliente(self):
        """Abre el diálogo de búsqueda de cliente."""
        # TODO: Implementar diálogo de búsqueda
        messagebox.showinfo("Búsqueda", "Funcionalidad de búsqueda en desarrollo")
    
    def _buscar_cuenta(self):
        """Abre el diálogo de búsqueda de cuenta."""
        # TODO: Implementar diálogo de búsqueda
        messagebox.showinfo("Búsqueda", "Funcionalidad de búsqueda en desarrollo")
    
    def _mostrar_estadisticas(self):
        """Muestra las estadísticas generales del sistema."""
        self._limpiar_contenido()
        
        try:
            vista_estadisticas = EstadisticasView(self.frame_contenido, self)
            self.frame_actual = vista_estadisticas.frame_principal
        except Exception as e:
            logger.error(f"Error al mostrar estadísticas: {str(e)}")
            messagebox.showerror("Error", f"Error al mostrar estadísticas: {str(e)}")
    
    def _mostrar_acerca_de(self):
        """Muestra información sobre la aplicación."""
        mensaje = """
Sistema CRUD - Cuentas Bancarias
Versión 1.0

Desarrollado con Python y Tkinter
Patrón de Arquitectura: MVC

Funcionalidades:
• Gestión de Clientes
• Gestión de Cuentas Bancarias
• Gestión de Usuarios
• Reportes y Estadísticas
        """
        messagebox.showinfo("Acerca de", mensaje)
    
    def _limpiar_contenido(self):
        """Limpia el área de contenido."""
        if self.frame_actual:
            self.frame_actual.destroy()
        self.frame_actual = None
    
    def _centrar_ventana(self):
        """Centra la ventana en la pantalla."""
        self.root.update_idletasks()
        ancho = self.root.winfo_width()
        alto = self.root.winfo_height()
        
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()
        
        x = (ancho_pantalla - ancho) // 2
        y = (alto_pantalla - alto) // 2
        
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")
    
    def _cerrar_aplicacion(self):
        """Cierra la aplicación."""
        if messagebox.askyesno("Salir", "¿Está seguro que desea salir de la aplicación?"):
            self.root.quit()
            self.root.destroy()


class InicioView(BaseView):
    """Vista de la pantalla de inicio."""
    
    def __init__(self, parent, main_window):
        super().__init__(parent, "Sistema CRUD - Cuentas Bancarias")
        self.main_window = main_window
        self._crear_interfaz()
    
    def _crear_interfaz(self):
        """Crea la interfaz de la pantalla de inicio."""
        # Título principal
        self.crear_titulo("Sistema CRUD - Cuentas Bancarias", 0, 0, 2)
        
        # Subtítulo
        subtitulo = ttk.Label(
            self.frame_principal, 
            text="Gestión Integral de Cuentas Bancarias",
            font=('Arial', 12)
        )
        subtitulo.grid(row=1, column=0, columnspan=2, pady=(0, 30), sticky=tk.W)
        
        # Frame para botones de acceso rápido
        frame_botones = ttk.LabelFrame(self.frame_principal, text="Acceso Rápido", padding="20")
        frame_botones.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Botones de acceso rápido
        btn_clientes = ttk.Button(
            frame_botones, 
            text="Gestionar Clientes", 
            command=self.main_window._abrir_clientes,
            width=20
        )
        btn_clientes.grid(row=0, column=0, padx=10, pady=5)
        
        btn_cuentas = ttk.Button(
            frame_botones, 
            text="Gestionar Cuentas", 
            command=self.main_window._abrir_cuentas,
            width=20
        )
        btn_cuentas.grid(row=0, column=1, padx=10, pady=5)
        
        btn_estadisticas = ttk.Button(
            frame_botones, 
            text="Ver Estadísticas", 
            command=self.main_window._mostrar_estadisticas,
            width=20
        )
        btn_estadisticas.grid(row=0, column=2, padx=10, pady=5)
        
        # Frame para información del sistema
        frame_info = ttk.LabelFrame(self.frame_principal, text="Información del Sistema", padding="20")
        frame_info.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Información del sistema
        info_texto = """
Bienvenido al Sistema CRUD de Cuentas Bancarias.

Este sistema le permite:
• Registrar y gestionar clientes del banco
• Crear y administrar cuentas bancarias
• Realizar operaciones CRUD completas
• Generar reportes y estadísticas

Utilice el menú superior o los botones de acceso rápido para navegar por el sistema.
        """
        
        info_label = ttk.Label(frame_info, text=info_texto, justify=tk.LEFT)
        info_label.grid(row=0, column=0, sticky=tk.W)


class EstadisticasView(BaseView):
    """Vista de estadísticas del sistema."""
    
    def __init__(self, parent, main_window):
        super().__init__(parent, "Estadísticas del Sistema")
        self.main_window = main_window
        self._crear_interfaz()
        self._cargar_estadisticas()
    
    def _crear_interfaz(self):
        """Crea la interfaz de estadísticas."""
        # Título
        self.crear_titulo("Estadísticas del Sistema", 0, 0, 2)
        
        # Frame para estadísticas de clientes
        frame_clientes = ttk.LabelFrame(self.frame_principal, text="Estadísticas de Clientes", padding="10")
        frame_clientes.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 5), pady=5)
        
        self.label_total_clientes = ttk.Label(frame_clientes, text="Total de Clientes: Cargando...")
        self.label_total_clientes.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.label_clientes_categoria = ttk.Label(frame_clientes, text="Por Categoría: Cargando...")
        self.label_clientes_categoria.grid(row=1, column=0, sticky=tk.W, pady=2)
        
        # Frame para estadísticas de cuentas
        frame_cuentas = ttk.LabelFrame(self.frame_principal, text="Estadísticas de Cuentas", padding="10")
        frame_cuentas.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=5)
        
        self.label_total_cuentas = ttk.Label(frame_cuentas, text="Total de Cuentas: Cargando...")
        self.label_total_cuentas.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.label_cuentas_activas = ttk.Label(frame_cuentas, text="Cuentas Activas: Cargando...")
        self.label_cuentas_activas.grid(row=1, column=0, sticky=tk.W, pady=2)
        
        self.label_saldo_total = ttk.Label(frame_cuentas, text="Saldo Total: Cargando...")
        self.label_saldo_total.grid(row=2, column=0, sticky=tk.W, pady=2)
        
        # Botón para actualizar
        btn_actualizar = ttk.Button(
            self.frame_principal, 
            text="Actualizar Estadísticas", 
            command=self._cargar_estadisticas
        )
        btn_actualizar.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Configurar grid responsivo
        self.frame_principal.columnconfigure(0, weight=1)
        self.frame_principal.columnconfigure(1, weight=1)
    
    def _cargar_estadisticas(self):
        """Carga las estadísticas del sistema."""
        try:
            # Estadísticas de clientes
            exito, mensaje, stats_clientes = self.main_window.cliente_controller.obtener_estadisticas_clientes()
            if exito:
                self.label_total_clientes.config(text=f"Total de Clientes: {stats_clientes['total_clientes']}")
                
                categorias_texto = "Por Categoría: "
                for categoria, cantidad in stats_clientes['clientes_por_categoria'].items():
                    categorias_texto += f"{categoria}: {cantidad}, "
                categorias_texto = categorias_texto.rstrip(", ")
                self.label_clientes_categoria.config(text=categorias_texto)
            else:
                self.label_total_clientes.config(text=f"Error: {mensaje}")
            
            # Estadísticas de cuentas
            exito, mensaje, stats_cuentas = self.main_window.cuenta_controller.obtener_estadisticas_cuentas()
            if exito:
                self.label_total_cuentas.config(text=f"Total de Cuentas: {stats_cuentas['total_cuentas']}")
                self.label_cuentas_activas.config(text=f"Cuentas Activas: {stats_cuentas['cuentas_activas']}")
                self.label_saldo_total.config(text=f"Saldo Total: S/ {stats_cuentas['saldo_total']:,.2f}")
            else:
                self.label_total_cuentas.config(text=f"Error: {mensaje}")
                
        except Exception as e:
            logger.error(f"Error al cargar estadísticas: {str(e)}")
            messagebox.showerror("Error", f"Error al cargar estadísticas: {str(e)}")
