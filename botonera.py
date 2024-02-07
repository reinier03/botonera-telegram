from flask import Flask, request
import telebot
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton
from telebot.types import ForceReply
from telebot.types import ReplyKeyboardRemove
import threading
from time import sleep
import time
import os
import sqlite3
import dill
from waitress import serve

local_ip = ""
hora_eliminacion_botonera=False

os.chdir(os.path.dirname(os.path.abspath(__file__)))
conexion = sqlite3.connect("Botonera_Canales", check_same_thread=False)
cursor = conexion.cursor()
try:
  cursor.execute('CREATE TABLE Canales (ID_Canal INTEGER, ID_Admin INTEGER)')
except Exception as e:
  if str(e) == "table Canales already exists":
    pass
del_hilo = ""
#-------------------Variables a utilizar en el codigo-------------------------------
reima = 1413725506
bot = telebot.TeleBot(os.environ["token"])
dic = {}
hora_publicacion = []
tiempo_de_espera_botonera = 10800  #Por defecto, tiene asignado 3 horas
ejecutar_hilo = False
hilo_publicaciones = ""
modo_reparacion = False
mensajes_a_eliminar = []
publicaciones = False
tiempo_eliminacion_botonera = False
hora_eliminacion_botonera = []
mensajes_a_eliminar_globales = []

#--------------------------------------------------------------------------
server_address = ""




#CARGAR las variables si existe ya un archivo
if os.path.isfile("variables"):
  with open("variables", "rb") as archivo:
    variables_cargadas = dill.load(archivo)

    for var_name, var_value in variables_cargadas.items():
      globals()[var_name] = var_value


def guardar_variables():
  global mensajes_a_eliminar_globales
  diccionario_copia = []
  if len(mensajes_a_eliminar_globales) > 30:
    for e, i in enumerate(mensajes_a_eliminar_globales, start=1):
      if e == 31:
        break
      diccionario_copia.append(mensajes_a_eliminar_globales[-e])
    mensajes_a_eliminar_globales = diccionario_copia.copy()
    del diccionario_copia

  with open("variables", "wb") as archivo:
    dict1 = {
        "dic": dic,
        "hora_publicacion": hora_publicacion,
        "tiempo_de_espera_botonera": tiempo_de_espera_botonera,
        "ejecutar_hilo": ejecutar_hilo,
        "hilo_publicaciones": hilo_publicaciones,
        "modo_reparacion": modo_reparacion,
        "mensajes_a_eliminar": mensajes_a_eliminar,
        "publicaciones": publicaciones,
        "tiempo_eliminacion_botonera": tiempo_eliminacion_botonera,
        "hora_eliminacion_botonera": hora_eliminacion_botonera,
        "mensajes_a_eliminar_globales": mensajes_a_eliminar_globales
    }
    dill.dump(dict1, archivo)



try:
  request.host_url
except:
  app = Flask(__name__)
  
  @app.route('/', methods=['GET'])
  def index():
    return f'¡Hola! Esta es la dirección local del host: {request.host_url}'

def flask():
  bot.remove_webhook()
  time.sleep(1)
  app.run(host="0.0.0.0", port=5000)





try:
  request.host_url
except:
  hilo_flask=threading.Thread(name="hilo_flask", target=flask)
  hilo_flask.start()



# def actualizar():
#     global mensajes_a_eliminar
#     global modo_reparacion
#     global hilo_publicaciones
#     global ejecutar_hilo
#     global tiempo_de_espera_botonera
#     global hora_publicacion
#     global dic
#     global publicaciones
#     with open("archivo_extraible.py", "w") as archivo:
#         archivo.seek(0)
#         archivo.truncate()
#         archivo.write(f"""
#                       mensajes_a_eliminar={mensajes_a_eliminar}
#                       modo_reparacion={modo_reparacion}
#                       hilo_publicaciones={hilo_publicaciones}
#                       ejecutar_hilo={ejecutar_hilo}
#                       tiempo_de_espera_botonera={tiempo_de_espera_botonera}
#                       hora_publicacion={hora_publicacion}
#                       dic={dic}
#                       publicaciones={publicaciones}
#                       """)

# try:
#     with open("contador_exe.txt", "r") as archivo:
#         archivo.seek(0)
#         lista=archivo.readlines()
#         if lista==[1]:
#             actualizar()
#             mensajes_a_eliminar=archivo_extraible.mensajes_a_eliminar
#             modo_reparacion=archivo_extraible.modo_reparacion
#             hilo_publicaciones=archivo_extraible.hilo_publicaciones
#             ejecutar_hilo=archivo_extraible.ejecutar_hilo
#             tiempo_de_espera_botonera=archivo_extraible.tiempo_de_espera_botonera
#             hora_publicacion=archivo_extraible.hora_publicacion
#             dic=archivo_extraible.dic

# except:
#     with open("contador_exe.txt", "w") as archivo:
#         archivo.seek()
#         archivo.write("1")

bot.send_message(reima, "Estoy online bitch >:)")

OS = ""

if os.name == "nt":
  OS = '\\'
else:
  OS = "//"

try:
  foto_lastHope = open(
      f"{os.path.dirname(os.path.abspath(__file__))}{OS}Last_Hope.jpg", 'rb')

except:
  pass


def funcion_reparacion(message):
  bot.send_message(
      message.chat.id,
      "🚨🚧Bot en Modo Construcción🚧🚨\n\nLo siento tigre, al parecer algo estalló en mi y ahora me ESTÁN reparando :( \n\n Vuelve luego a ver si ya me recuperé y seguir con las botoneras"
  )
  return


# except:
#     def recibir_foto_lastHope(message):
#         global foto_lastHope
#         if message.photo:
#             photo_id=message.photo[-1].file_id
#             photo_info=bot.get_file(photo_id)
#             downloaded_photo=bot.download_file(photo_info.file_path)
#             with open(f"{os.path.dirname(os.path.abspath(__file__))}{OS}Last_Hope.jpg", "wb") as archivo:
#                 archivo.write(downloaded_photo)
#             bot.send_message(reima, "Imagen capturada!")
#             foto_lastHope=open(f"{os.path.dirname(os.path.abspath(__file__))}{OS}Last_Hope.jpg", 'rb')

#         else:
#             msg=bot.send_message(reima, "Tiene que ser una foto!\nEnviala de nuevo!")
#             bot.register_next_step_handler(msg, recibir_foto_lastHope)

#     msg=bot.send_message(reima, "Al parecer no hay foto de la portada de Last Hope, envia una", reply_markup=ForceReply())
#     bot.register_next_step_handler(msg, recibir_foto_lastHope)

try:
  foto_LastBotonera = open(
      f"{os.path.dirname(os.path.abspath(__file__))}{OS}Last_Botonera.jpg",
      'rb')
except:

  def recibir_foto_promo(message):
    global foto_LastBotonera
    if message.photo:
      photo_id = message.photo[0].file_id
      photo_info = bot.get_file(photo_id)
      downloaded_file = bot.download_file(photo_info.file_path)
      with open(
          f"{os.path.dirname(os.path.abspath(__file__))}{OS}Last_Botonera.jpg",
          "wb") as archivo:
        archivo.write(downloaded_file)
      bot.send_message(reima, "imagen capturada!")
      foto_LastBotonera = open(
          f"{os.path.dirname(os.path.abspath(__file__))}{OS}Last_Botonera.jpg",
          'rb')
      return
    else:
      msg = bot.send_message(reima,
                             "Tiene que ser una foto!\nEnviala de nuevo!")
      bot.register_next_step_handler(msg, recibir_foto_promo)

  msg = bot.send_message(
      reima,
      "Al parecer, no hay foto de Last Botonera promo, envíame una para continuar",
      reply_markup=ForceReply())
  bot.register_next_step_handler(msg, recibir_foto_promo)


