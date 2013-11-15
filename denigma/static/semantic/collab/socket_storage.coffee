###
#SocketStorage#

This is a Socket storage adaptor needed to connect Batman's models to websocket
It has not been finished yet.
###

#= extern Batman.Object

#_require ./socket_event.coffee
#_require ./channel.coffee
#_require ./socket.coffee
#_require ./mock_storage.coffee

class Batman.SocketStorage extends Batman.StorageAdapter
  ###
  #SocketStorage#

  This is a Socket storage adaptor needed to connect Batman's models to websocket
  It has not been finished yet.
  ###

  constructor: (model) ->
    ###
      Initialize storage adaptor as well as socket
    ###
    super(model)
    @socket = new Batman.Socket.getInstance()

  _dataMatches: (conditions, data) ->
    match = true
    for k, v of conditions
      if data[k] != v
        match = false
        break
    match

  subscribe: (model)->
    ###
      Subscribe model to different events
      subscribe function is called after readall
    ###
    channel = @socket.getChannel(model.storageKey)
    if model.primaryKey?
      key = model.primaryKey
    else
      key = "id"

    #TODO: rewrite addition because it changes the order of elements
    channel.on "push", (event)=>
      all = model.get("loaded")
      res = all.find (item)->
        item.get(key)== event.content[key]
      all.remove(res)
      record = @getRecordFromData(event.content, model)
      all.add(record)
    channel.on "delete", (event)=>
      all = model.get("loaded")
      res = all.find (item)->
        item.get(key)== event.content[key]
      all.remove(res)
    channel


  readAll: (env, next) ->#@skipIfError (env, next) ->
    ###
    overrided readAll to add subscription
    TODO: what to do with subscriptions if readALL is called several times?
    ###
    channel = @subscribe(env.subject)
    options = env.options.data

    channel.onNextMessage (event)->
      try
        records = []
        if event.content? and event.content.length?

           for item in event.content
             records.push item if @_dataMatches(options,item)

        env.recordsAttributes = records
      catch error
        env.error = error
      next()
    channel.readAll()


  create: ({key,id, recordAttributes}, next) -> #@skipIfError ({channel,id, recordAttributes}, next) ->
    channel = @socket.getChannel(key)
    channel.save(recordAttributes,id)
    next()

  read: ({key,id, recordAttributes}, next) -> #@skipIfError ({key,id, recordAttributes}, next) ->
    channel = @socket.getChannel(key)
    channel.onNextMessage =>
      if !env.recordAttributes
        env.error = new @constructor.NotFoundError()
        next()
    channel.read(id)
    #do not forget about change in future


  update: ({key,id, recordAttributes}, next) ->#@skipIfError ({key,id, recordAttributes}, next) ->
    channel = @socket.getChannel(key)
    channel.save(recordAttributes,id)
    next()

  destroy: ({key,id}, next) -> #@skipIfError ({key,id}, next) ->
    channel = @socket.getChannel(key)
    channel.remove(id)
    next()


  @::before 'read', 'create', 'update', 'destroy', @skipIfError (env, next) ->
    if env.action == 'create'
      env.id = env.subject.get('id') || env.subject._withoutDirtyTracking => env.subject.set('id', Batman.SocketEvent.genId())
    else
      env.id = env.subject.get('id')

    unless env.id? then env.error = new @constructor.StorageError("Couldn't get/set record primary key on #{env.action}!")
    key = @storageKey(env.subject)
    env.key = key

    next()


  @::before 'create', 'update', @skipIfError (env, next) ->
    env.recordAttributes = JSON.stringify(env.subject)
    next()

  @::after 'read', @skipIfError (env, next) ->
    if typeof env.recordAttributes is 'string'
      try
        env.recordAttributes = @_jsonToAttributes(env.recordAttributes)
      catch error
        env.error = error
        return next()
    env.subject._withoutDirtyTracking -> @fromJSON env.recordAttributes
    next()

  @::after 'read', 'create', 'update', 'destroy', @skipIfError (env, next) ->
    env.result = env.subject
    next()

  @::after 'readAll', @skipIfError (env, next) ->
    env.result = env.records = for recordAttributes in env.recordsAttributes
      @getRecordFromData(recordAttributes, env.subject)
    next()

