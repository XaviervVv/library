# ESPAÑOL / ENGLISH
# Dependencias a descargar desde pip install: | Dependencies to install from pip install:
# - ttkbootstrap
# - mysql-connector-python
# Otras dependencias: / Other dependencies:
# - Instalar MySQL / Install MySQL
#------------------------------------------------
from tkinter import Menu, StringVar
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

import mysql.connector
from mysql.connector import Error

from time import strftime
from datetime import datetime

# Configure una variable de entorno para almacenar la contraseña
# Set an environment variable to store the password
import os
mysql_password = os.getenv('MYSQL_PASSWORD')

def conectar_base():
    try:
        conexion = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = mysql_password
        )
        cursor = conexion.cursor()
        crear_base_datos = "CREATE DATABASE IF NOT EXISTS bd_libreria"
        cursor.execute(crear_base_datos)
        cursor.close()
        conexion.close()

        conexion = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = mysql_password,
            database = 'bd_libreria'
        )

        cursor = conexion.cursor()
        crear_tabla = """
            CREATE TABLE IF NOT EXISTS libreria (
                Cod_prod INT PRIMARY KEY,
                Producto VARCHAR(100),
                Editorial VARCHAR(80),
                Precio_costo INT,
                Situacion_oferta VARCHAR(2),
                Precio_final INT
            )"""
        cursor.execute(crear_tabla)
        cursor.close()
        conexion.close()
        if language_idioma is True:
            messagebox.showinfo("Base de datos", "Conexión exitosa!")
        elif language_idioma is False:
            messagebox.showinfo("Database", "Connection successful!")
    except Error as err:
        if language_idioma is True:
            messagebox.showwarning("Error", message=f"Error al conectar a MySQL: \n\n{err}")
        elif language_idioma is False:
            messagebox.showwarning("Error", message=f"Error connecting to MySQL: \n\n{err}")

#***************************************************************
# Hacer pruebas con los errores que surjan del conector de MySQL
# Make some testing errors arising from the MySQL connector
#***************************************************************
#def errordebasededatos(error): # //////////////////// Estos eran errores de sqlite3 ////////////////////
#    error=str(error) #------------------------------- These were sqlite3 errors
#    if error=="incomplete input":
#        messagebox.showwarning("Error", message=f"Error: {error}\n\nNo deje espacios vacios o las funciones no serviran excepto la de Buscar.")
#    elif error=="no such table: Libreria":
#        messagebox.showwarning("Error", message=f"Error: {error}\n\nConecte la base de datos primero para poder usar las funciones.\n(Archivo BBDD -> Conectar)")

def salir():
    if language_idioma is True:
        valor=messagebox.askquestion("Salir", "Desea salir del programa?")
    elif language_idioma is False:
        valor=messagebox.askquestion("Exit", "Do you want to exit the program?")
    if valor=="yes":
        raiz.destroy()

def white_theme():
    raiz.style.theme_use("litera")

def grey_theme():
    raiz.style.theme_use("superhero")

def cyan_theme():
    raiz.style.theme_use("solar")

def purple_theme():
    raiz.style.theme_use("vapor")

def dark_theme():
    raiz.style.theme_use("darkly")

def black_theme():
    raiz.style.theme_use("cyborg")

def about():
    if language_idioma is True:
        messagebox.showinfo("Gracias por usar mi programa", "Hecho en Python por \nJavier Corrales\n\nContacto:\nlaboral.corrales@gmail.com")
    elif language_idioma is False:
        messagebox.showinfo("Thank you for using my program", "Made in Python by \nJavier Corrales\n\nContact:\nlaboral.corrales@gmail.com")

def buscar():
    try:
        if variableCod_Prod.get()!="":
            busqueda=0
            conexion = mysql.connector.connect(
                host ='localhost',
                user ='root',
                password = mysql_password,
                database = 'bd_libreria'
            )
            cursor = conexion.cursor()
            encontrar_b1 = (variableCod_Prod.get())
            cursor.execute("SELECT * FROM libreria WHERE Cod_prod=%s", (encontrar_b1,))
            buscar=cursor.fetchall()
            for i in buscar:
                busqueda=(i[0])
            
            if busqueda!=0:
                conexion = mysql.connector.connect(
                    host = 'localhost',
                    user = 'root',
                    password = mysql_password,
                    database = 'bd_libreria'
                )
                cursor = conexion.cursor()
                encontrar_b2 = (variableCod_Prod.get())
                cursor.execute("SELECT * FROM libreria WHERE Cod_prod=%s", (encontrar_b2,))
                mostrar=cursor.fetchall()
                for i in mostrar:
                    variableProd.set(i[1])
                    variableEditorial.set(i[2])
                    variablePrecioCosto.set(i[3])
                    variableOferta.set(i[4])
                    b_total=(i[5])
                    total_Label.config(text=f"${b_total}")
                conexion.commit()
                conexion.close()
            elif busqueda==0:
                if language_idioma is True:
                    messagebox.showwarning("Atención!","El código de producto ingresado no existe en la base de datos.")
                elif language_idioma is False:
                    messagebox.showwarning("Attention!", "The product code entered does not exist in the database.")
        elif variableCod_Prod.get()=="":
            if language_idioma is True:
                messagebox.showwarning("Espacio vacio","No dejes el espacio \"Código\" vacio si quieres encontrar algo.")
            elif language_idioma is False:
                messagebox.showwarning("Empty space", "Don't leave the \"Code\" space empty if you want to find something.")
    except Error as err:
        messagebox.showerror("Error", err)