def proxima_publicacion(message):
  global tiempo_de_espera_botonera
  global hora_publicacion
  horas = 0
  minutos_restantes = hora_publicacion[0] + tiempo_de_espera_botonera - float(
      time.time())
  minutos_restantes = round(minutos_restantes / 60)
  while not horas > 72:
    horas += 1
    if horas * 60 > minutos_restantes:
      horas -= 1
      break
  minutos_restantes = minutos_restantes - horas * 60
  try:
    if horas == 0:
      return bot.send_message(
          message.chat.id,
          f"Tiempo para la próxima publicación: {minutos_restantes} minutos")
    else:
      return bot.send_message(
          message.chat.id,
          f"Tiempo para la próxima publicación: {horas} hora(s) y {minutos_restantes} minuto(s)"
      )

  except:
    try:
      if horas == 0:
        return bot.send_message(
            message.from_user.id,
            f"Tiempo para la próxima publicación: {minutos_restantes} minutos")
      else:
        return bot.send_message(
            message.from_user.id,
            f"Tiempo para la próxima publicación: {horas} hora(s) y {minutos_restantes} minuto(s)"
        )

    except:
      if horas == 0:
        return bot.send_message(
            message,
            f"Tiempo para la próxima publicación: {minutos_restantes} minutos")
      else:
        return bot.send_message(
            message,
            f"Tiempo para la próxima publicación: {horas} hora(s) y {minutos_restantes} minuto(s)"
        )


def proxima_eliminacion_botonera(message):
  global tiempo_eliminacion_botonera
  global hora_eliminacion_botonera
  if tiempo_eliminacion_botonera == False or not hora_publicacion:
    bot.send_message(
        message.chat.id,
        "No hay tiempo de eliminacion de botonera definido, se borra a medida que se publica la nueva botonera"
    )
    return
  horas = 0
  minutos_restantes = hora_eliminacion_botonera[
      0] + tiempo_eliminacion_botonera - time.time()
  minutos_restantes = round(minutos_restantes / 60)
  while not horas > 72:
    horas += 1
    if horas * 60 > minutos_restantes:
      horas -= 1
      break
  minutos_restantes = minutos_restantes - horas * 60
  try:
    if horas == 0:
      return bot.send_message(
          message.chat.id,
          f"Tiempo para la próxima eliminación de las botoneras ya publicadas: {minutos_restantes} minutos"
      )
    else:
      return bot.send_message(
          message.chat.id,
          f"Tiempo para la próxima eliminación de las botoneras ya publicadas: {horas} hora(s) y {minutos_restantes} minuto(s)"
      )

  except:
    try:
      if horas == 0:
        return bot.send_message(
            message.from_user.id,
            f"Tiempo para la próxima eliminación de las botoneras ya publicadas: {minutos_restantes} minutos"
        )
      else:
        return bot.send_message(
            message.from_user.id,
            f"Tiempo para la próxima eliminación de las botoneras ya publicadas: {horas} hora(s) y {minutos_restantes} minuto(s)"
        )

    except:
      if horas == 0:
        return bot.send_message(
            message,
            f"Tiempo para la próxima eliminación de las botoneras ya publicadas: {minutos_restantes} minutos"
        )
      else:
        return bot.send_message(
            message,
            f"Tiempo para la próxima eliminación de las botoneras ya publicadas: {horas} hora(s) y {minutos_restantes} minuto(s)"
        )


# cursor.execute('SELECT * FROM Canales')
# lista_canales=cursor.fetchall()
# if lista_canales==[]:
#     lasthope=[(-1001161864648, 1413725506)]
#     cursor.executemany('INSERT INTO Canales VALUES (?,?)', lasthope)
#     conexion.commit()

bot.set_my_commands([
    telebot.types.BotCommand("/help", "Ofrece AYUDA de cómo funciona el bot"),
    telebot.types.BotCommand(
        "/mostrar",
        "Muestra los canales que conforman la botonera y el tiempo de la botonera"
    ),
    telebot.types.BotCommand(
        "/ingresar", "Ingresa SU canal en la botonera junto con los demás"),
    telebot.types.BotCommand("/eliminar",
                             "Eliminar su canal de la botonera :("),
    telebot.types.BotCommand("/panel_administrador",
                             "SÓLO disponible para mi creador ;)")
])

usuario = bot.user


def cancelar(message):
  bot.send_message(
      message.chat.id,
      "Envía /cancelar para cancelar la operación actual\nTodos tienen el derecho de arrepentirse\n\n(p≧w≦q)＼(ﾟｰﾟ＼)"
  )


def eliminar_botonera():
  global hora_eliminacion_botonera
  global tiempo_eliminacion_botonera
  global mensajes_a_eliminar
  while hora_eliminacion_botonera:
    if publicaciones == True and time.localtime(
        hora_eliminacion_botonera[0] +
        tiempo_eliminacion_botonera) <= time.localtime(time.time()):
      print(mensajes_a_eliminar)
      for item in mensajes_a_eliminar:
        try:
          bot.delete_message(item[0], item[1])
        except Exception as e:
          print(f"Excepcion: \n\n{e}")

      mensajes_a_eliminar = []
      hora_eliminacion_botonera = []
      bot.send_message(reima, "botonera eliminada")
      guardar_variables()
      return
    else:
      time.sleep(30)


def hilo_eliminaciones():
  global del_hilo
  del_hilo = threading.Thread(name="hilo_eliminar_botonera",
                              target=eliminar_botonera)
  del_hilo.start()


if hora_eliminacion_botonera and tiempo_eliminacion_botonera:
  hilo_eliminaciones()


