#= extern Batman.Object

class Denigma.TaskBoard extends Batman.Object

  @set "hideCompleted", false

  @classAccessor "items",->
    Denigma.Task.get("all")
      .filter (task)-> not Denigma.TaskBoard.get("hideCompleted") || not task.get('completed')

  @set "title",""

  @pressKey: (node,event)=>
    if event.keyCode == 13  and not (event.altKey or event.ctrlKey or event.shiftKey)
      Denigma.TaskBoard.addNew(node,event)

  @newTask: =>
    ###
      creates new empty message for binding
    ###
    userName = Batman.container.username
    tlt = Denigma.TaskBoard.get("title")
    new Denigma.Task(id:Batman.SocketEvent.genId(), owner:userName,title:tlt,completed:false) #bad code

  @addNew: (node,event)=>
    ###
      Adds new message
    ###
    if Denigma.TaskBoard.get("title").length>1
      task = Denigma.TaskBoard.newTask()
      task.save()
      @set "title", ""

  @set "expanded",true


  @toggle: (node,event)=>
    @set("expanded", not @get("expanded"))
