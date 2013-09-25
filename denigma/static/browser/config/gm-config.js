/**
 * This is a configuration file.
 * Changes to this file may cause the application does not work as it should
 *
 * Default hosts
 * CELLBASE_HOST = "http://usa.cellbase.org:8080/cellbase/rest";
 * CELLBASE_HOST = "http://ws.bioinfo.cipf.es/cellbase/rest";
 * OPENCGA_HOST = "http://ws.bioinfo.cipf.es/gcsa/rest";
 *
 * Deprecated hosts
 * WUM_HOST = "http://ws.bioinfo.cipf.es/wum/rest";
 *
 **/
CELLBASE_HOST = "http://ws.bioinfo.cipf.es/cellbase/rest";
//OPENCGA_HOST = "http://ws.bioinfo.cipf.es/opencga/rest";
OPENCGA_HOST = "http://ws-beta.bioinfo.cipf.es/opencga/rest";
OPENCGA_LOCALHOST = "http://localhost:61976/opencga/rest";

/** Devel only: custom URL check **/
if(window.location.host.indexOf("fsalavert")!=-1 ||
   window.location.host.indexOf("rsanchez")!=-1 ||
   window.location.host.indexOf("imedina")!=-1 ||
   window.location.host.indexOf("localhost")!=-1 ||
   window.location.href.indexOf("http://bioinfo.cipf.es/apps-beta")!=-1
){

    CELLBASE_HOST = "http://ws-beta.bioinfo.cipf.es/cellbase/rest";
//	CELLBASE_HOST = "http://fsalavert:8080/cellbase/rest";
	//CELLBASE_HOST = "http://rsanchez:8080/cellbase/rest";
	//CELLBASE_HOST = "http://imedina:8080/cellbase/rest";
	//CELLBASE_HOST = "http://ralonso:8080/naranjoma-ws/rest";

	OPENCGA_HOST = "http://ws-beta.bioinfo.cipf.es/opencgabeta/rest";
//  OPENCGA_HOST = "http://fsalavert:8080/opencga/rest";
//	OPENCGA_HOST = "http://rsanchez:8080/dqs/rest";
//	OPENCGA_HOST = "http://imedina:8080/dqs/rest";
}


/** List of available species in the cellbase service **/
var AVAILABLE_SPECIES = [
                        {	"name":"Homo sapiens 37.p7", "species":"hsa", "icon":"",
							"region":{"chromosome":"13","start":32889599,"end":32889739}
						},
                        {	"name":"Mus musculus m37", "species":"mmu", "icon":"",
							"region":{"chromosome":"1","start":18422009,"end":18422009}
						},
                        {	"name":"Rattus norvegicus 3.4", "species":"rno", "icon":"",
							"region":{"chromosome":"1","start":1570040,"end":1570040}
						},
                        {	"name":"Danio rerio v9", "species":"dre", "icon":"",
							"region":{"chromosome":"1","start":1570040,"end":1570040}
						},
                        {	"name":"Caenorhabditis elegans WS230", "species":"cel", "icon":"",
							"region":{"chromosome":"X","start":817895,"end":817895}
						},
                        {	"name":"Drosophila melanogaster 5.39", "species":"dme", "icon":"",
							"region":{"chromosome":"2L","start":158597,"end":158597}
						},
                        {	"name":"Saccharomyces cerevisiae 4", "species":"sce", "icon":"",
							"region":{"chromosome":"I","start":111532,"end":111532}
						},
                        {	"name":"Canis familiaris 2.0", "species":"cfa", "icon":"",
							"region":{"chromosome":"1","start":109898268,"end":109898268}
						},
                        //{	"name":"Sus scrofa 9", "species":"ssc", "icon":"",
							//"region":{"chromosome":"1","start":135353160,"end":135353160}
						//},
                        {	"name":"Sus scrofa 10.2", "species":"ssc", "icon":"",
							"region":{"chromosome":"1","start":135353160,"end":135353160}
						},
                        {	"name":"Anopheles gambiae 3", "species":"aga", "icon":"",
							"region":{"chromosome":"2L","start":12123831,"end":12123831}
                        },
                        {	"name":"Plasmodium falciparum 3D7", "species":"pfa", "icon":"",
							"region":{"chromosome":"01","start":238905,"end":238905}
						}
                        //{	"name":"Aspergillus fumigatus 68.2", "species":"afu", "icon":"",
							//"region":{"chromosome":"I","start":2905,"end":2905}
                        //},
                        //{	"name":"Fusarium oxysporum 68.2", "species":"fox", "icon":"",
                            //"region":{"chromosome":"1","start":2905,"end":2905}
						//}
                        ];

