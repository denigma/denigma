###
# MockSocket class #
Mock socket is needed for tests to simulate websocket behaviour
###

#= extern Batman.Object
#_require channel.coffee
#_require socket_event.coffee


class Batman.MockSocket extends Batman.Object
  ###
  #Mock socket#
  Mock socket is needed for tests to simulate websocket behaviour
  ###
  constructor: (@url)->
    super
    @onreceive = Batman.MockSocket.mockCallback(@)
    MockSocket.instance = @
    @onopen()

  @getInstance: (url="none")->if Batman.MockSocket.instance? then Batman.MockSocket.instance else return new Batman.MockSocket(url)

  isMock: true


  onreceive: (event)->event


  send: (event)=>@onreceive(event)

  onopen: ->
    ###
    Open event
    ###
    console.log "open"

  onmessage: (event)->
    ###
    On message
    ###
    data = event.data;

  onclose: =>
    console.log "close"

  randomInt: (min, max)=>
    ###
      random int generating function
    ###
    Math.floor(Math.random() * (max - min + 1)) + min

  @mockCallback:  (mock)=>
    ###
      this callback is needed to store data inside mock sockets and respond to read requests and other queirs
      NAPILNIK
    ###
    (event)=>
      #console.log event
      data = Batman.SocketEvent.fromString(event)
      #console.log data
      switch data.request
        when "save"
          ###
            if we received request to save something we answer to it with result
          ###
          data.request = "push"
          if data.content.id?
            id = data.content.id
            ###
              if we were give id we just give item with appropriate id
            ###
            mock.set id, data
            all = mock.getOrSet(data.channel, =>new Batman.SimpleSet())
            res = all.find (item)->item.id==id
            if res? then all.remove res
            all.add data.content
            mock.onmessage(data)
        when "delete"
          if data.content.id?
            id = data.content.id
            mock.unset id
            all = mock.getOrSet(data.channel, =>new Batman.SimpleSet())
            res = all.find (item)->item.id==id
            if res? then all.remove(res)
        when "read"
          if data.content.id?
            data = mock.get(data.content.id)
            data.request = "answer"
            mock.onmessage(data)
          else
            if data.content.query? and data.content.query=="all"
              col = mock.get(data.channel)
              if col? and col.length>0
                content = col.toArray()
                message = new Batman.SocketEvent(content, data.channel,"readAll")
                mock.onmessage(message)
              else
                mock.onmessage(new Batman.SocketEvent("_nil_", data.channel,"readAll"))

