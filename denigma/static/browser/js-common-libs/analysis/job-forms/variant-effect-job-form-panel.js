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

VariantEffectJobFormPanel.prototype = new GenericFormPanel("hpg-variant.effect");

function VariantEffectJobFormPanel(){
	this.id = Math.round(Math.random() * 10000000);
	
	this.tags = ["vcf|bed|gff"];
	this.paramsWS = {};//test
};

VariantEffectJobFormPanel.prototype.getPanels = function (){
	var items = [
	             	this._getSpeciesForm(),
	             	this._getBrowseForm(),
	             	this._getFilterForm(),
	             	this._getOutputForm()
	             ];

	var form1234 = Ext.create('Ext.panel.Panel', {
		margin:"15 0 0 0",
		border:false,
//		layout:{type:'vbox', align: 'stretch'},
		buttonAlign:'center',
		width:"100%",
		//height:900,
		//width: "600",
		items:items
	});
	
	return [this._getExampleForm(),form1234];
};
VariantEffectJobFormPanel.prototype._getSpeciesForm = function (){
	var _this=this;
	
	var checkFlags = function(value){
		var outputOptions = Ext.getCmp('outputOptions'+_this.id);
		if(value!="hsa"){
			outputOptions.getChildByElement("TF_binding_site_variant").setValue(false).disable();
			outputOptions.getChildByElement("miRNA_target_site").setValue(false).disable();
			outputOptions.getChildByElement("other_regulatory").setValue(false).disable();
			
			outputOptions.getChildByElement("SNP").setValue(false).disable();
			outputOptions.getChildByElement("uniprot_natural_variants").setValue(false).disable();
			
			outputOptions.getChildByElement("phenotypic_annotated_SNPs").setValue(false).disable();
			outputOptions.getChildByElement("disease_mutations").setValue(false).disable();
		}else{
			outputOptions.getChildByElement("TF_binding_site_variant").setValue(false).enable();
			outputOptions.getChildByElement("miRNA_target_site").setValue(false).enable();
			outputOptions.getChildByElement("other_regulatory").setValue(false).enable();
			
			outputOptions.getChildByElement("SNP").setValue(false).enable();
			outputOptions.getChildByElement("uniprot_natural_variants").setValue(false).enable();
			
			outputOptions.getChildByElement("phenotypic_annotated_SNPs").setValue(false).enable();
			outputOptions.getChildByElement("disease_mutations").setValue(false).enable();
		}
	};

	var speciesForm = Ext.create('Ext.panel.Panel', {
		title:"Species",
		border:true,
		padding:"5 0 0 0",
		bodyPadding:10,
		items: []
	});
	
	$.ajax({url:new CellBaseManager().host+"/latest/species?of=json",success:function(data, textStatus, jqXHR){
		// Create the combo box, attached to the states data store
		var objdata = JSON.parse(data);
		for ( var i = 0; i < objdata.length; i++) {
			objdata[i].sciAsembly = objdata[i].scientific+" ("+objdata[i].assembly+")";
		}
		var species = Ext.create('Ext.data.Store', {
			autoLoad: true,
		    fields: ['species', 'common','scientific','assembly','sciAsembly'],
		    data : objdata
		});
		var speciesCombo = Ext.create('Ext.form.field.ComboBox', {
			id:_this.id+"speciesCombo",
		    fieldLabel: 'Choose Species',
		    displayField: 'sciAsembly',
		    valueField: 'species',
		    editable:false,
		    width:350,
		    store: species,
			listeners:{
				 change:function(){
					 if(this.getValue()){
						 checkFlags(this.getValue());
						 _this.paramsWS["species"]=this.getValue();
			  		}
				 }
			 }
		});
		speciesCombo.select(speciesCombo.getStore().data.items[0]);
		speciesForm.add(speciesCombo);
	},error:function(jqXHR, textStatus, errorThrown){console.log(textStatus);}});
	
  	return speciesForm;
};


