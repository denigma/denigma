###
Single texture in the webglAtlas.
###
class Texture
  constructor: (size) ->
    @canvas = window.document.createElement("canvas")
    @ctx = @canvas.getContext("2d")
    @isDirty = false
    @canvas.width = @canvas.height = size
