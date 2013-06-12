###
  This is a shared worker that containes websocket connection inside itself
  the connection is shared between several
###
class SocketWorker extends BasicWorker
  constructor: ->
    super

  ports: []

  hasLogin: (obj)=> obj.user? and obj.password?
  hasAuth: (obj)=>@hasLogin(obj) and @websocket?

  hasAny: (obj)=> @hasLogin(obj) or obj.websocketURL? or @connections>0

  connect: (e)->
    ###
      connects to port
    ###
    super(e)
    @lastPort.onmessage = (e)=>@portHandler(e)
    @sendAuth()

  #onmessage: (e)->  @lastPortHandler(e)


  sendAuth: =>
    ###
      authorizes other clients of this shared webworker
    ###
    message = {}
    if @url? then message.websocketURL = @url
    if @user? then message.user = @user
    if @password? then message.password = @password
    if @websocket? then message.ready = true
    if @hasAny(@) then @postMessage message

  portHandler: (msg) =>
    data = msg.data
    if data.user? then @user = data.user
    if data.password? then @password = data.password
    if data.websocketURL? then @url = data.websocketURL
    unless @websocket?

      if @url? and @hasLogin(@)
        websocket = @createWebsocket(@user,@password,@url)
        @websocket = websocket
        notifyAll = @notifyAll #workaround to avoid "this" context change problems
        websocket.onmessage = notifyAll
        @listenAll (e)->
          #debugger
          websocket.send(e.data)
      ###
      if @url? and @hasLogin(@)
        websocket = @createWebsocket(@user,@password,@url)
        funMes = (e)=>
          event = e
          #debugger
          @notifyAll(e)
        @websocket = websocket

        websocket.onmessage = (e)->funMes(e.data)
        @listenAll (e)->
          #debugger
          websocket.send(e.data)

      ###
    @sendAuth()




worker = new SocketWorker()
self.addEventListener("connect", (e) ->worker.connect(e))

