jQuery ->

  window.jQuery.fn.regHighlight = (term,regex, description)->
    ###
jQuery extension to highligh something inside the element
###
    parts = @contents().filter(-> @nodeType is 3 and regex.test(@nodeValue))
    parts.replaceWith ->
      (@nodeValue or "").replace regex, (match) ->
        "<label class=\"#{term}\">#{match}</label>"
    $terms = @find(".#{term}")
    $terms.mouseover (event)->
      $pop = popByTerm(term)
      $pop.position()
      $pop.css("left", $(@).position().left + 20)
      $pop.css("top", $(@).position().top + $(@).height())
      $pop.show()
    $terms.mouseout (event)-> popByTerm(term).hide()



  makeGlossary = (dic)->
    ###
transforms ordinary javascript object with key-value pairs
to more appropriate format with descriptiop
###
    res = {}
    for key,val of dic
      res[key] =
        id: "_"+key
        term: key
        description : val
        regex: new RegExp(key, "gi")
    res

  popByTerm = (term)-> $("#pop_"+term.replace(/s+/, "_"))

  createPopus = (gloss)->
    doc = $("body")
    for key,val of gloss
      pid = "pop_"+val.term.replace(/s+/, "_")
      doc.append "<div class='popup' id=\"#{pid}\"><b>#{val.term}:</b> #{val.description}</div>"
      $("#"+pid).hide()

  window.jQuery.fn.annotate = (dic)->
    ###
dictionary consists of terms and annotations
###
    gloss = makeGlossary(dic)
    createPopus(gloss)
    @each (index, element)->
      $el = $(element)
      for key,val of gloss
        $el.regHighlight(val.term,val.regex,val.description)

  window.jQuery.fn.annotateTerm = (str, desription) ->
    ###
Annotating extension, use it for every tag you want
###
    regex = new RegExp(str, "gi")
    @each (index, element)->
      $(element).regHighlight(str,regex, desription)