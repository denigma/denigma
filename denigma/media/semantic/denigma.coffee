###
  #Denigma chat App#
  Application coffee of the chat
###

#= extern Batman.App
#= extern Batman.Object

#disable routingkey warnings for controllers
Batman.config.minificationErrors = false

class Denigma extends Batman.App
  #@route

  ###
  Application object of the chat
  ###

  @root ''
  #@route "/completed", "tasks#completed"
  #@route "/active", "tasks#active"

  @workerHandler: (e)->
    ###
      handles worker messages
    ###
    Denigma.login(e.data)

  @login: (data)->
    ###
      functions that fires when you logged in
      The loggin message can come from both shared webworker and loginform
      ant that is a reason why I put it here
    ###
    if data.user? and data.password?
        socket = Batman.Socket.getInstance(data.websocketURL)
        socket.router = new Batman.SimpleRouter()

        if Denigma.ws?
          #checks if we are connecting directly or there is a shared webworker that does it for us
          socket.setWebsocket Denigma.ws
        else
          socket.setWebsocket new WebSocket(data.websocketURL)
        Denigma.fire("login", data)

  @initWorker: ->
    ###
      Decides whether it should connect directly or through shared webworker
    ###
    if Batman.container.workerURL?
      Denigma.ws = new Batman.WorkerSocket(Batman.container.workerURL)
      Denigma.ws.onmessage = (e)->Denigma.workerHandler(e)

  @send: (data)->
    ###
      TODO: rename the function
    ###
    if Denigma.ws?
      Denigma.ws.send(data)
    else
      Denigma.login(data)

#stores to global container
container = Batman.container
container.Denigma = Denigma

class Batman.EmptyDispatcher extends Batman.Object
  ###
  to switch routing off
  ###


#add listener to the window object to fire run when everything has been loaded
if(window?)
  window.addEventListener 'load', ->
    disp = new Batman.EmptyDispatcher()
    Denigma.set "navigator", disp
    Denigma.set "dispatcher", disp
    Denigma.run()
    Denigma.initWorker()

jQuery =>
  ###
  this function connects to socket when logging in
  ###
  username = Batman.container.username
  password = Batman.container.password
  url = Batman.container.websocketURL.replace(/&amp;/g,"&").replace("nouser",username).replace("none",username).replace("nopassword",password)
  Batman.container.websocketURL = url
  message =
    user: username
    password: password
    websocketURL: url
  #alert (username+" | "+password)
  Denigma.send message
