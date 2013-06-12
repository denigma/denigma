###
# MockSocket class #
Mock socket is needed for tests to simulate websocket behaviour
###

#= extern Batman.Object
#_require Batman.Channel
#_require Batman.SocketEvent



class Batman.CacheSocket extends Batman.Object

  isMock: true
  isCache: true
  input: []

  onopen: ->
    ###
    Open event
    ###
    console.log "open"

  constructor: (@url)->
    super
    @input = []

  send: (data)=> @input.push(data)

  onmessage: (event)->
    ###
    On message
    ###
    data = event.data
    console.log(data)

  onerror: =>
    console.log "error"

  onclose: =>
    console.log "close"

  randomInt: (min, max)=>
    ###
      random int generating function
    ###
    Math.floor(Math.random() * (max - min + 1)) + min

  unapply: (successor)=>
    if(@input? and successor.send?)
      for el in @input then successor.send(el)

