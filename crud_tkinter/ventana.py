from os import stat
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from conexion import  DAO

class Ventana(Frame):
    
    dao=DAO()
    
    def __init__(self, master=None):
        super().__init__(master,width=1000,height=400)
        self.master=master
        self.pack()
        self.crear_widgets() #creamos todos los controles
        self.CargarDatos()
        self.HabilitarText("disabled")
        self.HabilitarBotonesEventos("normal")
        self.HabilitarBotonesGuardar("disabled")
        self.bandera="Guardar"
       
        
    #Todas las funciones del crud y Botonoes, Eventos Etc
    
    #Cargar Datos en el Grid
    def CargarDatos(self):
        datos=self.dao.consulta_clientes()
        for row in datos:
            self.grid.insert("",END,text=row[0], values=(row[1],row[2],row[3],row[4]))
            
    def LimpiarGrid(self):
        for item in self.grid.get_children():  #Obtengo todos los datos del Grid
            self.grid.delete(item)
            
    def HabilitarText(self, estado):
        self.txtCodigo.configure(state=estado) #"normal" o "disabled"
        self.txtNombre.configure(state=estado)
        self.txtAp.configure(state=estado)
        self.txtAm.configure(state=estado)
        self.txtCreditos.configure(state=estado)
    
    def HabilitarBotonesEventos(self,estado):
        self.btnNuevo.configure(state=estado)
        self.btnActualizar.configure(state=estado)
        self.btnEliminar.configure(state=estado)
    
    def HabilitarBotonesGuardar(self,estado):
        self.btnGuardar.configure(state=estado)
        self.btnCancelar.configure(state=estado)
        
    def LimpiarText(self):
        self.txtCodigo.delete(0,END)
        self.txtNombre.delete(0,END)
        self.txtAp.delete(0,END)
        self.txtAm.delete(0,END)
        self.txtCreditos.delete(0,END)
        self.txtCodigo.focus()
        
    
    
    def fNuevo(self):  
        self.HabilitarText("normal")
        self.HabilitarBotonesEventos("disable")
        self.HabilitarBotonesGuardar("normal")
        self.LimpiarText()      
        
    
    def fActualizar(self):
        select=self.grid.focus() #Selecciona el id
        #print(select)
        row=self.grid.item(select) #todos
        #print(row)
        codigo=self.grid.item(select,"text")
        #print(codigo)
        valores=self.grid.item(select,"values")
        #print(valores)
        
        if codigo=="":
            #print("Selecciona un elemento")
            messagebox.showwarning("Modificar","Debes de seleccionar un elemento para poderlo Modificar")
        else:
            #cambiar el self.codigo por el valor del codigo
            self.bandera="Actualizar"   #super importante para poder Actualizar     
            print(f"Mostrando el estado de la bandera: {self.bandera}")
            print(valores)
            self.HabilitarText("normal")
            self.LimpiarText()
            self.HabilitarBotonesGuardar("normal")
            self.txtCodigo.insert(0,codigo)
            self.txtNombre.insert(0,valores[0])
            self.txtAp.insert(0,valores[1])
            self.txtAm.insert(0,valores[2])
            self.txtCreditos.insert(0,valores[3])
            #self.txtCodigo.configure(state="disabled")
            #Pasar a Negativo
    
    
    
    def fEliminar(self):
        select=self.grid.focus() #Selecciona el id
        #print(select)
        row=self.grid.item(select) #todos
        #print(row)
        codigo=self.grid.item(select,"text")
        print(codigo)
        valores=self.grid.item(select,"values")
        print(valores)
        if codigo=="":
            #print("Selecciona un elemento")
            messagebox.showwarning("Eliminar","Debes de seleccionar un Elemento")
        else:
            r=messagebox.askquestion(f"Eliminar","Estas seguro de Eliminarlo ?")
            if r==messagebox.YES:
                n=self.dao.elimina_clientes(codigo)
                if n==1:
                    messagebox.showinfo("Eliminar","Registro Eliminado Exitosamente")
                    self.LimpiarGrid()
                    self.CargarDatos()
                else:
                     messagebox.showinfo("Eliminar","No se Puedo Eliminar")
            else:
                pass
            

    
    
    def fGuardar(self):
        
        if self.bandera=="Guardar":        
            cod=self.txtCodigo.get() #Obtengo el texto de la caja
            #print(cod)
            nom=self.txtNombre.get()
            ap=self.txtAp.get()
            am=self.txtAm.get()
            cre=self.txtCreditos.get() 
            try:      
                self.dao.inserta_clientes(cod,nom,ap,am,cre)
                messagebox.showinfo("Guardar","Registro Guardado Exitosamente")                
            except:
                messagebox.showinfo("Guardar","No se Pudo Insertar")
                
        elif self.bandera=="Actualizar":
            #messagebox.showinfo("Entro","Entro a modificar")
            codM=self.txtCodigo.get()
            #print(codigo)
            nomM=self.txtNombre.get()
            apM=self.txtAp.get()
            amM=self.txtAm.get()
            creM=self.txtCreditos.get()   
            self.dao.modifica_clientes(nomM,apM,amM,creM,codM)
            #Cambiar bandera a
            messagebox.showinfo("Actualizar","Registro Actualizado Exitosamente")
            #Muy importante regresar el estado a Guardar
            self.bandera="Guardar"
             
        self.LimpiarGrid()
        self.CargarDatos()
        self.LimpiarText()
        self.HabilitarBotonesEventos("normal")
        self.HabilitarBotonesGuardar("disabled")
        self.HabilitarText("disabled")  
            
            
    
    
    def fCancelar(self):
        self.LimpiarGrid()
        self.CargarDatos()
        self.LimpiarText()
        self.HabilitarBotonesEventos("normal")
        self.HabilitarBotonesGuardar("disabled")
        self.HabilitarText("disabled")

    
    
    
    
    
    def crear_widgets(self):
        #primer cuadro de la izq
        frame1=Frame(self, bg="#B60F1A")
        frame1.place(x=0,y=0,width=150,height=399)   
        
        #Boton Nuevo
        self.btnNuevo=Button(frame1,text="Alta Cliente",command=self.fNuevo, bg="black", fg="white")
        self.btnNuevo.place(x=15,y=50,width=90,height=40) 
        
        #Boton Actualizar
        self.btnActualizar=Button(frame1,text="Modificar Cliente",command=self.fActualizar, bg="black", fg="white")
        self.btnActualizar.place(x=15,y=140,width=120,height=40)
        
        #Boton Eliminar
        self.btnEliminar=Button(frame1,text="Eliminar Cliente",command=self.fEliminar, bg="black", fg="white")
        self.btnEliminar.place(x=15,y=220,width=90,height=40)
        
        #Sección de datos
        frame2=Frame(self, bg="#09436D")
        frame2.place(x=150,y=0,width=230,height=399)
        
        #Primer Etiqueta Codigo
        lbl1=Label(frame2,text="Código: ")
        lbl1.place(x=30, y=30)
        self.txtCodigo=Entry(frame2)
        self.txtCodigo.place(x=30,y=58,width=150,height=20)
        
        #Primer Etiqueta Nombre
        lbl2=Label(frame2,text="Nombre: ")
        lbl2.place(x=30, y=95)
        self.txtNombre=Entry(frame2)
        self.txtNombre.place(x=30,y=125,width=150,height=20)
        
        #Primer Etiqueta Ap
        lbl3=Label(frame2,text="Apellido Paterno: ")
        lbl3.place(x=30, y=160)
        self.txtAp=Entry(frame2)
        self.txtAp.place(x=30,y=185,width=150,height=20)
        
        #Primer Etiqueta Am
        lbl4=Label(frame2,text="Apellido Materno: ")
        lbl4.place(x=30, y=215)
        self.txtAm=Entry(frame2)
        self.txtAm.place(x=30,y=245,width=150,height=20)
        
        #Primer Etiqueta Credito
        lbl5=Label(frame2,text="Credito: ")
        lbl5.place(x=30, y=270)
        self.txtCreditos=Entry(frame2)
        self.txtCreditos.place(x=30,y=300,width=150,height=20)
        
        #Botonos de guardado 
        #Boton guardar
        self.btnGuardar=Button(frame2,text="Guardar",command=self.fGuardar, bg="#108EE9", fg="white")
        self.btnGuardar.place(x=20,y=340,width=90,height=40)
        
        #Boton Cancelar
        self.btnCancelar=Button(frame2,text="Cancelar",command=self.fCancelar, bg="#9A0812", fg="white")
        self.btnCancelar.place(x=120,y=340,width=90,height=40)
        
        
        #Grid
        #Sección de Para el Grid
        frame3=Frame(self, bg="#ed3913")
        frame3.place(x=380, y=0, width=590,height=390)
        
        self.grid=ttk.Treeview(self,columns=("col1","col2","col3","col4"))
        
        self.grid.column("#0", width=40, anchor=CENTER)
        self.grid.column("col1", width=90, anchor=CENTER)
        self.grid.column("col2", width=90, anchor=CENTER)
        self.grid.column("col3", width=90, anchor=CENTER)
        self.grid.column("col4", width=90, anchor=CENTER)
        
        self.grid.heading("#0", text="Código", anchor=CENTER)
        self.grid.heading("col1", text="Nombre", anchor=CENTER)
        self.grid.heading("col2", text="Ape. Paterno", anchor=CENTER)
        self.grid.heading("col3", text="Ape. Materno", anchor=CENTER)
        self.grid.heading("col4", text="Credito", anchor=CENTER)
        
        #Ponerlo
        self.grid.place(x=380, y=0, width=590,height=390)
        #Seleccionar uno solo
        self.grid['selectmode']='browse'
    
        
    
    
    
    