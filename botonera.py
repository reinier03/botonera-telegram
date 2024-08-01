from flask import Flask, request
import telebot
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton
from telebot.types import ForceReply
import threading
import time
import os
import sqlite3
import dill
from waitress import serve

local_ip = ""
hora_eliminacion_botonera=False

try:
  os.chdir(os.path.dirname(os.path.abspath(__file__)))
  #Esta es la BD para la lista de canales
  conexion = sqlite3.connect("Botonera_Canales.bd", check_same_thread=False)
  cursor = conexion.cursor()
  
  OS = ""

  if os.name == "nt":
    OS = '\\'
  else:
    OS = "//"

  
  
  try:
    cursor.execute('CREATE TABLE Canales (ID_Canal INTEGER, ID_Admin INTEGER, Username VARCHAR)')
  except Exception as e:
    if str(e) == "table Canales already exists":
      pass
  del_hilo = ""
  #-------------------Variables a utilizar en el codigo-------------------------------
  directorio_actual=f"{os.path.dirname(os.path.abspath(__file__))}{OS}"
  reima = 1413725506
  bot = telebot.TeleBot(os.environ["token"])
  admin=os.environ["admin"]
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
  mensajes_dic={"/start": "", "/mostrar": ""}

  #--------------------------------------------------------------------------
  server_address = ""



  #CARGAR las variables si existe ya un archivo
  if os.path.isfile("variables"):
    with open("variables", "rb") as archivo:
      variables_cargadas = dill.load(archivo)

      for var_name, var_value in variables_cargadas.items():
        globals()[var_name] = var_value


  #porqué guardo las variables? por si ocurre algún problema con el host
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
          "mensajes_a_eliminar_globales": mensajes_a_eliminar_globales,
          "mensajes_dic": mensajes_dic
      }
      dill.dump(dict1, archivo)



  try:
    request.host_url
  except:
    app = Flask(__name__)
    
    @app.route('/', methods=['GET'])
    def index():
      return 'OK', 200

  def flask():
    app.run(host="0.0.0.0", port=5000)





  try:
    request.host_url
  except:
    hilo_flask=threading.Thread(name="hilo_flask", target=flask)
    hilo_flask.start()


  bot.send_message(reima, "Estoy online bitch >:)")

  if str(admin)==str(reima):
      cursor.execute('SELECT * FROM Canales')
      lista_canales=cursor.fetchall()
      if lista_canales==[]:
          lasthope=[(-1001161864648, 1413725506, "LastHopePosting")]
          cursor.executemany('INSERT INTO Canales VALUES (?,?,?)', lasthope)
          conexion.commit()
  
  

  try:
    foto_lastHope = open(
        f"{os.path.dirname(os.path.abspath(__file__))}{OS}Last_Hope.jpg", 'rb')

  except:
    pass
  
  
  #Comprobación de foto de promo de botonera
  try:
    foto_botonera = open(
        f"{os.path.dirname(os.path.abspath(__file__))}{OS}botonera.jpg",
        'rb')
  except:
    try:
      bot.send_message(admin, "Al parecer, no hay una foto promocional para la botonera\n\nPara establecer una escriba /panel_administrador y presione en el botón 'Editar Bot 🗿' y ahí en el botón de 'Foto Promocional'")
      foto_botonera=False
    except:
      pass

  def funcion_reparacion(message):
    bot.send_message(
        message.chat.id,
        "🚨🚧Bot en Modo Construcción🚧🚨\n\nLo siento tigre, al parecer algo estalló en mi y ahora me ESTÁN reparando :( \n\n Vuelve luego a ver si ya me recuperé y seguir con las botoneras"
    )
    return



  def proxima_publicacion(message):
    global tiempo_de_espera_botonera
    global hora_publicacion
    horas = 0
    minutos_restantes = hora_publicacion[0] + tiempo_de_espera_botonera - float(time.time())
    minutos_restantes = round(minutos_restantes / 60)
    while True:
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




  def eliminar_botonera():
    global hora_eliminacion_botonera
    global tiempo_eliminacion_botonera
    global mensajes_a_eliminar
    global id_mensajes_fijados
    while hora_eliminacion_botonera:
      if publicaciones == True and time.localtime(
          hora_eliminacion_botonera[0] +
          tiempo_eliminacion_botonera) <= time.localtime(time.time()):
        for item in mensajes_a_eliminar:
          try:
            bot.delete_message(item[0], item[1])
          except Exception as e:
            print(f"Excepcion intentando eliminar una botonera: \n\n{e}")

        mensajes_a_eliminar = []
        hora_eliminacion_botonera = []
        bot.send_message(admin, "botonera eliminada")
        guardar_variables()
        return
      else:
        time.sleep(30)


  def hilo_eliminaciones():
    global del_hilo
    del_hilo = threading.Thread(name="hilo_eliminar_botonera", target=eliminar_botonera)
    del_hilo.start()


  if hora_eliminacion_botonera and tiempo_eliminacion_botonera:
    hilo_eliminaciones()


  def hacer_publicaciones():
    global tiempo_eliminacion_botonera
    global mensajes_a_eliminar_globales
    global hora_eliminacion_botonera
    global mensajes_a_eliminar
    global publicaciones
    global foto_botonera
    global ejecutar_hilo
    global hora_publicacion
    global admin
    global conexion
    global cursor
    
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
                #bot.send_message(admin, f"Ha ocurrido una excepción intentando eliminar la botonera ya publicada en el canal @{bot.get_chat(item[0]).username}:\n{str(e)}")
                a = "lol"
              except:
                pass

          mensajes_a_eliminar = []
        try:
          foto_botonera.seek(0)
        except:
          pass
        publicaciones = True
        bot.send_message(admin, "Publicaré la botonera ahora")
        botonera = InlineKeyboardMarkup(row_width=1)
        #Primeramente, tengo que asegurarme que el bot tenga permisos para publicar en el canal
        try:
          cursor.execute('SELECT * FROM Canales')
        except:
          bot.send_message(admin, "¡Ni siquiera hay canales en la botonera!\nPrueba agregando alguno y vuelve aquí")
          mensajes_a_eliminar = []
          ejecutar_hilo = False
          hora_publicacion = []
          publicaciones = False
          hora_eliminacion_botonera = []
          return
        
        lista_canales = cursor.fetchall()
        
        if len(lista_canales)==0:
          bot.send_message(admin, "¡Ni siquiera hay canales en la botonera!\nPrueba agregando alguno y vuelve aquí")
          mensajes_a_eliminar = []
          ejecutar_hilo = False
          hora_publicacion = []
          publicaciones = False
          hora_eliminacion_botonera = []
          return
        
        for linea in lista_canales:
          canal = linea[0]
          administrador = linea[1]
          canal_username = linea[2]
          
          if administrador==admin:
            continue
          try:
            bot.get_chat(canal).title
            member = bot.get_chat_member(chat_id=canal, user_id=bot.user.id)
          except Exception as e:
            cursor.execute(f'DELETE FROM Canales WHERE ID_Canal={canal}')
            conexion.commit()
            try:
              if "chat not found" in str(e):
                bot.send_message(admin, f"Fuí expulsado del canal @{bot.get_chat(canal).username}\n\nLo eliminaré de la botonera")
                try:
                    bot.send_message(administrador, f"He eliminado tu canal @{bot.get_chat(canal).username} de la botonera >:( Por haberme sacado\n\nVuelve a unirme a él como admin con derechos y regresa aquí escribiendome /ingresar para unirte de nuevo")
                except:
                    pass
              
              elif "bot was kicked from the channel chat" in str(e):
                bot.send_message(admin, f"Al parecer me han eliminado del canal: @{bot.get_chat(canal).username}, procedo a eliminarlo")
                try:
                  bot.send_message(administrador, f"Al parecer me han eliminado del canal: @{bot.get_chat(canal).username}\nEliminaré dicho canal de la botonera\n\nVuelve a unirme a él como admin con derechos y regresa aquí escribiendome /ingresar para unirte de nuevo\n\nTe estaré esperando :)")
                except:
                  pass
                
                
              else:
                try:
                  bot.send_message(admin, f"Ha ocurrido el siguiente error:\n\n{e}\n\nSe eliminará el canal: @{bot.get_chat(canal).username}\nSu administrador es @{bot.get_chat(administrador).username}")
                except Exception as ex:
                  try:
                    bot.send_message(admin, f"Excepción en el canal: @{bot.get_chat(canal).username} \n\n{ex}\n\n Lo he eliminado")
                  except:
                    bot.send_message(admin, f"Excepción en un canal: \n\n{ex}\n\n Lo he eliminado")
                try:
                  bot.send_message(administrador, f"Ha ocurrido un error, se eliminará tu canal @{bot.get_chat(canal).username}\n\nRevisa que tu canal me tenga concedido derechos administrativos así como también para publicar, cuando arregles el problema vuelve a escribirme /ingresar \n\nTe estaré esperando :)")
                except:
                  pass
                
            except:
              bot.send_message(admin, f"Ha sido eliminado el canal @{canal_username} de la botonera\nEl error fué el siguiente:\n\n{e}")
              try:
                bot.send_message(administrador, f"PELIGRO‼‼¡Tu canal @{canal_username} ha sido eliminado por algún tipo de error!\n\nRevisa que el bot de la botonera aún esté en el canal y tenga los permisos de administración")
              except:
                pass
              

        #Ahora actualizaré la lista con los canales de la BD
        cursor.execute('SELECT * FROM Canales')
        lista_canales = cursor.fetchall()
        
        if len(lista_canales)==0:
          bot.send_message(admin, "¡Ni siquiera hay canales en la botonera!\nPrueba agregando alguno y vuelve aquí")
          mensajes_a_eliminar = []
          ejecutar_hilo = False
          hora_publicacion = []
          publicaciones = False
          hora_eliminacion_botonera = []
          return
        
        for linea in lista_canales:
          try:
            canal = linea[0]
            #Si el bot tiene permisos pues agrega el canal a la botonera
            nombre = bot.get_chat(canal).title
            enlace = f"https://t.me/{bot.get_chat(canal).username}"
            boton = InlineKeyboardButton(nombre, url=enlace)
            botonera.add(boton)
            canal_username = linea[2]
          except:
            cursor.execute(f'DELETE FROM Canales WHERE ID_Canal={canal}')
            conexion.commit()
            try:
              bot.send_message(administrador, f"Por algún error, tu canal @{bot.get_chat(canal).username} no me deja publicar la botonera, por favor revise que todo está bien y vuelva a escribir /ingresar\n\nTe estaré esperando ;)")
            except:
              try:
                bot.send_message(administrador, f"PELIGRO‼‼\n¡Tu canal @{canal_username} ha sido eliminado por algún tipo de error!\n\nRevisa que el bot de la botonera aún esté en el canal y tenga los permisos de administración\n\nLuego vuelve conmigo y escribe /ingresar para volverlo a unir :)")
              except:
                pass
              try:
                bot.send_message(
                    admin,
                    f"Excepcion al enviar el mensaje a @{bot.get_chat(canal).username}: \n{e}\n\nEl canal fué eliminado de la botonera")
              except:
                bot.send_message(admin, f"Ha ocurrido una excepcion al enviar La Botonera en el canal @{canal_username}\n\nEl canal fué eliminado de la botonera")
          
          finally:  
            continue
          
        botonera.row(
            InlineKeyboardButton("(☞ﾟヮﾟ)☞ ÚNETE A LA BOTONERA ☜(ﾟヮﾟ☜)",
                                url=f"https://t.me/{bot.user.username}"))
        for linea in lista_canales:
          try:
            foto_botonera.seek(0)
          except:
            pass
          canal = linea[0]
          administrador = linea[1]
          canal_username = linea[2]
          try:
            if foto_botonera==False:
              if mensajes_dic["/mostrar"]== "":
                msg = bot.send_message(
                    int(canal),
                    "A continuación, Los Canales de la <b>MEJOR Botonera</b> de Telegram 😀🎉",
                    parse_mode="html",
                    reply_markup=botonera)
              else:
                msg = bot.send_message(int(canal), mensajes_dic["/mostrar"], parse_mode="MarkdownV2", reply_markup=botonera)
            else:
              #Si el usuario no ha personalizado el mensaje, entonces haz esto
              if mensajes_dic["/mostrar"]== "":
                msg = bot.send_photo(
                    int(canal),
                    photo=foto_botonera,
                    caption=
                    "A continuación, Los Canales de la <b>MEJOR Botonera</b> de Telegram 😀🎉",
                    parse_mode="html",
                    reply_markup=botonera) #Editar texto
              #Si lo personalizó entonces haz esto
              else:
                msg = bot.send_photo(int(canal), photo=foto_botonera, caption=mensajes_dic["/mostrar"], parse_mode="MarkdownV2", reply_markup=botonera)
            try:
              bot.pin_chat_message(int(canal), msg.message_id, disable_notification=True)
              time.sleep(3)
              bot.delete_message(int(canal), msg.message_id+1)
            except:
              pass
            mensajes_a_eliminar.append((canal, msg.message_id))
            mensajes_a_eliminar_globales.append((canal, msg.message_id))

          except Exception as e:
            if administrador == admin:
              # try:
              #   bot.send_message(
              #       administrador,
              #       f"OYE ESTÚPIDA!\n\nEste <a href='https://t.me/{bot.get_chat(canal).username}'>Canal</a> tuyo no me deja mandar la botonera porque no tengo permisos para publicar! <b>Lo dejaré ahí</b>, porque eres su dueño pero MUEVE EL CULO!",
              #       parse_mode="html")
              # except:
              #   bot.send_message(
              #       administrador,
              #       f"OYE ESTÚPIDA!\n\nHay un canal tuyo que no me deja mandar la botonera en sus publicaciones porque me expulsó probablemente! <b>Lo dejaré ahí</b>, porque eres su dueño pero MUEVE EL CULO!",
              #       parse_mode="html")
              continue
            
            cursor.execute(f'DELETE FROM Canales WHERE ID_Canal={canal}')
            conexion.commit()
            if "need administrator rights in the channel chat" in str(e):
              try:
                bot.send_message(administrador, f"No me has dado permisos administrativos en tu canal @{bot.get_chat(canal).username}, tengo que sacar tu canal de la botonera hasta que no lo hagas.\n\nCuando me hayas dado los permisos necesarios en tu canal, vuelve a escribir /ingresar :) te estaré esperando", reply_markup=InlineKeyboardMarkup().row(InlineKeyboardButton("Ir a tu Canal", url=f"https://t.me/{bot.get_chat(canal).username}")))
              except Exception as e:
                bot.send_message(admin, f"El canal @{bot.get_chat(canal).username} no me dió permisos administrativos para publicar, lo borré de la botonera")
                
              bot.send_message(
                  admin,
                  f"<b>Atención</b>\n\nHe eliminado el canal: @{bot.get_chat(canal).username} y su admin: @{bot.get_chat(admin).username}, por no dejarme permisos de publicación allí",
                  parse_mode="html")
              
            elif "bot is not a member of the channel chat" in str(e):
              try:
                bot.send_message(admin, f"El bot ha sido eliminado de @{bot.get_chat(canal).username} y su admin: @{bot.get_chat(admin).username} voy a eliminarlo de la lista")
              except:
                bot.send_message(admin, f"El bot ha sido expulsado de @{bot.get_chat(canal).username} voy a eliminarlo de la lista de canales")
              try:
                bot.send_message(administrador, f"El canal @{bot.get_chat(canal).username} ha sido eliminado de la botonera por haberme expulsado del canal, úneme de nuevo y dame permisos administrativos para volverlo a unir, luego escribeme /ingresar \n\n:)")
              except:
                pass
                
              continue
              
            elif bot.get_chat_member(canal, bot.user.id).status=='left':
              bot.send_message(admin, f"Me expulsaron de @{bot.get_chat(canal).username}, lo eliminaré de la botonera")
              try:
                bot.send_message(administrador, f"Su canal @{bot.get_chat(canal).username}, ha sido eliminado de la botonera por haberme expulsado\n\nPara Introducirlo nuevamente agregueme como administrador e ingrese aquí /ingresar \n\nTe estaré esperando :)")
              except:
                pass
              continue
            
            else:
              try:
                bot.send_message(administrador, f"Por algún error, tu canal @{bot.get_chat(canal).username} no me deja publicar la botonera, por favor revise que todo está bien y vuelva a escribir /ingresar\n\nTe estaré esperando ;)")
              except:
                try:
                  bot.send_message(administrador, f"PELIGRO‼‼\n¡Tu canal @{canal_username} ha sido eliminado por algún tipo de error!\n\nRevisa que el bot de la botonera aún esté en el canal y tenga los permisos de administración\n\nLuego vuelve conmigo y escribe /ingresar para volverlo a unir :)")
                except:
                  pass
              try:
                bot.send_message(
                    admin,
                    f"Excepcion al enviar el mensaje a @{bot.get_chat(canal).username}: \n{e}\n\nEl canal fué eliminado de la botonera")
              except:
                bot.send_message(admin, f"Ha ocurrido una excepcion al enviar La Botonera el canal @{canal_username}\n\nEl canal fué eliminado de la botonera")
          finally: 
            continue
          
              

        conexion.commit()
        try:
          foto_botonera.seek(0)
        except:
          pass
        hora_publicacion = [time.time()]
        if tiempo_eliminacion_botonera:
          hora_eliminacion_botonera = []
          hora_eliminacion_botonera.append(time.time())
          hilo_eliminaciones()
        proxima_publicacion(admin)
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
    global admin
    if not message.chat.type == "private":
      return
    global foto_botonera
    dic_admin = {}
    dic_admin[message.from_user.id] = []
    if message.chat.id == admin:
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
      b7 = InlineKeyboardButton("Editar Bot 🗿", callback_data="Modificar Mensajes")
      b8 = InlineKeyboardButton("Ver Archivo de canales 👀",
                                callback_data="Archivo de texto")
      b9 = InlineKeyboardButton("Administrar Archivo de Canales 🌠",
                                callback_data="Enviar archivos")
      b10 = InlineKeyboardButton("Limpiar archivo ✨",
                                callback_data="Limpiar archivo")
      b11 = InlineKeyboardButton("Enviar Mensaje a Admins 🎫",
                                callback_data="Enviar Mensaje a Admins")
      b12 = InlineKeyboardButton("Limpiar los canales",
                                callback_data="Limpiar canales")
      b13 = InlineKeyboardButton("🚨🚧Modo reparacion🚧🚨",
                                callback_data="Modo reparacion")
      botonera_panel.add(b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13)
      bot.send_message(message.chat.id, f"Bienvenido {bot.get_chat(admin).first_name} ;) Qué planeas hacer?",
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
    global foto_botonera
    global admin
    try:
      foto_botonera.seek(0)
    except:
      pass
    markup = ForceReply()
    cancelar_markup=InlineKeyboardMarkup(row_width=1)
    cancelar_markup.add(InlineKeyboardButton("Cancelar Operación", callback_data="Cancelar Operacion"))
    
    if call.data == "Cancelar Operacion":
      bot.send_message(call.from_user.id, "Operación Cancelada exitosamente :)")
      return

    #-----------------Iniciar Bucle de publicaciones--------------------
    elif call.data == "Iniciar bucle":
      if ejecutar_hilo == True:
        bot.send_message(call.from_user.id, "Ya estoy ejecutando un hilo pringado >:(")
        return
      else:
        ejecutar_hilo = True
        bot.send_message(call.from_user.id, "Voy a ejecutar el hilo de publicaciones :D")
        return iniciar_hilo()

  #-----------------------Parar bucle---------------------------------------------------
    elif call.data == "Parar bucle":
      global publicaciones
      global hora_publicacion
      if publicaciones == False:
        return bot.send_message(
            call.from_user.id,
            "Ni siquiera está activo el bucle :l\n\nPrueba otra cosa")

      else:

        def parar_bucle():
          # detener botonera
          global mensajes_a_eliminar
          global publicaciones
          global hora_publicacion
          global ejecutar_hilo
          global hilo_publicaciones
          global hora_eliminacion_botonera
          global admin
          try:
            global del_hilo
          except:
            pass
          bot.send_message(call.from_user.id, "Voy a detener el hilo de publicaciones")
          if mensajes_a_eliminar == []:
            pass
          else:
            for item in mensajes_a_eliminar:
              try:
                bot.delete_message(item[0], item[1])
              except Exception as e:
                bot.send_message(admin, f"Ha ocurrido una excepción intentando eliminar la botonera ya publicada en el canal @{bot.get_chat(item[0]).username}:\n\n{str(e)}")
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
              f"Los hilos de publicaciones han sido detenidos exitosamente mi queridísimo {bot.get_chat(admin).first_name} ;D\n\n<u>Hilos activos</u>:\n{threading.active_count()}",
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
                                      f"Bienvenido {bot.get_chat(admin).first_name} ;) Qué planeas hacer?",
                                      reply_markup=botonera_panel)

          if bot.get_chat_member(chat_admin,
                                bot.user.id).status != "administrator":
            bot.send_message(
                call.from_user.id,
                "No soy admin en ese chat, pero bueno, ya sabrás tú lo que haces...."
            )

          canal = [(chat_admin, call.from_user.id, bot.get_chat(dic_admin[message.chat.id]).username)]
          cursor.executemany('INSERT INTO Canales VALUES (?,?,?)', canal)

          bot.send_message(
              call.from_user.id,
              f"El canal {bot.get_chat(dic_admin[message.chat.id]).username} ha sido agregado exitosamente a la botonera"
          )
          conexion.commit()
          del dic_admin[message.chat.id]
          return bot.send_message(call.from_user.id,
                                  f"Bienvenido {bot.get_chat(admin).first_name} ;) Qué planeas hacer?",
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
                          f"Hola {bot.get_chat(admin).first_name} ;) En que te puedo ayudar",
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
                          f"Bienvenido {bot.get_chat(admin).first_name} ;) Qué planeas hacer?",
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
        bot.send_message(admin, "Para el hilo de publicaciones antes de cambiar el tiempo!")
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
              f"Bienvenido {bot.get_chat(admin).first_name} ;) Qué planeas hacer?",
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
        global admin
        if not message.text.isdigit():
          if tiempo_eliminacion_botonera == False:
            bot.send_message(message.chat.id,
                            "Bueno, igualmente no se estaba eliminando")
            bot.send_message(message.chat.id,
                            f"Bienvenido {bot.get_chat(admin).first_name} ;) qué tienes en mente?",
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
              f"El hilo de publicaciones ha sido detenido exitosamente mi queridísimo {bot.get_chat(admin).first_name} ;D\n\n<u>Hilos activos</u>:\n{threading.active_count()}",
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
      
      
  #----------------------Modificar Mensajes------------------------------------------
  # elif call.data == "Modificar Mensajes":
    elif call.data == "Modificar Mensajes":
      markup=InlineKeyboardMarkup(row_width=1)
      markup.add(InlineKeyboardButton("Foto Promocional", callback_data="Foto_promo"))
      markup.add(InlineKeyboardButton("Mensaje de Bienvenida", callback_data="Bienvenida"))
      markup.add(InlineKeyboardButton("Mensaje de Promoción", callback_data="Promo"))
      msg=bot.send_message(call.from_user.id, "<u>Explicación</u>\n\nEn esta sección podrá editar los principales mensajes que envío al resto de usuarios y en la promo de botonera\nSeleccione a continuación, el tipo de mensaje que quiere editar...", parse_mode="html", reply_markup=markup)
    
    elif call.data == "Foto_promo":
      
      if not foto_botonera==False:
        with open("botonera.jpg", "rb") as archivo:
          bot.send_photo(call.from_user.id, archivo, caption="Esta es actualmente la foto de Promoción de La Botonera")
      
      msg=bot.send_message(call.from_user.id, "A continuación, Envíame la foto de promoción que se enviará junto con la Botonera de Canales")
      
      
      def recibir_foto(message):
        global foto_botonera
        if not message.photo:
          bot.send_message(call.from_user.id, "¡Error!\n¡Tenías que enviar la foto! Te regreso al menú principal :(")
          bot.send_message(call.from_user.id, f"Hola {bot.get_chat(admin).first_name} ;) En que te puedo ayudar",
                          reply_markup=botonera_panel)
        else:
          with open(f'{os.path.dirname(os.path.abspath(__file__))}{OS}botonera.jpg', "wb") as foto:
            foto.write(bot.download_file(bot.get_file(message.photo[-1].file_id).file_path))
            
          foto_botonera=open(f"{os.path.dirname(os.path.abspath(__file__))}{OS}botonera.jpg", "rb")
          
          bot.send_message(call.from_user.id, "¡Foto Promocional guardada exitosamente! :)")
          bot.send_message(call.from_user.id, f"Hola {bot.get_chat(admin).first_name} ;) En que te puedo ayudar", reply_markup=botonera_panel)
          return
        
        
      bot.register_next_step_handler(msg, recibir_foto)
    
    
    elif call.data == "Promo":
      if mensajes_dic["/mostrar"] == "":
        msg=bot.send_message(call.from_user.id,"<u>El mensaje en cuestión, es el siguiente</u>:\n\nA continuación, Los Canales de la <b>MEJOR Botonera</b> de Telegram 😀🎉", parse_mode="html", reply_markup=markup)
      else:
        msg=bot.send_message(call.from_user.id,f"__El mensaje en cuestión, es el siguiente__:\n\{mensajes_dic['/mostrar']}", parse_mode="MarkdownV2", reply_markup=markup)
        
      bot.send_message(call.from_user.id, 
                            """A Continuación te dejaré una guía de estilos con sus códigos para escribir mejor, a la izquierda de cada fila está el resultado y el nombre del estilo y a la derecha está el código que debes introducir para generar el mismo resultado
                            <u>Subrayado</u> : __texto en subrayado__
                            <b>Negrita</b> : *texto en negrita*
                            <i>Cursiva</i> : _texto en cursiva_
                            <s>Tachado</>  : ~texto en tachado~
                            <code>Monoespaciado</code> : '''Texto en monoespaciado'''
                            <span class='tg-spoiler'>Spoiler</span> : |||Texto en Spoiler|||
                            <a href='https://google.com'>Enlace</a> : [Texto con Enlace](https://google.com)""", parse_mode="html")
      msg2=bot.send_message(call.from_user.id, "Seguido de este mensaje escriba un nuevo mensaje Promocional :)\n\nPresione en el botón <b>Cancelar</b> para dejar el que ya está", parse_mode="html", reply_markup=cancelar_markup)
      def nuevo_mensaje_promo(message):
        if message.text.lower() == "cancelar":
          bot.send_message(message.chat.id, f"Entendido {bot.get_chat(admin).first_name} ;) Dejaré el mensaje anterior intacto")
          return
        mensajes_dic["/mostrar"]=message.text
        bot.send_message(message.chat.id, f"Perfecto\nEl nuevo mensaje será:\n\n{mensajes_dic['/mostrar']}", parse_mode="MarkdownV2")
        guardar_variables()
        return
      
      bot.register_next_step_handler(msg2, nuevo_mensaje_promo)
      
      
    elif call.data == "Bienvenida":


      if mensajes_dic["/start"] == "":
        msg=bot.send_message(call.from_user.id, f"<u>El mensaje en cuestión, es el siguiente</u>:\n\nHola!😁, Bienvenido a la botonera más genial de Telegram. Los comandos disponibles (por ahora) son:\n\n/mostrar Si quiere SOLICITAR los CANALES de la Botonera e <b>Información</b> sobre el tiempo restante de la PRÓXIMA PUBLICACIÓN de dicha botonera y sus CANALES afiliados\n\n/ingresar Si quiere INGRESAR su CANAL EN la BOTONERA\n\n/eliminar Para borrar su canal de la botonera :(\n\n/start o /help Para mostrar ESTE mensaje de ayuda\n\n\n\n<u>Nota:</u>\nSi quiere notificar algo del bot o tiene alguna duda consulte con mi guapetón propietario ( ͡° ͜ʖ ͡°)\n\n👉<a href='https://t.me/{bot.get_chat(admin).username}'>{bot.get_chat(admin).first_name}</a>👈",parse_mode="html", disable_web_page_preview=True, reply_markup=markup)
      else:
        bot.send_message(call.from_user.id, f"__El mensaje en cuestión, es el siguiente__:\n\{mensajes_dic['/start']}", parse_mode="MarkdownV2", reply_markup=markup)
        
      bot.send_message(call.from_user.id, 
                            """A Continuación te dejaré una guía de estilos con sus códigos para escribir mejor, a la izquierda de cada fila está el resultado y el nombre del estilo y a la derecha está el código que debes introducir para generar el mismo resultado
                            <u>Subrayado</u> : 
                            __texto en subrayado__
                            <b>Negrita</b> : 
                            *texto en negrita*
                            <i>Cursiva</i> : 
                            _texto en cursiva_
                            <s>Tachado</>  : 
                            ~texto en tachado~
                            <code>Monoespaciado</code> : 
                            '''Texto en monoespaciado'''
                            <span class='tg-spoiler'>Spoiler</span> : 
                            |||Texto en Spoiler|||
                            <a href='https://google.com'>Enlace</a> : 
                            [Texto con Enlace](https://google.com)""", parse_mode="html")
      msg2=bot.send_message(call.from_user.id, "Seguido de este mensaje escriba una nueva Bienvenida :)\n\nPresione <b>Cancelar</b> para dejar el que ya está", parse_mode="html", reply_markup=cancelar_markup)
      def nuevo_mensaje_bienvenida(message):
        if message.text.lower() == "cancelar":
          bot.send_message(message.chat.id, f"Entendido {bot.get_chat(admin).first_name} ;) Dejaré el mensaje anterior intacto")
          return
        mensajes_dic["/start"]=message.text
        bot.send_message(message.chat.id, f"Perfecto\nEl nuevo mensaje será:\n\n{mensajes_dic['/start']}", parse_mode="MarkdownV2")
        guardar_variables()
        return
      
      
      bot.register_next_step_handler(msg2, nuevo_mensaje_bienvenida)
    
        
      
      
      
      
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
          cursor.execute(f'DELETE FROM Canales WHERE ID_Canal={linea[0]}')
          conexion.commit()
          if "bot was kicked from the channel chat" in str(e):
            bot.send_message(
                call.from_user.id,
                f"Fuí expulsado del canal: {linea[0]}\n\nLo eliminaré de la botonera")
          else:
            bot.send_message(call.from_user.id, f"Fuí expulsado del canal @{linea[2]}\n\nLo eliminaré de la botonera")
            
          
            
            
      bot.send_message(call.from_user.id,
                      f"<u>El contenido del archivo es</u>:\n\n{texto}",
                      parse_mode="html")
      return

  #----------------------------Enviar archivos-----------------------------

    elif call.data == "Enviar archivos":
      markup=InlineKeyboardMarkup(row_width=1)
      markup.add(InlineKeyboardButton("Enviar Archivo de Canales", callback_data="Enviar BD"))
      markup.add(InlineKeyboardButton("Recibir Canales", callback_data="Recibir BD"))
    
      bot.send_message(call.from_user.id, "<u>Primera opción</u>: 'Enviar Archivo de Canales'\nTe enviaré la base de datos de canales existentes para que Lo GUARDES \n\n<u>Segunda opción</u>: 'Recibir canales'\nReemplazar la existente por una que tengas guardada, cargaré la que me envíes (Una que yo te haya enviado anteriormente)\n\n Asegúrese de guardar la base de datos existente regularmente, para que así sirva de copia de seguridad en caso de algún error", parse_mode="html" ,reply_markup=markup)
      
    elif call.data=="Enviar BD":
      with open("Botonera_Canales.bd", "rb") as archivo_bd:
        bot.send_document(call.from_user.id, archivo_bd)
      cursor.execute('SELECT * FROM Canales')
      lista_canales = cursor.fetchall()
      
      with open("Lista_Canales.txt", "w") as archivo_txt:
        archivo_txt.seek(0)
        for item in lista_canales:
          try:
            archivo_txt.write(
              f"{bot.get_chat(item[0]).username} | {bot.get_chat(item[1]).username}\n")
          except:
            cursor.execute(f'DELETE FROM Canales WHERE ID_Canal={item[0]}')
            conexion.commit()
            bot.send_message(admin, f"Al parecer, me expulsaron del canal @{item[2]}\nVoy a ponerle en el documento 'Error' al espacio que correspondería a este canal")
            archivo_txt.write(
              f"Error\n")    
            continue
        archivo_txt.truncate()
        archivo_txt.seek(0)
        
      with open("Lista_Canales.txt", "r") as archivo_txt:
        try:
          bot.send_document(call.from_user.id, archivo_txt, caption="Aquí está la lista con el nombre de los canales, esto NO es una base de datos, es SOLAMENTE UNA GUÍA")
        except Exception as e:
          if "file must be non-empty" in str(e):
            bot.send_message(
                call.from_user.id,
                "El archivo de texto está vacío XD no lo puedo mandar así")
          else:
            bot.send_message(call.from_user.id,
                            f"Ha ocurrido una excepción:\n\n{e}")
      
    elif call.data == "Recibir BD":
      msg = bot.send_message(call.from_user.id, "Muy bien, a continuación de este mensaje, envíeme el archivo Botonera_Canales.bd que ya le proporcioné\n\n<u>ATENCIÓN:</u>\n¡Tenga en cuenta que para hacer este proceso necesito pausar el hilo de publicaciones de la botonera!\nPresione en 'Cancelar Operación' si prefiere no hacerlo por ahora", parse_mode="html" ,reply_markup=cancelar_markup)
      
      
      def recibir_bd(message):
        global conexion
        global cursor
        if hilo_publicaciones:
          #-----------parar bucle----------------------
          global mensajes_a_eliminar
          global publicaciones
          global hora_publicacion
          global ejecutar_hilo
          global hora_eliminacion_botonera
          global admin
          try:
            global del_hilo
          except:
            pass
          bot.send_message(call.from_user.id, "Voy a detener el hilo de publicaciones")
          if mensajes_a_eliminar == []:
            pass
          else:
            for item in mensajes_a_eliminar:
              try:
                bot.delete_message(item[0], item[1])
              except Exception as e:
                bot.send_message(admin, f"Ha ocurrido una excepción intentando eliminar la botonera ya publicada en el canal @{bot.get_chat(item[0]).username}:\n\n{str(e)}")
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
          bot.send_message(
              call.from_user.id,
              f"Los hilos de publicaciones han sido detenidos exitosamente mi queridísimo {bot.get_chat(admin).first_name} ;D\n\n<u>Hilos activos</u>:\n{threading.active_count()}",
              parse_mode="html")
          
          
          #--------------------------------------------
        else:
          bot.send_message(call.from_user.id, "Al parecer no hay ningún hilo activo....")
        
        
        if not message.document:
          bot.send_message(message.chat.id, "No me has enviado nada que pueda usar :(")
          bot.send_message(call.from_user.id,
                            f"Bienvenido {bot.get_chat(admin).first_name} ;) Qué planeas hacer?",
                            reply_markup=botonera_panel)
          return
        else:
          conexion.close()
          try:
            os.remove(f"{os.path.dirname(os.path.abspath(__file__))}{OS}Botonera_Canales.bd")
          except:
            pass
          with open(f"{os.path.dirname(os.path.abspath(__file__))}{OS}Botonera_Canales", "wb") as archivo:
            archivo.write(bot.download_file(bot.get_file(message.document.file_id).file_path))
            
        conexion = sqlite3.connect(f"{os.path.dirname(os.path.abspath(__file__))}{OS}Botonera_Canales.bd", check_same_thread=False)
        cursor=conexion.cursor()
        bot.send_message(message.chat.id, "Archivo de canales cargado correctamente :)")
        return
      
      bot.register_next_step_handler(msg, recibir_bd)
    
            
            

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
      cursor.executemany('INSERT INTO Canales VALUES (?,?,?)', lista_canales)
      del lista_canales
      del contador
      return

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
                        f"{bot.get_chat(message.chat.id).first_name}",
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
      if not call.from_user.id == admin:
        bot.send_message(call.from_user.id,
                        f"No te puedo dejar hacer esto si no eres {bot.get_chat(admin).username} :)")
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
          global admin
          try:
            global del_hilo
          except:
            pass
          
          if not message.text.lower() == "si":
            bot.send_message(call.from_user.id, "Te envío de vuelta al panel...")
            bot.send_message(call.from_user.id,
                            f"Bienvenido {bot.get_chat(admin).first_name} ;) Qué planeas hacer?",
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
              bot.send_message(admin, "¡Bot detenido exitosamente!")
              return modo_reparacion
            else:
              modo_reparacion = True
              guardar_variables()
              bot.send_message(admin, "¡Bot detenido exitosamente!")
              return

        bot.register_next_step_handler(msg, funcion_modo_reparacion)
      elif modo_reparacion == True:
        bot.send_message(admin, "Procedo a quitarlo :v")
        modo_reparacion = False
		#--------------------------------------------------------------------------------------
  
  
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
        administrador = item[1]
        if call.from_user.id == administrador:
          cursor.execute(f'DELETE FROM Canales WHERE ID_Canal={canal}')
          conexion.commit()
          bot.delete_message(call.from_user.id, mensajes_a_eliminar.id)
          try:
            bot.send_message(
                call.from_user.id,
                f"Su canal @{bot.get_chat(canal).username} ha sido eliminado exitosamente\n\nNo me siento del todo feliz con eso :( Estaré esperando tu regreso por si te arrepientes"
            )
          except:
            bot.send_message(call.from_user.id, f"Su canal ha sido eliminado exitosamente\n\nNo me siento del todo feliz con eso :( Estaré esperando tu regreso por si te arrepientes")
          return
      else:
        bot.send_message(
            call.from_user.id,
            f"Al parecer no es admin de ningún canal aquí\nNo he encontrado ninguno registrado a su nombre\nSi usted cree que sí, repórtelo a @{bot.get_chat(admin).username}"
        )
        return
    elif call.data == "no":
      bot.send_message(
          call.from_user.id,
          "ae\n\nVolvemos atrás entonces mulatón (o mulatona UwU)\n\n<b>*Suspira*</b>", parse_mode="html"
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
    if mensajes_dic["/start"]=="":
      bot.send_message(
          message.chat.id,
          f"Hola! 😁, Bienvenido a la botonera más genial de Telegram. Los comandos disponibles (por ahora) son:\n\n/mostrar Si quiere SOLICITAR los CANALES de la Botonera e <b>Información</b> sobre el tiempo restante de la PRÓXIMA PUBLICACIÓN de dicha botonera y sus CANALES afiliados\n\n/ingresar Si quiere INGRESAR su CANAL EN la BOTONERA\n\n/eliminar Para borrar su canal de la botonera :(\n\n/start o /help Para mostrar ESTE mensaje de ayuda\n\n\n\n<u>Nota:</u>\nSi quiere notificar algo del bot o tiene alguna duda consulte con mi guapetón propietario ( ͡° ͜ʖ ͡°)\n\n👉<a href='https://t.me/{bot.get_chat(admin).username}'>{bot.get_chat(admin).first_name}</a>👈", parse_mode="html", disable_web_page_preview=True) #Editar texto
    else:
      bot.send_message(message.chat.id, mensajes_dic["/start"], parse_mode="MarkdownV2", disable_web_page_preview=True)

    bot.send_message(message.chat.id, f"Este Bot fué creado por @{bot.get_chat(reima).username}")
    canal = "no"
  
    return

  
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
        "A continuación probaré si el <b>@username</b> del canal es correcto y tengo derechos administrativos...",
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
          f"Al parecer el canal/grupo que ingresaste no es correcto, o <b>QUIZÁS me Expulsaron</b> de ahí en algún momento\n\nVuelve a mirar si el <b>@username</b> es correcto y en todo caso, <b>Úneme</b> al canal como administrador para corregir el error\n\n<b>Te devolveremos al menú principal...</b>\nPara adjuntar tu canal a la botonera vuelve a escribir /ingresar y escribe el nombre si estás ABSOLUTAMENTE seguro de que es correcto\n\n<u>Nota:</u>\nSi tiene alguna duda o problema por favor contacte con 👉<a href='https://t.me/{bot.get_chat(admin).username}'>{bot.get_chat(admin).first_name}</a>👈",
          parse_mode="html",
          disable_web_page_preview=True)
      del dic[message.from_user.id]
      return
    else:

      cursor.execute('SELECT * FROM Canales')
      lista_canales = cursor.fetchall()
      if bot.get_chat_member(chat_id=dic[message.from_user.id][0],
                            user_id=bot.user.id).status == "administrator":
        for elemento in lista_canales:
          canal = elemento[0]
          administrador = elemento[1]
          if canal == dic[message.from_user.id][0]:
            bot.send_message(
                message.chat.id,
                "Ese canal que ingresaste ya está en la botonera Velociraptor\nNo te hagas el listo >:D Vuelve a escribir /ingresar y prueba con otro canal"
            )
            del dic[message.from_user.id]
            return
          elif administrador == message.from_user.id:
            bot.send_message(
                message.chat.id,
                "Al parecer, ya ingresaste otro canal aquí, deja espacio para los demás y no te quedes con la botonera tú solo listillo >:v"
            )
            return
        #si es un CANAL y no puede mandar mensajes, entra en la condicion
        if not bot.get_chat_member(
            chat_id=dic[message.from_user.id][0],
            user_id=bot.user.id).can_post_messages:
          bot.send_message(
              message.chat.id,
              f"Oye Mastodonte\nNo basta con que solamente me pongas de admin en tu canal si no me das permisos para publicar la botonera ahí 💀\n\nPonme los permisos de publicación en @{bot.get_chat(dic[message.from_user.id][0]).username}, si no sabes cual es el que te digo pues dale todos y ya.\n\n<b>Cuando me pongas el permiso para PUBLICAR en tu canal</b>, vuelve aquí y escríbeme de nuevo /ingresar :) Te estaré esperando",
              reply_markup=InlineKeyboardMarkup().row(
                  InlineKeyboardButton(
                      "Ir a tu Canal",
                      url=
                      f"https://t.me/{bot.get_chat(dic[message.from_user.id][0]).username}"
                  )),
              parse_mode="html")
          del dic[message.from_user.id]
          return

        else:
          canal = [(dic[message.from_user.id][0], dic[message.from_user.id][1], bot.get_chat(dic[message.from_user.id][0]).username)]

          cursor.executemany('INSERT INTO Canales VALUES (?,?,?)', canal)

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
                            "<b>ALERTA! EXTREMA ATENCION!</b>:\n\nAl parecer, no me has dado permiso en tu canal para eliminar mensajes, lo cual, no es nada bueno para ti ya que tengo capacidad de autoeliminado de mensajes\n\nEso beneficia mucho que los canales no se saturen, cuando, por ejemplo, tu canal tiene 3 publicaciones al día y 500000 de una botonera pedante.\n\nCuál es la mecánica/el procedimiento?:\n\nSegundos antes de publicarse la nueva botonera borraré la vieja ya publicada y se quedará únicamente la nueva, así la botonera se renueva en el tiempo y no satura el canal/grupo en cuestión con tanta publicidad. Se queda solamente con 1 botonera que se re nueva cada cierto tiempo\n\nSi realmente no quiere que esto ocurra, vaya a los ajustes de su canal y concédale al bot permisos para eliminar mensajes. Con cariño, Yo",
                            parse_mode="html")
          conexion.commit()
          bot.send_message(admin, "¡Se ha unido un nuevo canal a la botonera!\nA continuación te enviaré una copia de la lista de canales :)")
          del dic[message.from_user.id]
          with open(f"Botonera_Canales.bd", "rb") as archivo_bd:
            bot.send_document(admin, archivo_bd)
          return
      else:
        bot.send_message(
            message.chat.id,
            f">:V AÚN NO ES ADMIN MMGUEVO\n\nHaz admin al bot (@{bot.user.username}) y continuaremos el procedimiento\nnIntroduce nuevamente /ingresar para añadir tu canal\n\nY ASEGÚRATE DE QUE ESTA VEZ EL BOT SI SEA ADMIN (¬_¬ )",
            parse_mode="html")
        return


  #-------------------Funcion MOSTRAR--------------------


  @bot.message_handler(commands=["mostrar"])
  def cmd_mostrar(message):
    global cursor
    global modo_reparacion
    global conexion
    global hora_publicacion
    global foto_botonera
    if modo_reparacion == True:
      funcion_reparacion(message)
      return
    try:
      foto_botonera.seek(0)
    except:
      pass
    
    bot.send_chat_action(message.chat.id, action="upload_photo")
    botonera = InlineKeyboardMarkup(row_width=2)
    #Primeramente, tengo que asegurarme que el bot tenga permisos para publicar en el canal
    cursor = conexion.cursor()
    
    #Ahora voy a comprobar si no me sacaron de los canales
    
    cursor.execute('SELECT * FROM Canales')
    lista_canales = cursor.fetchall()
    if lista_canales==[]:
      return bot.send_message(message.chat.id, "Al parecer la lista de canales esá vacía. Ingresa el tuyo para ser el primero en la lista :D\n\nEscribe /ingresar ;)")
    for linea in lista_canales:
      canal = linea[0]
      administrador = linea[1]
      canal_username = linea[2]
      try:
        bot.get_chat(canal)
        if bot.get_chat_member(canal, bot.user.id).status=='left':
          bot.send_message(admin, f"Me expulsaron de @{canal_username}, lo eliminaré de la botonera")
          cursor.execute(f'DELETE FROM Canales WHERE ID_Canal={canal}')
          conexion.commit()
          try:
            bot.send_message(administrador, f"Su canal @{canal_username}, ha sido eliminado de la botonera por haberme expulsado\n\nPara Introducirlo nuevamente agrégueme como administrador e ingrese aquí /ingresar \n\nTe estaré esperando :)")
          except:
            pass
        elif not bot.get_chat_member(chat_id=canal, user_id=bot.user.id).status == 'administrator' and str(administrador) != str(admin):
          cursor.execute(f'DELETE FROM Canales WHERE ID_Canal={canal}')
          conexion.commit()
          bot.send_message(
              admin,
              f"Se ha eliminado el canal @{canal_username} por no dejarme como administrador >:("
          )
          bot.send_message(
              administrador,
              f"<u>ATENCIÓN</u>:\n Se ha eliminado el canal @{canal_username} por no dejarme como administrador >:(\n\nPara ingresar de nuevo el canal en la botonera escriba /ingresar",
              parse_mode="html")

      except Exception as e:
        if admin==administrador:
          continue
        cursor.execute(f'DELETE FROM Canales WHERE ID_Canal={canal}')
        conexion.commit()
        if "chat not found" in str(e):
          try:
            bot.send_message(admin, f"Me han eliminado de un canal, iré a notificarle a su administrador y a continuacion lo eliminaré\n\nEl canal es @{canal_username}")
          except:
            bot.send_message(admin, f"Me han eliminado de un canal, iré a notificarle a su administrador y a continuacion lo eliminaré")

          try:
            bot.send_message(administrador, f"Al parecer me has eliminado de tu canal @{canal_username}, lo eliminarré de mi lista de canales a publicar")
          except:
            pass

        else:
          try:
            bot.send_message(admin, f"Ha ocurrido el siguiente error:\n\n{e}\n\nSe eliminará el canal: @{canal_username}\nSu administrador es @{bot.get_chat(administrador).username}")
          except:
            try:
              bot.send_message(admin, f"Ha ocurrido el siguiente error:\n\n{e}\n\nSe eliminará el canal: @{canal_username}")
            except:
              bot.send_message(admin, f"Se ha eliminado el canal @{canal_username}, posiblemente por expulsarme")
          try:
            bot.send_message(administrador, f"Al parecer, me han expulsado de tu canal @{canal_username} \nPor favor, vuelve a unirme CON permisos administrativos y escríbeme /ingresar :)")
          except:
            pass
          
            
    #Ahora pondré los canales de la BD a una lista para comenzar a recorrerla
    cursor.execute('SELECT * FROM Canales')
    lista_canales = cursor.fetchall()
    for linea in lista_canales:
      try:
        canal = linea[0]
        #Si el bot tiene permisos pues agrega el canal a la botonera
        nombre = bot.get_chat(canal).title
        enlace = f"https://t.me/{bot.get_chat(canal).username}"
        boton = InlineKeyboardButton(nombre, url=enlace)
        botonera.add(boton)
      except:
        cursor.execute(f'DELETE FROM Canales WHERE ID_Canal={canal}')
        conexion.commit()
        try:
          bot.send_message(linea[1], f"Su canal @{linea[2]} sido eliminado de la botonera porque al parecer me han sacado de ahí\n\nPara volver a integrarme, nómbrame admin y a continuación concédeme permisos para publicar, editar y eliminar mensajes. Entonces vuelve aquí y escribe /ingresar :)")
        except:
          pass
        try:
          bot.send_message(admin, f"He eliminado el canal @{linea[2]} de la botonera por expulsarme ")
        except:
          pass
    try:
      foto_botonera.seek(0)
    except:
      foto_botonera=False
    botonera.row(
        InlineKeyboardButton("(☞ﾟヮﾟ)☞ ÚNETE A LA BOTONERA ☜(ﾟヮﾟ☜)",
                            url=f"https://t.me/{bot.user.username}"))
    
    try:
      #Si no hay ninguna foto en la variable "foto_botonera" entonces...
      if foto_botonera==False:
        if mensajes_dic["/mostrar"]== "":
          bot.send_message(message.chat.id,"A continuación, Los Canales de la <b>MEJOR Botonera</b> de Telegram 😀🎉", parse_mode="html", reply_markup=botonera)
        else:
          bot.send_message(message.chat.id, mensajes_dic["/mostrar"], parse_mode="MarkdownV2", reply_markup=botonera)
      #Si tiene una foto entonces...
      else:
        #Si el usuario no ha personalizado el mensaje, entonces haz esto
        foto_botonera.seek(0)
        if mensajes_dic["/mostrar"]== "":
          bot.send_photo(message.chat.id, photo=foto_botonera, caption="A continuación, Los Canales de la <b>MEJOR Botonera</b> de Telegram 😀🎉", parse_mode="html", reply_markup=botonera) #Editar texto
        else: 
          bot.send_photo(message.chat.id, photo=foto_botonera, caption=mensajes_dic["/mostrar"], parse_mode="MarkdownV2", reply_markup=botonera)
        #Si lo personalizó entonces haz esto
          
          
    except:
      cursor.execute(f'DELETE FROM Canales WHERE ID_Canal={canal}')
      conexion.commit()
      try:
        bot.send_message(linea[1], f"Su canal ha sido eliminado de la botonera porque al parecer me han sacado de ahí\n\nPara volver a integrarme, nómbrame admin y a continuación concédeme permisos para publicar, editar y eliminar mensajes. Entonces vuelve aquí y escribe /ingresar :)")
      except:
        pass
      try:
        bot.send_message(admin, "He eliminado un canal de la botonera por expulsarme ")
      except:
        pass     
    
    if publicaciones == False:
      bot.send_message(message.chat.id, f"Ahora mismo, no estoy publicando la botonera, quizás en un momento sí lo haré\n\nPero todo depende del baboso de <a href='https://t.me/{bot.get_chat(admin).username}'>{bot.get_chat(admin).first_name}</a>, no de mí :(", parse_mode="html", disable_web_page_preview=True)
      return
    
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
    texto = f"El ID del bot es: <code>{bot.user.id}</code>\n\n"
    texto += f"Tu ID de usuario es: <code>{message.from_user.id}</code>\n\n"   
    texto += f"El ID del chat es: <code>{message.chat.id}</code>\n"
    # Last Hope ID: -1001161864648
    # Reima ID: 1413725506 

    bot.send_message(message.chat.id, texto, parse_mode="html")



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


except Exception as e:
  bot.send_message(admin, f"Se ha producido el siguiente error en el bot:\n\n{e}\n\nPor favor, notifique a su creador @mistakedelalaif")
  pass



bot.infinity_polling()
