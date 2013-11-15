class Denigma.Experiment extends Batman.Object
  ###
    class that describes experimental group (it can be either test or control one
    it has many accessors as the info is often incomplete
  ###
  _number: 0
  _min: -1
  _mean: 0
  _median: 0
  _max: 0

  #TODO: rename organisms to organisms

  constructor: (@line, organisms = [])->
    if(organisms?)
      @set "organisms", organisms
    else
      @set "organisms", []

  rnd: (numberToRound) ->  Math.round(numberToRound * 100) / 100

  @makeGetSet: (prop,calc)->
    ###
        function to generate getters and setters for accessors
    ###
    get: ->
      organisms =@get("organisms")
      if(organisms.length>0)
        calc(organisms)
      else
        #alert "_#{prop} = " + @["_#{prop}"]
        @["_#{prop}"]

    set: (key, value)->
      if @get("organisms")?.length>0
        throw new Error("has organisms inside")
      else
        @["_#{prop}"]  = value


  @accessor "median", @makeGetSet("median",d3.median)

  @accessor "max", @makeGetSet("max",d3.max)

  @accessor "mean", @makeGetSet("mean",d3.mean)

  @accessor "min", @makeGetSet("min",d3.min)

  @accessor "number", @makeGetSet("number",(arr)->arr.length)