def hacer_publicaciones():
  global tiempo_eliminacion_botonera
  global mensajes_a_eliminar_globales
  global hora_eliminacion_botonera
  global mensajes_a_eliminar
  global publicaciones
  global foto_LastBotonera
  global ejecutar_hilo
  global hora_publicacion
  while ejecutar_hilo:
    if publicaciones == False or time.localtime(
        hora_publicacion[0] + tiempo_de_espera_botonera) <= time.localtime():
      if mensajes_a_eliminar == []:
        pass
      else:
        for item in mensajes_a_eliminar:
          try:
            bot.delete_message(item[0], item[1])
          except Exception as e:
            try:
              #bot.send_message(reima, f"Ha ocurrido una excepción intentando eliminar la botonera ya publicada en el canal @{bot.get_chat(item[0]).username}:\n{str(e)}")
              a = "lol"
            except:
              pass

        mensajes_a_eliminar = []

      foto_LastBotonera.seek(0)
      publicaciones = True
      bot.send_message(1413725506, "Publicaré la botonera ahora")
      botonera = InlineKeyboardMarkup(row_width=1)
      #Primeramente, tengo que asegurarme que el bot tenga permisos para publicar en el canal
      
      cursor.execute('SELECT * FROM Canales')
      lista_canales = cursor.fetchall()
      for linea in lista_canales:
        canal = linea[0]
        administrador = linea[1]
        try:
          bot.get_chat(canal).title
          member = bot.get_chat_member(chat_id=canal, user_id=bot.user.id)
        except Exception as e:
          if "chat not found" in str(e):
            bot.send_message(reima, f"Fuí expulsado del canal {linea[0]}\n\nLo eliminaré de la botonera")
            cursor.execute(f'DELETE FROM Canales WHERE ID_Canal={linea[0]}')
            conexion.commit()
            try:
                bot.send_message(administrador, "He eliminado tu canal de la botonera >:( Por haberme sacado")
            except:
                pass
            
          elif "bot was kicked from the channel chat" in str(e):
            bot.send_message(
                reima,
                f"Fuí expulsado del canal   {linea[0]}\n\nLo eliminaré de la botonera"
            )
            cursor.execute(f'DELETE FROM Canales WHERE ID_Canal={linea[0]}')
            conexion.commit()
            try:
              bot.send_message(
                  linea[1],
                  "He eliminado tu canal de la botonera\n\n>:D POR EXPULSARME MARICO"
              )
              continue
            except:
              continue
          elif not member.status == 'administrator' and str(administrador) != str(1413725506):
              cursor.execute(f'DELETE FROM Canales WHERE ID_Canal={canal}')
              conexion.commit()
              bot.send_message(reima,
              f"Se ha eliminado el canal {bot.get_chat(canal).username} por no dejarme como administrador >:(")
              
          bot.send_message(
              administrador,
              f"<u>ATENCIÓN</u>:\n Se ha eliminado el canal {bot.get_chat(canal).username} por no dejarme como administrador >:(\n\nPara ingresar de nuevo el canal en la botonera escriba /ingresar",
              parse_mode="html")
          
        else:
            bot.send_message(reima, f"Ha ocurrido un error con el canal {canal}:\n\n{e}\n\nProcedo a eliminarlo")
            cursor.execute(f'DELETE FROM Canales WHERE ID_Canal={linea[0]}')
            conexion.commit()

      #Ahora actualizaré la lista con los canales de la BD
      cursor.execute('SELECT * FROM Canales')
      lista_canales = cursor.fetchall()
      for linea in lista_canales:
        canal = linea[0]
        #Si el bot tiene permisos pues agrega el canal a la botonera
        nombre = bot.get_chat(canal).title
        enlace = f"https://t.me/{bot.get_chat(canal).username}"
        boton = InlineKeyboardButton(nombre, url=enlace)
        botonera.add(boton)
      botonera.row(
          InlineKeyboardButton("(☞ﾟヮﾟ)☞ ÚNETE A LA BOTONERA ☜(ﾟヮﾟ☜)",
                               url="https://t.me/LastBotoneraBot"))
      for linea in lista_canales:
        foto_LastBotonera.seek(0)
        canal = linea[0]
        admin = linea[1]
        try:

          msg = bot.send_photo(
              int(canal),
              photo=foto_LastBotonera,
              caption=
              "¡Si!, ¡Es eso mismo que estás pensando!\n Literalmente, <b>La Última Botonera</b> baby (☞ﾟヮﾟ)☞ ☜(ﾟヮﾟ☜)\n\n¡No pierdas la oportunidad de unirte a algún canal aquí Papazote'!",
              parse_mode="html",
              reply_markup=botonera)

          mensajes_a_eliminar.append((canal, msg.message_id))
          mensajes_a_eliminar_globales.append((canal, msg.message_id))

        except Exception as e:
          if "need administrator rights in the channel chat" in str(e):
            if admin == 1413725506:
              bot.send_message(
                  reima,
                  f"OYE ESTÚPIDA!\n\nEste <a href='https://t.me/{bot.get_chat(canal).username}'>canal</a> tuyo no me deja mandar la botonera porque no tengo permisos para publicar! <b>Lo dejaré ahí</b>, porque eres su dueño pero MUEVE EL CULO!",
                  parse_mode="html")
              continue
            cursor.execute(f'DELETE FROM Canales WHERE ID_Canal={canal}')
            conexion.commit()
            try:
              bot.send_message(
                  admin,
                  f"Haber ingenioso(a), no basta con que solamente me pongas de admin en tu canal si no me das permisos para publicar la botonera ahí\n\nPonme los permisos de publicación en @{bot.get_chat(canal).username}, si no sabes cual es pues dale todos y ya.\n\n<b>Te sacaré de la botonera</b>\n\nCuando me pongas el permiso para publicar en tu canal, vuelve a escribir /ingresar para volver :) Te estaré esperando",
                  reply_markup=InlineKeyboardMarkup().row(
                      InlineKeyboardButton(
                          "Ir a tu Canal",
                          url=f"https://t.me/{bot.get_chat(canal).username}")),
                  parse_mode="html")
            except Exception as e:
              bot.send_message(reima, f"Excepcion al enviar un mensaje: \n{e}")
            bot.send_message(
                reima,
                f"<b>Atención</b>\n\nHe eliminado el canal: @{bot.get_chat(canal).username} y su admin: @{bot.get_chat(admin).username}, por no dejarme permisos de publicación allí",
                parse_mode="html")
          else:
            bot.send_message(
                reima,
                f"Excepcion al enviar el mensaje a {bot.get_chat(canal).username}: \n{e}"
            )

      conexion.commit()
      foto_LastBotonera.seek(0)
      hora_publicacion = [time.time()]
      if tiempo_eliminacion_botonera:
        hora_eliminacion_botonera = []
        hora_eliminacion_botonera.append(time.time())
        hilo_eliminaciones()
      proxima_publicacion(reima)
      guardar_variables()
    else:
      time.sleep(30)


def iniciar_hilo():
  global hilo_publicaciones
  hilo_publicaciones = threading.Thread(name="hilo_publicaciones", target=hacer_publicaciones)
  return hilo_publicaciones.start()


if publicaciones or ejecutar_hilo:
  iniciar_hilo()


@bot.message_handler(commands=["panel_administrador"])
def cmd_comenzar(message):
  global cursor
  global modo_reparacion
  global botonera_panel
  if not message.chat.type == "private":
    return
  global foto_LastBotonera
  dic_admin = {}
  dic_admin[message.from_user.id] = []
  if message.chat.id == 1413725506:
    botonera_panel = InlineKeyboardMarkup(row_width=1)
    b1 = InlineKeyboardButton("Iniciar bucle de publicaciones 🙌",
                              callback_data="Iniciar bucle")
    b2 = InlineKeyboardButton("Parar el bucle de publicaciones 🖐",
                              callback_data="Parar bucle")
    b3 = InlineKeyboardButton("Agregar un canal a la lista de canales 🧻",
                              callback_data="Agregar canal")
    b4 = InlineKeyboardButton("Eliminar un canal de la lista de canales 💨",
                              callback_data="Eliminar canal")
    b5 = InlineKeyboardButton("Modificar el tiempo de la botonera ⌛",
                              callback_data="Modificar tiempo")
    b6 = InlineKeyboardButton("Tiempo de la eliminación Botonera 💥",
                              callback_data="Modificar eliminación")
    b7 = InlineKeyboardButton("Ver Archivo de canales 👀",
                              callback_data="Archivo de texto")
    b8 = InlineKeyboardButton("Enviar archivo de canales 🌠",
                              callback_data="Enviar archivos")
    b9 = InlineKeyboardButton("Limpiar archivo ✨",
                              callback_data="Limpiar archivo")
    b10 = InlineKeyboardButton("Enviar Mensaje a Admins 🎫",
                               callback_data="Enviar Mensaje a Admins")
    b11 = InlineKeyboardButton("Limpiar los canales",
                               callback_data="Limpiar canales")
    b12 = InlineKeyboardButton("🚨🚧Modo reparacion🚧🚨",
                               callback_data="Modo reparacion")
    botonera_panel.add(b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12)
    bot.send_message(message.chat.id,
                     "Bienvenido Reima ;) Qué planeas hacer?",
                     reply_markup=botonera_panel)
  else:
    bot.send_message(
        message.chat.id,
        "Lo siento mirei ;)\n\nNo eres mi creador como para mandarme ese mensaje >:D y decirme qué hacer"
    )
    return


