###
  #Socket class#
  it not only uses either real or mock socket but broadcasts messages to various channels through events
###

#= extern Batman.Object
#_require socket_event
#_require cache_socket
#_require channel


class Batman.Socket extends Batman.Object
  ###
    websocket wrapper that broadcast info to its channels
    it not only uses either real or mock socket but broadcasts messages to various channels through events
  ###
  constructor: (url)->
    ###
    creates a socket object
    ###
    #checks if websocket is in batman container
    @router = new Batman.SimpleRouter()
    @websocket = @getWebSocket(url)
    Batman.Socket.instance = @



  url: "none"


  isMock: => not @websocket? or @websocket.isMock?

  createWebSocket:  (url)=>
    ###
      creates websocket or mocksocket
    ###
    if url=="none"
      websocket = new Batman.CacheSocket(url)
    else
      websocket = new WebSocket(url)
    @url = url
    @setWebsocket(websocket)

  setWebsocket: (websocket)=>
    defOpen = (event)=>
      @websocket = websocket
      @addSocketHandlers(@websocket)
    if @websocket?
      if websocket==@websocket then return @websocket
      if @websocket.isCache?
        old = @websocket
        websocket.onopen = (event)=>
          defOpen(event)
          old.unapply(websocket)
      else
        websocket.onopen = defOpen
    else
      websocket.onopen = defOpen
    if websocket.isMock? then websocket.onopen()

  addSocketHandlers: (websocket)=>
    websocket.onmessage = (event)=> @broadcast(event)
    websocket.onerror = (err)=>alert "some ERROR occured"
    websocket.onclose = ()=>alert "socket is CLOSED"
    websocket

  broadcast: (info)->@router.broadcast(info,@)


  getWebSocket: (url)=>
    ###
      TODO: rewrite, all this searches, the global scope only confuses
    ###
    if  Batman.container.websocket?
      if (Batman.container.websocket.isMock and url=='none') or url==@url
        return Batman.container.websocket
    @createWebSocket(url)




  withUrl: (url)=>
    ###
      returns self but changes the websocket if needed
    ###
    if(url!=@url) then @websocket = @getWebSocket(url)
    @


  @getInstance: (url="none")=>
    ###
      works as singletone
      TODO: rewrite
    ###
    if Batman.Socket.instance? then Batman.Socket.instance else return new Batman.Socket(url)
    ###
    if Batman.container.socket?
      return Batman.container.socket.withUrl(url)
    else
      return new Batman.Socket(url)

    ###

  getChannel: (name)=>
    ###
      gets or creates channel
    ###
    @getOrSet(name,=>new Batman.Channel(name).attach(@))

  getSpecialChannel: (name,factory)=>
    ###
      gets or creates channel with factory that is provided
    ###
    @getOrSet(name,=>factory().attach(@))


  getVideoChannel: (name,room)=>
    ###
      gets or creates video channel
    ###
    #TODO: think how to fix in Future
    @getOrSet(name+"2"+room,=>new Batman.VideoChannel(name,room).attach(@))



  send: (obj)=> @router.send(obj, @websocket)

  ask: (question)=>
    ###
      executes if there is a request to the router (but without info to be send to server)
    ###
    @router.respond(question,@)



