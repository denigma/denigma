#a view for messages of this chat

#= extern Batman.View

class Denigma.MessageView extends Batman.View
  ###
    View for messages of this chat
  ###
  constructor: ->
    # process arguments and stuff
    super
    #writes node to separate variable, node is an HTMLNode to which view is attached to
    #@node = $ @get("node")

  render: ->
    super
    node = $ @get "node"
    node.hide().fadeIn("slow")