@bot.callback_query_handler(func=lambda x: True)
def respuesta_callback(call):
  global botonera_panel
  global ejecutar_hilo
  global cursor
  global foto_LastBotonera
  foto_LastBotonera.seek(0)
  markup = ForceReply()

  #-----------------Iniciar Bucle de publicaciones--------------------
  if call.data == "Iniciar bucle":
    if ejecutar_hilo == True:
      bot.send_message(call.from_user.id,
                       "Ya estoy ejecutando un hilo pringado >:(")
      return
    else:
      ejecutar_hilo = True
      bot.send_message(call.from_user.id, "Voy a ejecutar el hilo :D")
      return iniciar_hilo()

#-----------------------Parar bucle---------------------------------------------------
  elif call.data == "Parar bucle":
    global publicaciones
    global hora_publicacion
    global hilo
    if publicaciones == False:
      return bot.send_message(
          call.from_user.id,
          "Ni siquiera está activo el bucle :l\n\nPrueba otra cosa")

    else:

      def parar_bucle():
        global mensajes_a_eliminar
        global publicaciones
        global hora_publicacion
        global ejecutar_hilo
        global hilo_publicaciones
        global hora_eliminacion_botonera
        try:
          global del_hilo
        except:
          pass
        bot.send_message(call.from_user.id, "Voy a detener el hilo")
        if mensajes_a_eliminar == []:
          pass
        else:
          for item in mensajes_a_eliminar:
            try:
              bot.delete_message(item[0], item[1])
            except Exception as e:
              bot.send_message(reima, f"Ha ocurrido una excepción intentando eliminar la botonera ya publicada en el canal @{bot.get_chat(item[0]).username}:\n\n{str(e)}")
              pass
          
        mensajes_a_eliminar = []
        ejecutar_hilo = False
        hora_publicacion = []
        publicaciones = False
        hora_eliminacion_botonera = []
        while not "stopped" in str(hilo_publicaciones):
          time.sleep(1)
        if del_hilo:
          while not "stopped" in str(del_hilo):
            time.sleep(1)
        guardar_variables()
        return bot.send_message(
            call.from_user.id,
            f"Los hilos de publicaciones han sido detenidos exitosamente mi queridísimo Reima ;D\n\n<u>Hilos activos</u>:\n{threading.active_count()}",
            parse_mode="html")

      parar_bucle()
      return

#---------------------------Agregar Canal---------------------------------
  elif call.data == "Agregar canal":
    msg = bot.send_message(call.from_user.id,
                           "Muy bien, dime el @username del canal",
                           reply_markup=markup)

    def registro_de_admin(message):
      dic_admin = {}
      dic_admin[message.chat.id] = []
      if not message.text.startswith("@"):
        dic_admin[message.chat.id] = f"@{message.text}"
      else:
        dic_admin[message.chat.id] = message.text
      global botonera_panel
      try:
        cursor.execute('SELECT * FROM Canales')
        lista_canales = cursor.fetchall().copy()
      except:
        pass
      try:
        chat_admin = bot.get_chat(dic_admin[message.chat.id]).id
      except:
        msg = bot.send_message(call.from_user.id,
                               "El canal que ingresaste no existe")
        return
      else:
        for line in lista_canales:
          if chat_admin == line[0]:
            bot.send_message(
                call.from_user.id,
                "El canal ya existe en el archivo\n\nPrueba con otro")
            return bot.send_message(call.from_user.id,
                                    "Bienvenido Reima ;) Qué planeas hacer?",
                                    reply_markup=botonera_panel)

        if bot.get_chat_member(chat_admin,
                               bot.user.id).status != "administrator":
          bot.send_message(
              call.from_user.id,
              "No soy admin en ese chat, pero bueno, ya sabrás tú lo que haces...."
          )

        canal = [(chat_admin, call.from_user.id)]
        cursor.executemany('INSERT INTO Canales VALUES (?,?)', canal)

        bot.send_message(
            call.from_user.id,
            f"El canal {bot.get_chat(dic_admin[message.chat.id]).username} ha sido agregado exitosamente a la botonera"
        )
        conexion.commit()
        return bot.send_message(call.from_user.id,
                                "Bienvenido Reima ;) Qué planeas hacer?",
                                reply_markup=botonera_panel)

    bot.register_next_step_handler(msg, registro_de_admin)

#---------------------------------Eliminar canal--------------------------
  elif call.data == "Eliminar canal":
    msg = bot.send_message(
        call.from_user.id,
        "Ahora escribe el @username del chat al que quieres eliminar",
        reply_markup=markup)

    def eliminacion_de_grupo_admin(message):
      global cursor
      global remove_admin
      dic_admin = {}
      dic_admin[message.chat.id] = []
      if not message.text.startswith("@"):
        dic_admin[call.from_user.id] = f"@{message.text}"
      else:
        dic_admin[call.from_user.id] = message.text

      try:
        remove_admin = bot.get_chat(dic_admin[call.from_user.id]).id
      except:
        bot.send_message(
            call.from_user.id,
            "El canal no existe o lo escribiste de forma incorrecta\nTe regreso atrás",
            reply_markup=markup)
        bot.send_message(call.from_user.id,
                         "Hola reima ;) En que te puedo ayudar",
                         reply_markup=botonera_panel)
        return

      cursor.execute('SELECT * FROM Canales')
      lista_canales = cursor.fetchall()
      contador = 0
      for linea in lista_canales:
        if remove_admin == linea[0]:
          contador += 1
          try:
            channel_admin = bot.get_chat_member(remove_admin,
                                                linea[1]).user.username
          except:
            channel_admin = ""
            pass
          break
      if contador == 0:
        bot.send_message(
            call.from_user.id,
            "Al parecer ese canal no estaba en la lista\nNo ha sido eliminado ningún canal"
        )
        bot.send_message(call.from_user.id,
                         "Bienvenido Reima ;) Qué planeas hacer?",
                         reply_markup=botonera_panel)
        return

      cursor.execute(f'DELETE FROM Canales WHERE ID_Canal={remove_admin}')

      if not channel_admin == "":
        bot.send_message(
            call.from_user.id,
            f"Ha sido eliminado el canal de <b>@{bot.get_chat(dic_admin[call.from_user.id]).username}</b> de la botonera\nDel cual, el administrador era @{channel_admin})",
            parse_mode="html")
        conexion.commit()
        return
      else:
        bot.send_message(
            call.from_user.id,
            f"Ha sido eliminado el canal de <b>@{bot.get_chat(dic_admin[call.from_user.id]).username}</b> de la botonera",
            parse_mode="html")
        conexion.commit()
        return

    bot.register_next_step_handler(msg, eliminacion_de_grupo_admin)

