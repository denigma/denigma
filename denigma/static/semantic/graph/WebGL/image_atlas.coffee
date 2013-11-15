###
Defines simple UI for nodes in webgl renderer. Each node is rendered as an image.
###

###
My naive implementation of textures atlas. It allows clients to load
multimple images into atlas and get canvas representing all of them.

@param tilesPerTexture - indicates how many images can be loaded to one
texture of the atlas. If number of loaded images exceeds this
parameter a new canvas will be created.
###
ImageAtlas = (tilesPerTexture) ->
  tilesPerRow = Math.sqrt(tilesPerTexture or 1024) << 0
  tileSize = tilesPerRow
  lastLoadedIdx = 1
  loadedImages = {}
  dirtyTimeoutId = undefined
  skipedDirty = 0
  textures = []
  trackedUrls = []
  that = undefined
  isPowerOf2 = (n) ->
    (n & (n - 1)) is 0

  createTexture = ->
    texture = new Texture(tilesPerRow * tileSize)
    textures.push texture

  getTileCoordinates = (absolutePosition) ->
    textureNumber = (absolutePosition / tilesPerTexture) << 0
    localTileNumber = (absolutePosition % tilesPerTexture)
    row = (localTileNumber / tilesPerRow) << 0
    col = (localTileNumber % tilesPerRow)
    textureNumber: textureNumber
    row: row
    col: col

  markDirtyNow = ->
    that.isDirty = true
    skipedDirty = 0
    dirtyTimeoutId = null

  markDirty = ->

    # delay this call, since it results in texture reload
    if dirtyTimeoutId
      window.clearTimeout dirtyTimeoutId
      skipedDirty += 1
      dirtyTimeoutId = null
    if skipedDirty > 10
      markDirtyNow()
    else
      dirtyTimeoutId = window.setTimeout(markDirtyNow, 400)


  drawRect= (context,x,y,w,h, color="navy", lw = 1)->
    mx = x + w / 2
    my = y + h / 2
    context.beginPath()
    context.strokeStyle = color
    context.lineWidth = lw
    context.moveTo x, my
    context.quadraticCurveTo x, y, mx, y
    context.quadraticCurveTo x + w, y, x + w, my
    context.quadraticCurveTo x + w, y + h, mx, y + h
    context.quadraticCurveTo x, y + h, x, my
    context.stroke()


  wrapText = (context, text, x, y, maxWidth, lineHeight) ->
    ###
    TODO: make it work!
    ###
    words = text.split(" ")
    line = ""
    n = 0

    while n < words.length
      testLine = line + words[n] + " "
      metrics = context.measureText(testLine)
      testWidth = metrics.width
      if testWidth > maxWidth
        context.fillText line, x, y
        line = words[n] + " "
        y += lineHeight
      else
        line = testLine
      n++
    context.fillText line, x, y

  drawText= (context,text, x,y,w,h, color="navy", px = 14)->
    #context.textAlign = "center"
    context.fillStyle = color
    context.font = "bold #{px}px Calibri"
    context.fillText(text, x, y,w)
    #wrapText(context,text,x,y,w,px)


  draw =  (context, col, row,  img, text, realSize = true) ->
    x = col * tileSize
    y = row * tileSize

    ratio = img.width / img.height
    if ratio >= 1
      w = unless realSize then tileSize else Math.min(img.width,tileSize)
      h = w / ratio
    else
      h = unless realSize then tileSize else Math.min(img.height,tileSize)
      w = h * ratio

    drawRect(context,x,y,tileSize,tileSize)

    mX = 4
    mY = 4

    iX = x+mX
    iY = y+mY
    iW = w-mX*2
    iH = h+mY*2

    context.drawImage img, iX,iY,iW,iH

    drawText(context,text,iX,iY+iH+mY*2,iW,iH,"blue", 14)

  drawAt = (tileNumber, img, text, callback) ->
    tilePosition = getTileCoordinates(tileNumber)
    coordinates = offset: tileNumber
    createTexture()  if tilePosition.textureNumber >= textures.length
    currentTexture = textures[tilePosition.textureNumber]
    #currentTexture.ctx.drawImage img, tilePosition.col * tileSize, tilePosition.row * tileSize, tileSize, tileSize

    draw currentTexture.ctx, tilePosition.col, tilePosition.row, img, text


    trackedUrls[tileNumber] = img.src

    loadedImages[img.src] = coordinates
    currentTexture.isDirty = true
    callback coordinates

  copy = (from, to) ->

    fromCanvas = textures[from.textureNumber].canvas
    context = textures[to.textureNumber].ctx
    x = to.col * tileSize
    y = to.row * tileSize
    context.drawImage fromCanvas, from.col * tileSize, from.row * tileSize, tileSize, tileSize, x, y, tileSize, tileSize
    #draw currentTexture.ctx, coordinates.col, coordinates.row, img, "HelloWorld"

    textures[from.textureNumber].isDirty = true
    textures[to.textureNumber].isDirty = true




  throw "Tiles per texture should be power of two."  unless isPowerOf2(tilesPerTexture)

  # this is the return object
  that =

    ###
    indicates whether atlas has changed texture in it. If true then
    some of the textures has isDirty flag set as well.
    ###
    isDirty: false

    ###
    Clears any signs of atlas changes.
    ###
    clearDirty: ->
      i = undefined
      @isDirty = false
      i = 0
      while i < textures.length
        textures[i].isDirty = false
        ++i


    ###
    Removes given url from colleciton of tiles in the atlas.
    ###
    remove: (imgUrl) ->
      coordinates = loadedImages[imgUrl]
      return false  unless coordinates
      delete loadedImages[imgUrl]

      lastLoadedIdx -= 1
      return true  if lastLoadedIdx is coordinates.offset # Ignore if it's last image in the whole set.
      tileToRemove = getTileCoordinates(coordinates.offset)
      lastTileInSet = getTileCoordinates(lastLoadedIdx)
      copy lastTileInSet, tileToRemove
      replacedOffset = loadedImages[trackedUrls[lastLoadedIdx]]
      replacedOffset.offset = coordinates.offset
      trackedUrls[coordinates.offset] = trackedUrls[lastLoadedIdx]
      markDirty()
      true


    ###
    Gets all textures in the atlas.
    ###
    getTextures: ->
      textures # I trust you...


    ###
    Gets coordinates of the given image in the atlas. Coordinates is an object:
    {offset : int } - where offset is an absolute position of the image in the
    atlas.

    Absolute means it can be larger than tilesPerTexture parameter, and in that
    case clients should get next texture in getTextures() collection.
    ###
    getCoordinates: (imgUrl) ->
      loadedImages[imgUrl]




    ###
    Asynchronously Loads the image to the atlas. Cross-domain security
    limitation applies.
    ###
    load: (imgUrl, text, callback) ->
      if loadedImages.hasOwnProperty(imgUrl)
        callback loadedImages[imgUrl]
      else
        img = new window.Image()
        imgId = lastLoadedIdx
        lastLoadedIdx += 1
        img.crossOrigin = "anonymous"
        img.onload = ->
          markDirty()
          drawAt imgId, img, text, callback

        img.src = imgUrl

  that