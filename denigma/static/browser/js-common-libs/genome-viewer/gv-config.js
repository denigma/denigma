GV_CELLBASE_HOST = "http://ws.bioinfo.cipf.es/cellbase/rest";


FEATURE_CONFIG = {
	gene:{
		filters:[{
			name:"biotype",
			text:"Biotype",
			values:["3prime_overlapping_ncrna", "ambiguous_orf", "antisense", "disrupted_domain", "IG_C_gene", "IG_D_gene", "IG_J_gene", "IG_V_gene", "lincRNA", "miRNA", "misc_RNA", "Mt_rRNA", "Mt_tRNA", "ncrna_host", "nonsense_mediated_decay", "non_coding", "non_stop_decay", "polymorphic_pseudogene", "processed_pseudogene", "processed_transcript", "protein_coding", "pseudogene", "retained_intron", "retrotransposed", "rRNA", "sense_intronic", "sense_overlapping", "snoRNA", "snRNA", "transcribed_processed_pseudogene", "transcribed_unprocessed_pseudogene", "unitary_pseudogene", "unprocessed_pseudogene"],
			selection:"multi"
		}]
		//options:[
		//]
	},
	snp:{
		filters:[{
			name:"consequence_type",
			text:"Consequence Type",
			values:["2KB_upstream_variant", "5KB_upstream_variant", "500B_downstream_variant", "5KB_downstream_variant", "3_prime_UTR_variant", "5_prime_UTR_variant", "coding_sequence_variant", "complex_change_in_transcript", "frameshift_variant", "incomplete_terminal_codon_variant", "inframe_codon_gain", "inframe_codon_loss", "initiator_codon_change", "non_synonymous_codon", "intergenic_variant", "intron_variant", "mature_miRNA_variant", "nc_transcript_variant", "splice_acceptor_variant", "splice_donor_variant", "splice_region_variant", "stop_gained", "stop_lost", "stop_retained_variant", "synonymous_codon"],
			selection:"multi"
		}]
		//options:[
		//]
	},
	bam:{
		//filters:[{
				//name:"view",
				//text:"View",
				//values:["view_as_pairs","show_soft-clipped_bases"],
				//selection:"multi"
			//}
		//],
		options:[{
				text:"View as pairs",
				name:"view_as_pairs",
				type:"checkbox",
				fetch:true,
				checked : false
			},{
				text:"Show Soft-clipping",
				name:"show_softclipping",
				type:"checkbox",
				fetch:true,
				checked : false
			},{
				text:"Insert size interval",
				name:"insert_size_interval",
				type:"doublenumberfield",
				fetch:false,
				minValue : 0,
				maxValue : 0
			}
		]
	}
	
};
FEATURE_OPTIONS = {
	gene:[{
		name:"biotype",
		text:"Biotype",
		values:["3prime_overlapping_ncrna", "ambiguous_orf", "antisense", "disrupted_domain", "IG_C_gene", "IG_D_gene", "IG_J_gene", "IG_V_gene", "lincRNA", "miRNA", "misc_RNA", "Mt_rRNA", "Mt_tRNA", "ncrna_host", "nonsense_mediated_decay", "non_coding", "non_stop_decay", "polymorphic_pseudogene", "processed_pseudogene", "processed_transcript", "protein_coding", "pseudogene", "retained_intron", "retrotransposed", "rRNA", "sense_intronic", "sense_overlapping", "snoRNA", "snRNA", "transcribed_processed_pseudogene", "transcribed_unprocessed_pseudogene", "unitary_pseudogene", "unprocessed_pseudogene"],
		selection:"multi"
	}],
	snp:[{
		name:"consequence_type",
		text:"Consequence Type",
		values:["2KB_upstream_variant", "5KB_upstream_variant", "500B_downstream_variant", "5KB_downstream_variant", "3_prime_UTR_variant", "5_prime_UTR_variant", "coding_sequence_variant", "complex_change_in_transcript", "frameshift_variant", "incomplete_terminal_codon_variant", "inframe_codon_gain", "inframe_codon_loss", "initiator_codon_change", "non_synonymous_codon", "intergenic_variant", "intron_variant", "mature_miRNA_variant", "nc_transcript_variant", "splice_acceptor_variant", "splice_donor_variant", "splice_region_variant", "stop_gained", "stop_lost", "stop_retained_variant", "synonymous_codon"],
		selection:"multi"
	}],
	bam:[{
		name:"view",
		text:"View",
		values:["view_as_pairs","show_soft-clipped_bases"],
		selection:"multi"
	}]
};