def mostrar_total():
    global total_final
    IVA=21
    DESCUENTO=15
    precioCosto=0
    precioCosto=variablePrecioCosto.get()
    precioCosto=int(precioCosto)
    total=0
    total_c_des=0
    total_final=0
    if variableOferta.get()=="No":
        total=(precioCosto)+precioCosto*IVA//100
        total_Label.config(text=f"${total}")
        total_final=total
    elif variableOferta.get()=="Si":
        total=(precioCosto)+precioCosto*IVA//100
        total_c_des=(total)-total*DESCUENTO//100
        total_Label.config(text=f"${total_c_des}")
        total_final=total_c_des

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# Quita espacios de más del texto introducido por interfaz antes de guardar en base de datos
# Removes extra spaces from text entered by interface before saving to database
def elimina_espacios(texto):
    start = fin = 0
    nuevo = ''
    for start in range(len(texto)):
        if texto[start] != ' ':
            break
    
    for fin in range(len(texto) - 1, 0, -1):
        if texto[fin] != ' ':
            break
    
    if start != fin:
        nuevo = [texto[i] for i in range(start, fin + 1) if texto[i] != ' ' or texto[i-1] != ' ']
    return ''.join(nuevo)
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

lista_x=[]
def calcular():
    global total_final
    try:
        if variableCod_Prod.get()=="" or variableProd.get()=="" or variableEditorial.get()=="" or variablePrecioCosto.get()=="":
            if language_idioma is True:
                messagebox.showwarning("Atención!", "No deje ningún espacio vacio!")
            elif language_idioma is False:
                messagebox.showwarning("Attention!", "Don't leave any empty space!")
        elif variableCod_Prod.get()!="" and variableProd.get()!="" and variableEditorial.get()!="" and variablePrecioCosto.get()!="":
            if variableCod_Prod.get().isdigit()==True and variablePrecioCosto.get().isdigit()==True:
                # isspace() True si todos los caracteres de la cadena son espacios en blanco / True if all characters in the string are whitespace
                # isspace() False si la cadena tiene 1 o más caracteres que no son espacios en blanco / False if the string has 1 or more non-whitespace characters
                if all(variableProd.get().isalnum() and variableEditorial.get().isalnum() or variableProd.get().isspace()==False for i in variableProd.get() or variableEditorial.get().isspace()==False for j in variableEditorial.get()):

                    mostrar_total()
                    if language_idioma is True:
                        valor_ag=messagebox.askquestion("Guardar", "Desea guardar?")
                    elif language_idioma is False:
                        valor_ag=messagebox.askquestion("Save", "Do you want to save?")
                    if valor_ag=="yes":
                        comp=0
                        
                        conexion = mysql.connector.connect(
                            host = 'localhost',
                            user = 'root',
                            password = mysql_password,
                            database = 'bd_libreria'
                        )
                        cursor = conexion.cursor()
                        encontrar_ci=(variableCod_Prod.get())
                        cursor.execute("SELECT * FROM libreria WHERE Cod_prod=%s", (encontrar_ci,))
                        comparar=cursor.fetchall()
                        for i in comparar:
                            comp=(i[0])
                        
                        if comp==0:
                            e_prod=variableProd.get()
                            e_edit=variableEditorial.get()
                            if len(e_prod) > 1:
                                s_prod=elimina_espacios(e_prod)
                                prod = s_prod
                            elif len(e_prod) == 1:
                                prod = e_prod
                            if len(e_edit) > 1:
                                s_edit=elimina_espacios(e_edit)
                                edit = s_edit
                            elif len(e_edit) == 1:
                                edit = e_edit
                            lista_x.append(variableCod_Prod.get())
                            lista_x.append(prod)
                            lista_x.append(edit)
                            lista_x.append(variablePrecioCosto.get())
                            lista_x.append(variableOferta.get())
                            lista_x.append(total_final)
                            lista_cg=lista_x[0],lista_x[1],lista_x[2],lista_x[3],lista_x[4],lista_x[5]
                            
                            conexion = mysql.connector.connect(
                                host = 'localhost',
                                user = 'root',
                                password = mysql_password,
                                database = 'bd_libreria'
                            )
                            cursor = conexion.cursor()
                            cursor.execute("INSERT INTO libreria (Cod_prod,Producto,Editorial,Precio_costo,Situacion_oferta,Precio_final) VALUES (%s,%s,%s,%s,%s,%s)", lista_cg)
                            conexion.commit()
                            conexion.close()
                            if language_idioma is True:
                                messagebox.showinfo("Guardado!", message=f"{prod} guardado con exito!")
                            elif language_idioma is False:
                                messagebox.showinfo("Saved!", message=f"{prod} saved successfully!")
                        elif comp!=0:
                            if language_idioma is True:
                                messagebox.showwarning("Atención!", "Este código de producto ya fue guardado anteriormente.\nIngrese otro")
                            elif language_idioma is False:
                                messagebox.showwarning("Attention!", "This product code has already been saved previously.\nEnter another.")
                            conexion.rollback()
                    elif valor_ag=="no":
                        pass
            elif variableCod_Prod.get().isdigit()==False or variablePrecioCosto.get().isdigit()==False:
                if language_idioma is True:
                    messagebox.showwarning("Aviso!", "Los espacios de Código y Precio no pueden contener letras, revise los datos ingresados.")
                elif language_idioma is False:
                    messagebox.showwarning("Warning!", "The Code and Price spaces cannot contain letters, please check the data entered.")
    except Error as err:
        messagebox.showwarning("Error", err)
        conexion.rollback()

