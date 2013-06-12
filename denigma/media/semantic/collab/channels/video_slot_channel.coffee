class Batman.VideoSlotChannel extends Batman.Channel

  channels: null

  OPEN_PEERS: "openpeers"
  PEERS_OPENED: "peersopened"

  CALL_PEERS: "callpeers"
  PEERS_CALLED: "peerscalled"

  CLOSE_PEERS: "closepeers"
  PEERS_CLOSED: "peersclosed"


  ###
    mystream is a temporal global variable to save a stream from a webcome
  ###
  constructor: (name, @room)->
    super(name)
    @channels = new Batman.SimpleHash()
    @on @OPEN_PEERS , (event)=>@peersOpened(event)
    @on @CALL_PEERS , (event)=>@peersCalled(event)


  peersOpened: (event)=>
    ###
      fires when we received peers to be created
    ###
    console.log("PEERS OPENED: "+JSON.stringify(event))
    unless event.content then console.log "no content"
    cont = event.content
    if not (cont.from? or cont.to)  then console.log "no from or to"
    socket = Batman.Socket.getInstance()
    for f in cont.from
      h = @channels.getOrSet(f, =>new Batman.SimpleHash())
      for t in cont.to
        console.log("open video channel from #{f} to #{t}")
        ch = h.getOrSet(t,=>socket.getVideoChannel(f,t))
        ch.on "localStream", (stream)=> @fire "local", @stream2src(stream)
        ch.on "remoteStream", (stream)=>
          src = @stream2src(stream)
          console.log "#{@name}: remoteSRC = #{src}"
          @fire "remote", src

    event.content.name = @PEERS_OPENED
    event.request = @PEERS_OPENED
    event.room = @room
    @send event
    @fire(@PEERS_OPENED)


  peersCalled: (event)=>
    ###
      fires when we received peers to be created
    ###
    console.log("PEERS CALLED: "+JSON.stringify(event))
    unless event.content then console.log "no content"
    cont = event.content
    if not (cont.from? or cont.to)  then console.log "no from or to"
    socket = Batman.Socket.getInstance()
    for f in cont.from
      h = @channels.getOrSet(f, =>new Batman.SimpleHash())
      for t in cont.to
        console.log("call video channel from #{f} to #{t}")
        ch = h.getOrSet(t,=>socket.getVideoChannel(f,t))
        ch.call()
    event.content.name = @PEERS_CALLED
    event.request = @PEERS_CALLED
    event.room = @room
    @send event
    @fire(@PEERS_CALLED)

  call: =>
    req = "broadcast"
    evt = new Batman.SocketEvent(req, @name, req, @room)
    @fire "send", evt



  open: =>
    req = "video"
    content =
      name: req
    evt = new Batman.SocketEvent(content, @name, req, @room)
    @fire "send", evt


  onError: (e)->
    alert "There has been a problem with slot channel?"