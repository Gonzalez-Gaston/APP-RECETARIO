import tkinter as tk
from tkinter import ttk
from tkinter import *
import csv
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from datetime import datetime as dt
import random


recetas = []
with open("recetas.csv", "a+", newline="") as archivo:
        """Creamos un nuevo archivo de recetas, si ya existe, agregamos los datos de las recetas a ese mismo archivo"""
        escritor = csv.writer(archivo)
        escritor.writerows(recetas)   

class App(ttk.Frame):
    """"Representa la ventana principal de la aplicación."""
    def __init__(self, parent):
        super().__init__(parent, padding=(20))
        self.parent = parent    
        parent.title("Ventana Principal")
        parent.geometry("700x700")
        parent.columnconfigure(0, weight=1)
        self.grid()
        parent.resizable(False, False)
        self.filename = ("RP_logo.png")

        
        img = Image.open(self.filename)
        img = img.resize((600,100), Image.LANCZOS)
        imagen = ImageTk.PhotoImage(img)
        label1 = ttk.Label(self, image = imagen, relief="raised")
        label1.image = imagen
        label1.grid(row=0, column=0)

        self.receta_dia = ttk.Button(self, text="Receta del día", command=self.receta_del_dia, width=96, padding=10)
        self.receta_dia.grid(row=2, column=0)

        self.boton_receta = ttk.Button(text="Mostrar receta",padding=10, width=96,command=self.mostrar_receta)
        self.boton_receta.grid(row=3,column=0)

        self.boton_receta = ttk.Button(text="Editar receta",padding=10, width=96,command=self.editar_receta)
        self.boton_receta.grid(row=4, column=0)

        self.boton_eliminar = ttk.Button(text="Eliminar receta",padding=10, width=96,command=self.eliminar_receta)
        self.boton_eliminar.grid(row=5, column=0)

        self.crear = ttk.Button(text="Crear nueva receta", padding=10, width=96,command=self.abrir_ventana)
        self.crear.grid(row=6, column=0)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0) 
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)


        # definimos las columnas de la tabla
        columnas = ('nombre', 'ingredientes', 'tiempo_p')

        self.tabla = ttk.Treeview(self, columns=columnas, show='headings',selectmode="browse") # sin multi-seleccion
        self.tabla.grid(pady=10)

        # definimos los encabezados que se muestran
        self.tabla.heading('nombre', text='Nombre')
        self.tabla.heading('ingredientes', text='Ingredientes')
        self.tabla.heading('tiempo_p', text='Tiempo de preparacion')

        with open("recetas.csv",  newline="") as archivo:
            lector = csv.reader(archivo, delimiter=",")
            for r in lector:
                self.tabla.insert('', tk.END, values=r)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set) # la enlazamos al treeview
        scrollbar.grid(row=1, column=2, rowspan=3)


    def receta_del_dia(slef):
        """Esta funcion muestra una receta aleatoriamente"""
        toplevel = tk.Toplevel()
        with open("recetas.csv", newline="") as archivo:
            lector = csv.reader(archivo, delimiter=",")
            lista=[]
            
            for items in lector:
                lista.append(items)
                aleatorio = random.choice(lista)
            
            VerReceta(toplevel, aleatorio[0], aleatorio[1], aleatorio[2], aleatorio[3], aleatorio[4], aleatorio[5], aleatorio[6]).grid()

    def mostrar_receta(self):
        """Esta función nos muestra la ventana donde se visualiza una receta seleccionada con sus respectivos datos."""
        toplevel = tk.Toplevel(self.parent)       
               
        with open("recetas.csv", newline="") as archivo:
            lector = csv.reader(archivo, delimiter=",")

            select = self.tabla.selection()            
            item = self.tabla.item(select)
            nombre = item["values"][0]
             
            for item in lector:
                if item[0] == nombre:
                    lista=item      
            visualizacion =VerReceta(toplevel, lista[0], lista[1], lista[2], lista[3], lista[4], lista[5], lista[6]).grid()

    def editar_receta(self):
        """Esta función nos muestra una ventana donde se pueden editar los datos de una receta previamente cargada."""
        toplevel = tk.Toplevel(self.parent)   
        toplevel.tabla = self.tabla                   
        with open("recetas.csv", newline="") as archivo:
            lector = csv.reader(archivo, delimiter=",")
            select = self.tabla.selection()   
            item = self.tabla.item(select)
            lista = []
            nombre = item["values"][0]
            for item in lector:
                if item[0] == nombre:
                    lista=item  
            
            visualizacion = EditarReceta(toplevel, lista[0], lista[1], lista[2], lista[3], lista[4], lista[6]).grid()
      
            

    def eliminar_receta(self, mensaje = "¿Seguro que quieres eliminar receta?\nNo podrás deshacer esta acción"):
        """Esta función elimina una receta seleccionada de la lista de recetas."""
        with open("recetas.csv", "r+", newline="") as archivo:    
                lector = csv.reader(archivo, delimiter=",")
                select = self.tabla.selection()            
                item = self.tabla.item(select)
                nombre=item['values'][0]
                lista=[]
                for l in lector:
                    lista.append(l)
                for r in lista:    
                    if r[0]==nombre:
                        lista.remove(r)
                for item in select:
                    var = messagebox.askokcancel(message=mensaje)
                    if var == True:
                        self.tabla.delete(item)                             
        with open("recetas.csv", "w", newline="") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerows(lista)

           
    def abrir_ventana(self):
        """Esta función  nos muestra una ventana donde se creará una nueva receta."""
        toplevel = tk.Toplevel(self.parent)
        toplevel.tabla = self.tabla
        Receta(toplevel).grid()

    def eliminar_para_editar(self):
        """Esta función elimina previamente una receta seleccionada para editarla."""
        with open("recetas.csv", "r+", newline="") as archivo:    
                lector = csv.reader(archivo, delimiter=",")
                select = self.tabla.selection()            
                item = self.tabla.item(select)
                nombre=item['values'][0]
                lista=[]
                for l in lector:
                    lista.append(l)
                for r in lista:    
                    if r[0]==nombre:
                        lista.remove(r)
                for item in select:        
                    self.tabla.delete(item) 

        with open("recetas.csv", "w", newline="") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerows(lista)

