###
@fileOverview Contains definition of the core graph object.

@author Andrei Kashcha (aka anvaka) / http://anvaka.blogspot.com
###

###
@namespace Represents a graph data structure.

@example
var g = Viva.Graph.graph();
g.addNode(1);     // g has one node.
g.addLink(2, 3);  // now g contains three nodes and one link.
###
class Denigma.Graph

  # Graph structure is maintained as dictionary of nodes
  # and array of links. Each node has 'links' property which
  # hold all links related to that node. And general links
  # array is used to speed up all links enumeration. This is inefficient
  # in terms of memory, but simplifies coding. Furthermore, the graph structure
  # is isolated from outter world, and can be changed to adjacency matrix later.
  nodes : {}
  links : []
  nodesCount : 0
  suspendEvents : 0

  # Accumlates all changes made during graph updates.
  # Each change element contains:
  #  changeType - one of the strings: 'add', 'remove' or 'update';
  #  node - if change is related to node this property is set to changed graph's node;
  #  link - if change is related to link this property is set to changed graph's link;
  changes : []

  constructor: ->
    Viva.Graph.Utils.events(@).extend()


  fireGraphChanged: (graph) ->

    # TODO: maybe we shall copy changes?
    graph.fire "changed", @changes


  # Enter, Exit Mofidication allows bulk graph updates without firing events.
  enterModification: ->
    @suspendEvents += 1

  exitModification:  (graph) ->
    @suspendEvents -= 1
    if @suspendEvents is 0 and @changes.length > 0
      @fireGraphChanged graph
      @changes.length = 0

  recordNodeChange: (node, changeType) ->

    # TODO: Could add changeType verification.
    @changes.push
      node: node
      changeType: changeType


  recordLinkChange: (link, changeType) ->

    # TODO: Could add change type verification;
    @changes.push
      link: link
      changeType: changeType


  isArray: (value) ->
    value and typeof value is "object" and typeof value.length is "number" and typeof value.splice is "function" and not (value.propertyIsEnumerable("length"))




  ###
  Adds node to the graph. If node with given id already exists in the graph
  its data is extended with whatever comes in 'data' argument.

  @param nodeId the node's identifier. A string is preferred.
  @param [data] additional data for the node being added. If node already
  exists its data object is augmented with the new one.

  @return {node} The newly added node or node with given id if it already exists.
  ###
  addNode: (nodeId, data) ->
    throw message: "Invalid node identifier"  if typeof nodeId is "undefined"
    @enterModification()
    node = @getNode(nodeId)
    unless node
      node = new Viva.Graph.Node(nodeId)
      @nodesCount++
      @recordNodeChange node, "add"
    else
      @recordNodeChange node, "update"
    if data?
      augmentedData = node.data or {}
      dataType = typeof data
      name = undefined
      if dataType is "string" or @isArray(data) or dataType is "number" or dataType is "boolean"
        augmentedData = data
      else if dataType is "undefined"
        augmentedData = null
      else
        for name of data
          augmentedData[name] = data[name]  if data.hasOwnProperty(name)
      node.data = augmentedData
    @nodes[nodeId] = node
    @exitModification this
    node

  addEdge: (fromId, toId, data) => @addLink(fromId,toId,data)

  ###
  Adds a link to the graph. The function always create a new
  link between two nodes. If one of the nodes does not exists
  a new node is created.

  @param fromId link start node id;
  @param toId link end node id;
  @param [data] additional data to be set on the new link;

  @return {link} The newly created link
  ###
  addLink: (fromId, toId, data) ->
    @enterModification()
    fromNode = @getNode(fromId) or @addNode(fromId)
    toNode = @getNode(toId) or @addNode(toId)
    link = new Viva.Graph.Link(fromId, toId, data)
    @links.push link

    # TODO: this is not cool. On large graphs potentially would consume more memory.
    fromNode.links.push link
    toNode.links.push link
    @recordLinkChange link, "add"
    @exitModification this
    link


  ###
  Removes link from the graph. If link does not exist does nothing.

  @param link - object returned by addLink() or getLinks() methods.

  @returns true if link was removed; false otherwise.
  ###
  removeLink: (link) ->
    return false  unless link
    idx = Viva.Graph.Utils.indexOfElementInArray(link, @links)
    return false  if idx < 0
    enterModification()
    @links.splice idx, 1
    fromNode = @getNode(link.fromId)
    toNode = @getNode(link.toId)
    if fromNode
      idx = Viva.Graph.Utils.indexOfElementInArray(link, fromNode.links)
      fromNode.links.splice idx, 1  if idx >= 0
    if toNode
      idx = Viva.Graph.Utils.indexOfElementInArray(link, toNode.links)
      toNode.links.splice idx, 1  if idx >= 0
    @recordLinkChange link, "remove"
    @exitModification this
    true


  ###
  Removes node with given id from the graph. If node does not exist in the graph
  does nothing.

  @param nodeId node's identifier passed to addNode() function.

  @returns true if node was removed; false otherwise.
  ###
  removeNode: (nodeId) ->
    node = @getNode(nodeId)
    return false  unless node
    @enterModification()
    while node.links.length
      link = node.links[0]
      @removeLink link
    @nodes[nodeId] = null
    delete @nodes[nodeId]

    @nodesCount--
    @recordNodeChange node, "remove"
    @exitModification this


  ###
  Gets node with given identifier. If node does not exist undefined value is returned.

  @param nodeId requested node identifier;

  @return {node} in with requested identifier or undefined if no such node exists.
  ###
  getNode: (nodeId) =>
    @nodes[nodeId]


  ###
  Gets number of nodes in this graph.

  @return number of nodes in the graph.
  ###
  getNodesCount: ->
    @nodesCount


  ###
  Gets total number of links in the graph.
  ###
  getLinksCount: ->
    @links.length


  ###
  Gets all links (inbound and outbound) from the node with given id.
  If node with given id is not found null is returned.

  @param nodeId requested node identifier.

  @return Array of links from and to requested node if such node exists;
  otherwise null is returned.
  ###
  getLinks: (nodeId) ->
    node = @getNode(nodeId)
    (if node then node.links else null)


  ###
  Invokes callback on each node of the graph.

  @param {Function(node)} callback Function to be invoked. The function
  is passed one argument: visited node.
  ###
  forEachNode: (callback) =>
    return  if typeof callback isnt "function"
    node = undefined

    # TODO: could it be faster for nodes iteration if we had indexed access?
    # I.e. use array + 'for' iterator instead of dictionary + 'for .. in'?
    for node of @nodes
      # For performance reasons you might want to sacrifice this sanity check:
      callback(@nodes[node])  if @nodes.hasOwnProperty(node)


  ###
  Invokes callback on every linked (adjacent) node to the given one.

  @param nodeId Identifier of the requested node.
  @param {Function(node, link)} callback Function to be called on all linked nodes.
  The function is passed two parameters: adjacent node and link object itself.
  @param oriented if true graph treated as oriented.
  ###
  forEachLinkedNode: (nodeId, callback, oriented) ->
    node = @getNode(nodeId)
    i = undefined
    link = undefined
    linkedNodeId = undefined
    if node and node.links and typeof callback is "function"

      # Extraced orientation check out of the loop to increase performance
      if oriented
        i = 0
        while i < node.links.length
          link = node.links[i]
          callback nodes[link.toId], link  if link.fromId is nodeId
          ++i
      else
        i = 0
        while i < node.links.length
          link = node.links[i]
          linkedNodeId = (if link.fromId is nodeId then link.toId else link.fromId)
          callback nodes[linkedNodeId], link
          ++i


  ###
  Enumerates all links in the graph

  @param {Function(link)} callback Function to be called on all links in the graph.
  The function is passed one parameter: graph's link object.

  Link object contains at least the following fields:
  fromId - node id where link starts;
  toId - node id where link ends,
  data - additional data passed to graph.addLink() method.
  ###
  forEachLink: (callback) ->
    i = undefined
    if typeof callback is "function"
      i = 0
      while i < @links.length
        callback @links[i]
        ++i


  ###
  Suspend all notifications about graph changes until
  endUpdate is called.
  ###
  beginUpdate: ->
    @enterModification()


  ###
  Resumes all notifications about graph changes and fires
  graph 'changed' event in case there are any pending changes.
  ###
  endUpdate: ->
    @exitModification this


  ###
  Removes all nodes and links from the graph.
  ###
  clear: ->
    that = this
    that.beginUpdate()
    that.forEachNode (node) ->
      that.removeNode node.id

    that.endUpdate()


  ###
  Detects whether there is a link between two nodes.
  Operation complexity is O(n) where n - number of links of a node.

  @returns link if there is one. null otherwise.
  ###
  hasLink: (fromNodeId, toNodeId) ->

    # TODO: Use adjacency matrix to speed up this operation.
    node = @getNode(fromNodeId)
    i = undefined
    return null  unless node
    i = 0
    while i < node.links.length
      link = node.links[i]
      return link  if link.fromId is fromNodeId and link.toId is toNodeId
      ++i
    null # no link.


  # Let graph fire events before we return it to the caller.

