# cs263-final-project
Security Systems Final Project Repository

System Usage:

Requires the following python packages (dependencies in requirements.txt):
    scikit-image
    subprocess
    urllib2
    re
    time
    sys
    os

The "bot herder" can encode a bytecode file into an image with the following command: 

    $ python2.7 messageEncode.py [image file] [plaintext-file-to-encode] [encode density] [output encoded image file]

where "image file" refers the the image in which to encode the secret bytecode,
"plaintext-file-to-encode" refers to the plaintext python script that you would 
like the bots to run, "encode density" refers to the number of bits to encode 
in each pixel color channel, and "output encoded image file" refers the the 
output file to save the resulting image message as. Please note that "image file"
must refer to a four-channel .png. We've included example transparent .png files
in the /images/plain_transparencies directory. For example, running the following
will encode the script which adds Twitter users to a bot's config file.

    $ python2.7 messageEncode.py images/plain_transparencies/transparentImage.png scripts/add_users.py 2 add_users.png 

In order to avoid compression on Twitter, images must have an alpha channel for 
transparency. This can be added in common photo manipulation programs such as 
PhotoShop, Gimp, or through online tools.

After creating the message with encoded image, the "bot herder" must post the 
image as a reply to a tweet from one of the specified user accounts. For example, 
one could post the resulting image from the command above, "add_users.png," as a
comment to a recent post (not retweet) on Twitter account, "@pt." Then, the bot
would simply need to run, 

    $ python2.7 bot.py
 
This will check all specified user accounts for encoded images from the control 
server and execute any valid bytecode messages that it observes. In practice, the
malware would install this program as a daemon on the infected computers, and they
would constantly be monitoring Twitter in the background.