GENE_BIOTYPE_COLORS = {
		"3prime_overlapping_ncrna":"Orange",
		"ambiguous_orf":"SlateBlue",
		"antisense":"SteelBlue",
		"disrupted_domain":"YellowGreen",
		"IG_C_gene":"#FF7F50",
		"IG_D_gene":"#FF7F50",
		"IG_J_gene":"#FF7F50",
		"IG_V_gene":"#FF7F50",
		"lincRNA":"#8b668b",
		"miRNA":"#8b668b",
		"misc_RNA":"#8b668b",
		"Mt_rRNA":"#8b668b",
		"Mt_tRNA":"#8b668b",
		"ncrna_host":"Fuchsia",
		"nonsense_mediated_decay":"seagreen",
		"non_coding":"orangered",
		"non_stop_decay":"aqua",
		"polymorphic_pseudogene":"#666666",
		"processed_pseudogene":"#666666",
		"processed_transcript":"#0000ff",
		"protein_coding":"#a00000",
		"pseudogene":"#666666",
		"retained_intron":"gold",
		"retrotransposed":"lightsalmon",
		"rRNA":"indianred",
		"sense_intronic":"#20B2AA",
		"sense_overlapping":"#20B2AA",  
		"snoRNA":"#8b668b",
		"snRNA":"#8b668b",
		"transcribed_processed_pseudogene":"#666666",
		"transcribed_unprocessed_pseudogene":"#666666",
		"unitary_pseudogene":"#666666",
		"unprocessed_pseudogene":"#666666",
		"":"orangered",
		"other":"#000000"
};



SNP_BIOTYPE_COLORS = {
	"2KB_upstream_variant":"#a2b5cd",
	"5KB_upstream_variant":"#a2b5cd",
	"500B_downstream_variant":"#a2b5cd",
	"5KB_downstream_variant":"#a2b5cd",
	"3_prime_UTR_variant":"#7ac5cd",
	"5_prime_UTR_variant":"#7ac5cd",
	"coding_sequence_variant":"#458b00",
	"complex_change_in_transcript":"#00fa9a",
	"frameshift_variant":"#ff69b4",
	"incomplete_terminal_codon_variant":"#ff00ff",
	"inframe_codon_gain":"#ffd700",
	"inframe_codon_loss":"#ffd700",
	"initiator_codon_change":"#ffd700",
	"non_synonymous_codon":"#ffd700",
	"intergenic_variant":"#636363",
	"intron_variant":"#02599c",
	"mature_miRNA_variant":"#458b00",
	"nc_transcript_variant":"#32cd32",
	"splice_acceptor_variant":"#ff7f50",
	"splice_donor_variant":"#ff7f50",
	"splice_region_variant":"#ff7f50",
	"stop_gained":"#ff0000",
	"stop_lost":"#ff0000",
	"stop_retained_variant":"#76ee00",
	"synonymous_codon":"#76ee00",
	"other":"#000000"
};


SEQUENCE_COLORS = {A:"#009900", C:"#0000FF", G:"#857A00", T:"#aa0000", N:"#555555"}

SAM_FLAGS = [["read paired", 0x1],
             ["read mapped in proper pair", 0x2],
             ["read unmapped", 0x4],
             ["mate unmapped", 0x8],
             ["read reverse strand", 0x10],
             ["mate reverse strand", 0x20],
             ["first in pair", 0x40],
             ["second in pair", 0x80],
             ["not primary alignment", 0x100],
             ["read fails platform/vendor quality checks", 0x200],
             ["read is PCR or optical duplicate", 0x400]];