def actualizar():
    global total_final
    try:
        if variableCod_Prod.get()=="" or variableProd.get()=="" or variableEditorial.get()=="" or variablePrecioCosto.get()=="":
            if language_idioma is True:
                messagebox.showwarning("Atención!", "No deje ningún espacio vacio!")
            elif language_idioma is False:
                messagebox.showwarning("Attention!", "Don't leave any empty space!")
        elif variableCod_Prod.get()!="" and variableProd.get()!="" and variableEditorial.get()!="" and variablePrecioCosto.get()!="":
            if variableCod_Prod.get().isdigit()==True and variablePrecioCosto.get().isdigit()==True:
                # isspace() True si todos los caracteres de la cadena son espacios en blanco / True if all characters in the string are whitespace
                # isspace() False si la cadena tiene 1 o más caracteres que no son espacios en blanco / False if the string has 1 or more non-whitespace characters
                if all(variableProd.get().isalnum() and variableEditorial.get().isalnum() or variableProd.get().isspace()==False for i in variableProd.get() or variableEditorial.get().isspace()==False for j in variableEditorial.get()):

                    mostrar_total()
                    if language_idioma is True:
                        valor_ac=messagebox.askquestion("Actualizar", "Desea actualizar?")
                    elif language_idioma is False:
                        valor_ac=messagebox.askquestion("Update", "Do you want to update?")
                    if valor_ac=="yes":
                        n_actualizar=0
                        conexion = mysql.connector.connect(
                            host = 'localhost',
                            user = 'root',
                            password = mysql_password,
                            database = 'bd_libreria'
                        )
                        cursor = conexion.cursor()
                        encontrar_ac_1 = (variableCod_Prod.get())
                        cursor.execute("SELECT * FROM libreria WHERE Cod_prod=%s", (encontrar_ac_1,))
                        b_actualizar=cursor.fetchall()
                        for i in b_actualizar:
                            n_actualizar=(i[0])
                        
                        if n_actualizar!=0:
                            e_prod=variableProd.get()
                            e_edit=variableEditorial.get()
                            if len(e_prod) > 1:
                                s_prod=elimina_espacios(e_prod)
                                prod = s_prod
                            elif len(e_prod) == 1:
                                prod = e_prod
                            if len(e_edit) > 1:
                                s_edit=elimina_espacios(e_edit)
                                edit = s_edit
                            elif len(e_edit) == 1:
                                edit = e_edit
                            conexion = mysql.connector.connect(
                                host = 'localhost',
                                user = 'root',
                                password = mysql_password,
                                database = 'bd_libreria'
                            )
                            cursor = conexion.cursor()
                            sql = """UPDATE libreria
                                SET Producto=%s,Editorial=%s,Precio_costo=%s,Situacion_oferta=%s,Precio_final=%s
                                WHERE Cod_prod=%s"""
                            cursor.execute(sql, (prod,edit,variablePrecioCosto.get(),variableOferta.get(),total_final,variableCod_Prod.get()))
                            conexion.commit()
                            conexion.close()
                            if language_idioma is True:
                                messagebox.showinfo("Actualizado!", message=f"{prod} actualizado con exito!")
                            elif language_idioma is False:
                                messagebox.showinfo("Updated!", message=f"{prod} updated successfully!")
                        elif n_actualizar==0:
                            if language_idioma is True:
                                messagebox.showwarning("Atención!", "El registro no existe, ingrese un código de producto existente\npara poder actualizar.")
                            elif language_idioma is False:
                                messagebox.showwarning("Attention!", "The record does not exist, please enter an existing product code to update.")
                    elif valor_ac=="no":
                        pass
            elif variableCod_Prod.get().isdigit()==False or variablePrecioCosto.get().isdigit()==False:
                if language_idioma is True:
                    messagebox.showwarning("Aviso!", "Los espacios de Código y Precio no pueden contener letras, revise los datos ingresados.")
                elif language_idioma is False:
                    messagebox.showwarning("Warning!", "The Code and Price spaces cannot contain letters, please check the data entered.")
    except Error as err:
        messagebox.showwarning("Error", err)
        conexion.rollback()

