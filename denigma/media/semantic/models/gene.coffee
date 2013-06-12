###
#model for search query#
contains id and query fields
###

#= extern Batman.Model

class Denigma.Gene extends Batman.Model
  ###
  contains id and query fields
  ###

  @encode 'name'
  ###
    id and two other fields to be stored: text and user
    when you make models do not forget about id
  ###


  @persist Batman.SocketStorage
  ###
    searches are stored in socket storage
  ###

  @storageKey: 'genes'
