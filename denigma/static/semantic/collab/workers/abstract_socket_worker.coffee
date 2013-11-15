class AbstractSocketWorker
  constructor: ->
    @connections = 0
    @ports = []

  connections: 0

  connect: (e)->
    @lastPort = e.ports[0]
    @ports.push @lastPort
    @connections++

  postMessage: (data)=>
    @lastPort.postMessage(data)

  listenAll: (fun)=>
    unless @ports? or @ports.length==0 then return
    num = 0
    while num < @ports.length
      port = @ports[num]
      port.onmessage = (e)->fun(e)
      num++

  notifyAll: (data)=>
    unless @ports? or @ports.length==0 then return
    num = 0
    while num < @ports.length
      port = @ports[num]
      port.postMessage(data)
      num++


  broadcast: (data)=>
    num = 0
    while num < @ports.length
      port = @ports[num]
      port.postMessage(data)
      num++

