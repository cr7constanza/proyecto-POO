import tkinter as tk #Biblioteca para crear interfaces gráficas en Python.
from tkinter import messagebox, StringVar #Para mostrar mensajes emergentes como alertas o confirmaciones.

#Clase de tkinterpara manejar variables de texto en la interfaz.
import smtplib #Para enviar correos electrónicos utilizando el protocolo SMTP.

#Para construir mensajes de correo con texto y múltiples partes.
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Usuario: #se crea clase llamada usuario 
    def __init__(self, nombre, correo, clave):
        #contiene 3 atributos
        self.nombre = nombre #Nombre del usuario
        self.correo = correo #Dirección de correo del usuario
        self.clave = clave #Contraseña para autenticación


class Auto:#se crea clase auto
    def __init__(self, nombre, precio):
        #contiene 3 atributos
        self.nombre = nombre #Nombre o modelo del auto
        self.precio = precio #Precio por día del auto
        self.dias = 1 #Días de alquiler (inicialmente 1)
   
    #Calcula el costo total del auto según los días de alquiler.
    def precio_total(self):
        return self.precio * self.dias

#se crea clase canasta 
#Representa la canasta de autos seleccionados para alquilar
class Canasta:
    def __init__(self):
        self.autos = [] ## Lista para almacenar autos seleccionados

    #Agregue un auto a la lista si no está ya en la canasta.
    def agregar(self, auto):
        if auto not in self.autos:
            self.autos.append(auto)
            
    #Elimina un auto de la lista si está presente.
    def eliminar(self, auto):
        if auto in self.autos:
            self.autos.remove(auto)
    #Calcula el costo total de los autos en la canasta.
    def total(self):
        return sum(auto.precio_total() for auto in self.autos)

#se crea clase pago
#Maneja el proceso de pago y envío de correo.
class Pago:
    def __init__(self, destinatario):
        self.destinatario = destinatario #Dirección de correo del receptor del pago.

    #Define el remitente y su contraseña.
    def enviar_correo(self):
        remitente = "rent.auto.lagos@gmail.com"
        contraseña_empresarial = "ceyo gmel xnum zjwf"
     
       #Construye un mensaje de correo electrónico con título y cuerpo.
        mensaje = MIMEMultipart()
        mensaje["From"] = remitente
        mensaje["To"] = self.destinatario
        mensaje["Subject"] = 'Pago RentAuto'
        mensaje.attach(MIMEText("Estimado, el pago ha sido realizado con éxito.", 'plain'))
       
        #Envía el correo utilizando el servidor de Gmail y maneja errores.
        try:
            servicio = smtplib.SMTP('smtp.gmail.com', 587)
            servicio.starttls()  # coneccion segura
            servicio.login(remitente, contraseña_empresarial)
            servicio.sendmail(remitente, self.destinatario, mensaje.as_string())
            servicio.quit()
            print("Correo enviado exitosamente")
        except Exception as e:
            print(f"Hubo un error al enviar el correo: {e}")

