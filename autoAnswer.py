import sys,tweepy, textwrap, time, threading, msvcrt, os
from PIL import Image, ImageDraw, ImageFont

'''Añadir credenciales'''
consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

def deEmojify(text):
    return text.encode('ascii', 'ignore').decode('ascii')

def img_gen(ansSimi):
	ansSimi = textwrap.fill(ansSimi,34)
	div = ansSimi.split('http')
	ansSimi = div[0]
	if not ansSimi:
		ansSimi = 'I posted without text!'
		ansSimi = textwrap.fill(ansSimi,34)
		div = ansSimi.split('http')
		ansSimi = div[0]
	image = Image.open('Saniel.png')
	font_type = ImageFont.truetype('arial.ttf',52)
	draw = ImageDraw.Draw(image)
	draw.text((1300,200), deEmojify(ansSimi),'black',font=font_type, align = 'left')
	image.save('SaniAns.png')

def suspender():
	while True:
		sus = msvcrt.getwch()
		if(sus == 's'):
			print("Terminando...")
			sys.exit()
	


usuario = input("Indicar usuario: ")
tdSuspension = threading.Thread(target=suspender)
tdSuspension.start()

while True:
	if (not tdSuspension.is_alive()):
		sys.exit()
	page = 1
	tweet = api.user_timeline(usuario, page = page)[0]
	print(tweet.text+' '+ str(tweet.id)+'\n')

	if (os.path.exists('last.txt')):
		read = open('last.txt','r')
	else:
		open('last.txt','w').write('0')
		read = open('last.txt','r')
	id = int(read.read())
	read.close()
	if(id != tweet.id):
		write = open('last.txt','w')
		write.write(str(tweet.id))
		write.close()
		img_gen(tweet.text)
		'''Activar la próxima línea para responder directamente al tweet original'''
		'''api.update_with_media('SaniAns.png', in_reply_to_status_id = tweet.id)'''
		api.update_with_media('SaniAns.png')
	else:
		print('waiting...')
	time.sleep(5)
