###
# Channel class #
Every sockets info to channels.
Channels are needed to communicate directly with the model
###
#= extern Batman.Object

#= require <socket.coffee>


class Batman.Channel extends Batman.Object
  ###
  #Channel class
  Every sockets info to channels.
  Channels are needed to communicate directly with the model
  ###
  constructor: (name) ->
    @name = name
    @on "onmessage", (event)=>@onmessage(event)

  save: (obj, id) =>
    obj.id = id
    @save obj

  save: (obj)=> @fire "send", Batman.SocketEvent.makeSaveEvent(obj,@name)

  read: (id)=> @fire "send", Batman.SocketEvent.makeReadEvent(id, @name)

  readAll: => @fire "send", Batman.SocketEvent.makeReadAllEvent(@name)

  remove: (id)=> @fire "send", Batman.SocketEvent.makeRemoveEvent(id, @name)

  lookup: (field,query)=> @fire "send", Batman.SocketEvent.makeLookupEvent(field,query, @name)

  query: (query)=> @fire "send", Batman.SocketEvent.makeQueryEvent(query, @name)

  stream2src: (stream)=>
    ###
      gets URL from the stream
    ###
    if window.URL?
      window.URL.createObjectURL(stream)
    else
      if window.webkitURL?
        window.webkitURL.createObjectURL(stream)
      else
        if window.mozURL?
          window.mozURL.createObjectURL(stream)
        else
          stream

  askWebcam: =>
    @ask "webcam"



  send: (obj) =>
    data = Batman.SocketEvent.fromData(obj)
    data.channel = @name
    @fire "send", data


  receive: (event) =>
    #should receive event with data
    @fire "onmessage", event
    @fire(event.request, event)

  onNextMessage:(fun)=>@once "onmessage", (event)=>fun(event)

  onmessage: (event) =>
    ###
      call back the receives info from socket send to this channel
    ###

  ask: (question)=>
    ###
      asks router for some additional info
    ###
    @fire "ask", question


  attach: (obj)=>
    ###
      Attaches the channel to the socket wrapper and subscribes to its events
    ###
    receive = @receive #trick to overcome "this" javascript change
    obj.on @name, receive
    obj.on "all", receive

    send = obj.send
    @on "send", send

    @on "ask", obj.ask
    cl = @constructor.name
    obj.fire(cl,@name)
    @