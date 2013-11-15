###
  ##Message board view model. Needed for various sophisticated operations with messages
###

#= extern Batman.Object


class Denigma.MessageBoard extends Denigma.Board


  @set "text",""



  @classAccessor "items",-> Denigma.Message.get("all") #.toArray().reverse()



  @newMessage: =>
    ###
      creates new empty message for binding
    ###
    username = Batman.container.username
    txt = Denigma.MessageBoard.get("text")
    new Denigma.Message(user:username,text:txt) #bad code

  @pressKey: (node,event)=>
    if event.keyCode == 13  and not (event.altKey or event.ctrlKey or event.shiftKey)
      Denigma.MessageBoard.addNew(node,event)


  @addNew: (node,event)=>
    ###
      Adds new message
    ###
    if Denigma.MessageBoard.get("text").length>1
      message = Denigma.MessageBoard.newMessage()
      message.save()
      @set "text", ""

  @set "expanded",true


  @toggle: (node,event)=>
    @set("expanded", not @get("expanded"))
