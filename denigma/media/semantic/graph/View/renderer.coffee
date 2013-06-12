###
@fileOverview Defines a graph renderer that uses CSS based drawings.

@author Andrei Kashcha (aka anvaka) / http://anvaka.blogspot.com
###
Viva.Graph.View = Viva.Graph.View or {}

###
This is heart of the rendering. Class accepts graph to be rendered and rendering settings.
It monitors graph changes and depicts them accordingly.

@param graph - Viva.Graph.graph() object to be rendered.
@param settings - rendering settings, composed from the following parts (with their defaults shown):
settings = {
// Represents a module that is capable of displaying graph nodes and links.
// all graphics has to correspond to defined interface and can be later easily
// replaced for specific needs (e.g. adding WebGL should be piece of cake as long
// as WebGL has implemented required interface). See svgGraphics for example.
// NOTE: current version supports Viva.Graph.View.cssGraphics() as well.
graphics : Viva.Graph.View.svgGraphics(),

// Where the renderer should draw graph. Container size matters, because
// renderer will attempt center graph to that size. Also graphics modules
// might depend on it.
container : document.body,

// Layout algorithm to be used. The algorithm is expected to comply with defined
// interface and is expected to be iterative. Renderer will use it then to calculate
// grpaph's layout. For examples of the interface refer to Viva.Graph.Layout.forceDirected()
// and Viva.Graph.Layout.gem() algorithms.
layout : Viva.Graph.Layout.forceDirected(),

// Directs renderer to display links. Usually rendering links is the slowest part of this
// library. So if you don't need to display links, consider settings this property to false.
renderLinks : true,

// Number of layout iterations to run before displaying the graph. The bigger you set this number
// the closer to ideal position graph will apper first time. But be careful: for large graphs
// it can freeze the browser.
prerender : 0
}
###
class Denigma.Graph.Renderer

  graph: null
  graphEvents : undefined
  containerDrag : undefined
  inputManager : undefined
  animationTimer : undefined
  rendererInitialized : false
  updateCenterRequired : true
  currentStep : 0
  totalIterationsCount : 0
  isStable : false
  userInteraction : false
  viewPortOffset :
    x: 0
    y: 0

  cachedFromPos:
    # Cache positions object to prevent GC pressure
    x: 0
    y: 0
    node: null

  cachedToPos:
    x: 0
    y: 0
    node: null

  cachedNodePos:
    x: 0
    y: 0

  transform : undefined




  constructor: (@graph, @settings) ->
    # TODO: This class is getting hard to understand. Consider refactoring.
    # TODO: I have a technical debt here: fix scaling/recentring! Currently it's total mess.
    @FRAME_INTERVAL = 30
    @settings = settings or {}
    @layout = settings.layout
    @graphics = settings.graphics
    @container = settings.container

    @transform =
      offsetX: 0
      offsetY: 0
      scale: 1

    @windowEvents = Viva.Graph.Utils.events(window)
    @publicEvents = Viva.Graph.Utils.events({}).extend()


  prepareSettings: =>
    @container = @container or window.document.body
    @layout = @layout or Viva.Graph.Layout.forceDirected(@graph)
    @graphics = @graphics or Viva.Graph.View.svgGraphics(@graph,
      container: @container
    )
    @settings.renderLinks = true  unless @settings.hasOwnProperty("renderLinks")
    @settings.prerender = @settings.prerender or 0
    @inputManager = (@graphics.inputManager or Viva.Input.domInputManager)(@graph, @graphics)

  renderLink:  (link) =>
    fromNode = @graph.getNode(link.fromId)
    toNode = @graph.getNode(link.toId)
    return  if not fromNode or not toNode
    @cachedFromPos.x = fromNode.position.x
    @cachedFromPos.y = fromNode.position.y
    @cachedFromPos.node = fromNode
    @cachedToPos.x = toNode.position.x
    @cachedToPos.y = toNode.position.y
    @cachedToPos.node = toNode
    @graphics.updateLinkPosition link.ui, @cachedFromPos, @cachedToPos

  renderNode: (node) =>
    @cachedNodePos.x = node.position.x
    @cachedNodePos.y = node.position.y
    @graphics.updateNodePosition node.ui, @cachedNodePos

  renderGraph: ->
    @graphics.beginRender()
    rn = @renderNode
    rl = @renderLink

    @graph.forEachLink rl # if settings.renderLinks and not graphics.omitLinksRendering
    @graph.forEachNode rn
    @graphics.endRender()

  onRenderFrame: =>
    @isStable = @layout.step() and not @userInteraction
    @renderGraph()
    not @isStable

  renderIterations : (iterationsCount) ->
    onR = @onRenderFrame
    if @animationTimer?
      @totalIterationsCount += iterationsCount
      return
    if iterationsCount?
      @totalIterationsCount += iterationsCount
      @animationTimer = Viva.Graph.Utils.timer(=>
        onR()
      , @FRAME_INTERVAL)
    else
      @currentStep = 0
      @totalIterationsCount = 0
      @animationTimer = Viva.Graph.Utils.timer(onR, @FRAME_INTERVAL)

  resetStable : ->
    @isStable = false
    @animationTimer.restart()

  prerender : ->

    # To get good initial positions for the graph
    # perform several prerender steps in background.
    i = undefined
    if typeof @settings.prerender is "number" and @settings.prerender > 0
      i = 0
      while i < @settings.prerender
        @layout.step()
        i += 1
    else
      @layout.step() # make one step to init positions property.

  updateCenter: =>
    @graphRect = @layout.getGraphRect()
    @containerSize = Viva.Graph.Utils.getDimension(@container)
    @viewPortOffset.x = @viewPortOffset.y = 0
    @transform.offsetX = @containerSize.width / 2 - (@graphRect.x2 + @graphRect.x1) / 2
    @transform.offsetY = @containerSize.height / 2 - (@graphRect.y2 + @graphRect.y1) / 2
    @graphics.graphCenterChanged @transform.offsetX + @viewPortOffset.x, @transform.offsetY + @viewPortOffset.y
    @updateCenterRequired = false

  createNodeUi: (node) ->
    nodeUI = @graphics.node(node)
    node.ui = nodeUI
    @graphics.initNode nodeUI
    @layout.addNode node
    @renderNode node

  removeNodeUi: (node) ->
    if node.hasOwnProperty("ui")
      @graphics.releaseNode node.ui
      node.ui = null
      delete node.ui
    @layout.removeNode node

  createLinkUi:  (link) ->
    linkUI = @graphics.link(link)
    link.ui = linkUI
    @graphics.initLink linkUI
    @renderLink link  unless @graphics.omitLinksRendering

  removeLinkUi: (link) ->
    if link.hasOwnProperty("ui")
      @graphics.releaseLink link.ui
      link.ui = null
      delete link.ui

  listenNodeEvents: (node) ->
    wasPinned = false

    startHandler = =>
      wasPinned = node.isPinned
      node.isPinned = true
      @userInteraction = true
      @resetStable()

    dragHandler = (e, offset) =>
      node.position.x += offset.x / @transform.scale
      node.position.y += offset.y / @transform.scale
      @userInteraction = true
      @renderGraph()

    stopHandler = =>
      node.isPinned = wasPinned
      @userInteraction = false

    handlers =
      onStart: startHandler
      onDrag: dragHandler
      onStop: stopHandler

    # TODO: This may not be memory efficient. Consider reusing handlers object.
    @inputManager.bindDragNDrop node, handlers


  releaseNodeEvents: (node) ->
    @inputManager.bindDragNDrop node, null

  initDom: =>
    @graphics.init @container
    @graph.forEachNode @createNodeUi
    @graph.forEachLink @createLinkUi  #if settings.renderLinks

  releaseDom: =>
    @graphics.release @container

  processNodeChange: (change) ->
    node = change.node
    switch change.changeType
      when "add"
        @createNodeUi node
        @listenNodeEvents node
        @updateCenter()  if @updateCenterRequired
      when "remove"
        @releaseNodeEvents node
        @removeNodeUi node
        @updateCenterRequired = true  if @graph.getNodesCount() is 0 # Next time when node is added - center the graph.
      when "update"
          @releaseNodeEvents(node)
          @removeNodeUi(node)
          @createNodeUi(node)
          @listenNodeEvents(node)
          console.log "TODO:REWRITE node change"
      else
        throw "Update type is not implemented. TODO: Implement me!"

  processLinkChange: (change) ->
    link = change.link
    switch change.changeType
      when "add"
        @createLinkUi link  if @settings.renderLinks
        @layout.addLink link
      when "remove"
        @removeLinkUi link  if @settings.renderLinks
        @layout.removeLink link
      when "update"
        @removeLinkUi link  if @settings.renderLinks
        @layout.removeLink link
        @createLinkUi link  if @settings.renderLinks
        @layout.addLink link
        console.log "TODO:REWRITE link change"
      else
        throw "Update type is not implemented. TODO: Implement me!"

  onGraphChanged:  (changes) =>
    i = undefined
    change = undefined
    i = 0
    while i < changes.length
      change = changes[i]
      if change.node
        @processNodeChange change
      else @processLinkChange change  if change.link
      i += 1
    @resetStable()

  onWindowResized: =>
    @updateCenter()
    @onRenderFrame()

  releaseContainerDragManager: =>
    if @containerDrag
      @containerDrag.release()
      @containerDrag = null

  releaseGraphEvents : =>
    if @graphEvents
      ch = @onGraphChanged
      # Interesting.. why is it not null? Anyway:
      @graphEvents.stop "changed", ch
      @graphEvents = null

  dragHandler: (e, offset) =>
    @viewPortOffset.x += offset.x
    @viewPortOffset.y += offset.y
    @graphics.translateRel offset.x, offset.y
    @renderGraph()

  scrollHandler: (e, scaleOffset, scrollPoint) =>
    @scaleFactor = Math.pow(1 + 0.4, (if scaleOffset < 0 then -0.2 else 0.2))
    @transform.scale = @graphics.scale(@scaleFactor, scrollPoint)
    @renderGraph()
    @publicEvents.fire "scale", @transform.scale


  listenToEvents: ->
    resize = @onWindowResized
    @windowEvents.on "resize", resize
    @releaseContainerDragManager()
    @containerDrag = Viva.Graph.Utils.dragndrop(@container)
    dh = @dragHandler
    @containerDrag.onDrag dh
    sc = @scrollHandler
    @containerDrag.onScroll sc
    lne = @listenNodeEvents
    @graph.forEachNode lne
    @releaseGraphEvents()
    @graphEvents = Viva.Graph.Utils.events(@graph)
    ch = @onGraphChanged
    @graphEvents.on "changed", ch

  removeLinkHandler: (link)->
    @removeLinkUi link  if @settings.renderLinks
    @layout.removeLink link

  removeNodeHandler: (node)->
    @releaseNodeEvents node
    @removeNodeUi node

  stopListenToEvents: ->
    @rendererInitialized = false
    @releaseGraphEvents()
    @releaseContainerDragManager()
    resize = @onWindowResized
    @windowEvents.stop "resize", resize
    @publicEvents.removeAllListeners()
    @animationTimer.stop()
    rml = @removeLinkHandler
    @graph.forEachLink rml

    rmn = @removeNodeHandler
    @graph.forEachNode rmn

    @layout.dispose()
    @releaseDom()


  ###
  Performs rendering of the graph.

  @param iterationsCount if specified renderer will run only given number of iterations
  and then stop. Otherwise graph rendering is performed infinitely.

  Note: if rendering stopped by used started dragging nodes or new nodes were added to the
  graph renderer will give run more iterations to reflect changes.
  ###
  run: (iterationsCount) ->
    unless @rendererInitialized
      @prepareSettings()
      @prerender()
      @updateCenter()
      @initDom()
      @listenToEvents()
      @rendererInitialized = true
    @renderIterations iterationsCount
    this

  reset: ->
    @graphics.resetScale()
    @updateCenter()
    @transform.scale = 1

  pause: ->
    @animationTimer.stop()

  resume: ->
    @animationTimer.restart()

  rerender: ->
    @renderGraph()
    this


  ###
  Removes this renderer and deallocates all resources/timers
  ###
  @dispose: ->
    @stopListenToEvents() # I quit!

  @on: (eventName, callback) ->
    @publicEvents.addEventListener eventName, callback
    this

  @off: (eventName, callback) ->
    @publicEvents.removeEventListener eventName, callback
    this