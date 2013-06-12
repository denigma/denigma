###
#User class#
model for users of the chat, now is only used for test purposes
Class for chat users
###


#= extern Batman.Model

class Denigma.User extends Batman.Model
  ###
  Class for chat users
  ###

  #@hasMany('messages', {name:"Message",saveInline:false})
  #@hasMany('tasks', {name:"Task",saveInline:false})

  #@set("currentUser", null)

  #declares that properties name and status will be saved when @save() is called
  @encode  'username', 'status', 'password'

  #validate if name is present each time we create User
  @validate 'name', presence: true


  @persist Batman.SocketStorage
  ###
    messages are stored in socket storage
  ###

  @primaryKey: 'username'

  #key for local (by the browser) storage
  @storageKey: 'users'

  @login: ->
    alert "LOGIN MODEL!"
    console.log "LOGIN MODEL!"