#se crea clase interfazusuario
class InterfazUsuario:
    #Defina la interfaz gráfica y variables principales para manejar
    # usuarios, autos y canasta.
    def __init__(self, root):
        self.root = root
        self.canasta = Canasta()
        self.usuarios = {}  # Diccionario para almacenar usuarios
        self.usuario_actual = None  # Usuario logueado
        self.autos_disponibles = [
            Auto("Nissan X-Trail", 14000),
            Auto("Toyota Hilux", 24000),
            Auto("Nissan Versa", 17000),
            Auto("Mitsubishi L200", 18000),
            Auto("Peugeot 208", 15000),
            Auto("Hyundai Accent RB", 12000),
            Auto("Chevrolet Sail", 28000),
            Auto("Ford F-150 Raptor", 50000),
        ]
        self.inicializar_interfaz()
    #Elimina todos los elementos visibles en la ventana para redibujarla.
    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    #Muestra la pantalla principal con opciones de inicio de sesión y registro.
    def inicializar_interfaz(self):
        self.limpiar_ventana()
        tk.Label(self.root, text="Sistema de Autos", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="Iniciar Sesión", command=self.mostrar_login).pack(pady=5)
        tk.Button(self.root, text="Registrarse", command=self.mostrar_registro).pack(pady=5)
    
    #Pantalla para que el usuario inicie sesión.
    def mostrar_login(self):
        self.limpiar_ventana()
        tk.Label(self.root, text="Login").pack(pady=10)

        usuario_var = StringVar()
        clave_var = StringVar()
        correo_var = StringVar()

        tk.Label(self.root, text="Usuario:").pack()
        tk.Entry(self.root, textvariable=usuario_var).pack()

        tk.Label(self.root, text="Contraseña:").pack()
        tk.Entry(self.root, textvariable=clave_var).pack()

        tk.Label(self.root, text="Correo:").pack()
        tk.Entry(self.root, textvariable=correo_var).pack()

        def verificar_login():
            usuario = usuario_var.get()
            clave = clave_var.get()
            correo = correo_var.get()

            if not usuario or not clave or not correo:
                messagebox.showerror("Error", "Por favor complete todos los campos.")
                return

            if usuario in self.usuarios:
                usuario_obj = self.usuarios[usuario]
                if usuario_obj.clave == clave and usuario_obj.correo == correo:
                    self.usuario_actual = usuario_obj
                    self.mostrar_pantalla_principal()
                else:
                    messagebox.showerror("Error", "Credenciales incorrectas.")
            else:
                messagebox.showerror("Error", "Usuario no encontrado.")

        tk.Button(self.root, text="Iniciar Sesión", command=verificar_login).pack(pady=10)
        tk.Button(self.root, text="Cancelar", command=self.inicializar_interfaz).pack(pady=5)
    # Pantalla para registrar nuevos usuarios.
    def mostrar_registro(self):
        self.limpiar_ventana()
        tk.Label(self.root, text="Registro").pack(pady=10)

        usuario_var = StringVar()
        clave_var = StringVar()
        correo_var = StringVar()
    
        tk.Label(self.root, text="Usuario:").pack()
        tk.Entry(self.root, textvariable=usuario_var).pack()

        tk.Label(self.root, text="Contraseña:").pack()
        tk.Entry(self.root, textvariable=clave_var).pack()

        tk.Label(self.root, text="Correo:").pack()
        tk.Entry(self.root, textvariable=correo_var).pack()

        def registrar_usuario():
            usuario = usuario_var.get()
            clave = clave_var.get()
            correo = correo_var.get()

            if not usuario or not clave or not correo:
                messagebox.showerror("Error", "Por favor complete todos los campos.")
                return

            if usuario in self.usuarios:
                messagebox.showerror("Error", "El usuario ya está registrado.")
            else:
                self.usuarios[usuario] = Usuario(usuario, correo, clave)
                messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
                self.inicializar_interfaz()

        tk.Button(self.root, text="Registrarse", command=registrar_usuario).pack(pady=10)
        tk.Button(self.root, text="Cancelar", command=self.inicializar_interfaz).pack(pady=5)
    #Pantalla principal tras iniciar sesión.
    def mostrar_pantalla_principal(self):
        self.limpiar_ventana()
        tk.Label(self.root, text=f"Bienvenido {self.usuario_actual.nombre}", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="Ver Autos", command=self.mostrar_autos).pack(pady=5)
        tk.Button(self.root, text="Ver Canasta", command=self.mostrar_canasta).pack(pady=5)
        tk.Button(self.root, text="Cerrar Sesión", command=self.inicializar_interfaz).pack(pady=5)
    #Lista los autos disponibles.
    def mostrar_autos(self):
        self.limpiar_ventana()
        tk.Label(self.root, text="Autos Disponibles", font=("Arial", 14)).pack(pady=10)

        for auto in self.autos_disponibles:
            frame = tk.Frame(self.root, relief="solid", borderwidth=1)
            frame.pack(pady=5, padx=10, fill="x")

            tk.Label(frame, text=f"{auto.nombre} - ${auto.precio}/día").pack(side="left", padx=10)
            tk.Button(frame, text="Agregar a Canasta", command=lambda a=auto: self.agregar_a_canasta(a)).pack(side="right")

        tk.Button(self.root, text="Volver", command=self.mostrar_pantalla_principal).pack(pady=10)
    #Añade autos a la canasta.
    def agregar_a_canasta(self, auto):
        if auto in self.canasta.autos:
            messagebox.showwarning("Informacion", f"{auto.nombre} ya está en la canasta.")
        else:
            self.canasta.agregar(auto)
            messagebox.showinfo("Agregado", f"{auto.nombre} añadido a la canasta.")
    #Muestra los autos seleccionados y permite modificarlos
    def mostrar_canasta(self):
        self.limpiar_ventana()

        tk.Label(self.root, text="Canasta", font=("Arial", 14)).pack(pady=10)

        if not self.canasta.autos:
            tk.Label(self.root, text="La canasta está vacía.").pack()
        else:
            for auto in self.canasta.autos:
                frame = tk.Frame(self.root, relief="solid", borderwidth=1)
                frame.pack(pady=5, padx=10, fill="x")

                tk.Label(frame, text=f"{auto.nombre} - {auto.dias} días - ${auto.precio_total()}").pack(side="left", padx=10)
                tk.Button(frame, text="+", command=lambda a=auto: self.cambiar_dias(a, 1)).pack(side="left")
                tk.Button(frame, text="-", command=lambda a=auto: self.cambiar_dias(a, -1)).pack(side="left")
                tk.Button(frame, text="Eliminar", command=lambda a=auto: self.eliminar_auto(a)).pack(side="right")

            tk.Label(self.root, text=f"Total: ${self.canasta.total()}", font=("Arial", 14)).pack(pady=10)

        tk.Button(self.root, text="Pagar", command=self.pagar).pack(pady=10)

        tk.Button(self.root, text="Volver", command=self.mostrar_pantalla_principal).pack(pady=10)


    def cambiar_dias(self, auto, incremento):
        if incremento == 1 or (incremento == -1 and auto.dias > 1):
            auto.dias += incremento
        self.mostrar_canasta()

    def eliminar_auto(self, auto):
        self.canasta.eliminar(auto)
        self.mostrar_canasta()
    #Maneja el proceso de pago e invoca el envío de correos.
    def pagar(self):
        if not self.canasta.autos:
            tk.Label(self.root, text="Tu canasta está vacía. No puedes proceder con el pago.").pack()
            return

        self.limpiar_ventana()

        # Mostrar mensaje de confirmación
        tk.Label(self.root, text="¿Estás seguro que deseas proceder con el pago?").pack(pady=10)

        def confirmar_pago():
            pago = Pago(self.usuario_actual.correo)
            pago.enviar_correo()
            tk.Label(self.root, text="Pago realizado con éxito.").pack(pady=10)
            self.mostrar_pantalla_principal()

        def cancelar_pago():
            self.mostrar_canasta()

        tk.Button(self.root, text="Sí", command=confirmar_pago).pack(pady=5)
        tk.Button(self.root, text="No", command=cancelar_pago).pack(pady=5)


# Inicia la aplicación creando una ventana principal y lanzando la interfaz.
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sistema POO")
    root.geometry("800x600")
    app = InterfazUsuario(root)
    root.mainloop()