VariantEffectJobFormPanel.prototype._getExampleForm = function (){
	var _this = this;
	
	var example1 = Ext.create('Ext.Component', {
		width:275,
		html:'<span class="u"><span class="emph u">Load example 1.</span> <span class="info s110">VCF file with ~3500 variants</span></span>',
		cls:'dedo',
		listeners:{
			afterrender:function(){
				this.getEl().on("click",function(){_this.loadExample1();Ext.example.msg("Example loaded","");});
				
			}
		}
	});
	var example2 = Ext.create('Ext.Component', {
		width:275,
		html:'<span class="u"><span class="emph u">Load example 2.</span> <span class="info s110">VCF file with ~5000 variants</span></span>',
		cls:'dedo',
		listeners:{
			afterrender:function(){
				this.getEl().on("click",function(){_this.loadExample2();Ext.example.msg("Example loaded","");});
				
			}
		}
	});
	
	var exampleForm = Ext.create('Ext.container.Container', {
		bodyPadding:10,
		items: [this.note1,example1,example2],
		defaults:{margin:'5 0 0 5'}
	});
	
	return exampleForm;
};


VariantEffectJobFormPanel.prototype._getBrowseForm = function (){
	var _this = this;
	
	var note1 = Ext.create('Ext.container.Container', {
		html:'<p>Please select a file from your <span class="info">server account</span> using the <span class="emph">Browse data</span> button.</p>'
	});
	this.fileBrowserLabel = Ext.create('Ext.toolbar.TextItem', {
		margin:"2 0 0 5",
		html:'<p class="emph">No file selected.</p>'
	});
	var btnBrowse = Ext.create('Ext.button.Button', {
        text: 'Browse data',
        handler: function (){
	   		_this.browserData.draw($.cookie('bioinfo_sid'),_this.tags);
   		}
	});
	var browse = Ext.create('Ext.container.Container', {
		margin:"5 0 0 0",
		layout: 'hbox',
		items:[btnBrowse,this.fileBrowserLabel]
	});

	
	var note2 = Ext.create('Ext.container.Container', {
		margin:"20 0 0 0",
		html:'<p>Remember that files must be uploaded before using them. To upload a file, please use the <span class="emph">Upload data</span> button.</p>'
	});	
	var btnUpload = Ext.create('Ext.button.Button', {
		margin:"5 0 0 0",
		text: 'Upload data',
		iconCls:'icon-upload',
		handler: function (){
			_this.uploadWidget.draw();
		}
	});
	
	var formBrowser = Ext.create('Ext.panel.Panel', {
			title:"Select your data",
			//cls:'panel-border-top',
			border:true,
			padding:"5 0 0 0",
			bodyPadding:10,
			items: [note1,browse,note2,btnUpload]
		});
	return formBrowser;
};


VariantEffectJobFormPanel.prototype._getFilterForm = function (){
	var _this=this;
	var items = [];
	var coverage = Ext.create('Ext.form.field.Number', {
		id:this.id+"coverage",
		fieldLabel: 'Coverage (min)',
		width:500,
		minValue:0,
		allowDecimals:false
	});
	items.push(coverage);
	var quality = Ext.create('Ext.form.field.Number', {
		id:this.id+"quality",
		fieldLabel: 'VCF Quality (min)',
		width:500,
		minValue:0,
		allowDecimals:false
	});
	items.push(quality);
	var alleles = Ext.create('Ext.form.field.Number', {
		id:this.id+"alleles",
		fieldLabel: 'Alleles',
		width:500,
		minValue:1,
		allowDecimals:false
	});
	items.push(alleles);
	var minAlleles = Ext.create('Ext.form.field.Number', {
		id:this.id+"minAlleles",
		fieldLabel: 'Min Alleles Freq (max)',
		width:500,
		minValue:0,
		maxValue:1,
		step:0.01,
		decimalPrecision:12,
		allowDecimals:true
	});
	items.push(minAlleles);
	
	var radioItems = [];
	radioItems.push(this.createRadio("All","snp",true));
	radioItems.push(this.createRadio("Only SNPs","snp"));
	radioItems.push(this.createRadio("Only Non-SNPs","snp"));
	var radioGroup = Ext.create('Ext.form.RadioGroup', {
		fieldLabel: 'SNP',
		width:500,
		items: radioItems
	});
	items.push(radioGroup);
	

	var formFilterOptions = Ext.create('Ext.form.Panel', {
		title:"Input data filter options",
		border:true,
		padding:"5 0 0 0",
		//cls:'panel-border-top',
		bodyPadding:10,
		items: items
	});
	
	//regions
	_this.regionFields = [];
	var region = Ext.create('Ext.form.field.Text', {
		id:this.id+"region",
		fieldLabel: 'Region',
		width:500,
		emptyText:"chr:start-end",
		regex : /^([a-zA-Z0-9])+\:([0-9])+\-([0-9])+$/
	});
	formFilterOptions.insert(4,region);
	_this.regionFields.push(region);
	
	var button = Ext.create('Ext.button.Button', {
		text:"Add more regions",
		margin:"0 0 15 105",
		handler: function(){
			var reg = Ext.create('Ext.form.field.Text', {
				fieldLabel: 'Region',
				width:500,
				emptyText:"chr:start-end",
				regex : /^([a-zA-Z0-9])+\:([0-9])+\-([0-9])+$/
			});
			formFilterOptions.insert(4,reg);
			_this.regionFields.push(reg);
		}
	});
	formFilterOptions.insert(5,button);
	
	return formFilterOptions;
};