class VerReceta(ttk.Frame):
    """Representa una ventana donde se visualiza una receta con sus respectivos datos."""
    def __init__(self, parent, nombre="Nombre", ingredientes=[], tiempo_p="Tiempo de preparacion",
                  preparacion = "Preparacion", tiempo_c="Tiempo de coccion", creacion = "Fecha de creacion", imagen ="imagen"):
        super().__init__(parent, padding=(10))
        self.parent = parent
        parent.title("Receta")
        parent.geometry("700x700")
        parent.resizable(False, False)
        parent.grab_set()
        

        self.l1 = ttk.Label(self, text="Nombre de la receta:").grid(row=1, column=0)   
        self.label1 = ttk.Label(self, text=nombre).grid(row=1, column=1,padx=10, pady=10)

        self.l2 = ttk.Label(self, text="Ingredientes de la receta:").grid(row=2, column=0) 
        self.label2 = ttk.Label(self, text=ingredientes).grid(row=2, column=1, padx=10, pady=10)

        self.l3 = ttk.Label(self, text="Tiempo de preparacion:").grid(row=3, column=0) 
        self.label3 = ttk.Label(self, text=tiempo_p).grid(row=3, column=1, padx=10, pady=10)

        self.l4 = ttk.Label(self, text="Modo de preparacion:").grid(row=4, column=0) 
        self.label4 = ttk.Label(self, text=preparacion).grid(row=4, column=1, padx=10, pady=10)

        self.l5 = ttk.Label(self, text="Tiempo de coccion:").grid(row=5, column=0) 
        self.label5 = ttk.Label(self, text=tiempo_c).grid(row=5, column=1, padx=10, pady=10)

        self.l6 = ttk.Label(self, text="Fecha de creacion:").grid(row=6, column=0, padx=10, pady=10) 
        self.label6 = ttk.Label(self, text=creacion).grid(row=6, column=1, padx=10, pady=10)

        self.l8 = ttk.Label(self, text="Foto de la receta").grid(row=7, column=0)
        self.filename = imagen
        
        if self.filename:
            try:
                imag = Image.open(self.filename)
                imag = imag.resize((250,250), Image.LANCZOS)
                imagen = ImageTk.PhotoImage(imag)
                label7 = ttk.Label(self, image = imagen)
                label7.image = imagen
                label7.grid(row = 7, column =1,columnspan=2, padx=100, pady=10)
            except Exception as e:
                print(f"Error al cargar la imagen: {e}")

        


