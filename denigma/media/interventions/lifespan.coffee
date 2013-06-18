###
  Here is where the main code of the demo is
###

class Denigma.LifeSpan extends Batman.Object

  fixture: undefined
  barcharts: undefined
  @w: 640
  @h: 640

  @main: ->
    @fixture = new Denigma.Fixture()

    @barcharts = new Denigma.BarCharts("#lifespanbars","row")
    @positionBars()
    @generateBars()

    @curves = new Denigma.Curves("#lifespancurves","curve")
    @positionCurves()
    @generateCurves()

  @positionBars: ->
    @barcharts.svg.attr("class","chart")
    @barcharts.setSize(@w,@h)

  @generateBars: ->
    num = @fixture.rand(2,5)
    data = @fixture.generate(num)
    @barcharts.draw(data)

  @positionCurves: ->
    @curves.svg.attr("class","chart")
    @curves.setSize(@w,@h)

  @generateCurves: =>
    num =  @fixture.rand(2,5)
    groups = @fixture.generateCurves(num)
    @curves.draw(groups)

Denigma.on "start", ->
  ###
    Event to initiate the main app
  ###
  Denigma.LifeSpan.main()
  #ls.experiment()