def limpiar():
    variableCod_Prod.set("")
    variableProd.set("")
    variableEditorial.set("")
    variablePrecioCosto.set("")
    variableOferta.set("No")
    total_Label.config(text="")

def eliminar():
    try:
        eliminar=0
        conexion = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = mysql_password,
            database = 'bd_libreria'
        )
        cursor = conexion.cursor()
        encontrar_el_1 = (variableCod_Prod.get())
        cursor.execute("SELECT * FROM libreria WHERE Cod_prod=%s", (encontrar_el_1,))
        b_eliminar = cursor.fetchall()
        for i in b_eliminar:
            eliminar=(i[0])
        conexion.commit()

        if eliminar!=0:
            if language_idioma is True:
                e=messagebox.askquestion("Eliminar", "Esta seguro que quiere borrar este artículo?")
            elif language_idioma is False:
                e=messagebox.askquestion("Eliminate", "Are you sure you want to delete this article?")
            if e=="yes":
                conexion = mysql.connector.connect(
                    host = 'localhost',
                    user = 'root',
                    password = mysql_password,
                    database = 'bd_libreria'
                )
                cursor = conexion.cursor()
                encontrar_el_2 = (variableCod_Prod.get())
                cursor.execute("DELETE FROM libreria WHERE Cod_prod=%s", (encontrar_el_2,))
                conexion.commit()
                conexion.close()
                if language_idioma is True:
                    messagebox.showinfo("Eliminado", "Registro borrado con exito!")
                elif language_idioma is False:
                    messagebox.showinfo("Deleted", "Registration deleted successfully!")
            elif e=="no":
                pass
        elif eliminar==0:
            if language_idioma is True:
                messagebox.showwarning("Aviso!", "Registro no existente o ya borrado.")
            elif language_idioma is False:
                messagebox.showwarning("Warning!", "Record does not exist or has already been deleted.")
    except Error as err:
        messagebox.showwarning("Error", err)
        conexion.rollback()

def dest():
    global titulo
    #-------
    global lf_codigo
    global cod_p_Entry
    global lf_libro
    global nom_prod_Entry
    global lf_editorial
    global editorial_Entry
    global lf_pre_cos
    global pre_cos_Entry
    #-------
    global lf_botones
    global boton_buscar
    global boton_limpiar
    global boton_actualizar
    global boton_eliminar
    #-------
    global lf_oferta
    global ofertaSi
    global ofertaNo
    #-------
    global hint
    global boton_calcular
    #-------
    global lineademenu
    global accesoBD
    global tema
    global idioma
    global acercaDe
    #-------
    titulo.destroy()
    #-------
    lf_codigo.destroy()
    cod_p_Entry.destroy()
    lf_libro.destroy()
    nom_prod_Entry.destroy()
    lf_editorial.destroy()
    editorial_Entry.destroy()
    lf_pre_cos.destroy()
    pre_cos_Entry.destroy()
    #-------
    lf_botones.destroy()
    boton_buscar.destroy()
    boton_limpiar.destroy()
    boton_actualizar.destroy()
    boton_eliminar.destroy()
    #-------
    lf_oferta.destroy()
    ofertaSi.destroy()
    ofertaNo.destroy()
    #-------
    hint.destroy()
    boton_calcular.destroy()
    #-------
    lineademenu.destroy()
    accesoBD.destroy()
    tema.destroy()
    idioma.destroy()
    acercaDe.destroy()