FEATURE_TYPES = {
	
	//methods
	formatTitle : function (str){
		var s = str.replace(/_/gi, " ");
		s = s.charAt(0).toUpperCase() + s.slice(1);
		return s;
	},
	getTipCommons : function(f){
		var strand = (f.strand != null) ? f.strand : "NA";
		return 'start-end:&nbsp;<span class="emph">'+f.start+'-'+f.end+'</span><br>'+
		'strand:&nbsp;<span class="emph">'+strand+'</span><br>'+
		'length:&nbsp;<span class="info">'+(f.end-f.start+1).toString().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,")+'</span><br>';
	},
		
	//items
	sequence:{
		color: SEQUENCE_COLORS
	},
	undefined:{
		getLabel: function(f){
			var str = "";
			str+= f.chromosome + ":" + f.start + "-" + f.end;
			return str;
		},
		getTipTitle: function(f){
			return " ";
		},
		getTipText: function(f){
			return " ";
		},
		getColor: function(f){
			return "grey";
		},
//		infoWidgetId: "stableId",
		height:10
//		histogramColor:"lightblue"
	},
	gene:{
		getLabel: function(f){
			var str = "";
			str+= (f.strand < 0) ? "<" : "";
			str+= " "+f.externalName+" ";
			str+= (f.strand > 0) ? ">" : "";
			str+= " ["+f.biotype+"]";
			return str;
		},
		getTipTitle: function(f){
			return FEATURE_TYPES.formatTitle(f.featureType) +
			' - <span class="ok">'+f.externalName+'</span>';
		},
		getTipText: function(f){
			var color = GENE_BIOTYPE_COLORS[f.biotype];
			return	'Ensembl&nbsp;ID:&nbsp;<span class="ssel">'+f.stableId+'</span><br>'+
			'biotype:&nbsp;<span class="emph" style="color:'+color+';">'+f.biotype+'</span><br>'+
			'description:&nbsp;<span class="emph">'+f.description+'</span><br>'+
			FEATURE_TYPES.getTipCommons(f)+
			'source:&nbsp;<span class="ssel">'+f.source+'</span><br>';
		},
		getColor: function(f){
			return GENE_BIOTYPE_COLORS[f.biotype];
		},
		infoWidgetId: "stableId",
		height:4,
		histogramColor:"lightblue"
	},
	geneorange:{
		getLabel: function(f){
			var str = "";
			str+= (f.strand < 0) ? "<" : "";
			str+= " "+f.externalName+" ";
			str+= (f.strand > 0) ? ">" : "";
			str+= " ["+f.biotype+"]";
			return str;
		},
		getTipTitle: function(f){
			return FEATURE_TYPES.formatTitle(f.featureType) +
			' - <span class="ok">'+f.externalName+'</span>';
		},
		getTipText: function(f){
			var color = GENE_BIOTYPE_COLORS[f.biotype];
			return	'Ensembl&nbsp;ID:&nbsp;<span class="ssel">'+f.stableId+'</span><br>'+
			'biotype:&nbsp;<span class="emph" style="color:'+color+';">'+f.biotype+'</span><br>'+
			'description:&nbsp;<span class="emph">'+f.description+'</span><br>'+
			FEATURE_TYPES.getTipCommons(f)+
			'source:&nbsp;<span class="ssel">'+f.source+'</span><br>';
		},
		getColor: function(f){
			return GENE_BIOTYPE_COLORS[f.biotype];
		},
		infoWidgetId: "stableId",
		height:4,
		histogramColor:"lightblue"
	},
	transcript:{
		getLabel: function(f){
			var str = "";
			str+= (f.strand < 0) ? "<" : "";
			str+= " "+f.externalName+" ";
			str+= (f.strand > 0) ? ">" : "";
			str+= " ["+f.biotype+"]";
			return str;
		},
		getTipTitle: function(f){
			return FEATURE_TYPES.formatTitle(f.featureType) +
			' - <span class="ok">'+f.externalName+'</span>';
		},
		getTipText: function(f){
			var color = GENE_BIOTYPE_COLORS[f.biotype];
			return	'Ensembl&nbsp;ID:&nbsp;<span class="ssel">'+f.stableId+'</span><br>'+
			'biotype:&nbsp;<span class="emph" style="color:'+color+';">'+f.biotype+'</span><br>'+
			'description:&nbsp;<span class="emph">'+f.description+'</span><br>'+
			FEATURE_TYPES.getTipCommons(f);
		},
		getColor: function(f){
			return GENE_BIOTYPE_COLORS[f.biotype];
		},
		infoWidgetId: "stableId",
		height:1,
		histogramColor:"lightblue"
	},
	exon:{//not yet
		getLabel: function(f){
			var str = "";
			str+= f.stableId;
			return str;
		},
		getTipTitle: function(f){
			return FEATURE_TYPES.formatTitle(f.exon.featureType)+' - <span class="ok">'+f.exon.stableId+'</span>';
		},
		getTipText: function(e2t,t){
			var color = GENE_BIOTYPE_COLORS[t.biotype];
			return	'transcript name:&nbsp;<span class="ssel">'+t.externalName+'</span><br>'+
			'transcript Ensembl&nbsp;ID:&nbsp;<span class="ssel">'+t.stableId+'</span><br>'+
			'transcript biotype:&nbsp;<span class="emph" style="color:'+color+';">'+t.biotype+'</span><br>'+
			'transcript description:&nbsp;<span class="emph">'+t.description+'</span><br>'+
			'transcript start-end:&nbsp;<span class="emph">'+t.start+'-'+t.end+'</span><br>'+
			'exon start-end:&nbsp;<span class="emph">'+e2t.exon.start+'-'+e2t.exon.end+'</span><br>'+
			'strand:&nbsp;<span class="emph">'+t.strand+'</span><br>'+
			'length:&nbsp;<span class="info">'+(e2t.exon.end-e2t.exon.start+1).toString().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,")+'</span><br>';
		},
		getColor: function(f){
			return "black";
		},
		infoWidgetId: "stableId",
		height:5,
		histogramColor:"lightblue"
	},
	snp:{
		getLabel: function(f){
			return f.name;
		},
		getTipTitle: function(f){
			return f.featureType.toUpperCase() +
			' - <span class="ok">'+f.name+'</span>';
		},
		getTipText: function(f){
			var color = SNP_BIOTYPE_COLORS[f.displaySoConsequence];
			return 'alleles:&nbsp;<span class="ssel">'+f.alleleString+'</span><br>'+
			'ancestral allele:&nbsp;<span class="ssel">'+f.ancestralAllele+'</span><br>'+
			'SO consequence:&nbsp;<span class="emph" style="color:'+color+';">'+f.displaySoConsequence+'</span><br>'+
			FEATURE_TYPES.getTipCommons(f)+
			'source:&nbsp;<span class="ssel">'+f.source+'</span><br>';
			
		},
		getColor: function(f){
			return SNP_BIOTYPE_COLORS[f.displaySoConsequence];
		},
		infoWidgetId: "name",
		height:8,
		histogramColor:"orange"
	},
	cpg_island:{
		getLabel: function(f){
			return f.name;
		},
		getTipTitle: function(f){
			return 'CpG island - <span class="ok">'+f.name+'</span>';
		},
		getTipText: function(f){
			return 'CpG number:&nbsp;<span class="ssel">'+f.cpgNum+'</span><br>'+
			'CpG precentage:&nbsp;<span class="ssel">'+f.perCpG+'</span><br>'+
			'CG number:&nbsp;<span class="ssel">'+f.gcNum+'</span><br>'+
			'CG percentage:&nbsp;<span class="ssel">'+f.perGc+'</span><br>'+
			'observed-expected ratio:&nbsp;<span class="ssel">'+f.observedExpectedRatio+'</span><br>'+
			FEATURE_TYPES.getTipCommons(f);
		},
		getColor: function(f){
			return "Aquamarine";
		},
		infoWidgetId: "name",
		height:8,
		histogramColor:"Aquamarine"
	},
	mutation:{
		getLabel: function(f){
			return f.mutationCds;
		},
		getTipTitle: function(f){
			return FEATURE_TYPES.formatTitle(f.featureType)+' - <span class="ok">'+f.mutationCds+'</span>';
		},
		getTipText: function(f){
			return 'mutation CDS:&nbsp;<span class="ssel">'+f.mutationCds+'</span><br>'+
			'mutation Aa:&nbsp;<span class="ssel">'+f.mutationAa+'</span><br>'+
			'mutation description:&nbsp;<span class="ssel">'+f.mutationDescription+'</span><br>'+
			'primary histology:&nbsp;<span class="ssel">'+f.primaryHistology+'</span><br>'+
			'primary site:&nbsp;<span class="ssel">'+f.primarySite+'</span><br>'+
			'site subtype:&nbsp;<span class="ssel">'+f.siteSubtype+'</span><br>'+
			'gene name:&nbsp;<span class="ssel">'+f.geneName+'</span><br>'+
			FEATURE_TYPES.getTipCommons(f)+
			'source:&nbsp;<span class="ssel">'+f.source+'</span><br>';
		},
		getColor: function(f){
			return "Chartreuse";
		},
		infoWidgetId: "mutationCds",
		height:8,
		histogramColor:"Chartreuse"
	},
	structural_variation:{
		getLabel: function(f){
			return f.displayId;
		},
		getTipTitle: function(f){
			return FEATURE_TYPES.formatTitle(f.featureType)+' - <span class="ok">'+f.displayId+'</span>';
		},
		getTipText: function(f){
			return 'display ID:&nbsp;<span class="ssel">'+f.displayId+'</span><br>'+
			'SO term:&nbsp;<span class="ssel">'+f.soTerm+'</span><br>'+
			'study description:&nbsp;<span class="emph">'+f.studyDescription+'</span><br>'+
			FEATURE_TYPES.getTipCommons(f)+
			'source:&nbsp;<span class="ssel">'+f.source+'</span><br>';
		},
		getColor: function(f){
			return "indigo";
		},
		infoWidgetId: "name",
		height:8,
		histogramColor:"indigo"
	},
	tfbs:{
		getLabel: function(f){
			return f.tfName;
		},
		getTipTitle: function(f){
			return 'TFBS - <span class="ok">'+f.tfName+'</span>';
		},
		getTipText: function(f){
			return 'TF name:&nbsp;<span class="ssel">'+f.tfName+'</span><br>'+
			'relative start:&nbsp;<span class="ssel">'+f.relativeStart+'</span><br>'+
			'relative end:&nbsp;<span class="ssel">'+f.relativeEnd+'</span><br>'+
			'target gene name:&nbsp;<span class="ssel">'+f.targetGeneName+'</span><br>'+
			'score:&nbsp;<span class="ssel">'+f.score+'</span><br>'+
			'sequence:&nbsp;<span class="ssel">'+f.sequence+'</span><br>'+
			FEATURE_TYPES.getTipCommons(f)+
			'source:&nbsp;<span class="ssel">'+f.source+'</span><br>';
		},
		getColor: function(f){
			return "blue";
		},
		infoWidgetId: "name",
		height:8,
		histogramColor:"blue"
	},
	mirna_target:{
		getLabel: function(f){
			return f.mirbaseId;
		},
		getTipTitle: function(f){
			return 'miRNA target - <span class="ok">'+f.mirbaseId+'</span>';
		},
		getTipText: function(f){
			return 'gene target name:&nbsp;<span class="ssel">'+f.geneTargetName+'</span><br>'+
			'experimental method:&nbsp;<span class="ssel">'+f.experimentalMethod+'</span><br>'+
			'score:&nbsp;<span class="ssel">'+f.score+'</span><br>'+
			FEATURE_TYPES.getTipCommons(f)+
			'source:&nbsp;<span class="ssel">'+f.source+'</span><br>';
		},
		getColor: function(f){
			return "#8b668b";
		},
		infoWidgetId: "name",
		height:8,
		histogramColor:"#8b668b"
	},
	conserved_region:{
		getLabel: function(f){
			return f.conservedRegionId;
		},
		getTipTitle: function(f){
			return FEATURE_TYPES.formatTitle(f.featureType)+' - <span class="ok">'+f.conservedRegionId+'</span>';
		},
		getTipText: function(f){
			return 'method:&nbsp;<span class="ssel">'+f.method+'</span><br>'+
			'data range primate:&nbsp;<span class="ssel">'+f.dataRangePrimate+'</span><br>'+
			'lower limit primate:&nbsp;<span class="ssel">'+f.lowerLimitPrimate+'</span><br>'+
			'sumData primate:&nbsp;<span class="ssel">'+f.sumDataPrimate+'</span><br>'+
			'sumSquare primate:&nbsp;<span class="ssel">'+f.sumSquarePrimate+'</span><br>'+
			FEATURE_TYPES.getTipCommons(f);
		},
		getColor: function(f){
			return "DodgerBlue";
		},
		infoWidgetId: "name",
		height:8,
		histogramColor:"DodgerBlue"
	},
	file:{
		getLabel: function(f){
			var str = "";
			str+= f.label;
			return str;
		},
		getTipTitle: function(f){
			return FEATURE_TYPES.formatTitle(f.featureType);
		},
		getTipText: function(f){
			return FEATURE_TYPES.getTipCommons(f);
		},
		getColor: function(f){
			return "black";
		},
		height:8,
		histogramColor:"orange"
	},
	vcf:{
		getLabel: function(f){
                return f.id;
				try {
						var fields = f.sampleData.split("\t");
					} catch (e) {
					//Uncaught TypeError: Cannot call method 'split' of undefined 
						console.log(e)
						debugger
						
					}
			
			if(fields.length>10 || fields.length==9)
				return f.id+" "+f.ref+"/"+f.alt+"";
			else{
				var gt = fields[9].split(":")[0];
				if(gt.indexOf(".")!= -1 || gt.indexOf("-")!= -1)
					return gt;
				var label = "";
				var alt = f.alt.split(",");
				if(gt.charAt(0)=='0')
					label = f.ref;
				else{
					var pos = gt.charAt(0)-1
					label = alt[pos] 
				}				
				label+=gt.charAt(1)
				if(gt.charAt(2)=='0')
					label += f.ref;
				else{
					var pos = gt.charAt(2)-1
					label += alt[pos] 
				}
		
				return label;
			}
		},
		getTipTitle: function(f){
			return 'VCF variant - <span class="ok">'+f.id+'</span>';
		},
		getTipText: function(f){
			return 'alleles (ref/alt):&nbsp;<span class="emph">'+f.reference+"/"+f.alternate+'</span><br>'+
			'quality:&nbsp;<span class="emph">'+f.quality+'</span><br>'+
			'filter:&nbsp;<span class="emph">'+f.filter+'</span><br>'+
			FEATURE_TYPES.getTipCommons(f);
		},
		getColor: function(f){
			return "black";
		},
		infoWidgetId: "id",
		height:8,
		histogramColor:"gray"
	},
	gff2:{
		getLabel: function(f){
			var str = "";
			str+= f.label;
			return str;
		},
		getTipTitle: function(f){
			return f.featureType.toUpperCase() +
			' - <span class="ok">'+f.label+'</span>';
		},
		getTipText: function(f){
			return 'score:&nbsp;<span class="emph">'+f.score+'</span><br>'+
			'frame:&nbsp;<span class="emph">'+f.frame+'</span><br>'+
			FEATURE_TYPES.getTipCommons(f);
		},
		getColor: function(f){
			return "black";
		},
		height:8,
		histogramColor:"gray"
	},
	gff3:{
		getLabel: function(f){
			var str = "";
			str+= f.label;
			return str;
		},
		getTipTitle: function(f){
			return f.featureType.toUpperCase() +
			' - <span class="ok">'+f.label+'</span>';
		},
		getTipText: function(f){
			return 'score:&nbsp;<span class="emph">'+f.score+'</span><br>'+
			'frame:&nbsp;<span class="emph">'+f.frame+'</span><br>'+
			FEATURE_TYPES.getTipCommons(f);
		},
		getColor: function(f){
			return "black";
		},
		height:8,
		histogramColor:"gray"
	},
	gtf:{
		getLabel: function(f){
			var str = "";
			str+= f.label;
			return str;
		},
		getTipTitle: function(f){
			return f.featureType.toUpperCase() +
			' - <span class="ok">'+f.label+'</span>';
		},
		getTipText: function(f){
			return 'score:&nbsp;<span class="emph">'+f.score+'</span><br>'+
			'frame:&nbsp;<span class="emph">'+f.frame+'</span><br>'+
			FEATURE_TYPES.getTipCommons(f);
		},
		getColor: function(f){
			return "black";
		},
		height:8,
		histogramColor:"gray"
	},
	bed:{
		getLabel: function(f){
			var str = "";
			str+= f.label;
			return str;
		},
		getTipTitle: function(f){
			return FEATURE_TYPES.formatTitle(f.featureType);
		},
		getTipText: function(f){
			return FEATURE_TYPES.getTipCommons(f);
		},
		getColor: function(f){
			//XXX convert RGB to Hex
	        var rgbColor = new Array();
	        rgbColor = f.itemRgb.split(",");
	        var hex = function (x) {
	        	var hexDigits = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"];
	            return isNaN(x) ? "00" : hexDigits[(x - x % 16) / 16] + hexDigits[x % 16];
	        };
	        var hexColor = hex(rgbColor[0])+ hex(rgbColor[1]) + hex(rgbColor[2]);
			return "#"+hexColor;
		},
		height:8,
		histogramColor:"orange"
	},
	bam:{
		explainFlags : function(flags) {
			var summary = '<div style="background:#FFEF93;font-weight:bold;margin:0 15px 0 0;">flags : <span class="ssel">'+flags+'</span></div>';
			for(var i = 0; i < SAM_FLAGS.length; i++) {
				if(SAM_FLAGS[i][1] & flags) {
					summary  += SAM_FLAGS[i][0] + "<br>";
				} 
			}
			return summary;
		},
		getLabel: function(f){
			return  "bam  "+f.chromosome+":"+f.start+"-"+f.end;
		},
		getTipTitle: function(f){
			return FEATURE_TYPES.formatTitle(f.featureType)+' - <span class="ok">'+f.name+'</span>';
		},
		getTipText: function(f){
			f.strand = FEATURE_TYPES.bam.getStrand(f);
			var one =  'cigar:&nbsp;<span class="ssel">'+f.cigar+'</span><br>'+
				'insert size:&nbsp;<span class="ssel">'+f.inferredInsertSize+'</span><br>'+
				FEATURE_TYPES.getTipCommons(f)+'<br>'+
				this.explainFlags(f.flags);
			
			var three = '<div style="background:#FFEF93;font-weight:bold;">attributes</div>';
			delete f.attributes["BQ"];//for now because is too long
			for (var key in f.attributes) {
				three += key+":"+f.attributes[key]+"<br>";
			}
			var style = "background:#FFEF93;font-weight:bold;";
			return '<div style="float:left">'+one+'</div>'+
					'<div style="float:right">'+three+'</div>';
		},
		getColor: function(f, chr){
			if(f.mateReferenceName != chr){return "lightgreen";}
			return (parseInt(f.flags)&(0x10)) == 0 ? "DarkGray" : "LightGray";/**/
		},
		getStrokeColor: function(f){
			if(this.getMateUnmappedFlag(f)){return "tomato"}
			return "whitesmoke";
		},
		getStrand: function(f){
			return (parseInt(f.flags)&(0x10)) == 0 ? "Forward" : "Reverse";
		},
		getReadPairedFlag: function(f){
			return (parseInt(f.flags)&(0x1)) == 0 ? false : true;
		},
		getFirstOfPairFlag: function(f){
			return (parseInt(f.flags)&(0x40)) == 0 ? false : true;
		},
		getMateUnmappedFlag: function(f){
			return (parseInt(f.flags)&(0x8)) == 0 ? false : true;
		},
		height:10,
		histogramColor:"grey"
	},
	das:{
		getLabel: function(f){
			var str = "";
			str+= f.id;
			return str;
		},
		getTipTitle: function(f){
			return FEATURE_TYPES.formatTitle(f.featureType);
		},
		getTipText: function(f){
			return FEATURE_TYPES.getTipCommons(f);
		},
		getColor: function(f){
			return "black";
		},
		height:8,
		histogramColor:"orange"
	}
};

