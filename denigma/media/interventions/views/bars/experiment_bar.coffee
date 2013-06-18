class Denigma.ExperimentBar extends Denigma.BasicView
  ###
    creates a bar for interventions
  ###

  scale:undefined

  constructor: (poser,@group,@minW,@minH)->
    super(poser)

  append: (row)->
    bars = row.append("svg")
    bars.attr("class", @group)

    bars.append("rect").attr("class","max")
    bars.append("rect").attr("class","mean")
    bars.append("rect").attr("class","min")
    bars


  updateBar: (sel,key,h)->
    h = @minH unless h?
    posY = @poser.getMiddlePos(h)
    fun = (d)=>@scale(d[@group].get(key))
    bar = @select(sel,key, "rect")
    bar.attr("x",@poser.marginX)
      .attr("y",posY)
      .attr("width",@minW)
      .attr("height",h)

    bar.transition().duration(@poser.dur)
      .attr("width",fun)
      .attr("rx",3)
      .attr("ry",3)

  select: (sel,key,cl="rect")->
    sel.select(".#{@group} #{cl}.#{key}")

  update: (sel)->
    h = @minH
    @updateBar(sel,"min",h)
    @updateBar(sel, "mean",h)
    @updateBar(sel, "max",h)
    sel
