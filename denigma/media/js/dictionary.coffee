jQuery ->
  p = $('p')
  dic =
    "denigma": "Will defeat aging"
    "Daniel": "Is founder of Denigma"
    "aging": "Will be defeated"
    "Crowd": "a large group of individuals capable of collective effort, in this case in the benefit of ageing research.",
    "Citizen scientists": "is a representative of the crowd working in a research project.",
    "Group intelligence": "is a capability delivered to science by the crowd through citizen scientists.",
    "Ontology": "is an explicit, formal specification of a shared conceptualization. You will find more about this term in http://denigma.de/data/entry/ontology.",
  $("p").annotate(dic,"term")
jQuery ->
  p = $('b')
  dic =
    "denigma": "Will defeat aging"
    "Daniel": "Is founder of Denigma"
    "aging": "Will be defeated"
    "Crowd": "a large group of individuals capable of collective effort, in this case in the benefit of ageing research.",
    "Citizen scientists": "is a representative of the crowd working in a research project.",
    "Group intelligence": "is a capability delivered to science by the crowd through citizen scientists.",
    "Ontology": "is an explicit, formal specification of a shared conceptualization. You will find more about this term in http://denigma.de/data/entry/ontology.",
  $("b").annotate(dic,"term")