# Cambiar idioma / Change language
global language_idioma
language_idioma = True
def esp(): # ////////////////////////// Destruir los widgets y rehacerlos en el idioma seleccionado
    global language_idioma
    language_idioma = True
    global titulo
    #-------
    global lf_codigo
    global cod_p_Entry
    global lf_libro
    global nom_prod_Entry
    global lf_editorial
    global editorial_Entry
    global lf_pre_cos
    global pre_cos_Entry
    #-------
    global lf_botones
    global boton_buscar
    global boton_limpiar
    global boton_actualizar
    global boton_eliminar
    #-------
    global lf_oferta
    global ofertaSi
    global ofertaNo
    #-------
    global hint
    global boton_calcular
    #-------
    global lineademenu
    global accesoBD
    global tema
    global idioma
    global acercaDe
    #-------
    dest()
    #-------
    titulo=ttk.Label(raiz, text="Libreria Genim")
    titulo.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
    titulo.config(font=("Comic Sans MS", 14))

    lf_codigo = ttk.LabelFrame(raiz, text="Código")
    lf_codigo.grid(row=2, column=0, padx=20, pady=2, sticky="nwse")
    cod_p_Entry=ttk.Entry(lf_codigo, textvariable=variableCod_Prod, bootstyle="success")
    cod_p_Entry.grid(row=2, column=0, padx=10, pady=8)

    lf_libro = ttk.LabelFrame(raiz, text="Libro")
    lf_libro.grid(row=3, column=0, padx=20, pady=2, sticky="nwse")
    nom_prod_Entry=ttk.Entry(lf_libro, textvariable=variableProd, bootstyle="info")
    nom_prod_Entry.grid(row=3, column=0, padx=10, pady=8)

    lf_editorial = ttk.LabelFrame(raiz, text="Editorial")
    lf_editorial.grid(row=4, column=0, padx=20, pady=2, sticky="nwse")
    editorial_Entry=ttk.Entry(lf_editorial, textvariable=variableEditorial, bootstyle="info")
    editorial_Entry.grid(row=4, column=0, padx=10, pady=8)

    lf_pre_cos = ttk.LabelFrame(raiz, text="Precio")
    lf_pre_cos.grid(row=5, column=0, padx=20, pady=2, sticky="nwse")
    pre_cos_Entry=ttk.Entry(lf_pre_cos, textvariable=variablePrecioCosto, bootstyle="info")
    pre_cos_Entry.grid(row=5, column=0, padx=10, pady=8)
    #-------
    lf_botones = ttk.LabelFrame(raiz, text="Operaciones")
    lf_botones.grid(row=2, rowspan=4, column=1, padx=15, pady=2, sticky="nwse")

    boton_buscar=ttk.Button(lf_botones, text="Buscar", command=buscar, bootstyle="success-outline")
    boton_buscar.grid(row=2, column=1, padx=10, pady=15, sticky="we")
    boton_buscar.configure(cursor="hand2")

    boton_limpiar=ttk.Button(lf_botones, text="Limpiar", command=limpiar, bootstyle="secondary")
    boton_limpiar.grid(row=3, column=1, padx=10, pady=15, sticky="we")
    boton_limpiar.configure(cursor="hand2")

    boton_actualizar=ttk.Button(lf_botones, text="Actualizar", command=actualizar, bootstyle="warning")
    boton_actualizar.grid(row=4, column=1, padx=10, pady=15, sticky="we")
    boton_actualizar.configure(cursor="hand2")

    boton_eliminar=ttk.Button(lf_botones, text="Eliminar", command=eliminar, bootstyle="danger")
    boton_eliminar.grid(row=5, column=1, padx=10, pady=15, sticky="we")
    boton_eliminar.configure(cursor="hand2")
    #-------
    lf_oferta = ttk.LabelFrame(raiz, text="En Oferta? (Descuento del 15%)")
    lf_oferta.grid(row=6, column=0, columnspan=2, padx=10, pady=15)

    variableOferta=StringVar(value="No")
    ofertaSi=ttk.Radiobutton(lf_oferta, text="Si", variable=variableOferta, value="Si", bootstyle="light")
    ofertaSi.grid(row=6, column=0, padx=30, pady=8)
    ofertaNo=ttk.Radiobutton(lf_oferta, text="No", variable=variableOferta, value="No", bootstyle="light")
    ofertaNo.grid(row=6, column=1, padx=30, pady=8)
    #-------
    hint=ttk.Label(raiz, text="El botón Calcular tambien sirve para guardar")
    hint.grid(row=7, column=0, columnspan=2, padx=5, pady=5)
    hint.config(font=("Comic Sans MS", 9), foreground="gray") # gray77

    boton_calcular=ttk.Button(raiz, text="Calcular", command=calcular, bootstyle="success-outline")
    boton_calcular.grid(row=8, column=0, columnspan=2, padx=5, pady=10, ipadx=40, ipady=10)
    boton_calcular.configure(cursor="hand2")

    lf_total = ttk.LabelFrame(raiz, text="Total")
    lf_total.grid(row=9, column=0, columnspan=2, padx=15, pady=15, sticky="we")

    total_Label=ttk.Label(lf_total, text="")
    total_Label.grid(row=8, column=0, columnspan=2, padx=10, pady=8)
    total_Label.configure(font=("Comic Sans MS", 12))
    #-------
    lineademenu=Menu(raiz)
    raiz.config(menu=lineademenu, width=300, height=300)

    accesoBD=Menu(lineademenu, tearoff=0)
    accesoBD.add_command(label="Archivo BBDD", command=conectar_base)
    accesoBD.add_command(label="Salir", command=salir)

    tema=Menu(lineademenu, tearoff=0)
    tema.add_command(label="Claro", command=white_theme)
    tema.add_command(label="Gris", command=grey_theme)
    tema.add_command(label="Cian", command=cyan_theme)
    tema.add_command(label="Purpura", command=purple_theme)
    tema.add_command(label="Oscuro", command=dark_theme)
    tema.add_command(label="Negro", command=black_theme)

    idioma=Menu(lineademenu, tearoff=0)
    idioma.add_command(label="Español", command=esp)
    idioma.add_command(label="English", command=eng)

    acercaDe=Menu(lineademenu, tearoff=0)
    acercaDe.add_command(label="...quien lo programo", command=about)

    lineademenu.add_cascade(label="Conectar", menu=accesoBD)
    lineademenu.add_cascade(label="Tema", menu=tema)
    lineademenu.add_cascade(label="Idioma", menu=idioma)
    lineademenu.add_cascade(label="Acerca de...", menu=acercaDe)

