class BasicWorker extends AbstractSocketWorker
  constructor: ->
    super

  createWebsocket: (user, password, url)->
    if url!="none" then url = url.replace(/&amp;/g,"&").replace("none",user).replace("nopassword",password)
    return new WebSocket(url)