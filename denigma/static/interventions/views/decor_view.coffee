class Denigma.DecorView extends Denigma.BasicView

  constructor: (poser,@width)->
    super(poser)

  append: (rows)->
    ###
      adds rowumn decorations
    ###
    h = @poser.contentHeight()
    border = rows.append("rect")
    border.attr("class","decor")
      .attr("width",@width)
      .attr("height",h)
      .attr("rx",10)
      .attr("ry",10)

  update: (rows)->



