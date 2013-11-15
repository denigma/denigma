###
  In many cases we need to search with search suggessions, t
  he intention of this class if to provide such functionality
###

#= require <channel_view.coffee>

class Denigma.SearchBoard extends Batman.ChannelView

  @edit: null

  constructor: ->
    super
    @set("titles",new Batman.Set())
    @set("results",new Batman.Set())

  @register("result")
  @register("field")
  @register("input")



  lookupHandler: (event)=>
    ###
      fires when lookup info received
    ###
    tlt = @get("titles")
    tlt.clear()
    for t in event.content.list
      tlt.add(t)
    @set("titles",tlt) #just for 'overcheck'

  searchHandler: (event)=>
    ###
      fires when search resultsreceived
    ###
    @get("titles").clear()
    res = @get("results")
    res.clear()
    for r in event.content.list
      res.add(r)

  render: ->
    super
    node = $ @get("node")
    inp = "#"+@get("input")
    @edit = $(inp)
    @bind(@edit)

  connect: ->
    ###
      works with channel
    ###
    super
    #@channel.on("lookup", lookme)
    searchme = @searchHandler
    @channel.on "search", searchme


  @accessor "active",-> @get("query").length>0
  #@set("query","test")

  lookup: (newVal,oldVal)=>
    if @channel?
      field = @get "field"
      if(field?)
        @channel.lookup(field,newVal)
      else
        console.log "no field #{field}"
        @channel.query(newVal)
    else
      alert "no suggesssion channel!"

  split: (val) => val.split(" ") #/,\s*/

  extractLast: (term) =>  @split(term).pop() if term?

  look: (request, response) =>
    ###
      sends request to the channel
    ###
    #delegate back to autocomplete, but extract the last term
    term = @extractLast(request.term)
    field = @get "field"
    onceHandler = (event)=>
      lookme(event)
      titles = @get "titles"
      response(titles.toArray())

    @channel.lookup(field,term)
    lookme = @lookupHandler #assigment to overcome dreadful this javascript problem
    @channel.once "lookup", onceHandler

  focus:
    =>false

  select: (event, ui) =>
    ###
      fires when you selected the term
    ###
    newVal = ui.item.value
    s1 = newVal.indexOf("(")
    s2 = newVal.indexOf(")")

    if s1>1 and s2>s1
      name = newVal.substring(0,s1-1)
      value = newVal.substring(s1+1,newVal.length-1)
    else
      name = newVal
      value = newVal
    @edit.val(name)
    Denigma.fire "fisheye", value,"genesgraph" #make fishyey event to traverse the graph
    true



  multiSelect: (event, ui) =>
    value = @edit.val()
    terms = @split(value)
    newVal = ui.item.value
    # remove the current input
    terms.pop()
    # add the selected item
    terms.push newVal
    # add placeholder to get the comma-and-space at the end
    terms.push " "
    @edit.val(terms.join(" "))
    false


  keyDownHandler: (event)=>
      event.preventDefault()  if event.keyCode is $.ui.keyCode.TAB and $(this).data("ui-autocomplete").menu.active



  bind: (input)=>
    minLength = 2
    source = @look
    select = @select
    focus = @focus

    # don't navigate away from the field on tab when selecting an item
    input.bind("keydown", @keyDownHandler).autocomplete
      minLength:minLength
      delay: 300
      source: source
      select: select
      focus: focus


