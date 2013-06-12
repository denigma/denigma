###
# WorkerSocket class #
###

#= extern Batman.Object

class Batman.WorkerSocket extends Batman.Object
  ###
  #Worker socket#
  ###
  constructor: (worker)->
    if typeof(worker) =="string" then @worker = worker = new SharedWorker(worker)  else  @worker = worker
    @worker.port.onmessage = (e)=>@onmessage(e)
    @worker.port.onerror = (e)=>@onerror(e)
    Batman.container.worker =  @worker;
    @worker.port.start()
    Batman.WorkerSocket.instance = @

  @getInstance: (url="none")-> if Batman.WorkerSocket.instance? then Batman.WorkerSocket.instance else return new Batman.WorkerSocket(url)


  send: (obj)=>@worker.port.postMessage(obj)

  onopen: (i)->

  onerror: (error)->

  onmessage: (event)->
    data = if event.data? then event.data else event
    if data.ready? then onopen(data)

  onclose: ->
