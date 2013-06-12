
#= extern Batman.View

class Batman.BetterView extends Batman.View
  ###
    this view is an alternative to Batman's default's one prodiving an ability to
  ###

  node: false
  options: null

  @register: (key,param)->
    ###
      as default option of Batman seems to be buggy I had to write my own function for that
      it stores key to be used for view creation
      on rendered values of all from data-view-{key} will be saved inside the view
    ###
    @::options?=new Batman.SimpleHash
    @::options.set key, param

  render: ->
    super
    @node = @get("node")
    fun = (key,param) =>
      path = "data-view-#{key}".toLowerCase()
      if @node.hasAttribute(path)
        attr = @node.getAttribute path
        @set(key,attr)
      else
        if param=="mandatory" then Batman.developer.error("there is no mandatory option #{key} for the view")
    @options.forEach(fun) if @options?

  keyCode:
    BACKSPACE: 8,
    COMMA: 188,
    DELETE: 46,
    DOWN: 40,
    END: 35,
    ENTER: 13,
    ESCAPE: 27,
    HOME: 36,
    LEFT: 37,
    NUMPAD_ADD: 107,
    NUMPAD_DECIMAL: 110,
    NUMPAD_DIVIDE: 111,
    NUMPAD_ENTER: 108,
    NUMPAD_MULTIPLY: 106,
    NUMPAD_SUBTRACT: 109,
    PAGE_DOWN: 34,
    PAGE_UP: 33,
    PERIOD: 190,
    RIGHT: 39,
    SPACE: 32,
    TAB: 9,
    UP: 38