#---------Modificar el intervalo de tiempo de publicacion de botonera--------------------
  elif call.data == "Modificar tiempo":
    global guardar_variables
    if ejecutar_hilo == True:
      bot.send_message(reima, "Para el hilo antes de cambiar el tiempo!")
      return
    msg = bot.send_message(
        call.from_user.id,
        "Cada cuánto tiempo planeas que la botonera se publique?\n\nIngresa el valor en minutos",
        reply_markup=markup)

    def tiempo_botonera(message):
      global hora_publicacion
      global tiempo_de_espera_botonera
      if message.text.isdigit():
        tiempo_de_espera_botonera = int(message.text) * 60
        hora_publicacion = [time.time()]
        proxima_publicacion(message)
        guardar_variables()
        return tiempo_de_espera_botonera, bot.send_message(
            call.from_user.id,
            "Bienvenido Reima ;) Qué planeas hacer?",
            reply_markup=botonera_panel), hora_publicacion

      else:
        bot.send_message(
            call.from_user.id,
            "No has introducido correctamente un VALOR NÚMERICO en minutos para el tiempo de espera\nVuelve a intentarlo luego",
            reply_markup=markup)
        return

    bot.register_next_step_handler(msg, tiempo_botonera)

#-------------------------------------"Modificar eliminación"---------------------------------------
  elif call.data == "Modificar eliminación":
    global guardar_variables
    global tiempo_eliminacion_botonera
    if tiempo_eliminacion_botonera:
      msg = bot.send_message(
          call.from_user.id,
          f"Introduce el tiempo (EN MINUTOS) que quieres que quieres que la botonera sea eliminada\n\nSi quieres que se elimine cada vez que una nueva publicación de dicha botonera se haga escribe cualquier otra cosa\n\nTu tiempo actual de eliminacion es de {tiempo_eliminacion_botonera//60} minuto(s)",
          reply_markup=ForceReply())
    else:
      msg = bot.send_message(
          call.from_user.id,
          "Introduce el tiempo (EN MINUTOS) que quieres que quieres que la botonera sea eliminada\n\nSi quieres que se elimine cada vez que una nueva publicación de dicha botonera se haga escribe cualquier otra cosa",
          reply_markup=ForceReply())

    def eliminacion(message):
      global hilo_eliminaciones
      global botonera_panel
      global tiempo_eliminacion_botonera
      global hora_eliminacion_botonera
      if not message.text.isdigit():
        if tiempo_eliminacion_botonera == False:
          bot.send_message(message.chat.id,
                           "Bueno, igualmente no se estaba eliminando")
          bot.send_message(message.chat.id,
                           "Bienvenido Reima ;) qué tienes en mente?",
                           reply_markup=botonera_panel)
          return
        bot.send_message(
            message.chat.id,
            "Entendido! la dejaré eliminándose cada vez que una nueva sea publicada"
        )
        tiempo_eliminacion_botonera = False
        while not "stopped" in str(hilo_eliminaciones):
          time.sleep(1)
        guardar_variables()
        bot.send_message(
            call.from_user.id,
            f"El hilo de publicaciones ha sido detenido exitosamente mi queridísimo Reima ;D\n\n<u>Hilos activos</u>:\n{threading.active_count()}",
            parse_mode="html")
        return

      elif message.text.isdigit():
        if int(message.text) >= tiempo_de_espera_botonera / 60:
          bot.send_message(
              message.chat.id,
              f"El tiempo que has asignado es mayor al de la propia publicación de la botonera!, usa un valor menor.....\n\nActual tiempo de publicacion de la botonera: {tiempo_de_espera_botonera // 60} minutos"
          )
          return

        tiempo_eliminacion_botonera = int(message.text) * 60
        bot.send_message(
            message.chat.id,
            "Se comenzará el conteo del tiempo de eliminación cuando la botonera se vuelva a publicar :)"
        )
        guardar_variables()
        return

    bot.register_next_step_handler(msg, eliminacion)

#----------------------Mostrar archivo---------------------------------------------

  elif call.data == "Archivo de texto":
    texto = ""
    cursor.execute('SELECT * FROM Canales')
    lista_canales = cursor.fetchall()
    if lista_canales == []:
      bot.send_message(call.from_user.id,
                       f"<b>El archivo está vacío</b>:v",
                       parse_mode="html")
      return
    for linea in lista_canales:
      try:
        texto += f"Canal: @{bot.get_chat(linea[0]).username}, Admin: @{bot.get_chat(linea[1]).username}\n\n"
      except Exception as e:
        if "bot was kicked from the channel chat" in str(e):
          bot.send_message(
              call.from_user.id,
              f"Fuí expulsado del canal   {linea[0]}\n\nLo eliminaré de la botonera"
          )
          cursor.execute(f'DELETE FROM Canales WHERE ID_Canal={linea[0]}')
          conexion.commit()
          return
    bot.send_message(call.from_user.id,
                     f"<u>El contenido del archivo es</u>:\n\n{texto}",
                     parse_mode="html")
    return

#----------------------------Enviar archivos-----------------------------

  elif call.data == "Enviar archivos":
    with open("Botonera_Canales", "rb") as archivo_bd:
      bot.send_document(call.from_user.id, archivo_bd)
    cursor.execute('SELECT * FROM Canales')
    lista_canales = cursor.fetchall()
    with open("Lista_Canales.txt", "w") as archivo_txt:
      archivo_txt.seek(0)
      for item in lista_canales:
        archivo_txt.write(
            f"{bot.get_chat(item[0]).username} | {bot.get_chat(item[1]).username}\n"
        )
      archivo_txt.truncate()
      archivo_txt.seek(0)
    with open("Lista_Canales.txt", "r") as archivo_txt:
      try:
        bot.send_document(call.from_user.id, archivo_txt)
      except Exception as e:
        if "file must be non-empty" in str(e):
          bot.send_message(
              call.from_user.id,
              "El archivo de texto está vacío XD no lo puedo mandar así")
        else:
          bot.send_message(call.from_user.id,
                           f"Ha ocurrido una excepcion:\n\n{e}")

#----------------------------Limpiar archivo----------------------------

  elif call.data == "Limpiar archivo":

    contador = 0
    cursor.execute('SELECT * FROM Canales')
    lista_canales = cursor.fetchall()
    for tupla in lista_canales:
      for item in range(len(lista_canales)):
        if item == lista_canales.index(tupla):
          continue
        elif tupla[0] == lista_canales[item][0]:
          contador += 1
          lista_canales.remove(lista_canales[item])

    if contador == 0:
      bot.send_message(call.from_user.id,
                       "Al parecer no hay ningun canal repetido")
    else:
      bot.send_message(call.from_user.id,
                       f"Había(n) {contador} canal(es) repetido(s)")

    cursor.execute('DELETE FROM Canales')
    cursor.executemany('INSERT INTO Canales VALUES (?,?)', lista_canales)