class EditarReceta(ttk.Frame):
    """Represeta una ventana donde se pueden editar los datos de una receta y guardar esos cambios."""
    def __init__(self, parent, nombre="Nombre", ingredientes=[], tiempo_p="Tiempo de preparacion",
                  preparacion = "Preparacion", tiempo_c="Tiempo de coccion", imagen ="imagen"):
        super().__init__(parent, padding=(10))
        self.parent = parent
        parent.title("Receta")
        parent.geometry("700x700")
        parent.resizable(False, False)
        parent.grab_set()

        self.nombre = tk.StringVar()
        self.lista_ingredientes = ingredientes
        self.ingrediente = tk.StringVar()
        self.tiempo_prep = tk.IntVar()
        self.prep = tk.StringVar()        
        self.tiempo_coccion = tk.IntVar()
        self.creacion = dt.now().strftime('%Y-%m-%d %H:%M:%S')
        self.filename = tk.StringVar()
           
        self.nombre.set(nombre)
        self.ingrediente.set(ingredientes)
        self.tiempo_prep.set(tiempo_p)
        self.prep.set(tiempo_p)
        self.tiempo_coccion.set(tiempo_c)
        self.filename.set(imagen)
        
        

        
        self.e1 = ttk.Label(self, text="Nombre de la receta:").grid(row=1, column=0)   
        self.entry1 = ttk.Entry(self, textvariable=self.nombre).grid(row=1, column=1,padx=10, pady=10)

        self.e2 = ttk.Label(self, text="Ingredientes de la receta:").grid(row=2, column=0) 
        self.entry2 = ttk.Entry(self, textvariable=self.ingrediente).grid(row=2, column=1, padx=10, pady=10)

        self.e3 = ttk.Label(self, text="Tiempo de preparacion:").grid(row=3, column=0) 
        self.entry3 = ttk.Entry(self, textvariable=self.tiempo_prep).grid(row=3, column=1, padx=10, pady=10)

        self.e4 = ttk.Label(self, text="Modo de preparacion:").grid(row=4, column=0) 
        self.entry4 = ttk.Entry(self, textvariable=self.prep).grid(row=4, column=1, padx=10, pady=10)

        self.e5 = ttk.Label(self, text="Tiempo de coccion:").grid(row=5, column=0) 
        self.entry5 = ttk.Entry(self, textvariable=self.tiempo_coccion).grid(row=5, column=1, padx=10, pady=10)

        self.l8 = ttk.Label(self, text="Foto de la receta").grid(row=6, column=0)
        self.filename = imagen

        if self.filename:
            try:
                imag = Image.open(self.filename)
                imag = imag.resize((250,250), Image.LANCZOS)
                imagen = ImageTk.PhotoImage(imag)
                label7 = ttk.Label(self, image = imagen)
                label7.image = imagen
                label7.grid(row = 7, column =1,columnspan=2, padx=100, pady=10)
            except Exception as e:
                print(f"Error al cargar la imagen: {e}")

        self.boton_editar = ttk.Button(self, text = "Guardar cambios", padding= 10, command=self.guardar).grid(row=8, column=0, padx=10, pady=10)        
        
    def eliminar_para_editar(self):
        """Esta función elimina previamente una receta seleccionada para editarla."""
        with open("recetas.csv", "r+", newline="") as archivo:    
                lector = csv.reader(archivo, delimiter=",")
                select = self.parent.tabla.selection()            
                item = self.parent.tabla.item(select)
                nombre=item['values'][0]
                lista=[]
                for l in lector:
                    lista.append(l)
                for r in lista:    
                    if r[0]==nombre:
                        lista.remove(r)
                for item in select:        
                    self.parent.tabla.delete(item) 

        with open("recetas.csv", "w", newline="") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerows(lista)
    def guardar(self):
        """Esta función nos guarda los datos de la receta editada y la carga nuevamente a la lista de recetas."""
        self.eliminar_para_editar()
        recetas = []
        receta = []
       
        nombre = self.nombre.get()
        ingredientes = self.ingrediente.get()
        tiempo_p = self.tiempo_prep.get()
        preparacion = self.prep.get()        
        tiempo_c = self.tiempo_coccion.get()
        creacion = self.creacion
        imagen = self.filename

        receta.append(nombre)
        receta.append(ingredientes)
        receta.append(tiempo_p)
        receta.append(preparacion)        
        receta.append(tiempo_c)        
        receta.append(creacion)
        receta.append(imagen)    
        recetas.append(receta)      

        with open("recetas.csv", "a", newline="") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerows(recetas) 
            lector = csv.reader(archivo, delimiter=",")
            self.parent.tabla.insert('', tk.END, values=receta)



         
       
        print(f"Guardados los datos: {self.nombre.get()}, {self.lista_ingredientes}, {self.prep.get()}, {self.tiempo_prep.get()}, {self.tiempo_coccion.get()}, {self.creacion}, {self.filename}" ) #momentanea
        self.parent.destroy()   # terminamos el programa al destruir la ventana ppal

        messagebox.showinfo(message="¡Receta editada y guardada con éxito!")



