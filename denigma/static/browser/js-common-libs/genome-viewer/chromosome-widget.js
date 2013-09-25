/*
 * Copyright (c) 2012 Francisco Salavert (ICM-CIPF)
 * Copyright (c) 2012 Ruben Sanchez (ICM-CIPF)
 * Copyright (c) 2012 Ignacio Medina (ICM-CIPF)
 *
 * This file is part of JS Common Libs.
 *
 * JS Common Libs is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * JS Common Libs is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with JS Common Libs. If not, see <http://www.gnu.org/licenses/>.
 */

function ChromosomeWidget(parent, args) {
	
	this.id = Math.round(Math.random()*10000000);
	if(args != null){
		if(args.width != null){
			this.width = args.width;
		}
		if(args.height != null){
			this.height = args.height;
		}
		if(args.species != null){
			this.species = args.species;
		}
		if(args.region != null){
			this.region = args.region;
		}
	}

	this.lastChromosome = "";

	this.onClick = new Event();
	
	this.svg = SVG.init(parent,{
		"width":this.width,
		"height":this.height
	});
	
	this.colors = {gneg:"white", stalk:"#666666", gvar:"#CCCCCC", gpos25:"silver", gpos33:"lightgrey", gpos50:"gray", gpos66:"dimgray", gpos75:"darkgray", gpos100:"black", gpos:"gray", acen:"blue"};
	
	this.data = null;
};

ChromosomeWidget.prototype.setWidth = function(width){
	this.width=width;
	this.svg.setAttribute("width",width);
	this.tracksViewedRegion = this.width/Utils.getPixelBaseByZoom(this.zoom);
	while (this.svg.firstChild) {
		this.svg.removeChild(this.svg.firstChild);
	}
	this._drawSvg(this.data);
};

ChromosomeWidget.prototype.drawChromosome = function(){
	var _this = this;
	
	var cellBaseManager = new CellBaseManager(this.species);
 	cellBaseManager.success.addEventListener(function(sender,data){
 		_this.data = data;
 		_this._drawSvg(data);
 	});
 	cellBaseManager.get("genomic", "region", this.region.chromosome,"cytoband");
 	this.lastChromosome = this.region.chromosome;
};

