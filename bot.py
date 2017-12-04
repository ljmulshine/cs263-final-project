import urllib2
import re
import time
import sys
import bot_config as config
from skimage import io
import messageDecode

# Globals
seen_images_file = open(config.seen_images, 'r+')
seen_images = map(str.rstrip, seen_images_file.readlines())

twitter_accounts_file = open(config.twitter_accounts, 'r+')
twitter_accounts_to_monitor = map(str.rstrip, twitter_accounts_file.readlines())


def mark_image_seen(image_url):
	seen_images.append(image_url)
	seen_images_file.write(image_url + '\n')


def get_recent_tweet_ids(twitter_account):
	f = urllib2.urlopen('https://twitter.com/%s' % twitter_account)
	data = f.read()
	f.close()
	tweet_id_pattern = re.compile(r'data-permalink-path="/%s/status/(\d+)"' % twitter_account)
	user_tweet_ids = tweet_id_pattern.findall(data)
	return user_tweet_ids


def get_comment_image_urls(twitter_account, tweet_id):
	f = urllib2.urlopen('https://twitter.com/%s/status/%s' % (twitter_account, tweet_id))
	data = f.read()
	f.close()
	image_url_pattern = re.compile(r'<img data-aria-label-part src="(.+?)"')
	image_urls = image_url_pattern.findall(data)
	return image_urls


def process_image(image_url):
	
	# Extract binary code from image
	imMessage = io.imread(image_url)
	try:
		[payload, numPixels] = messageDecode.bot(imMessage)
		print payload
	except:
		print "Invalid image"

	# TODO: Update twitter accounts



def main(sleep_timeout=300):

	while True:
		for twitter_account in twitter_accounts_to_monitor:
			print "Processing @" + twitter_account
			
			tweet_ids = get_recent_tweet_ids(twitter_account)
			for tweet_id in tweet_ids:
				image_urls = get_comment_image_urls(twitter_account, tweet_id)
				
				for image_url in image_urls:
					if image_url not in seen_images:
						print "Processing Image: " + image_url
						mark_image_seen(image_url)
						process_image(image_url)

		print "Sleeping"
		time.sleep(float(sleep_timeout))


if __name__ == "__main__":
    args = sys.argv
    try:
        sleep_timeout = args[1]
    except:
        sleep_timeout = 300

    main(sleep_timeout)

