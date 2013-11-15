class Denigma.BarView extends Denigma.BasicView
  ###
    view that shows all the bars in the charts
  ###

  width: undefined
  test: undefined
  control: undefined
  xAxis: undefined

  constructor: (poser,@minW,@minH)->
    super(poser)
    @test = new Denigma.LabeledBar(@poser,"test",@minW,@minH) #for experimental group
    @control = new Denigma.ExperimentBar(@poser,"control",@minW,@minH*3) #for control group
    @xAxis = d3.svg.axis().orient("bottom")


  append: (novel)->
    @control.append(novel)
    @test.append(novel)
    novel.append("svg").attr("class","axis")


  update: (sel)->
    @makeScale(sel)
    @updateAxis(sel)
    @control.scale = @scale
    @control.update(sel)
    @test.scale = @scale
    @test.update(sel)

  makeScale: (sel)->
    @width = sel.attr("width")
    data = sel.data()
    max = d3.max(data, (d)->d.get "max")
    @scale = d3.scale.linear().domain([0,max]).range([@poser.marginX, @width-@poser.marginX])
    @scale

  updateAxis: (sel)->
    @xAxis.scale(@scale)
    g = sel.select("svg.axis")
    h = @poser.contentHeight()
    g.attr("y",h)
      .call(@xAxis)