ChromosomeWidget.prototype._drawSvg = function(data){
	var _this = this;
	
	this.chromosomeLength = data.result[0][data.result[0].length-1].end;
	_this.pixelBase = (_this.width - 40) / this.chromosomeLength;
	var x = 20;
	var y = 10;
	var firstCentromere = true;

	var offset = 20;
	var centerPosition = _this.region.center();
	
	var pointerPosition = (centerPosition * _this.pixelBase) + offset;

	var group = SVG.addChild(_this.svg,"g",{"cursor":"pointer"});

	var selBox = SVG.addChild(this.svg,"rect",{
		"x":0,
		"y":2,
		"stroke-width":"2",
		"stroke":"deepskyblue",
		"opacity":"0.5",
		"fill":"honeydew"
	});

	/*Remove event listeners*/
	$(this.svg).off('contextmenu');
	$(this.svg).off('mousedown');
	$(this.svg).off('mouseup');
	$(this.svg).off('mousemove');
	$(this.svg).off('mouseleave');

	//Prevent browser context menu
	$(this.svg).contextmenu(function(e) {
		e.preventDefault();
	});
	var overPositionBox = false;
	var movingPositionBox = false;
	var selectingRegion = false;
	var downY, downX, moveX, moveY, lastX;
	$(this.svg).mousedown(function(event) {
		downX = (event.pageX - $(_this.svg).offset().left);
		selBox.setAttribute("x",downX);
		lastX = _this.positionBox.getAttribute("x");
		$(this).mousemove(function(event){
			moveX = (event.pageX - $(_this.svg).offset().left);
			if(overPositionBox==false && movingPositionBox==false){
				selectingRegion = true;
				if(moveX < downX){
					selBox.setAttribute("x",moveX);
				}
				selBox.setAttribute("width",Math.abs(moveX - downX));
				selBox.setAttribute("height",_this.height-3);
			}else if(selectingRegion == false){
				movingPositionBox=true;
				var w = _this.positionBox.getAttribute("width");
				_this.positionBox.setAttribute("x",moveX-(w/2));
			}
		});
	});
	
	$(this.svg).mouseup(function(event) {
		$(this).off('mousemove');
		if(downX != null){
			if(moveX != null){
				if(overPositionBox==false && movingPositionBox==false){
					var bioS = (downX-offset)/_this.pixelBase;
					var bioE = (moveX-offset)/_this.pixelBase;
					_this.region.start = parseInt(Math.min(bioS,bioE));
					_this.region.end =  parseInt(Math.max(bioS,bioE));

					var w = Math.abs(downX-moveX);
					_this.positionBox.setAttribute("width",w);
					_this.positionBox.setAttribute("x",Math.abs((downX+moveX)/2)-(w/2));
					_this.onClick.notify();
					selectingRegion = false;
				}else{//click to move the positionBox
					var w = _this.positionBox.getAttribute("width");
					var pixS = moveX-(w/2);
					var pixE = moveX+(w/2);
					var bioS = (pixS-offset)/_this.pixelBase;
					var bioE = (pixE-offset)/_this.pixelBase;
					_this.region.start = Math.round(bioS);
					_this.region.end =  Math.round(bioE);

					_this.positionBox.setAttribute("x",moveX-(w/2));
					_this.onClick.notify();
					movingPositionBox=false;
				}
			}else{
				var w = _this.positionBox.getAttribute("width");
				var pixS = downX-(w/2);
				var pixE = downX+(w/2);
				var bioS = (pixS-offset)/_this.pixelBase;
				var bioE = (pixE-offset)/_this.pixelBase;
				_this.region.start = Math.round(bioS);
				_this.region.end =  Math.round(bioE);

				_this.positionBox.setAttribute("x",downX-(w/2));
				_this.onClick.notify();
			}
		}
		selBox.setAttribute("width",0);
		selBox.setAttribute("height",0);
		downX = null;
		moveX = null;
		lastX = _this.positionBox.getAttribute("x");
	});
	$(this.svg).mouseleave(function(event) {
		$(this).off('mousemove')
		if(lastX!=null){
			_this.positionBox.setAttribute("x",lastX);
		}
		selBox.setAttribute("width",0);
		selBox.setAttribute("height",0);
		downX = null;
		moveX = null;
		lastX = null;
		overPositionBox = false;
		movingPositionBox = false;
		selectingRegion = false;
	});

	for (var i = 0; i < data.result[0].length; i++) {
		var width = _this.pixelBase * (data.result[0][i].end - data.result[0][i].start);
		var height = 18;
		var color = _this.colors[data.result[0][i].stain];
		if(color == null) color = "purple";
		var cytoband = data.result[0][i].cytoband;
		var middleX = x+width/2;
		var endY = y+height;

		if(data.result[0][i].stain == "acen"){
			var points = "";
			var middleY = y+height/2;
			var endX = x+width;
			if(firstCentromere){
				points = x+","+y+" "+middleX+","+y+" "+endX+","+middleY+" "+middleX+","+endY+" "+x+","+endY;
				firstCentromere = false;
			}else{
				points = x+","+middleY+" "+middleX+","+y+" "+endX+","+y+" "+endX+","+endY+" "+middleX+","+endY;
			}
			SVG.addChild(group,"polyline",{
				"points":points,
				"stroke":"black",
				"opacity":0.8,
				"fill":color
			});
		}else{
			SVG.addChild(group,"rect",{
				"x":x,
				"y":y,
				"width":width,
				"height":height,
				"stroke":"black",
				"opacity":0.8,
				"fill":color
			});
		}

		var textY = endY+2;
		var text = SVG.addChild(group,"text",{
			"x":middleX,
			"y":textY,
			"font-size":10,
			"transform": "rotate(90, "+middleX+", "+textY+")",
			"fill":"black"
		});
		text.textContent = cytoband;

		x = x + width;
	}

	var positionBoxWidth = _this.region.length()*_this.pixelBase;
	this.positionBox = SVG.addChild(group,"rect",{
		"x":pointerPosition-(positionBoxWidth/2),
		"y":2,
		"width":positionBoxWidth,
		"height":_this.height-3,
		"stroke":"orangered",
		"stroke-width":2,
		"opacity":0.5,
		"fill":"navajowhite"
	});
	$(this.positionBox).off('mouseenter');
	$(this.positionBox).off('mouseleave');
	$(this.positionBox).mouseenter(function(event) {
		if(selectingRegion==false){
			overPositionBox = true;
		}
	});
	$(this.positionBox).mouseleave(function(event) {
		overPositionBox = false;
	});
};


ChromosomeWidget.prototype.setRegion = function(item){//item.chromosome, item.region
	var needDraw = false;
	if(item.species!=null){
		this.species = item.species;
		needDraw = true;
	}
	if(this.lastChromosome != this.region.chromosome){
		needDraw = true;
	}
	
	var centerPosition = this.region.center();
	if(!isNaN(centerPosition)){
		var pointerPosition = (centerPosition*this.pixelBase)+20;
		var positionBoxWidth = parseFloat(this.positionBox.getAttribute("width"));
		this.positionBox.setAttribute("x",pointerPosition-(positionBoxWidth/2));
		var positionBoxWidth = this.region.length()*this.pixelBase;
		this.positionBox.setAttribute("width",positionBoxWidth);
	}
	if(needDraw){
//		$(this.svg).empty();
		while (this.svg.firstChild) {
			this.svg.removeChild(this.svg.firstChild);
		}
		this.drawChromosome();
	}
};

//ChromosomeWidget.prototype.setZoom = function(zoom){
	//this.zoom=zoom;
	//this.tracksViewedRegion = this.width/Compbio.getPixelBaseByZoom(this.zoom);
	//var width = this.tracksViewedRegion*this.pixelBase;
	//this.positionBox.setAttribute("width",width);
//
	//var centerPosition = Compbio.centerPosition(this.region);
	//var pointerPosition = centerPosition*this.pixelBase+20;
	//this.positionBox.setAttribute("x",pointerPosition-(width/2));
//};
