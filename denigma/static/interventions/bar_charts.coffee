class Denigma.BarCharts extends Denigma.Charts
  ###
    class to generate chars with d3js
  ###

  node: undefined
  svg: undefined

  width: 0
  height: 0

  poser: undefined
  iconView: undefined
  decorView:undefined

  iconWidth: 180

  durNew: 400


  constructor: (selector,subclass)->
    ###
      jquery-like selector string is passed,
      something like '#lifespan'
    ###
    super(selector,subclass)
    @poser = new Denigma.RowPoser(rowMargin =20, rowHeight = 56,marginX = 10, dur = 2000)
    @decorView = new Denigma.DecorView(@poser,@width)
    @iconView = new Denigma.IconView(poser = @poser, resources ="static/interventions/resources")
    @barView = new Denigma.BarView(poser =@poser,minW = 15,minH = 10)

  setSize: (w,h)->
    ###
      sets size of the main svg
    ###
    @width = w
    @height = h
    @svg.attr("width",w).attr("height",h)



  append: (novel)->
    rows = novel.append('svg')
    rows.attr "class", "row"
    rows.attr "y", 0
    #@posRows(rows)
    @decorView.width = @width
    @decorView.append(rows)

    icons = rows.append("svg")
    icons.attr "class", "icon"
    @iconView.append(icons)

    bars = rows.append("svg")
    bars.attr("class", "bar")
      .attr("x",@iconWidth)
    @barView.append(bars)

    #novel.append("rect").attr("class","icon").attr("y",(d,i)=>i*c).attr("width",100).attr("height",h).attr("x",0)

    #novel.append("rect").attr("class","test").attr("y",(d,i)=>i*c).attr("width",100).attr("height",h).attr("x",150)
    #novel.append("rect").attr("class","control").attr("y",(d,i)=>i*c).attr("width",100).attr("height",h).attr("x",300)
    novel

  update: (sel)->
    pos = @poser.getRowPos

    icons = sel.select("svg.icon")
    icons.attr("width", @iconWidth)
    @iconView.update(icons)

    bars = sel.select("svg.bar")
    bars.attr("x",@iconWidth)
    bars.attr("width",@width-@iconWidth)
    @barView.update(bars)

    sel.transition().duration(@durNew)
      .attr("y", pos)
      .attr("width",@width)

  hide: (sel)->
    tr = sel.transition()
    tr.duration(@durNew).attr("y", 0)
    tr.delay(@durNew).remove()