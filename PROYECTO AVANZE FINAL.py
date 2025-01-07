import tkinter as tk  # Para la interfaz gráfica
from tkinter import messagebox, StringVar  # Manejo de cuadros de diálogo y variables
import smtplib  # Para el envío de correos electrónicos
from email.mime.text import MIMEText  # Manejo de mensajes de texto en correos
from email.mime.multipart import MIMEMultipart  # Para correos con múltiples partes (texto y adjuntos)
import re
import os  # Para la gestión de variables de entorno


# Clase que representa a un usuario
class Usuario:
    def __init__(self, nombre, correo, clave, es_admin=False):
        self.nombre = nombre  # Nombre del usuario
        self.correo = correo  # Correo del usuario
        self.clave = clave  # Contraseña del usuario
        self.es_admin = es_admin  # Indica si es administrador


# Clase que representa un auto
class Auto:
    def __init__(self, nombre, precio, descripcion=""):
        self.nombre = nombre  # Nombre del auto
        self.precio = precio  # Precio del auto por día
        self.dias = 1  # Días de renta (por defecto 1)
        self.descripcion = descripcion  # Descripción del auto

    def precio_total(self):
        # Calcula el precio total según los días
        return self.precio * self.dias


# Clase para manejar la canasta de autos seleccionados
class Canasta:
    def __init__(self):
        self.autos = []  # Lista de autos en la canasta

    def agregar(self, auto):
        # Agrega un auto a la canasta si no está ya incluido
        if auto not in self.autos:
            self.autos.append(auto)

    def eliminar(self, auto):
        # Elimina un auto de la canasta
        if auto in self.autos:
            self.autos.remove(auto)

    def total(self):
        # Calcula el costo total de todos los autos en la canasta
        return sum(auto.precio_total() for auto in self.autos)


# Clase para manejar los pagos
class Pago:
    def __init__(self, destinatario):
        self.destinatario = destinatario  # Correo del destinatario

    def enviar_correo(self):
        # Configuración del correo electrónico
        remitente = "rent.auto.lagos@gmail.com"
        contraseña_empresarial = "cytj fqme eamf zmyw"

        # Creación del mensaje
        mensaje = MIMEMultipart()
        mensaje["From"] = remitente
        mensaje["To"] = self.destinatario
        mensaje["Subject"] = 'Pago RentAuto'
        mensaje.attach(MIMEText("Estimado, el pago ha sido realizado con éxito.", 'plain'))

        # Envío del correo
        try:
            servicio = smtplib.SMTP('smtp.gmail.com', 587)
            servicio.starttls()  # Conexión segura
            servicio.login(remitente, contraseña_empresarial)
            servicio.sendmail(remitente, self.destinatario, mensaje.as_string())
            servicio.quit()
            print("Correo enviado exitosamente")
        except Exception as e:
            print(f"Error al enviar el correo: {e}")