def eng(): # ////////////////////////// Destroy widgets and remake them in the selected language
    global language_idioma
    language_idioma = False
    global titulo
    #-------
    global lf_codigo
    global cod_p_Entry
    global lf_libro
    global nom_prod_Entry
    global lf_editorial
    global editorial_Entry
    global lf_pre_cos
    global pre_cos_Entry
    #-------
    global lf_botones
    global boton_buscar
    global boton_limpiar
    global boton_actualizar
    global boton_eliminar
    #-------
    global lf_oferta
    global ofertaSi
    global ofertaNo
    #-------
    global hint
    global boton_calcular
    #-------
    global lineademenu
    global accesoBD
    global tema
    global idioma
    global acercaDe
    #-------
    dest()
    #-------
    titulo=ttk.Label(raiz, text="Genim Bookstore")
    titulo.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
    titulo.config(font=("Comic Sans MS", 14))

    lf_codigo = ttk.LabelFrame(raiz, text="Code")
    lf_codigo.grid(row=2, column=0, padx=20, pady=2, sticky="nwse")
    cod_p_Entry=ttk.Entry(lf_codigo, textvariable=variableCod_Prod, bootstyle="success")
    cod_p_Entry.grid(row=2, column=0, padx=10, pady=8)

    lf_libro = ttk.LabelFrame(raiz, text="Book")
    lf_libro.grid(row=3, column=0, padx=20, pady=2, sticky="nwse")
    nom_prod_Entry=ttk.Entry(lf_libro, textvariable=variableProd, bootstyle="info")
    nom_prod_Entry.grid(row=3, column=0, padx=10, pady=8)

    lf_editorial = ttk.LabelFrame(raiz, text="Editorial")
    lf_editorial.grid(row=4, column=0, padx=20, pady=2, sticky="nwse")
    editorial_Entry=ttk.Entry(lf_editorial, textvariable=variableEditorial, bootstyle="info")
    editorial_Entry.grid(row=4, column=0, padx=10, pady=8)

    lf_pre_cos = ttk.LabelFrame(raiz, text="Price")
    lf_pre_cos.grid(row=5, column=0, padx=20, pady=2, sticky="nwse")
    pre_cos_Entry=ttk.Entry(lf_pre_cos, textvariable=variablePrecioCosto, bootstyle="info")
    pre_cos_Entry.grid(row=5, column=0, padx=10, pady=8)
    #-------
    lf_botones = ttk.LabelFrame(raiz, text="Operations")
    lf_botones.grid(row=2, rowspan=4, column=1, padx=15, pady=2, sticky="nwse")

    boton_buscar=ttk.Button(lf_botones, text="Search", command=buscar, bootstyle="success-outline")
    boton_buscar.grid(row=2, column=1, padx=10, pady=15, sticky="we")
    boton_buscar.configure(cursor="hand2")

    boton_limpiar=ttk.Button(lf_botones, text="Clean", command=limpiar, bootstyle="secondary")
    boton_limpiar.grid(row=3, column=1, padx=10, pady=15, sticky="we")
    boton_limpiar.configure(cursor="hand2")

    boton_actualizar=ttk.Button(lf_botones, text="Update", command=actualizar, bootstyle="warning")
    boton_actualizar.grid(row=4, column=1, padx=10, pady=15, sticky="we")
    boton_actualizar.configure(cursor="hand2")

    boton_eliminar=ttk.Button(lf_botones, text="Eliminate", command=eliminar, bootstyle="danger")
    boton_eliminar.grid(row=5, column=1, padx=10, pady=15, sticky="we")
    boton_eliminar.configure(cursor="hand2")
    #-------
    lf_oferta = ttk.LabelFrame(raiz, text="On Sale? (15% off)")
    lf_oferta.grid(row=6, column=0, columnspan=2, padx=10, pady=15)

    variableOferta=StringVar(value="No")
    ofertaSi=ttk.Radiobutton(lf_oferta, text="Yes", variable=variableOferta, value="Yes", bootstyle="light")
    ofertaSi.grid(row=6, column=0, padx=30, pady=8)
    ofertaNo=ttk.Radiobutton(lf_oferta, text="No", variable=variableOferta, value="No", bootstyle="light")
    ofertaNo.grid(row=6, column=1, padx=30, pady=8)
    #-------
    hint=ttk.Label(raiz, text="The Calculate button also serves to save")
    hint.grid(row=7, column=0, columnspan=2, padx=5, pady=5)
    hint.config(font=("Comic Sans MS", 9), foreground="gray") # gray77

    boton_calcular=ttk.Button(raiz, text="Calculate", command=calcular, bootstyle="success-outline")
    boton_calcular.grid(row=8, column=0, columnspan=2, padx=5, pady=10, ipadx=40, ipady=10)
    boton_calcular.configure(cursor="hand2")

    lf_total = ttk.LabelFrame(raiz, text="Total")
    lf_total.grid(row=9, column=0, columnspan=2, padx=15, pady=15, sticky="we")

    total_Label=ttk.Label(lf_total, text="")
    total_Label.grid(row=8, column=0, columnspan=2, padx=10, pady=8)
    total_Label.configure(font=("Comic Sans MS", 12))
    #-------
    lineademenu=Menu(raiz)
    raiz.config(menu=lineademenu, width=300, height=300)

    accesoBD=Menu(lineademenu, tearoff=0)
    accesoBD.add_command(label="Database File", command=conectar_base)
    accesoBD.add_command(label="Exit", command=salir)

    tema=Menu(lineademenu, tearoff=0)
    tema.add_command(label="Clear", command=white_theme)
    tema.add_command(label="Grey", command=grey_theme)
    tema.add_command(label="Cyan", command=cyan_theme)
    tema.add_command(label="Purple", command=purple_theme)
    tema.add_command(label="Dark", command=dark_theme)
    tema.add_command(label="Black", command=black_theme)

    idioma=Menu(lineademenu, tearoff=0)
    idioma.add_command(label="Español", command=esp)
    idioma.add_command(label="English", command=eng)

    acercaDe=Menu(lineademenu, tearoff=0)
    acercaDe.add_command(label="...who programmed it", command=about)

    lineademenu.add_cascade(label="Connect", menu=accesoBD)
    lineademenu.add_cascade(label="Theme", menu=tema)
    lineademenu.add_cascade(label="Language", menu=idioma)
    lineademenu.add_cascade(label="About...", menu=acercaDe)

