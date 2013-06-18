class Denigma.Curves extends Denigma.Charts
  ###
    class to display lifespan curves
  ###

  marginX : 15 #left margin
  marginY : 15 #top margin
  ticksY: 20

  pointRad: 5

  constructor: (selector,subclass)->
    super(selector,subclass)
    @xAxis = d3.svg.axis().orient("bottom")
    funY = (t)->if(t==0) then "" else (t+"%")
    @yAxis = d3.svg.axis().orient("right").ticks(@ticksY).tickFormat(funY)
    @svg.append("svg").attr("class","xAxis")
    @svg.append("svg").attr("class","yAxis")


  draw: (data)->
    max = @max(data)
    yrMax = @height-@marginY
    @xScale = d3.scale.linear().domain([0,max]).range([@marginX, @width-@marginX])
    @yScale = d3.scale.linear().domain([0,100]).range([yrMax, @marginY])
    @updateAxises(data)
    sel =  @select(data)
    @hide(sel.exit())
    novel = @append(sel.enter())
    @update(sel)

  max: (data)->d3.max(data,(d)->d.get("max"))

  append: (novel)->
    sv = novel.append("svg")
    sv.attr("class","#{@subclass}")
    sv.append("path")
    novel

  makePoint: (x,y,color)=> {x:x,y:y,c:color}

  makeCoords: (d)=>
    ###
      creates coord array for curves
    ###
    col = @randColor()
    orgs = d.get("organisms").sort((a,b)->a-b)
    res = [@makePoint(0,100,col)]
    len = orgs.length
    alive = len
    for o in orgs
      alive = alive-1
      res.push(@makePoint(o,Math.round(alive/len*100),col))
    res

  randColor: =>'#'+(Math.random()*0xFFFFFF<<0).toString(16)



  update: (sel)->
    xFun = (d)=> @xScale(d.x)
    yFun = (d)=> @yScale(d.y)

    poly = d3.svg.line()
      .x( xFun)
      .y( yFun )
    #  .interpolate("line")
      .interpolate("monotone")

    coords = @makeCoords
    data = sel.data().map((d)->coords(d))
    path = sel.select("path")
    getData = (d,i)->data[i]
    getColor = (d,i)->data[i][0].c
    makePoly = (d,i)->poly(data[i])

    path
      .attr("stroke",getColor)
      .attr("fill","none")
      .attr("d",makePoly)

    points = sel.selectAll("circle.point").data(getData)
    points.exit().remove()
    points.enter().append("circle").attr("class","point").attr("r",@pointRad)
    points.attr("cx",xFun).attr("cy",yFun).attr("fill",(d)->d.c)



  updateAxises: (data)->
    @xAxis.scale(@xScale)
    gx = @svg.select("svg.xAxis")
    gx.attr("y",@height-@marginY).call(@xAxis)

    @yAxis.scale(@yScale)
    gy = @svg.select("svg.yAxis")
    gy.attr("x",@marginX)
      .call(@yAxis)


