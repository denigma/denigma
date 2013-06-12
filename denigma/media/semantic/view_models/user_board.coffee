class Denigma.UserBoard extends Denigma.Board

  @classAccessor "items",-> Denigma.User.get("all") #.toArray().reverse()

  @set "expanded",true


  @toggle: (node,event)=>
    @set("expanded", not @get("expanded"))

