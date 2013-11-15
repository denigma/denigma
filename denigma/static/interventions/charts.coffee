###
  the basic workflow with charts is the following::

    on construction you pass the id of the element where you want to insert your charts to
    and the name of the class for your basic elements

  When you want to draw something you


###
class Denigma.Charts
  ###
    abstract class that works with charts
  ###

  node: undefined
  svg: undefined
  marginX : 10 #left margin
  marginY : 10 #top margin

  width: 0
  height: 0
  durNew: 400


  constructor: (@selector,@subclass)->
    ###
      jquery-like selector string is passed,
      something like '#lifespan'
    ###
    @node = d3.select(@selector)
    @svg = @node.append("svg")

  select: (data)->
    @svg.selectAll("svg.#{@subclass}").data(data)

  enter:(data)->@select(data).enter()

  exit:(data)->@select(data).exit().remove()

  setSize: (w,h)->
    ###
      sets size of the main svg
    ###
    @width = w
    @height = h
    @svg.attr("width",w).attr("height",h)



  append: (novel)->
      error("append is not implemented")
      novel


  draw: (data)->
    sel =  @select(data)
    @hide(sel.exit())
    novel = @append(sel.enter())
    @update(sel)

  hide: (sel)->
    sel.remove()


  update: (sel)->
    error("update is not implemented")
