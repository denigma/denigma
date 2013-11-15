#= require <better_view.coffee>

class Batman.ChannelView extends Batman.BetterView
  ###
  View that is connected to some socket channel
  ###
  channelName: null
  channel: null

  @register("key","mandatory")

  connect: ->
    ###
      works with channel
    ###
    @channelName ?= @get "key"
    @channel = Batman.Socket.getInstance().getChannel(@channelName)

  render: ->
    super
    @connect()