VariantEffectJobFormPanel.prototype._getOutputForm = function (){

	var outputOptions = Ext.create('Ext.form.CheckboxGroup', {
		id: 'outputOptions'+this.id,
		columns: 1,
		vertical: true,
		defaults: {margin: '0 0 0 0'},
		items: [
				{ xtype:"label", html:'<span class="emph">Consequence types</span>'},
		        { boxLabel: 'Non-synonymous coding', name: 'outputOptions', inputValue: 'non_synonymous_codon', checked:true },
		        { boxLabel: 'Synonymous coding', name: 'outputOptions', inputValue: 'synonymous_codon' },
		        { boxLabel: 'Splice sites', name: 'outputOptions', inputValue: 'splice_donor_variant,splice_acceptor_variant,splice_region_variant', checked:true },
		        { boxLabel: 'Stop gained/lost', name: 'outputOptions', inputValue: 'stop_gained,stop_lost' },
		        { boxLabel: 'Upstream', name: 'outputOptions', inputValue: '5KB_upstream_variant', checked:true },
		        { boxLabel: 'Downstream', name: 'outputOptions', inputValue: '5KB_downstream_variant', checked:true },
		        { boxLabel: "5' UTR", name: 'outputOptions', inputValue: '5_prime_UTR_variant', checked:true },
		        { boxLabel: "3' UTR", name: 'outputOptions', inputValue: '3_prime_UTR_variant', checked:true },
		        { boxLabel: 'Non-coding RNA', name: 'outputOptions', inputValue: 'pseudogene,nc_transcript_variant,miRNA,lincRNA', checked:true },
		        { boxLabel: 'Intergenic', name: 'outputOptions', inputValue: 'intergenic_variant' },

		        { xtype:"label", html:'<br><span class="emph">Regulatory</span>'},
		        { boxLabel: 'Jaspar TFBS regions', name: 'outputOptions', inputValue: 'TF_binding_site_variant', id: 'TF_binding_site_variant' },
		        { boxLabel: 'miRNA targets', name: 'outputOptions', inputValue: 'miRNA_target_site', id: 'miRNA_target_site' },
		        { boxLabel: 'Other regulatory regions (CTCF, DNaseI, ...)', name: 'outputOptions', inputValue: 'regulatory_region_variant,DNAseI_hypersensitive_site,RNA_polymerase_promoter', id: 'other_regulatory' },


				{ xtype:"label", html:'<br><span class="emph">Variations</span>'},
		        { boxLabel: 'SNPs', name: 'outputOptions', inputValue: 'SNP', id: 'SNP' },
		        { boxLabel: 'Uniprot Natural Variants', name: 'outputOptions', inputValue: '', id: 'uniprot_natural_variants' },//not yet

		        
				{ xtype:"label", html:'<br><span class="emph">Phenotype and diseases</span>'},
		        { boxLabel: 'Phenotypic annotated SNPs', name: 'outputOptions', inputValue: '', id: 'phenotypic_annotated_SNPs' },//not yet --- "no-phenotype"
		        { boxLabel: 'Disease mutations', name: 'outputOptions', inputValue: '', id: 'disease_mutations' }//not yet --- "no-phenotype"
		       ]
	});

	var pan = Ext.create('Ext.form.Panel', {
		title:"Output options",
		border:true,
		padding:"5 0 0 0",
//		cls:'panel-border-left',
		flex:1,
		bodyPadding:10,
		//cls:'panel-border-top',
		items: outputOptions
	});
	return pan;
};


