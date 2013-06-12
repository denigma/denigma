###
  video channel class, temporal version
  will be refactored in the future
###

#= require <socket.coffee>
#= require <channel.coffee>


class Batman.VideoChannel extends Batman.Channel

  peer: null


  ###
    mystream is a temporal global variable to save a stream from a webcome
  ###

  constructor: (name, @room, @myStream = null)->
    super(name)
    @set("src","")
    #alert "name = #{name} | room = #{@room}"
    @startPeer()
    @on "ICE", (event)=>@onGetICE(event.content)
    @on "offer",  (event)=>@onGetOffer(event.content)
    @on "answer", (event)=>@onGetAnswer(event.content)


  askWebcam: =>
    @ask "webcam"

  startPeer: (servers=null)=>
    ###
    starts p2p connection
    ###
    @peer = @makePeer()
    @peer.onicecandidate = @onCreateICE
    @peer.onaddstream = @onGetRemoteStream





  makePeer:  (servers=null)=>
    if window.RTCPeerConnection?
      new RTCPeerConnection(servers)
    else
      if window.mozRTCPeerConnection?
        new mozRTCPeerConnection(servers)
      else
        new webkitRTCPeerConnection(servers)

  onWebCamSuccess:  (stream)=>
    ###
      when webcam stream received
    ###
    @myStream = stream
    @peer.onaddstream = (st)=>  #just for protection
    @peer.addStream(stream)
    @peer.onaddstream = @onGetRemoteStream
    @fire "localStream", stream



  call: =>
    ###
      Makes a call
    ###
    console.log "VideoChannel CALL from #{@name} 2 #{@room}"
    if @myStream?
      @peer.createOffer(@onCreateOffer)
    else
      @askWebcam()
      @on "localStream", @call


  onCreateOffer: (desc)=>
    ###
      fires when you propose and offer
    ###
    @peer.setLocalDescription(desc)
    offer = Batman.SocketEvent.makeEvent(desc,@name,"offer",@room)
    @fire "send", offer

  onGetOffer: (event)=>
    ###
      fires when you received another's offer
    ###
    desc = new RTCSessionDescription(event)
    @peer.setRemoteDescription(desc)
    @peer.createAnswer(@onCreateAnswer)
    console.log "offer received"



  onCreateAnswer:  (desc)=>
    ###
      fires when you created an answer
    ###
    @peer.setLocalDescription(desc)
    answer = Batman.SocketEvent.makeEvent(desc,@name,"answer",@room)
    @fire "send", answer

  onGetAnswer:  (event)=>
    ###
      fires when you received an answer
    ###
    desc = new RTCSessionDescription(event)
    @peer.setRemoteDescription(desc)
    console.log "answer received"

  onGetRemoteStream: (e)=>
    ###
      fires when you got stream
    ###
    console.log "got remote stream"
    if e.stream?
      stream = e.stream
      @fire "remoteStream", stream
    else
      alert "bug in onGetRemoteStream"

  onCreateICE: (event)=>
    ###
      fires when you make an ICE candidates
    ###
    if event.candidate?
      cand = event.candidate
      evt = Batman.SocketEvent.makeEvent(cand,@name,"ICE",@room)
      @fire "send", evt
    ###
    else
      alert "onICE do not work well"
      alert JSON.stringify(event)
    ###

  onGetICE: (event)=>
    ###
      fires when you received and ICE
    ###
    #cand = event.candidate?
    #str = JSON.stringify(event)
    #№alert "I got ice! "+str
    @peer.addIceCandidate(new RTCIceCandidate(event))

  ###
  onmessage: (event)=>
    switch event.request
      when "ICE" then @onGetICE(event.content)
      when "offer" then  @onGetOffer(event.content)
      when "answer" then @onGetAnswer(event.content)
  ###

  onError: (e)->
    alert "There has been a problem retrieving the streams - did you allow access?"

  subscribeLocal: (vid)=>
    @on "localStream", (stream)=>
      src = @stream2src(stream)
      @set "src", src
      vid.src = src

  subscribeRemote: (vid)=>
    @on "remoteStream", (stream)=>
      src = @stream2src(stream)
      @set "src", src
      vid.src = src

  attach: (obj)=>
    ###
      Attaches the channel to the socket wrapper and subscribes to its events
    ###
    receive = @receive #trick to overcome "this" javascript change
    if @room? and @room!="all" #TODO: fix this Indus-like code in Future
      obj.on(@name+"2"+@room,receive)
    else
      obj.on @name, receive
    obj.on "all", receive

    send = obj.send
    @on "send", send

    @on "ask", obj.ask
    cl = @constructor.name
    obj.fire(cl,@name)
    @

  attach: (obj)=>
    onStream = @onWebCamSuccess
    obj.on "localStream", onStream
    super(obj)
    if @myStream?
      @peer.addStream(@myStream)
      @peer.onaddstream = @onGetRemoteStream
    else
      @askWebcam()
    @