#--------------------------Enviar Mensaje a Admins---------------------------------
  elif call.data == "Enviar Mensaje a Admins":
    msg = bot.send_message(
        call.from_user.id,
        "A continuacion, escribe el mensaje que quieres dar: ")

    def emitir_mensaje(message):
      cursor.execute('SELECT * FROM Canales')
      lista_canales = cursor.fetchall()

      for admin in lista_canales:
        try:
          bot.forward_message(admin[1], call.from_user.id, message.message_id)
          bot.send_message(
              admin[1],
              "Para más información, presione el siguiente botón",
              reply_markup=InlineKeyboardMarkup(row_width=1).row(
                  InlineKeyboardButton(
                      f"{bot.get_chat(call.from_user.id).username}",
                      url=
                      f"https://t.me/{bot.get_chat(call.from_user.id).username}"
                  )))
        except Exception as e:
          bot.send_message(
              message.chat.id,
              f"Se ha producido una excepcion intendando enviarle el mensaje a un admin:\n\n{e}"
          )

      # bot.forward_message(message.chat.id, message.chat.id, mensaje_a_enviar.message_id)
      # bot.send_message(admin[1], "Para más información, presione el siguiente botón", reply_markup=InlineKeyboardMarkup(row_width=1).row(InlineKeyboardButton(f"{bot.get_chat(call.from_user.id).username}", url=f"https://t.me/{bot.get_chat(call.from_user.id).username}")))

    bot.register_next_step_handler(msg, emitir_mensaje)

#----------------------------------Limpiar canales--------------------------------------------
  elif call.data == "Limpiar canales":
    global hora_eliminacion_botonera
    global mensajes_a_eliminar
    global mensajes_a_eliminar_globales
    for id_canal, id_message in mensajes_a_eliminar:
      try:
        bot.delete_message(id_canal, id_message)
      except:
        pass

    mensajes_a_eliminar = []

    for id_canal, id_message in mensajes_a_eliminar_globales:
      try:
        bot.delete_message(id_canal, id_message)
      except:
        pass

    mensajes_a_eliminar_globales = []
    hora_eliminacion_botonera = []
    guardar_variables()

    bot.send_message(
        call.from_user.id,
        "Las botoneras han sido eliminadas de los canales exitosamente :D")
    return


#--------------------------------🚨🚧Modo Reparacion🚧--------------------------------------
  elif call.data == "Modo reparacion":
    global modo_reparacion
    if not call.from_user.id == reima:
      bot.send_message(call.from_user.id,
                       "No te puedo dejar hacer esto si no eres Reima :)")
      return
    if modo_reparacion == False:
      msg = bot.send_message(
          call.from_user.id,
          "Seguro de querer entrar en el modo reparación?\n\nEscribe 'si' si es así, sino, simplemente escribe cualquier otra cosa"
      )

      def funcion_modo_reparacion(message):
        global modo_reparacion
        global ejecutar_hilo
        global publicaciones
        global hora_publicacion
        global hora_eliminacion_botonera
        global mensajes_a_eliminar
        try:
          global del_hilo
        except:
          pass
        
        if not message.text.lower() == "si":
          bot.send_message(call.from_user.id, "Te envío de vuelta al panel...")
          bot.send_message(call.from_user.id,
                           "Bienvenido Reima ;) Qué planeas hacer?",
                           reply_markup=botonera_panel)
          return
        else:
          if ejecutar_hilo == True:
            bot.send_message(call.from_user.id,
                             "Empezaré deteniendo el hilo de publicaciones")
            if mensajes_a_eliminar==[]:
                pass
            else:
              for item in mensajes_a_eliminar:
                try:
                  bot.delete_message(item[0], item[1])
                except Exception as e:
                  # bot.send_message(reima, f"Ha ocurrido una excepción intentando eliminar la botonera ya publicada en el canal @{bot.get_chat(item[0]).username}:\n{str(e)}")
                  pass
            mensajes_a_eliminar = []
            contador = 0
            hora_publicacion = []
            publicaciones = False
            ejecutar_hilo = False
            while not "stopped" in str(hilo_publicaciones):
              contador += 1
              time.sleep(1)
            if hora_eliminacion_botonera:
              hora_eliminacion_botonera=[]
              while not "stopped" in str(del_hilo):
                contador += 1
                time.sleep(1)
            bot.send_message(
                call.from_user.id,
                f"El hilo de publicaciones ha sido detenido exitosamente")
            modo_reparacion = True
            guardar_variables()
            bot.send_message(reima, "¡Bot detenido exitosamente!")
            return modo_reparacion
          else:
            modo_reparacion = True
            guardar_variables()
            bot.send_message(reima, "¡Bot detenido exitosamente!")
            return

      bot.register_next_step_handler(msg, funcion_modo_reparacion)
    elif modo_reparacion == True:
      bot.send_message(reima, "Procedo a quitarlo :v")
      modo_reparacion = False

  elif call.data == "si":
    cursor.execute("SELECT * FROM Canales")
    lista_canales = cursor.fetchall()
    contador = 0
    if lista_canales == []:
      bot.delete_message(call.from_user.id, mensajes_a_eliminar.id)
      bot.send_message(
          call.from_user.id,
          "Bueno, al parecer ni siquiera hay canales en la propia botonera Lol"
      )
      return
    for item in lista_canales:
      contador = 1
      canal = item[0]
      admin = item[1]
      if call.from_user.id == admin:
        cursor.execute(f'DELETE FROM Canales WHERE ID_Canal={canal}')
        conexion.commit()
        bot.delete_message(call.from_user.id, mensajes_a_eliminar.id)
        bot.send_message(
            call.from_user.id,
            f"Su canal {bot.get_chat(canal).username} ha sido eliminado exitosamente\n\nNo me siento del todo feliz con eso :( Estaré esperando tu regreso por si te arrepientes"
        )
        return
    else:
      bot.send_message(
          call.from_user.id,
          "Al parecer no es admin de ningún canal aquí\nNo he encontrado ninguno registrado a su nombre\nSi usted cree que sí, repórtelo a @mistakedelalaif"
      )
      return
  elif call.data == "no":
    bot.send_message(
        call.from_user.id,
        "ae\n\nVolvemos atrás entonces mulatón (o mulatona UwU)\n\n<b>*Suspira*</b>"
    )


@bot.message_handler(commands=["eliminar"])
def cmd_eliminar(message):
  global modo_reparacion
  if not message.chat.type == "private":
    return
  if modo_reparacion == True:
    funcion_reparacion(message)
    return
  global mensajes_a_eliminar
  eliminacion = InlineKeyboardMarkup(row_width=2)
  b1 = InlineKeyboardButton("Si :(", callback_data="si")
  b2 = InlineKeyboardButton("No! ¡Ni loco!", callback_data="no")
  eliminacion.add(b1, b2)
  mensajes_a_eliminar = bot.send_message(
      message.chat.id,
      "Estás SEGURO Que quieres eliminar el canal de la botonera? ;(",
      reply_markup=eliminacion)


@bot.message_handler(commands=["start", "help"])
def cmd_start(message):
  global modo_reparacion
  if not message.chat.type == "private":
    return
  if modo_reparacion == True:
    funcion_reparacion(message)
    return
  markup = ReplyKeyboardRemove()
  bot.send_message(
      message.chat.id,
      "Hola! 😁, Bienvenido a <b>Last Botonera</b> bot.\nAquí se encuentran los canales afiliados a la botonera y por ende, a <a href='https://t.me/LastHopePosting'>Last Hope</a>\n\n\n<u>Los comandos disponibles (por ahora) son</u>:\n\n/mostrar Si quiere SOLICITAR los CANALES de la Botonera e <b>Información</b> sobre el tiempo restante de la PRÓXIMA PUBLICACIÓN de dicha botonera en sus CANALES afiliados\n\n/ingresar Si quiere INGRESAR su CANAL EN la BOTONERA\n\n/start o /help Para mostrar ESTE mensaje de ayuda\n\n\n\n<u>Nota:</u>\nSi quiere notificar algo o tiene alguna duda consulte con mi creador y guapetón propietario de Last Hope ( ͡° ͜ʖ ͡°)\n\n👉<a href='https://t.me/mistakedelalaif'>Reima</a>👈",
      parse_mode="html",
      disable_web_page_preview=True,
      reply_markup=markup)
  #/promocionar LA MÁS FACHERA utilidad de este bot, escucha bien pepillo 🦻\nCon este comando puedes hacer pxp (promocion de tu canal a través de otro owner como tú) sin tener que acosar por privado al pobre muchacho (o muchacha, ve a ver tú) (¬‿¬) Simplemente me envias tu publicación de promoción, yo le pido que confirme si quiere hacer el pxp contigo y si acepta, directamente publico las promos en los respectivos canales. Como requisitos indispensables es que tanto tú como él me tienen que dar admin y permisos para publicar, el otro requisito es que ambos ya hayan hablado conmigo y no me tengan bloqueado ¿Qué esperas para comenzar? ಠ_ಠ


