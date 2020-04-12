import tkinter as tk
from PIL import ImageTk, Image
from tkinter import messagebox
import os
import mysql.connector
from mysql.connector import Error
from datetime import datetime



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
        messagebox.showerror("Error", "Login y/o clave inválidos")
        state = "fallido"
      else:
        messagebox.showinfo("Bienvenido", "Ingreso exitoso.")
        state = "exitoso"
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
    
if __name__ == "__main__":
  app = AppFoto()
  app.mainloop()

