jQuery ->
  p = $('p')
  dic =
    "denigma": "Will defeat aging"
    "Daniel": "Is founder of Denigma"
    "aging": "Will be defeated"
    "Crowd": "a large group of individuals capable of collective effort, in this case in the benefit of ageing research.",
    "Citizen scientist": "is a representative of the crowd working in a research project.",
    "Group intelligence": "is a capability delivered to science by the crowd through citizen scientists.",
  $("p").annotate(dic,"term")