canal = "no"


#INGRESAR***********************************************************----------------INGRESAR
@bot.message_handler(commands=["ingresar"])
def cmd_ingresar(message, usuario=usuario, dic=dic):
  global modo_reparacion
  if not message.chat.type == "private":
    return
  if modo_reparacion == True:
    funcion_reparacion(message)
    return
  global canal
  global cursor
  dic[message.from_user.id] = []
  if " " in message.text or message.text.isdigit():
    canal = message.text.split(" ")[1]
    recibir_grupo(message, canal)

  else:
    msg = bot.send_message(
        message.chat.id,
        f"A continuación:\nUne este bot (@{usuario.username}) a tu canal y dale permisos de administración para que pueda publicar mensajes y continuar tu inserción a la botonera\n\nCuando lo hagas, escribe el nombre de usuario de tu canal (@username) seguido de este mensaje\n\n<u>Ejemplo:</u>\n@LastHopePosting",
        parse_mode="html",
        reply_markup=ForceReply())
    bot.register_next_step_handler(msg, recibir_grupo)


def recibir_grupo(message, canal=None):
  dic[message.from_user.id] = []
  if canal:
    if not canal.startswith("@") and not canal.startswith("-"):
      dic[message.from_user.id] = f"@{canal}"
    else:
      dic[message.from_user.id] = canal
  else:
    if not message.text.startswith("@") and not message.text.startswith("-"):
      dic[message.from_user.id] = f"@{message.text}"
    else:
      dic[message.from_user.id] = message.text

  bot.send_message(
      message.chat.id,
      "A continuación probaré si el <b>@username</b> es correcto y tengo derechos administrativos...",
      parse_mode="html")
  try:
    if not message.text.isdigit():
      chat_id = bot.get_chat(dic[message.from_user.id]).id
      dic[message.from_user.id] = []
      dic[message.from_user.id] = [chat_id]
      dic[message.from_user.id].append(message.from_user.id)
      #en dic[message.from_user.id]:
    else:
      dic[message.from_user.id].append(message.from_user.id)

    #El 1er elemento será el ID del canal
    #y el 2do será el ID del usuario en cuestion
  except:
    markup = ForceReply()
    msg = bot.send_message(
        message.chat.id,
        "Al parecer el canal/grupo que ingresaste no es correcto, ya que NO existe tigre\n\nVuelve a mirar si el <b>@username</b> es correcto\n\n<b>Te devolveremos al menú principal...</b>\nPara adjuntar tu canal a la botonera vuelve a escribir /ingresar y escribe el nombre si estás ABSOLUTAMENTE seguro de que es correcto\n\n<u>Nota:</u>\nSi tiene alguna duda o problema por favor contacte con el hermoso 👉<a href='https://t.me/mistakedelalaif'>Reima</a>👈",
        parse_mode="html",
        disable_web_page_preview=True)
    return
  else:

    cursor.execute('SELECT * FROM Canales')
    lista_canales = cursor.fetchall()
    if bot.get_chat_member(chat_id=dic[message.from_user.id][0],
                           user_id=bot.user.id).status == "administrator":
      for elemento in lista_canales:
        canal = elemento[0]
        admin = elemento[1]
        if canal == dic[message.from_user.id][0]:
          bot.send_message(
              message.chat.id,
              "Ese canal que ingresaste ya está en la botonera Velociraptor\nNo te hagas el listo >:D Vuelve a escribir /ingresar y prueba con otro canal"
          )
          return
        elif admin == message.from_user.id:
          bot.send_message(
              message.chat.id,
              "Al parecer, ya ingresaste otro canal aquí, deja espacio para los demás y no te quedes con la botonera tú solo listillo >:v"
          )
          return
      #si es un CANAL y no puede mandar mensajes, entra en la condicion
      if message.chat.type == "channel" and not bot.get_chat_member(
          chat_id=dic[message.from_user.id][0],
          user_id=bot.user.id).can_post_messages:
        bot.send_message(
            message.chat.id,
            f"Oye Mastodonte\nNo basta con que solamente me pongas de admin en tu canal si no me das permisos para publicar la botonera ahí\n\nPonme los permisos de publicación en @{bot.get_chat(dic[message.from_user.id][0]).username}, si no sabes cual es el que te digo pues dale todos y ya.\n\n<b>Cuando me pongas el permiso para publicar en tu canal</b>, vuelve a escribir /ingresar para volver :) Te estaré esperando",
            reply_markup=InlineKeyboardMarkup().row(
                InlineKeyboardButton(
                    "Ir a tu Canal",
                    url=
                    f"https://t.me/{bot.get_chat(dic[message.from_user.id][0]).username}"
                )),
            parse_mode="html")
        return

      else:
        canal = [(dic[message.from_user.id][0], dic[message.from_user.id][1])]

        cursor.executemany('INSERT INTO Canales VALUES (?,?)', canal)

        bot.send_message(
            message.chat.id,
            "PERFECTO! 🤩\n\nEl registro está completo mastodonte, añadiré tu canal a la botonera e igualmente AÑADIRÉ tu nombre de usuario por si ocurre algún problema a futuro con el bot y notificarte (❁´◡`❁).\n<u>Nota:</u>\nRecuerda que NO PUEDES quitar al bot de la administración o tu canal será ELIMINADO de la botonera",
            parse_mode="html")
        bot.send_message(
            message.chat.id,
            "Para ver tu canal en la botonera ingresa el comando /mostrar y verás como se hace la magia ;)"
        )
        if not bot.get_chat_member(chat_id=dic[message.from_user.id][0],
                                   user_id=bot.user.id).can_delete_messages:
          bot.send_message(message.chat.id,
                           """
                                     <b>ALERTA! EXTREMA ATENCION!</b>:
                                     
                                     Al parecer, no me has dado permiso en tu canal para eliminar mensajes, lo cual, no es nada bueno para ti ya que tengo capacidad de autoeliminado de mensajes
                                     
                                     Eso beneficia mucho que los canales no se saturen, cuando, por ejemplo, tu canal tiene 3 publicaciones al día y 500000 de una botonera pedante.

                                     Cuál es la mecánica/el procedimiento?:

                                     Segundos antes de publicarse la nueva botonera borraré la vieja ya publicada y se quedará únicamente la nueva, así la botonera se renueva en el tiempo y no satura el canal/grupo en cuestión con tanta publicidad. Se queda solamente con 1 botonera que se re nueva cada cierto tiempo
                                     
                                     Si realmente no quiere que esto ocurra, vaya a los ajustes de su canal y concédale al bot permisos para eliminar mensajes. Con cariño, Reima
                                     
                                     """,
                           parse_mode="html")
        conexion.commit()
        return
    else:
      bot.send_message(
          message.chat.id,
          ">:V AÚN NO ES ADMIN MMGUEVO\n\nHaz admin al bot y continuaremos el procedimiento\nnIntroduce nuevamente /ingresar para añadir tu canal\n\nY ASEGÚRATE DE QUE ESTA VEZ EL BOT SI SEA ADMIN (¬_¬ )",
          parse_mode="html")
      return


