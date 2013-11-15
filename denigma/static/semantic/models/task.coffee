###
  #model for the task#
  contains owner, title and completed of the task
###


#= extern Batman.Model

class Denigma.Task extends Batman.Model
  ###
  model for the task
  contains owner, title and completed of the task
  ###


#declares that properties title and completed will be saved when @save() is called
  @encode 'id','owner','title', 'completed'


  @persist Batman.SocketStorage
  #@persist Batman.LocalStorage
  ###
    messages are stored in socket storage
  ###

  #validate if title is present each time we create Task
  @validate 'title', presence: true

  #key for local (by the browser) storage
  @storageKey: 'tasks'

  @classAccessor 'active', ->
    ###return all active tasks###
    @get('all').filter (task) -> !task.get('completed')

  #returns all completed tasks
  @classAccessor 'completed', ->
    ###
      gets all tasks and than applies filter function
    ###
    @get('all').filter (task) -> task.get('completed')

  @wrapAccessor 'title', (core) ->
    set: (key, value) -> core.set.call(@, key, value?.trim())

