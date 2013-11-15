###
# SocketEvent class #
Socket Event class is a class that does all conversions and packing of events send by sockets and channels
###

#= extern Batman.Object

class Batman.SocketEvent
  ###
  Socket Event class is a class that does all conversions and packing of events send by sockets and channels
  it contains a lot of useful static helpers to generate events that needed
  ###

  constructor: (@content, @channel, @request = "push", @room = "all")->
    ###
      creates websocket event where
      content is inside content variable, channel is for source (model) or type of content
      request is for what you want to do with content
      room is for what users to you want to spread this info
    ###
    unless @content.id? or @content.query then @content.id = SocketEvent.genId()
    #@id = if id=="" then SocketEvent.genId() else id



  @makeEvent: (content,channel, req, room = "all")->
    ###
      creates a socketevent, where:
      content is content of event
      channel is name of the channel that is used for this event
      req is a request with what this event is send
      room is an info to which users should the event be sent to
    ###
    new Batman.SocketEvent(content, channel, req, room)

  @makeQueryEvent: (query,channel, room = "all")->Batman.SocketEvent.makeEvent(query:query, channel, "read", room)

  @makeLookupEvent: (lField,lQuery,channel, room = "me")->
    content =
      field: lField
      query: lQuery
    Batman.SocketEvent.makeEvent(content, channel, "lookup", room)



  @makePushEvent: (content,channel, room = "all")->Batman.SocketEvent.makeEvent(content, channel, "push", room)

  @makeReadEvent: (id,channel, room = "all")->Batman.SocketEvent.makeEvent(id:id, channel, "read", room)

  @makeReadAllEvent: (channel,  room = "all")->Batman.SocketEvent.makeEvent(query:"all", channel, "read", room)

  @makeSaveEvent: (obj, channel)->
    data = Batman.SocketEvent.fromData(obj)
    data.channel = channel
    data.request = "save"
    data.room = "all"
    data


  @makeRemoveEvent: (id,channel, room="all")->Batman.SocketEvent.makeEvent(id:id, channel, "delete", room)



  @fromEvent: (event)->
    ###
    factory that generate SocketEvent from websocket event
    ###
    if event instanceof Batman.SocketEvent then return event
    if not event.data? then throw new Error("No data inside of websocket event")
    @fromData(event.data)

  @genId : ->
    ###
    ##Generates GUI as id for a record
    ###
    "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace /[xy]/g, (c) ->
      r = Math.random() * 16 | 0
      v = (if c is "x" then r else (r & 0x3 | 0x8))
      v.toString 16


  @fromData: (data)->
    ###
    factory that generate SocketEvent from the data
    ###
    if data instanceof Batman.SocketEvent then return data
    if typeof(data) =="string" then return @fromString(data)
    #to avoid typical bug of nested data
    data = data.data if data.data?
    channel = if data.channel? then data.channel else "default"
    content =
      if data.content?
        if typeof data.content =="string" then @toJSON(data.content) else data.content
      else
        data
    request = if data.request? then data.request else "push"
    room = if data.room? then data.room else "all"
    new Batman.SocketEvent(content,channel,request,room)


  @fromString: (str)->
    ###
    factory that generate SocketEvent from some string
    ###
    #if typeof str !="string" then throw new Error("not string received by fromString but "+JSON.stringify(str))
    data = @toJSON(str)
    return  if data is undefined or typeof(data)=="string" then new Batman.SocketEvent(str,"default","save") else @fromData(data)


  @toJSON = (str) ->
    ###
    tries to convert string to json, returns initial string if failed
    ###
    if typeof str !="string" then return str
    try
      obj = JSON.parse str
    catch e
      return str
    if obj==undefined then str else obj