# Clase principal para la interfaz gráfica
class InterfazUsuario:
    def __init__(self, root):
        self.root = root  # Ventana principal
        self.canasta = Canasta()  # Canasta de autos
        self.usuarios = {}  # Diccionario de usuarios registrados
        self.usuarios = {
            "admin": Usuario("admin", "admin@rentauto.com", "12345", es_admin=True)
        }  # Diccionario de usuarios registrados, con el admin preinscrito
        self.usuario_actual = None  # Usuario que inició sesión
        self.autos_disponibles = [
            Auto("Nissan X-Trail", 14000, "SUV compacta ideal para viajes familiares."),
            Auto("Toyota Hilux", 24000, "Pickup confiable para trabajos duros y terrenos difíciles."),
            Auto("Nissan Versa", 17000, "Sedán económico con gran eficiencia de combustible."),
            Auto("Mitsubishi L200", 18000, "Pickup versátil con excelente capacidad de carga."),
            Auto("Peugeot 208", 15000, "Hatchback moderno y eficiente para la ciudad."),
            Auto("Hyundai Accent RB", 12000, "Sedán compacto con diseño elegante."),
            Auto("Chevrolet Sail", 28000, "Auto familiar con amplio espacio interior."),
            Auto("Ford F-150 Raptor", 50000, "Pickup deportiva de alta potencia y lujo."),
        ]

        self.inicializar_interfaz()  # Configura la pantalla inicial

   

    def limpiar_ventana(self):
        # Elimina todos los widgets de la ventana
        for widget in self.root.winfo_children():
            widget.destroy()

    def inicializar_interfaz(self):
        # Pantalla inicial con opciones de login y registro
        self.limpiar_ventana()
        tk.Label(self.root, text="Sistema de autos", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="Iniciar sesión", command=self.mostrar_login).pack(pady=5)
        tk.Button(self.root, text="Registrarse", command=self.mostrar_registro).pack(pady=5)

    def mostrar_login(self):
        self.limpiar_ventana()
        tk.Label(self.root, text="Inicio sesión", font=("Arial", 14)).pack(pady=10)

        usuario_var = StringVar()
        clave_var = StringVar()

        tk.Label(self.root, text="Usuario:").pack()
        tk.Entry(self.root, textvariable=usuario_var).pack()

        tk.Label(self.root, text="Contraseña:").pack()
        tk.Entry(self.root, textvariable=clave_var, show="*").pack()

        def verificar_login():
            usuario = usuario_var.get()
            clave = clave_var.get()

            if not usuario or not clave:
                messagebox.showerror("Error", "Por favor complete todos los campos.")
                return

            if usuario in self.usuarios:
                usuario_obj = self.usuarios[usuario]
                if usuario_obj.clave == clave:  # Verifica solo usuario y contraseña
                    self.usuario_actual = usuario_obj
                    messagebox.showinfo("Éxito", f"Bienvenido, {usuario}!")
                    self.mostrar_pantalla_principal()
                else:
                    messagebox.showerror("Error", "Contraseña incorrecta.")
            else:
                messagebox.showerror("Error", "Usuario no encontrado.")

        tk.Button(self.root, text="Iniciar sesión", command=verificar_login).pack(pady=10)
        tk.Button(self.root, text="Cancelar", command=self.inicializar_interfaz).pack(pady=5)

    def mostrar_registro(self):
        self.limpiar_ventana()
        tk.Label(self.root, text="Registro", font=("Arial", 14)).pack(pady=10)

        usuario_var = StringVar()
        clave_var = StringVar()
        correo_var = StringVar()

        tk.Label(self.root, text="Usuario:").pack()
        tk.Entry(self.root, textvariable=usuario_var).pack()

        tk.Label(self.root, text="Contraseña:").pack()
        tk.Entry(self.root, textvariable=clave_var, show="*").pack()

        tk.Label(self.root, text="Correo:").pack()
        tk.Entry(self.root, textvariable=correo_var).pack()

        def es_correo_valido(correo):
            patron = r"^[^@]+@[^@]+\.(cl|com)$"
            return re.match(patron, correo) is not None
        
        def registrar_usuario():
            usuario = usuario_var.get()
            clave = clave_var.get()
            correo = correo_var.get()

            if not usuario or not clave or not correo:
                messagebox.showerror("Error", "Por favor complete todos los campos.")
                return

            if not es_correo_valido(correo):
                messagebox.showerror("Error", "Por favor, ingresa un correo válido. ")
                return

            if usuario in self.usuarios:
                messagebox.showerror("Error", "El usuario ya está registrado.")
            else:
                self.usuarios[usuario] = Usuario(usuario, correo, clave)
                messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
                self.inicializar_interfaz()

        tk.Button(self.root, text="Registrar", command=registrar_usuario).pack(pady=10)
        tk.Button(self.root, text="Cancelar", command=self.inicializar_interfaz).pack(pady=5)


    def mostrar_pantalla_principal(self):
        # Pantalla principal del sistema
        self.limpiar_ventana()
        tk.Label(self.root, text=f"Bienvenido {self.usuario_actual.nombre}", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="Ver autos", command=self.mostrar_autos).pack(pady=5)
        tk.Button(self.root, text="Ver canasta", command=self.mostrar_canasta).pack(pady=5)
        tk.Button(self.root, text="Cerrar sesión", command=self.inicializar_interfaz).pack(pady=5)
        
        if self.usuario_actual.es_admin:
            tk.Label(self.root, text="Opciones de Administrador:", font=("Arial", 14)).pack(pady=10)
            tk.Button(self.root,text="Ver todos los usuarios",command=self.mostrar_usuarios,).pack(pady=5)
            tk.Button(self.root,text="Añadir auto",command=self.mostrar_agregar_auto,).pack(pady=5)

    def mostrar_usuarios(self):
        self.limpiar_ventana()
        tk.Label(self.root, text="Usuarios registrados", font=("Arial", 14)).pack(pady=10)

        for usuario in self.usuarios.values():
            rol = "Admin" if usuario.es_admin else "Usuario"
            tk.Label(self.root, text=f"{usuario.nombre} ({rol})").pack(pady=5)

        tk.Button(self.root, text="Volver", command=self.mostrar_pantalla_principal).pack(pady=10)
    
    def mostrar_agregar_auto(self):
        self.limpiar_ventana()
        tk.Label(self.root, text="Agregar un nuevo auto", font=("Arial", 14)).pack(pady=10)

        nombre_var = tk.StringVar()
        precio_var = tk.StringVar()
        descripcion_var = tk.StringVar()

        tk.Label(self.root, text="Nombre del auto:").pack()
        tk.Entry(self.root, textvariable=nombre_var).pack()

        tk.Label(self.root, text="Precio por día:").pack()
        tk.Entry(self.root, textvariable=precio_var).pack()

        tk.Label(self.root, text="Descripción del auto:").pack()
        tk.Entry(self.root, textvariable=descripcion_var).pack()

        def agregar_auto():
            nombre = nombre_var.get()
            descripcion = descripcion_var.get()
            try:
                precio = int(precio_var.get())
                if nombre and precio > 0 and descripcion:
                    self.autos_disponibles.append(Auto(nombre, precio, descripcion))
                    tk.messagebox.showinfo(
                        "Éxito", f"El auto {nombre} ha sido agregado con éxito."
                    )
                    self.mostrar_pantalla_principal()
                else:
                    tk.messagebox.showerror("Error", "Por favor ingrese datos válidos.")
            except ValueError:
                tk.messagebox.showerror("Error", "El precio debe ser un número entero.")

        tk.Button(self.root, text="Agregar", command=agregar_auto).pack(pady=10)
        tk.Button(self.root, text="Cancelar", command=self.mostrar_pantalla_principal).pack(pady=5)

    
    def mostrar_autos(self):
        # Muestra los autos disponibles para rentar
        self.limpiar_ventana()
        tk.Label(self.root, text="Autos disponibles", font=("Arial", 14)).pack(pady=10)
        self.buscar_por_nombre()
        for auto in self.autos_disponibles:
            frame = tk.Frame(self.root, relief="solid", borderwidth=1)
            frame.pack(pady=5, padx=10, fill="x")
            tk.Label(frame, text=f"{auto.nombre} - ${auto.precio}/día").pack(side="left", padx=10)
            tk.Button(frame, text="Agregar a canasta", command=lambda a=auto: self.agregar_a_canasta(a)).pack(side="right")
            tk.Button(frame, text="Descripción", command=lambda a=auto: self.mostrar_descripcion(a)).pack(side="right")
        tk.Button(self.root, text="Volver", command=self.mostrar_pantalla_principal).pack(pady=10)
    
    def mostrar_descripcion(self, auto):
        self.limpiar_ventana()
        tk.Label(self.root, text=f"Descripción de {auto.nombre}", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text=f"Precio: ${auto.precio}/día", font=("Arial", 12)).pack(pady=5)
        tk.Label(self.root, text=f"Descripción: {auto.descripcion}", font=("Arial", 12), wraplength=400, justify="left").pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.mostrar_autos).pack(pady=20)


    def buscar_por_nombre(self):
        # Campo de entrada
        tk.Label(self.root, text="Nombre del vehículo:").pack(pady=5)
        entrada_busqueda = tk.Entry(self.root)
        entrada_busqueda.pack(pady=20, fill="x", padx=10)

        # Función de búsqueda
        def realizar_busqueda():
            nombre_busqueda = entrada_busqueda.get().strip().lower()
            resultados_canasta = [
                auto for auto in self.canasta.autos
                if nombre_busqueda in auto.nombre.lower()
            ]

            resultados_disponibles = [
                auto for auto in self.autos_disponibles
                if nombre_busqueda in auto.nombre.lower()
            ]

            self.limpiar_ventana()
            tk.Label(self.root, text="Resultados de la búsqueda", font=("Arial", 14)).pack(pady=10)

            if resultados_canasta or resultados_disponibles:
                # Mostrar resultados disponibles
                if resultados_disponibles:
                    tk.Label(self.root, text="Disponibles para agregar:", font=("Arial", 12)).pack(pady=5)
                    for auto in resultados_disponibles:
                        frame = tk.Frame(self.root, relief="solid", borderwidth=1)
                        frame.pack(pady=5, padx=10, fill="x")

                        tk.Label(frame, text=f"{auto.nombre} - ${auto.precio} por día").pack(side="left", padx=10)
                        tk.Button(frame, text="Agregar a la Canasta", command=lambda a=auto: self.agregar_a_canasta(a)).pack(side="right")
            else:
                tk.Label(self.root, text="No se encontraron vehículos con ese nombre.").pack(pady=10)

            tk.Button(self.root, text="Volver", command=self.mostrar_autos).pack(pady=10)
        tk.Button(self.root, text="Buscar", command=realizar_busqueda).pack(pady=10)

    def agregar_a_canasta(self, auto):
        # Agrega un auto a la canasta
        if auto in self.canasta.autos:
            messagebox.showerror("Error", "El auto ya está en la canasta.")
        else:
            self.canasta.agregar(auto)
            messagebox.showinfo("Éxito", f"El auto {auto.nombre} ha sido agregado.")

    def mostrar_canasta(self):
        self.limpiar_ventana()
        tk.Label(self.root, text="Canasta", font=("Arial", 14)).pack(pady=10)
        
        if not self.canasta.autos:
            tk.Label(self.root, text="La canasta está vacía.").pack()
        else:
            for auto in self.canasta.autos:
                frame = tk.Frame(self.root, relief="solid", borderwidth=1)
                frame.pack(pady=5, padx=10, fill="x")
                dias_texto = "día" if auto.dias == 1 else "días"

                tk.Label(frame, text=f"{auto.nombre} - {auto.dias} {dias_texto} - ${auto.precio_total()}").pack(side="left", padx=10)
                tk.Button(frame, text="+", command=lambda a=auto: self.cambiar_dias(a, 1)).pack(side="left")
                tk.Button(frame, text="-", command=lambda a=auto: self.cambiar_dias(a, -1)).pack(side="left")
                tk.Button(frame, text="Eliminar", command=lambda a=auto: self.eliminar_de_canasta(a)).pack(side="right")

            tk.Label(self.root, text=f"Total: ${self.canasta.total()}", font=("Arial", 14)).pack(pady=10)

        tk.Button(self.root, text="Pagar", command=self.pagar).pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.mostrar_pantalla_principal).pack(pady=10)


    def cambiar_dias(self, auto, incremento):
        if incremento == 1 or (incremento == -1 and auto.dias > 1):
            auto.dias += incremento
        self.mostrar_canasta()

    def eliminar_de_canasta(self, auto):
        # Elimina un auto de la canasta
        self.canasta.eliminar(auto)
        self.mostrar_canasta()
    

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



# Configuración y ejecución de la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    root.title("RentAuto")
    root.geometry("800x600")
    InterfazUsuario(root)
    root.mainloop()

