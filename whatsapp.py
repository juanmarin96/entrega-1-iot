
from twilio.rest import Client
from datetime import datetime

# Datos de API Twilio, tomados de twilio.com/console
account_sid = 'XXXX'
auth_token = 'XXXX'
# Crear nuevo cliente
client = Client(account_sid, auth_token)

# Parámetros
# resultado_ingreso: Si el intento fue satisfactorio, enviar como parámetro 'correcto', de lo contrario 'incorrecto'
# usuario: si el ingreso fue correcto, o el usuario que intenta ingresar existe, se pasa nombre de usuario que realiza el intento.
# Si es un intruso, enviar como parámetro, la palabra 'intruso'
def enviarMensaje(resultado_ingreso, usuario):

    # Obtener fecha de intento de login
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    if resultado_ingreso == 'correcto':
        mensaje =  'Nuevo intento de ingreso a la app, con resultado satisfactorio.\n'
        mensaje +=  'Usuario: ' + usuario + '. Hora del evento: ' + str(dt_string)
    elif resultado_ingreso == 'incorrecto':
        mensaje =  'Nuevo intento de ingreso a la app, con acceso denegado.\n'
        mensaje +=  'Usuario: ' + usuario + '. Hora del evento: ' + str(dt_string)
    else :
        print ('Parámetros incorrectos ')
        return

    print (mensaje)
    #return

    #Enviar mensaje
    message = client.messages.create(
        body = mensaje,
        from_='whatsapp:+14155238886',
        to='whatsapp:+573207853636'
    )

    print(message.sid)

#enviarMensaje('incorrecto', 'intruso')