class Denigma.IconView extends Denigma.BasicView
  ###
    this icon view that draws icons
  ###
  resources: undefined  #path to pics folder

  constructor: (poser,@resources)->
    super(poser)


  addIcons: (icons)->
    ###
      this function add all icons to the rowumn and groups them inside svg
    ###

    #pos = @poser.getTopPos
    #icon.attr("y",pos)
    icons.append("rect")
      .attr("class","billet") #TODO: move to another place
    icons.append("image")
      .attr("class","species")
      .attr("x",0)

    icons.append("image").attr("class","manipulation")
      .attr("x",0)

    icons.append("text")
      .attr("class","label")
      .text("species") #test text
      .attr("x",0)
      .attr("font-size","16pt")

  getAnimalPic: (d)=>"#{@resources}/#{d.species.icon}"

  getManipulationPic: (d)=>"#{@resources}/#{d.manipulation.icon}"

  updateIcons: (sel)->
    ###
      make all icons drawing and binding routine
    ###
    width = sel.attr("width")

    icLen = @poser.contentHeight() #length (w and h ) of the icon
    manLen = icLen / 2

    lw = width - icLen - manLen - @poser.marginX

    posM  = @poser.getMiddlePos(manLen)

    sel.select("rect.billet")
      .attr("width",width)
      .attr("height",icLen)
      .attr("rx",10)
      .attr("ry",10)


    gpa = @getAnimalPic
    sel.select("image.species").transition().duration(@poser.dur)
      .attr("xlink:href",gpa)
      .attr("x",@poser.marginX)
      .attr("width",icLen)
      .attr("height",icLen)



    gma = @getManipulationPic
    manip = sel.select("image.manipulation")
    manip.attr("xlink:href",gma)
      .attr("width",manLen)
      .attr("height",manLen)
    manip.transition().duration(@poser.dur)
      .attr("x",icLen+lw)
      .attr("y",posM)

    gsp = Denigma.Intervention.getSpeciesName

    txt = sel.select("text")
    txt
    .attr("class","label")
    .attr("width",lw)
    .attr("height",icLen)
    .attr("y",manLen)
    .attr("x",icLen+@poser.marginX)
    .text(gsp)

    #spName = Denigma.Intervention.getSpeciesName
    txt.transition().duration(@poser.dur)
      .attr("x",icLen+@poser.marginX*2)
      .attr("width",lw)
      .attr("height",icLen)

  append: (novel)->
    @addIcons(novel)


  update: (sel)->
    @updateIcons(sel)