/** Reference to a species from the list to be shown at start **/
var DEFAULT_SPECIES = AVAILABLE_SPECIES[0];

var SPECIES_TRACKS_GROUP = {"hsa":"group1",
							"mmu":"group2",
							"dre":"group2",
							"rno":"group2",
							"dme":"group2",
							"sce":"group2",
							"cel":"group2",
							"ssc":"group2",
							"cfa":"group3",
							"aga":"group3",
							"pfa":"group3"
							};

var TRACKS ={"group1":[
			          {"category":"Core",
					   "tracks":[
//					          {"id":"Cytoband", "disabled":false, "checked":true},
					          {"id":"Sequence", "disabled":false, "checked":true},
					          {"id":"Gene/Transcript", "disabled":false, "checked":true},
			                  {"id":"CpG islands", "disabled":false, "checked":false}
			                  ]
					  },
					  {"category":"Variation",
					   "tracks":[
			                  {"id":"SNP", "disabled":false, "checked":true},
			                  {"id":"Mutation", "disabled":false, "checked":false},
			                  {"id":"Structural variation (<20Kb)", "disabled":false, "checked":false},
			                  {"id":"Structural variation (>20Kb)", "disabled":false, "checked":false}
			                  ]
					  },
					  {"category":"Regulatory",
					   "tracks":[
					          {"id":"TFBS", "disabled":false, "checked":false},
			                  {"id":"miRNA targets", "disabled":false, "checked":false},
//			                  {"id":"Histone", "disabled":false, "checked":false},
//			                  {"id":"Polymerase", "disabled":false, "checked":false},
//			                  {"id":"Open Chromatin", "disabled":true, "checked":false},
			                  {"id":"Conserved regions", "disabled":false, "checked":false}
			                  ]
					  }
			],
			"group2":[
			          {"category":"Core",
					   "tracks":[
//					          {"id":"Cytoband", "disabled":false, "checked":true},
					          {"id":"Sequence", "disabled":false, "checked":true},
					          {"id":"Gene/Transcript", "disabled":false, "checked":true},
			                  {"id":"CpG islands", "disabled":true, "checked":false}
			                  ]
					  },
					  {"category":"Variation",
					   "tracks":[
			                  {"id":"SNP", "disabled":false, "checked":true},
			                  {"id":"Mutation", "disabled":true, "checked":false},
			                  {"id":"Structural variation (<20Kb)", "disabled":true, "checked":false},
			                  {"id":"Structural variation (>20Kb)", "disabled":true, "checked":false}
			                  ]
					  },
					  {"category":"Regulatory",
					   "tracks":[
					          {"id":"TFBS", "disabled":true, "checked":false},
			                  {"id":"miRNA targets", "disabled":true, "checked":false},
			                  {"id":"Histone", "disabled":true, "checked":false},
			                  {"id":"Polymerase", "disabled":true, "checked":false},
			                  {"id":"Open Chromatin", "disabled":true, "checked":false},
			                  {"id":"Conserved regions", "disabled":true, "checked":false}
			                  ]
					  }
			],
			"group3":[
			          {"category":"Core",
					   "tracks":[
//					          {"id":"Cytoband", "disabled":false, "checked":true},
					          {"id":"Sequence", "disabled":false, "checked":true},
					          {"id":"Gene/Transcript", "disabled":false, "checked":true},
			                  {"id":"CpG islands", "disabled":true, "checked":false}
			                  ]
					  },
					  {"category":"Variation",
					   "tracks":[
			                  {"id":"SNP", "disabled":true, "checked":false},
			                  {"id":"Mutation", "disabled":true, "checked":false},
			                  {"id":"Structural variation (<20Kb)", "disabled":true, "checked":false},
			                  {"id":"Structural variation (>20Kb)", "disabled":true, "checked":false}
			                  ]
					  },
					  {"category":"Regulatory",
					   "tracks":[
					          {"id":"TFBS", "disabled":true, "checked":false},
			                  {"id":"miRNA targets", "disabled":true, "checked":false},
			                  {"id":"Histone", "disabled":true, "checked":false},
			                  {"id":"Polymerase", "disabled":true, "checked":false},
			                  {"id":"Open Chromatin", "disabled":true, "checked":false},
			                  {"id":"Conserved regions", "disabled":true, "checked":false}
			                  ]
					  }
			]
};