#-------------------Funcion MOSTRAR--------------------


@bot.message_handler(commands=["mostrar"])
def cmd_mostrar(message, conexion=conexion, hora_publicacion=hora_publicacion,):
  global cursor
  global modo_reparacion
  if modo_reparacion == True:
    funcion_reparacion(message)
    return
  global foto_LastBotonera
  foto_LastBotonera.seek(0)
  bot.send_chat_action(message.chat.id, action="upload_photo")
  botonera = InlineKeyboardMarkup(row_width=2)
  #Primeramente, tengo que asegurarme que el bot tenga permisos para publicar en el canal
  cursor = conexion.cursor()
  cursor.execute('SELECT * FROM Canales')
  lista_canales = cursor.fetchall()
  for linea in lista_canales:
    canal = linea[0]
    administrador = linea[1]
    try:
      bot.get_chat(canal)
      member = bot.get_chat_member(chat_id=canal, user_id=bot.user.id)
    except Exception as e:
      if "chat not found" in str(e):
        bot.send_message(reima, f"Me han eliminado de un canal, iré a notificarle a su administrador y a continuacion lo eliminaré\n\nEl canal es {canal}")
        cursor.execute(f'DELETE FROM Canales WHERE ID_Canal={canal}')
        try:
          bot.send_message(administrador, "Al parecer me has eliminado de tu canal, lo eliminarré de mi lista de canales")
        except:
          continue
      elif not member.status == 'administrator' and str(administrador) != str(1413725506):
        cursor.execute(f'DELETE FROM Canales WHERE ID_Canal={canal}')
        bot.send_message(
            1413725506,
            f"Se ha eliminado el canal {bot.get_chat(canal).username} por no dejarme como administrador >:("
        )
        bot.send_message(
            administrador,
            f"<u>ATENCIÓN</u>:\n Se ha eliminado el canal {bot.get_chat(canal).username} por no dejarme como administrador >:(\n\nPara ingresar de nuevo el canal en la botonera escriba /ingresar",
            parse_mode="html")
      else:
        bot.send_message(reima, f"Ha ocurrido el siguiente error:\n\n{e}\n\nSe eliminará el canal: {canal}")
        cursor.execute(f'DELETE FROM Canales WHERE ID_Canal={canal}')

  conexion.commit()
  #Ahora pondré los canales de la BD a una lista
  cursor.execute('SELECT * FROM Canales')
  lista_canales = cursor.fetchall()
  for linea in lista_canales:
    canal = linea[0]
    #Si el bot tiene permisos pues agrega el canal a la botonera
    nombre = bot.get_chat(canal).title
    enlace = f"https://t.me/{bot.get_chat(canal).username}"
    boton = InlineKeyboardButton(nombre, url=enlace)
    botonera.add(boton)
  foto_LastBotonera.seek(0)
  botonera.row(
      InlineKeyboardButton("(☞ﾟヮﾟ)☞ ÚNETE A LA BOTONERA ☜(ﾟヮﾟ☜)",
                           url="https://t.me/LastBotoneraBot"))
  foto_LastBotonera.seek(0)
  bot.send_photo(
      message.chat.id,
      foto_LastBotonera,
      caption=
      "¡Si!, ¡Es eso mismo que estás pensando!\n Literalmente, <b>La Última Botonera</b> baby (☞ﾟヮﾟ)☞ ☜(ﾟヮﾟ☜)\n\n¡No pierdas la oportunidad de unirte a alguno!",
      parse_mode="html",
      reply_markup=botonera)
  foto_LastBotonera.seek(0)
  if publicaciones == False:
    return bot.send_message(
        message.chat.id,
        "Ahora mismo, no estoy publicando la botonera, quizás en un momento sí lo haré\n\nPero todo depende del baboso de <a href='https://t.me/mistakedelalaif'>Reima</a>, no de mí :(",
        parse_mode="html",
        disable_web_page_preview=True)
  else:
    proxima_publicacion(message)
    if hora_eliminacion_botonera and tiempo_eliminacion_botonera:
      proxima_eliminacion_botonera(message)
    return


@bot.message_handler(commands=['id'])
def start(message):
  global modo_reparacion
  if modo_reparacion == True:
    funcion_reparacion(message)
    return
  texto = f"El ID del bot es: {bot.user.id}\n\n"
  texto += f"Tu ID es: {message.from_user.id}\n\n"  #1413725506
  texto += f"El ID de Last Hope es: {bot.get_chat('@LastHopePosting').id}\n\n"  #-1001161864648
  texto += f"El ID del chat es: {message.chat.id}\n"

  bot.reply_to(message, texto)




@bot.message_handler(commands=["promo"])
def start(message):
  global modo_reparacion
  if not message.chat.type == "private":
    return
  if modo_reparacion == True:
    funcion_reparacion(message)
    return
  global foto_lastHope
  markup = InlineKeyboardMarkup(row_width=3)
  b1 = InlineKeyboardButton("🌚Únete🌝", url="http://t.me/lasthopeposting")
  b2 = InlineKeyboardButton("✨Pxp✨", url="http://t.me/mistakedelalaif")
  b3 = InlineKeyboardButton("🔥Grupo🔥", url="http://t.me/lasthopepost")
  markup.add(b1, b2, b3)
  mensaje = "<b>¡HOLA ZORRA!</b> 😈\n\nCansad@ de ir por canales sin ver a uno que robe los Memes/Shitpost de otros canales?🥵\nCansad@ de conversaciones completamente normales sin nada que haga sangrar tus ojos?\nCansad@de que nadie entienda tus parloteos intelectuales? 🧠\nCansado de leer esto como un comercial?🌞🍷\n\n¡No te preocupes! ¡LA SOLUCIÓN acaba de LLEGAR! \nSólo únete a:\n\n<a href='http://t.me/lasthopeposting'>¡LAST HOPE!</a>\n\nPara sentir el VERDADERO salseo en esas nalgas negras😳\n\nTambién tenemos chat <s>hot con mujerzuelas</s>  😳\n\n<u>Atentamente</u>:\nTu mamá en tanga ❤️"

  foto_lastHope.seek(0)
  bot.send_photo(message.chat.id,
                 foto_lastHope,
                 caption=mensaje,
                 parse_mode="html",
                 reply_markup=markup)
  foto_lastHope.seek(0)


@bot.message_handler(func=lambda x: True)
def mensajes_al_chat(message):
  global modo_reparacion
  if not message.chat.type == "private":
    return
  if modo_reparacion == True:
    funcion_reparacion(message)
    return
  bot.send_message(
      message.chat.id,
      "Ingresa uno de los comandos disponibles en el bot, chacal\n\nA continuación, escribe /start para mostrar mis comandos de uso\n\nNo harás nada si no escribes nada (¬_¬ )"
  )
  return


#----------------------------Servidor de Flask------------------------------------








bot.infinity_polling()