class Receta(ttk.Frame):
    """Representa a una receta."""
    def __init__(self, parent):
        super().__init__(parent, padding=(10))
        self.parent = parent 
        parent.title("Crear o modificar receta")
        parent.geometry("500x700")
        parent.resizable(False, False)
        parent.grab_set()      
        
                
        self.nombre = tk.StringVar()
        self.lista_ingredientes = tk.StringVar()
        self.tiempo_prep = tk.IntVar()
        self.prep = tk.StringVar()        
        self.tiempo_coccion = tk.IntVar()
        self.creacion = dt.now().strftime('%Y-%m-%d %H:%M:%S')
        self.filename = None
        

        
        ttk.Label(self, text="Nombre de la receta", padding=3).grid(row=2, column=1)
        ttk.Entry(self, textvariable=self.nombre).grid(row=2, column=2)

        ttk.Label(self, text="Lista de ingredientes", padding=10).grid(row=3, column=1)
        ttk.Entry(self, textvariable=self.lista_ingredientes).grid(row=3, column=2)

        ttk.Label(self, text="Tiempo de preparación", padding=10).grid(row=4, column=1)
        ttk.Entry(self,textvariable=self.tiempo_prep).grid(row=4, column=2)

        ttk.Label(self, text="Preparación", padding=10).grid(row=6, column=1)
        ttk.Entry(self,textvariable=self.prep).grid(row=6, column=2)     
        

        ttk.Label(self, text="Tiempo de cocción", padding=10).grid(row=7, column=1)
        ttk.Entry(self,textvariable=self.tiempo_coccion).grid(row=7, column=2)

        ttk.Label(self, text="Imagen del plato preparado", padding=10).grid(row=8, column=1)
        btn_imagen = ttk.Button(self, text="Buscar Imagen", padding=0, command= self.buscar_imagen)
        btn_imagen.grid(row=8, column=2)
        
        btn_guardar = ttk.Button(self, text="Guardar", padding=5, command=self.guardar)
        btn_guardar.grid(row=11, columnspan=3, rowspan=2)

        parent.bind('<Return>', lambda e: btn_guardar.invoke()) # para ejecutar el btn al presionar enter


    def guardar(self):
        """Funcion que guarda la receta en una lista y la covierte en un archivo CSV"""
        recetas = []
        receta = []
       
        nombre = self.nombre.get()
        ingredientes = self.lista_ingredientes.get()
        tiempo_p = self.tiempo_prep.get()
        preparacion = self.prep.get()        
        tiempo_c = self.tiempo_coccion.get()
        creacion = self.creacion
        imagen = self.filename

        receta.append(nombre)
        receta.append(ingredientes)
        receta.append(tiempo_p)
        receta.append(preparacion)        
        receta.append(tiempo_c)        
        receta.append(creacion)
        receta.append(imagen)    
        recetas.append(receta)      

        with open("recetas.csv", "a", newline="") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerows(recetas)  
            lector = csv.reader(archivo, delimiter=",")
            self.parent.tabla.insert('', tk.END, values=receta)

       
        print(f"Guardados los datos: {self.nombre.get()}, {self.lista_ingredientes.get()}, {self.prep.get()}, {self.tiempo_prep.get()}, {self.tiempo_coccion.get()}, {self.creacion}, {self.filename}" ) #momentanea           
        self.parent.destroy()   # terminamos el programa al destruir la ventana ppal
        messagebox.showinfo(message="¡Receta guardada!")

    
    def buscar_imagen(self):
        """Funcion que sirve para buscar una imagen e insertarla en la receta"""
        global img_tk
        self.filename = filedialog.askopenfilename(title="Buscar imagen", filetypes=(("Archivos .jpg", "*.jpg"),("Archivos .png", "*.png"),("Todos los archivos", "*")))

        
        img = Image.open(self.filename)
        img = img.resize((200,200), Image.LANCZOS)
        imagen = ImageTk.PhotoImage(img)
        label1 = ttk.Label(self, image = imagen)
        label1.image = imagen
        label1.grid(row=10, column=0, columnspan= 3)


        
root = tk.Tk()
App(root).grid()
root.mainloop()