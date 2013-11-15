###
  Chat router class
###
#= require <socket.coffee>
#= require <simple_router.coffee>

class Batman.ChatRouter extends Batman.SimpleRouter

  broadcast: (info, socket)->
    ###
      routes events to the chat
    ###
    #if not info.data? then throw new Error("no data inside event cannot route further")
    unless info.data? then return super(info,socket)

    if info.data.content? then return super(info,socket)
    data = Batman.SocketEvent.toJSON(info.data)
    if data.kind?
      switch data.kind
        when "join"
          @addUser(data,socket)
          @message(data,socket)

        when "quit"
          @removeUser(data,socket)
          @message(data,socket)

        when "talk"  then @message(data,socket)
        when "message" then @message(data,socket)

  addUser: (data,socket) ->
    content =
      id:data.user
      name:data.user
    event = new Batman.SocketEvent.makePushEvent(content,"users")
    socket.fire "users", event

  removeUser: (data,socket) -> socket.fire "users", Batman.SocketEvent.makeRemoveEvent(data.user,"users")

  message: (data,socket) ->
    text = if data.message? then data.message else data.text
    content =
      "user": data.user
      "text": text
    event = Batman.SocketEvent.makePushEvent(content,"messages")
    socket.fire "messages", event

  task: (data,socket) ->
    content =
      "user": data.user
      "title": data.title
    event = Batman.SocketEvent.makePushEvent(content,"tasks")
    socket.fire "tasks", event



  send: (obj, websocket)->
    ###
      sends event to the websocket
    ###
    #return super(obj, websocket)
    if typeof obj == 'string'
      websocket.send(obj)
    else
      event = Batman.SocketEvent.fromData(obj)
      if event.channel =="messages"
        if event.content?
          if event.content.text?
            event.text = event.content.text
          else
            if event.content.data?
              event.text = event.content.data
            else event.text = event.content
      str = JSON.stringify Batman.SocketEvent.fromData(obj)
      websocket.send str
      #websocket.send obj



