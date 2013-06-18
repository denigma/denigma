class Denigma.Intervention extends Batman.Object
  ###
    Intervention with animal
  ###

  @makeSum: (key)->
    get: -> @test.get(key) + @control.get(key)


  @makeDelta: (key)->
    get: -> @test.get(key) - @control.get(key)

  @makeMax: (key)->
    get: -> Math.max(@test.get(key), @control.get(key))

  @makeMin: (key)->
    get: -> Math.min(@test.get(key), @control.get(key))

  @accessor "number", @makeSum("number")

  @accessor "deltaNumber", @makeDelta("number")

  @accessor "deltaMax", @makeDelta("max")

  @accessor "deltaMean", @makeDelta("mean")

  @accessor "deltaMin", @makeDelta("min")

  @accessor "max", @makeMax("max")

  @accessor "min", @makeMin("min")

  constructor: (@species, @manipulation, @test, @control)->
    ###
      constructor that stores test, control groups and manipulations
    ###

  @getSpeciesName: (d)=>d.species.commonName



