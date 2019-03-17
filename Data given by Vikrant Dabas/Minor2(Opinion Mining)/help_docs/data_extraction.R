library("twitteR")
requestURL <-  "https://api.twitter.com/oauth/request_token"
accessURL =    "https://api.twitter.com/oauth/access_token"
authURL =      "https://api.twitter.com/oauth/authorize"
consumerKey =   "PqSPfWBPGNbnh7ONUDddsxZVW"
consumerSecret = "xigDFiLAOkzsrlbXempi1KDjbYlIR09TCTjjmjpkEsF702fePR"
twitCred <- OAuthFactory$new(consumerKey=consumerKey,consumerSecret=consumerSecret,requestURL=requestURL,accessURL=accessURL,authURL=authURL);
twitCred$handshake(cainfo="cacert.pem")
7931394
registerTwitterOAuth(twitCred)
me <- getUser("arvindkejrival",cainfo="cacert.pem")
wea_tweets = userTimeline("arvindkejrival",cainfo="cacert.pem")
s