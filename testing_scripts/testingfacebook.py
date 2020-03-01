# coding=utf-8
import facebook

def main():

	#Values for access
	cfg = {
		"page_id"	: "",
		"access_token"	: ""
	}

	api = get_api(cfg)
	#msg = "A testar a Caixa Mágica para o #EI2016"
	#status = api.put_wall_post(msg)
	
	albumid = "406674999728661"
	
	# directly on the page
	api.put_photo(image=open("foto_.jpg","rb"),caption="caption for photo")
	# If you want to put it in an album
	#api.put_photo(image=open("MagicBox.jpg","rb"),caption="A testar MagicBox #makerfairecb",album_path=albumid + "/photos")

def get_api(cfg):
	graph = facebook.GraphAPI(cfg['access_token'])
	# Get page token to post as the page. You can skip 
	# the following if you want to post as yourself. 
	resp = graph.get_object('me/accounts')
	page_access_token = None
	for page in resp['data']:
		if page['id'] == cfg['page_id']:
			page_access_token = page['access_token']

	graph = facebook.GraphAPI(page_access_token)
	return graph


if __name__ == "__main__":
	main()