raiz = ttk.Window(themename="darkly")
raiz.title("Libreria")
raiz.eval('tk::PlaceWindow . center')
raiz.resizable(False, False)

def time_hora():
    now=datetime.now()
    string=now.strftime('%I:%M %p <--')
    hora_label.config(text=string)
    fecha_str=now.strftime('--> %d/%m/%Y')
    fecha_label.config(text=fecha_str)
    hora_label.after(1000, time_hora)

variableCod_Prod=StringVar()
variableProd=StringVar()
variableEditorial=StringVar()
variablePrecioCosto=StringVar()

hora_label=ttk.Label(raiz)
hora_label.grid(row=0, column=1, columnspan=2, sticky="e")

fecha_label=ttk.Label(raiz)
fecha_label.grid(row=0, column=0, columnspan=2, sticky="w")

global titulo
titulo=ttk.Label(raiz, text="Libreria Genim")
titulo.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
titulo.config(font=("Comic Sans MS", 14))

# Entradas - Entries ////////////////////////////////////////////////////////////////////////////////////////////
global lf_codigo
global cod_p_Entry
global lf_libro
global nom_prod_Entry
global lf_editorial
global editorial_Entry
global lf_pre_cos
global pre_cos_Entry
#-------
lf_codigo = ttk.LabelFrame(raiz, text="Código")
lf_codigo.grid(row=2, column=0, padx=20, pady=2, sticky="nwse")
cod_p_Entry=ttk.Entry(lf_codigo, textvariable=variableCod_Prod, bootstyle="success")
cod_p_Entry.grid(row=2, column=0, padx=10, pady=8)

lf_libro = ttk.LabelFrame(raiz, text="Libro")
lf_libro.grid(row=3, column=0, padx=20, pady=2, sticky="nwse")
nom_prod_Entry=ttk.Entry(lf_libro, textvariable=variableProd, bootstyle="info")
nom_prod_Entry.grid(row=3, column=0, padx=10, pady=8)

lf_editorial = ttk.LabelFrame(raiz, text="Editorial")
lf_editorial.grid(row=4, column=0, padx=20, pady=2, sticky="nwse")
editorial_Entry=ttk.Entry(lf_editorial, textvariable=variableEditorial, bootstyle="info")
editorial_Entry.grid(row=4, column=0, padx=10, pady=8)

lf_pre_cos = ttk.LabelFrame(raiz, text="Precio")
lf_pre_cos.grid(row=5, column=0, padx=20, pady=2, sticky="nwse")
pre_cos_Entry=ttk.Entry(lf_pre_cos, textvariable=variablePrecioCosto, bootstyle="info")
pre_cos_Entry.grid(row=5, column=0, padx=10, pady=8)
# Entradas - Entries ////////////////////////////////////////////////////////////////////////////////////////////

