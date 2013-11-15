class Denigma.RowPoser

  constructor: (@rowMargin,@rowHeight,@marginX,@dur)->

  getRowPos: (d,i)=>
    i* @rowHeight+i*@rowMargin

  contentHeight: => @rowHeight-@rowMargin


  #indian-like code warning: all these pos functions are inaccurate and mostly wrong
  getTopPos: (d)=> @rowHeight+@rowMargin/2
  getBottomPos: (d)=> @rowHeight+@rowMargin-@rowMargin*2

  getMiddlePos: (h=0)=>
    (d)=>  (@contentHeight()-h) / 2


  makeCentered: (fun,h)=>
    ###
      Makes position function centered
    ###
    (d,i)=>fun(d,i)-h/2