VariantEffectJobFormPanel.prototype.loadExample1 = function (){
	Ext.getCmp("jobNameField_"+this.id).setValue("Example vcf 3500");
	this.paramsWS["vcf-file-fileid"] = "example1";
	
	
	
	Ext.getCmp("Only SNPs_"+this.id).setValue(true);
	this.fileBrowserLabel.setText('<span class="emph">CHB_exon.vcf</span> <span class="info">(server)</span>',false);
	
	Ext.getCmp("Non-synonymous coding_"+this.id).setValue(true);
	Ext.getCmp("Synonymous coding_"+this.id).setValue(true);
	Ext.getCmp("Splice sites_"+this.id).setValue(true);
	Ext.getCmp("Stop gained/lost_"+this.id).setValue(true);
	Ext.getCmp("Upstream_"+this.id).setValue(true);
	Ext.getCmp("Downstream_"+this.id).setValue(true);
	Ext.getCmp("5' UTR_"+this.id).setValue(true);
	Ext.getCmp("3' UTR_"+this.id).setValue(false);
	Ext.getCmp("Non-coding RNA_"+this.id).setValue(true);
	Ext.getCmp("Intergenic_"+this.id).setValue(false);
	
	Ext.getCmp("Jaspar TFBS regions_"+this.id).setValue(true);
	Ext.getCmp("miRNA targets_"+this.id).setValue(true);
	Ext.getCmp("Other regulatory regions (CTCF, DNaseI, ...)_"+this.id).setValue(false);
	
	Ext.getCmp("SNPs_"+this.id).setValue(true);
	Ext.getCmp("Uniprot Natural Variants_"+this.id).setValue(false);
	
	Ext.getCmp("Phenotypic annotated SNPs_"+this.id).setValue(false);
	Ext.getCmp("Disease mutations_"+this.id).setValue(false);
	Ext.getCmp(this.id+"speciesCombo").select(Ext.getCmp(this.id+"speciesCombo").findRecordByValue("hsa"));
	console.log(this.paramsWS);
	this.validateRunButton();

};
VariantEffectJobFormPanel.prototype.loadExample2 = function (){
	Ext.getCmp("jobNameField_"+this.id).setValue("Example vcf 5000");
	this.paramsWS["vcf-file-fileid"] = "example2";
	
	
	
	Ext.getCmp("Only SNPs_"+this.id).setValue(true);
	this.fileBrowserLabel.setText('<span class="emph">1000genomes_5000_variants.vcf</span> <span class="info">(server)</span>',false);
	
	Ext.getCmp("Non-synonymous coding_"+this.id).setValue(true);
	Ext.getCmp("Synonymous coding_"+this.id).setValue(true);
	Ext.getCmp("Splice sites_"+this.id).setValue(true);
	Ext.getCmp("Stop gained/lost_"+this.id).setValue(true);
	Ext.getCmp("Upstream_"+this.id).setValue(true);
	Ext.getCmp("Downstream_"+this.id).setValue(true);
	Ext.getCmp("5' UTR_"+this.id).setValue(true);
	Ext.getCmp("3' UTR_"+this.id).setValue(true);
	Ext.getCmp("Non-coding RNA_"+this.id).setValue(true);
	Ext.getCmp("Intergenic_"+this.id).setValue(false);
	
	Ext.getCmp("Jaspar TFBS regions_"+this.id).setValue(true);
	Ext.getCmp("miRNA targets_"+this.id).setValue(true);
	Ext.getCmp("Other regulatory regions (CTCF, DNaseI, ...)_"+this.id).setValue(false);
	
	Ext.getCmp("SNPs_"+this.id).setValue(true);
	Ext.getCmp("Uniprot Natural Variants_"+this.id).setValue(false);
	
	Ext.getCmp("Phenotypic annotated SNPs_"+this.id).setValue(false);
	Ext.getCmp("Disease mutations_"+this.id).setValue(false);
	Ext.getCmp(this.id+"speciesCombo").select(Ext.getCmp(this.id+"speciesCombo").findRecordByValue("hsa"));
	console.log(this.paramsWS);
	this.validateRunButton();

};


VariantEffectJobFormPanel.prototype.validateRunButton = function (){
	if(this.paramsWS["vcf-file-fileid"] != null && Ext.getCmp("jobNameField_"+this.id).getValue()!=""){
		this.runButton.enable();
	}else{
		this.runButton.disable();
	}
//	this.runButton.enable();
};
VariantEffectJobFormPanel.prototype.getCheckValue = function (checkbox){
	if(checkbox.getValue())
		return null;
	return "";
};