# Label Frame de Botones //////////////////////////////////////////////////////////////////////////////
global lf_botones
global boton_buscar
global boton_limpiar
global boton_actualizar
global boton_eliminar
#-------
lf_botones = ttk.LabelFrame(raiz, text="Operaciones")
lf_botones.grid(row=2, rowspan=4, column=1, padx=15, pady=2, sticky="nwse")

boton_buscar=ttk.Button(lf_botones, text="Buscar", command=buscar, bootstyle="success-outline")
boton_buscar.grid(row=2, column=1, padx=10, pady=15, sticky="we")
boton_buscar.configure(cursor="hand2")

boton_limpiar=ttk.Button(lf_botones, text="Limpiar", command=limpiar, bootstyle="secondary")
boton_limpiar.grid(row=3, column=1, padx=10, pady=15, sticky="we")
boton_limpiar.configure(cursor="hand2")

boton_actualizar=ttk.Button(lf_botones, text="Actualizar", command=actualizar, bootstyle="warning")
boton_actualizar.grid(row=4, column=1, padx=10, pady=15, sticky="we")
boton_actualizar.configure(cursor="hand2")

boton_eliminar=ttk.Button(lf_botones, text="Eliminar", command=eliminar, bootstyle="danger")
boton_eliminar.grid(row=5, column=1, padx=10, pady=15, sticky="we")
boton_eliminar.configure(cursor="hand2")
# Label Frame de Botones //////////////////////////////////////////////////////////////////////////////

#----------------------------------------------------------------------------------------------------///>>
global lf_oferta
global ofertaSi
global ofertaNo
#-------
lf_oferta = ttk.LabelFrame(raiz, text="En Oferta? (Descuento del 15%)")
lf_oferta.grid(row=6, column=0, columnspan=2, padx=10, pady=15)

variableOferta=StringVar(value="No")
ofertaSi=ttk.Radiobutton(lf_oferta, text="Si", variable=variableOferta, value="Si", bootstyle="light")
ofertaSi.grid(row=6, column=0, padx=30, pady=8)
ofertaNo=ttk.Radiobutton(lf_oferta, text="No", variable=variableOferta, value="No", bootstyle="light")
ofertaNo.grid(row=6, column=1, padx=30, pady=8)
#----------------------------------------------------------------------------------------------------///>>
global hint
global boton_calcular
#-------
hint=ttk.Label(raiz, text="El botón Calcular tambien sirve para guardar")
hint.grid(row=7, column=0, columnspan=2, padx=5, pady=5)
hint.config(font=("Comic Sans MS", 9), foreground="gray") # gray77

boton_calcular=ttk.Button(raiz, text="Calcular", command=calcular, bootstyle="success-outline")
boton_calcular.grid(row=8, column=0, columnspan=2, padx=5, pady=10, ipadx=40, ipady=10)
boton_calcular.configure(cursor="hand2")

lf_total = ttk.LabelFrame(raiz, text="Total")
lf_total.grid(row=9, column=0, columnspan=2, padx=15, pady=15, sticky="we")

total_Label=ttk.Label(lf_total, text="")
total_Label.grid(row=8, column=0, columnspan=2, padx=10, pady=8)
total_Label.configure(font=("Comic Sans MS", 12))

#///////////////////////////////////////////////////////////////
# Barra de opciones - Options bar
global lineademenu
global accesoBD
global tema
global idioma
global acercaDe
#-------
lineademenu=Menu(raiz)
raiz.config(menu=lineademenu, width=300, height=300)

accesoBD=Menu(lineademenu, tearoff=0)
accesoBD.add_command(label="Archivo BBDD", command=conectar_base)
accesoBD.add_command(label="Salir", command=salir)

tema=Menu(lineademenu, tearoff=0)
tema.add_command(label="Claro", command=white_theme)
tema.add_command(label="Gris", command=grey_theme)
tema.add_command(label="Cian", command=cyan_theme)
tema.add_command(label="Purpura", command=purple_theme)
tema.add_command(label="Oscuro", command=dark_theme)
tema.add_command(label="Negro", command=black_theme)

idioma=Menu(lineademenu, tearoff=0)
idioma.add_command(label="Español", command=esp)
idioma.add_command(label="English", command=eng)

acercaDe=Menu(lineademenu, tearoff=0)
acercaDe.add_command(label="...quien lo programo", command=about)

lineademenu.add_cascade(label="Conectar", menu=accesoBD)
lineademenu.add_cascade(label="Tema", menu=tema)
lineademenu.add_cascade(label="Idioma", menu=idioma)
lineademenu.add_cascade(label="Acerca de...", menu=acercaDe)
#///////////////////////////////////////////////////////////////

time_hora()
raiz.mainloop()
