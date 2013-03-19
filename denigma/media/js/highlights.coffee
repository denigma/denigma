jQuery ->

  window.jQuery.fn.regHighlight = (term,regex, description)->
    ###
        jQuery extension to highlight something inside the element.
    ###
    id = toId(term)
    parts = @contents().filter(-> @nodeType is 3 and regex.test(@nodeValue))
    parts.replaceWith ->
      (@nodeValue or "").replace regex, (match) ->
        "<code class=\"#{id}\">#{match}</code>"
    $terms = @find(".#{id}")
    $terms.mouseover (event) ->
      $pop = popByTerm(term)
      $pop.position()
      $pop.css("left", $(@).position().left + 20)
      $pop.css("top", $(@).position().top + $(@).height())
      $pop.show()
    $terms.mouseout (event)-> popByTerm(term).hide()

  makeGlossary = (dic) ->
    ###
        Transfors ordniary JavaScript object with key-value-pairs
        to more appropriate format with description.
    ###
    res = {}
    for key,val of dic
      res[key] =
        term: key
        description: val
        regex: new RegExp(key, "gi")
    res

  toId = (term)->"pop_"+term.replace(" ", "_")

  popByTerm = (term)-> $("#pop_"+toId(term))

  createPopus = (gloss) ->
    doc = $("body")
    for key, val of gloss
      pid = "pop_"+toId(val.term)
      doc.append "<div class='popup' id=\"#{pid}\"><b>#{val.term}:</b> #{val.description}</div>"
      $("#"+pid).hide()

  window.jQuery.fn.annotate = (dic)->
    ###
        Dictionary consists of terms and annotations.
    ###
    gloss = makeGlossary(dic)
    createPopus(gloss)
    @each (index, element) ->
      $el = $(element)
      for key, val of gloss
        $el.regHighlight(val.term, val.regex, val.description)

  window.jQuery.fn.annotateTerm = (str, description) ->
    ###
        Annotating extension, use it for every tag you want
    ###
    regex = new RegExp(str, "gi")
    @each (index, element)->
      $(element).regHighlight(str, regex, description)