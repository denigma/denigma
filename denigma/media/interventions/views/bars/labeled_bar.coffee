class Denigma.LabeledBar extends Denigma.ExperimentBar

  append: (row)->
    bars = super(row)
    bars.append("rect").attr("class","textmax")
    bars.append("rect").attr("class","textmean")
    bars.append("rect").attr("class","textmin")
    bars.append("text").attr("class","max").text("max")
    bars.append("text").attr("class","mean").text("mean")
    bars.append("text").attr("class","min").text("min")
    bars

  updateLabel: (sel,key)->

  rnd: (numberToRound) ->  Math.round(numberToRound * 10) / 10


  updateBar: (sel,key,h)->
    super(sel,key,h)
    val = (d)=> @rnd(d[@group].get(key))
    fun = (d)=>@scale(val(d)) - @minW + @poser.marginX

    bh = @minH*2
    bw = @minW*2
    posBY = @poser.getMiddlePos(bh)
    #TODO: work with text width instead of constant size

    back = @select(sel,"text#{key}", "rect")
    back.attr("height",bh)
      .attr("x",@poser.marginX)
      .attr("y",posBY)
      .attr("width",bw)


    posTY = @poser.getMiddlePos(-@minH)
    text = @select(sel,key, "text")
    text.attr("x",@poser.marginX)
      .attr("y",posTY)
    text.transition().duration(@poser.dur)
      .attr("x",fun)
      .attr("width",bw)
      .attr("text-anchor", "middle")
      .text(val)


    back.transition().duration(@poser.dur)
      .attr("x",(d)->fun(d)-bw/2)

