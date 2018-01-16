import tweepy

# Twitter settings
def get_api(cfg):
	auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
	auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
	return tweepy.API(auth)

# Send to twitter
def sendToTwitter():
	cfg = {
		"consumer_key"		: "",
		"consumer_secret"	: "",
		"access_token"		: "",
		"access_token_secret"	: ""
	}

	api = get_api(cfg)
	# Status Message
	tweet = "tweeter message"
	status = api.update_with_media("jpg_foto_to_Send",tweet)


sendToTwitter()
