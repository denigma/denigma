###
  Routerclass
###

#= extern Batman.Object


class Batman.SimpleRouter extends Batman.Object
  ###
    Simple router does only simple broadcasting relying on channel info from the socket
  ###

  broadcast: (info, socket)->
    ###
      transforms info into SocketEvents and routes them further, to the channels
      some routers split info into several parts and send to difference channels
    ###
    event = Batman.SocketEvent.fromEvent(info)
    ### broadcasts the message further ###
    unless event instanceof Batman.SocketEvent
      throw Error 'should be socket event'
    ### broadcast event to appropriate channels ###
    socket.fire(event.channel, event)
    if(event.room? and event.room!="all")
      socket.fire(event.channel+"2"+event.room, event)  #TODO: fix this indus code


  send: (obj, websocket)->
    ###
      sends event to the websocket
    ###
    if typeof obj == 'string'
      websocket.send(obj)
    else
      str = JSON.stringify Batman.SocketEvent.fromData(obj)
      websocket.send str
      #websocket.send obj

  myStream: null
  webCamPending: false


  respond: (question,socket)->
    ###
      respond to questions from channels
    ###
    switch question
      when "webcam"
        if @myStream?
          socket.fire "localStream", @myStream
        else
          if @webCamPending==false
            navigator.getUserMedia or (navigator.getUserMedia = navigator.mozGetUserMedia or navigator.webkitGetUserMedia or navigator.msGetUserMedia)
            if navigator.getUserMedia
              onsuccess = (stream)=>
                socket.fire "localStream", stream
                @webCamPending = false
              onerror = @onError
              @webCamPending = true
              navigator.getUserMedia
                video: true
                audio: true
                onsuccess
                onerror
            else
              alert "getUserMedia is not supported in this browser."
          @webCamPending = true