var DAS_TRACKS = [
				{"species":"hsa",
				   "categories":[
				      {"name":"Core",
					   "sources":[
                	        {"name":"GRC Region GRCh37","url":"http://das.sanger.ac.uk/das/grc_region_GRCh37/features","checked":false},
                	        {"name":"Vega genes","url":"http://das.sanger.ac.uk/das/vega_ens_zv8_genes/features","checked":false}
                	        ]
				      },
				      {"name":"Variation",
					   "sources":[
                	        {"name":"Cosmic Mutations GRCh37","url":"http://das.sanger.ac.uk/das/cosmic_mutations_GRCh37/features","checked":false}
                	        ]
				      },
				      {"name":"Regulatory",
					   "sources":[]
				      }
				   ]
				},
				{"species":"mmu",
				   "categories":[
				      {"name":"Core",
					   "sources":[]
				      },
				      {"name":"Variation",
					   "sources":[]
				      },
				      {"name":"Regulatory",
					   "sources":[
					   		{"name":"miRNAs", "url":"http://www.ebi.ac.uk/das-srv/genomicdas/das/mmuprimiRNA/", "checked":false}
					   		]
				      }
				   ]
				},
				{"species":"dre",
				   "categories":[
				      {"name":"Core",
					   "sources":[]
				      },
				      {"name":"Variation",
					   "sources":[]
				      },
				      {"name":"Regulatory",
					   "sources":[]
				      }
				   ]
				},
				{"species":"rno",
				   "categories":[
				      {"name":"Core",
					   "sources":[]
				      },
				      {"name":"Variation",
					   "sources":[]
				      },
				      {"name":"Regulatory",
					   "sources":[
					   		{"name":"miRNAs", "url":"http://www.ebi.ac.uk/das-srv/genomicdas/das/rnoprimiRNA/", "checked":false}
					   		]
				      }
				   ]
				},
				{"species":"dme",
				   "categories":[
				      {"name":"Core",
					   "sources":[]
				      },
				      {"name":"Variation",
					   "sources":[]
				      },
				      {"name":"Regulatory",
					   "sources":[]
				      }
				   ]
				},
				{"species":"sce",
				   "categories":[
				      {"name":"Core",
					   "sources":[]
				      },
				      {"name":"Variation",
					   "sources":[]
				      },
				      {"name":"Regulatory",
					   "sources":[]
				      }
				   ]
				},
				{"species":"cel",
				   "categories":[
				      {"name":"Core",
					   "sources":[]
				      },
				      {"name":"Variation",
					   "sources":[]
				      },
				      {"name":"Regulatory",
					   "sources":[]
				      }
				   ]
				}
				];
