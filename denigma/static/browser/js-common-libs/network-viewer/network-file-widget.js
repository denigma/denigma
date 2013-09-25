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

function NetworkFileWidget(args){
	this.targetId = null;
	this.id = "NetworkFileWidget-" + Math.round(Math.random()*10000000);
	
	this.title = 'Open a Network JSON file';
	this.width = 600;
	this.height = 300;
	
    if (args != null){
        if (args.title!= null){
        	this.title = args.title;       
        }
        if (args.targetId!= null){
        	this.targetId = args.targetId;       
        }
        if (args.width!= null){
        	this.width = args.width;       
        }
        if (args.height!= null){
        	this.height = args.height;       
        }
    }
    
    
	this.dataAdapter = null;
	this.onOk = new Event(this);
	
	this.previewId = this.id+'-preview';
};

NetworkFileWidget.prototype.getTitleName = function(){
	return Ext.getCmp(this.id + "_title").getValue();
};

NetworkFileWidget.prototype.getFileUpload = function(){
	var _this = this;
	this.fileUpload = Ext.create('Ext.form.field.File', {
		msgTarget: 'side',
		allowBlank: false,
		emptyText:'JSON network file',
		flex:1,
		buttonText: 'Browse local',
		listeners: {
			change: function(){
				_this.panel.setLoading(true);
				var dataadapter = new FileDataAdapter();
				var file = document.getElementById(_this.fileUpload.fileInputEl.id).files[0];
				dataadapter.read(file);
				dataadapter.onRead.addEventListener(function (sender, content){
					try{
						_this.content = content.content; //para el onOK.notify event
						var json = JSON.parse(content.content);
						
						var numNodes = json.metaInfo.numNodes;
						var numEdges = json.metaInfo.numEdges;
						
						var edges = json.edges;
						for (var id in edges) {
							var link = "--";
							if(json.edges[id].directed) link = "->";
							_this.gridStore.loadData([[json.edges[id].source, link, json.edges[id].target]], true);
						}
						
						_this.infoLabel.setText('<span class="ok">File loaded sucessfully</span>',false);
						_this.countLabel.setText('nodes:<span class="info">'+numNodes+'</span> edges:<span class="info">'+numEdges+'</span>',false);
					
					}catch(e) {
						_this.infoLabel.setText('<span class="err">File not valid </span>'+e,false);
					};
					_this.panel.setLoading(false);
				});
			}
	    }
	});
	
	return this.fileUpload;
};

//NetworkFileWidget.prototype.loadJSON = function(content){
//	this.metaNetworkViewer.loadJSON(content);
//	this.draw(this.metaNetworkViewer.getDataset(), this.metaNetworkViewer.getFormatter(), this.metaNetworkViewer.getLayout());
//};
NetworkFileWidget.prototype.draw = function(){
	var _this = this;
	
	if (this.panel == null){
		/** Bar for the file upload browser **/
		var browseBar = Ext.create('Ext.toolbar.Toolbar',{cls:'bio-border-false'});
		browseBar.add(this.getFileUpload());
		
		this.infoLabel = Ext.create('Ext.toolbar.TextItem',{html:'Please select a network saved File'});
		this.countLabel = Ext.create('Ext.toolbar.TextItem');
		var infobar = Ext.create('Ext.toolbar.Toolbar',{cls:'bio-border-false'});
		infobar.add([this.infoLabel,'->',this.countLabel]);
		
//		/** Container for Preview **/
//		var previewContainer = Ext.create('Ext.container.Container', {
//			id:this.previewId,
//			cls:'x-unselectable',
//			flex:1,
//			autoScroll:true
//		});
		
		
		/** Grid for Preview **/
		this.gridStore = Ext.create('Ext.data.Store', {
		    fields: ["0","1","2"]
		});
		this.grid = Ext.create('Ext.grid.Panel', {
			border:false,
			flex:1,
		    store: this.gridStore,
		    columns: [{"header":"Node","dataIndex":"0",flex:1},{"header":"Relation","dataIndex":"1",flex:1,menuDisabled:true},{"header":"Node","dataIndex":"2",flex:1}],
		    features: [{ftype:'grouping'}],
		    tbar:browseBar,
		    bbar:infobar
		});
		
		var comboLayout = Ext.create('Ext.form.field.ComboBox', {
			margin: "0 0 0 5",
			width: 120,
			editable: false,
			displayField: 'name',
			valueField: 'name',
			value: "none",
			store: new Ext.data.SimpleStore({
				fields: ['name'],
				data: [["none"],["dot"],["neato"],["twopi"],["circo"],["fdp"],["sfdp"],["Random"],["Circle"],["Square"]]
			})
		});
		
		this.panel = Ext.create('Ext.window.Window', {
			title : this.title,
			width: this.width,
			height:this.height,
			resizable:false,
			layout: { type: 'vbox',align: 'stretch'},
			items : [this.grid],
			buttons:[
			         {
			        	 xtype: 'text',
			        	 margin: "5 0 0 0",
			        	 text: 'Apply layout:'
			         },
			         comboLayout, '->',
			         {text:'Ok', handler: function() {
			        	 _this.onOk.notify({"content":_this.content, "layout":comboLayout.getValue()});
			        	 _this.panel.close();
			        	 }
			         }, 
			         {text:'Cancel', handler: function() { _this.panel.close(); }}
			         ],
			listeners: {
				scope: this,
				minimize:function() {
					this.panel.hide();
				},
				destroy: function() {
					delete this.panel;
				}
			}
		});
	}
	this.panel.show();
};