VariantEffectJobFormPanel.prototype.beforeRun = function (){

		

		
		//validate regions
		var regions = "";
		var regionPatt = /^([a-zA-Z0-9])+\:([0-9])+\-([0-9])+$/;
		for ( var i = 0; i < this.regionFields.length; i++) {
			var value = this.regionFields[i].getValue();
			if (value!="" && regionPatt.test(value)){
				regions +=value+",";
			}
		}
		if(regions != ""){
			this.paramsWS["region"] = regions;
		}
		
		if(Ext.getCmp(this.id+"coverage").getValue()!=null){
			this.paramsWS["coverage"] = Ext.getCmp(this.id+"coverage").getValue();
		}
		if(Ext.getCmp(this.id+"quality").getValue()!=null){
			this.paramsWS["quality"] = Ext.getCmp(this.id+"coverage").getValue();
		}
		if(Ext.getCmp(this.id+"alleles").getValue()!=null){
			this.paramsWS["alleles"] = Ext.getCmp(this.id+"coverage").getValue();
		}
		if(Ext.getCmp(this.id+"minAlleles").getValue()!=null){
			this.paramsWS["maf"] = Ext.getCmp(this.id+"minAlleles").getValue();
		}
		
		if(Ext.getCmp("Only SNPs_"+this.id).getValue()){
			this.paramsWS["snp"] = "include";
		}
		if(Ext.getCmp("Only Non-SNPs_"+this.id).getValue()){
			this.paramsWS["snp"] = "exclude";
		}


		

		/*Input data filter options*/
		
		/*END Input data filter options*/
		

		/*Output options*/
		var soTerms = [];
		Ext.getCmp('outputOptions'+this.id).items.each(function(item) {
			if(!item.isDisabled() && item.inputValue != null && item.inputValue != "" && !item.getValue()){
				soTerms.push(item.inputValue);
			}
		});
		if(soTerms.length > 0){
			this.paramsWS["exclude"] = soTerms.toString();
		}
		/*END Output options*/
		
		
		console.log(this.paramsWS);
		//this.adapter.variantAnalysis(this.paramsWS);
		//this.panel.close();
};



//helping functions
VariantEffectJobFormPanel.prototype.createCheckBox = function (name, checked, margin){
	if(checked == null)
		cheched = false;
	if(margin == null)
		margin = 0;
	var cb = Ext.create('Ext.form.field.Checkbox', {
		 id:name+"_"+this.id,
		 boxLabel : name,
		 name : name,
		 checked : checked,
		 margin: '0 0 0 '+margin
	});
	return cb;
};
VariantEffectJobFormPanel.prototype.createLabel = function (text, margin){
	if(margin == null){
		margin = "15 0 0 0";
	}
	var label = Ext.create('Ext.form.Label', {
		id:text+"_"+this.id,
		margin:margin,
		html:'<span class="emph">'+text+'</span>'
	});
	
	return label;
};
VariantEffectJobFormPanel.prototype.createTextFields = function (name){
	var tb = Ext.create('Ext.form.field.Text', {
		id:name+"_"+this.id,
		fieldLabel : name,
		name : name
//		allowBlank: false
	});
	return tb;
};
VariantEffectJobFormPanel.prototype.createTextAreas = function (name, emptyText){
	var tb = Ext.create('Ext.form.field.TextArea', {
		id:name+"_"+this.id,
		fieldLabel : name,
		name : name,
		width:500,
		emptyText:emptyText
//		allowBlank: false
	});
	return tb;
};
VariantEffectJobFormPanel.prototype.createTextField = function (name, emptyText){
	var tb = Ext.create('Ext.form.field.Text', {
		id:name+"_"+this.id,
		fieldLabel : name,
		name : name,
		width:500,
		emptyText:emptyText
//		allowBlank: false
	});
	return tb;
};
VariantEffectJobFormPanel.prototype.createRadio = function (name, group, checked, hidden){
	var cb = Ext.create('Ext.form.field.Radio', {
		 id:name+"_"+this.id,
		 boxLabel : name,
		 inputValue : name,
		 checked:checked,
		 name : group,
		 hidden: hidden
	});
	return cb;
};
