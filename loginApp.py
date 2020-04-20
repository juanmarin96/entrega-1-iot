import tkinter as tk
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import Toplevel
import os
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import paho.mqtt.client as mqtt

# Punto 2
# Importar programa externo Python, encargado de enviar notificaciones whatsapp
import whatsapp

puerta = 'cerrada'
class AppFoto(tk.Frame):

    def __init__(self,master = None):

        super().__init__(master)
        # Configurando las dimensiones y el titulo de la ventana
        self.master.title('Login App')
        self.master.resizable(width=False, height=False)
        # Agregando el marco
        self.pack()

        # imagen
        self.img = ImageTk.PhotoImage(Image.open("foto.png"))

        # Agregando el label para la Foto
        self.photo = tk.Label(self, image = self.img)
        self.photo.pack(fill=tk.BOTH, expand=True)

        # Frame login
        self.loginFrame = tk.LabelFrame(self, text = "Login")
        self.loginFrame.pack(fill=tk.BOTH, expand=True)

        # Frame User
        self.frameUser = tk.Frame(self.loginFrame)
        self.frameUser.pack(fill=tk.BOTH, expand=True)
        self.labelUser = tk.Label(self.frameUser, width=9, \
                                  justify = tk.LEFT, text = "User:")
        self.labelUser.pack(fill=tk.BOTH, expand=True, side = tk.LEFT)
        self.inputUser = tk.Entry(self.frameUser, text = "")
        self.inputUser.pack(fill=tk.BOTH, expand=True, side = tk.LEFT)

        # Pass login
        self.passFrame = tk.Frame(self.loginFrame)
        self.passFrame.pack(fill=tk.BOTH, expand=True)
        self.labelPass = tk.Label(self.passFrame, width=9, \
                                  justify = tk.LEFT, text = "Password:")
        self.labelPass.pack(fill=tk.BOTH, expand=True, side = tk.LEFT)
        self.inputPass = tk.Entry(self.passFrame, show="*", text = "")
        self.inputPass.pack(fill=tk.BOTH, expand=True, side = tk.LEFT)
        # Button
        self.bLogin = tk.Button(self.loginFrame,text = "Login", command = self.login)
        self.bLogin.pack(fill=tk.BOTH, expand=True)

    def login(self):
        now = datetime.now()
        today = now.strftime("%d/%m/%Y %H:%M:%S")
        login_message = 'Fecha y hora de logueo: {0} - Usuario: {1}'.format(today,self.inputUser.get() )
        print(login_message)
        try:
          connection = mysql.connector.connect(host='localhost',
                                             database='login-app',
                                             user='root',
                                             password='root')
          if not connection.is_connected():
            print("No se pudo conectar a la base de datos")
            raise Exception("Error conectandose a la base de datos")
          sql_select_query = "select * from usuarios where username = %s and password = %s"
          cursor = connection.cursor()
          cursor.execute(sql_select_query,(self.inputUser.get(), self.inputPass.get()))
          records = cursor.fetchall()
          if cursor.rowcount <= 0:
            messagebox.showerror("Error", "Login y/o clave invalidos")
            state = "fallido"

            # Ejecutar programa para enviar notificacion whatsapp
            whatsapp.enviarMensaje('incorrecto', self.inputUser.get())
          else:
            messagebox.showinfo("Bienvenido", "Ingreso exitoso.")
            state = "exitoso"

            # Ejecutar programa para enviar notificacion whatsapp
            whatsapp.enviarMensaje('correcto', self.inputUser.get())

          mysql_insert_query = "INSERT INTO `acces-log` (user, password, state) VALUES ('{0}', '{1}', '{2}')".format(self.inputUser.get(), self.inputPass.get(),state)
          cursor.execute(mysql_insert_query)
          connection.commit()

        except Error as e:
          print("Error while connecting to MySQL", e)
        finally:
          if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
            if(state == "exitoso"):
                #self.master.withdraw()
                self.newWindow = Toplevel(self.master)
                bb = controlServo(self.newWindow)

class controlServo(tk.Frame):

    def __init__(self, master = None):
        super().__init__(master)
        self.master.title('Control puerta')
        self.master.resizable(width=False, height=False)
        self.pack()

        # Variables asociadas al cliente mqtt
        self.doorState = False
        self.broker_IP = "127.0.0.1"
        self.topic = "servo/rotation"

        # cliente mqtt
        CLIENT_ID = "doorController"
        self.mqttc=mqtt.Client(client_id=CLIENT_ID)
        self.mqttc.connect(self.broker_IP, 1883, 60)

        # Agregando frames principales
        self.buttonDoor= tk.Button(self,text="Abrir",command = self.open_close)
        self.buttonDoor.pack(side=tk.LEFT)
        self.doorLabel = tk.Label(self,text = "Puerta cerrada")
        self.doorLabel.pack(side=tk.LEFT)

        # Iniciando el loop infinito del cliente mqtt
        self.mqttc.loop_start()

    def open_close(self):

        if self.doorState == True:
            #self.ser.write('h'.encode("ascii","ignore"))
            self.buttonDoor.config(text = "Abrir")
            self.doorLabel.config(text = "Puerta Cerrada")
            self.mqttc.publish("servo/rotation","0")  # Uso de publish para
                                                                 # prender la lampara
        else:
            #self.ser.write('l'.encode("ascii","ignore"))
            self.buttonDoor.config(text = "Cerrar")
            self.mqttc.publish("servo/rotation","90")  # Uso de publish para
            self.doorLabel.config(text = "Puerta abierta")

        self.doorState = not(self.doorState)



if __name__ == "__main__":
    app = AppFoto()
    app.mainloop()
