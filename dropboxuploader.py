# Include the Dropbox SDK libraries
from dropbox import client, rest, session
#import clipboard
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", type=str,
                    help="a name of file to upload")
parser.add_argument("-s", "--status", action="store_true",
                    help="Show account info and status")
args = parser.parse_args()


# Get your app key and secret from the Dropbox developer website
APP_KEY = ''
APP_SECRET = ''

# ACCESS_TYPE should be 'dropbox' or 'app_folder' as configured for your app
ACCESS_TYPE = 'app_folder'
sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)

try:
    ac_file = open('act.txt', 'r')
    if ac_file:
        ac_d = ac_file.read()
        ac_d = ac_d.split('*')
        acc_token, acc_token_secret = ac_d[0], ac_d[1]
        ac_file.close()
        sess.set_token(acc_token, acc_token_secret)
    else:
        print 'Ooops'
except:
    request_token = sess.obtain_request_token()

    url = sess.build_authorize_url(request_token)
    #clipboard.Paste(url)
    print "url:", url
    print "Please visit this website and press the 'Allow' button, then hit 'Enter' here."
    raw_input()

    access_token = sess.obtain_access_token(request_token)
    print access_token
    print dir(access_token)
    print 'Key:'
    print access_token.key
    print 'Secret:'
    print access_token.secret
    ac_file = open('act.txt', 'w')
    ac_file.write(str(access_token.key)+'*'+str(access_token.secret))
    ac_file.close()

client = client.DropboxClient(sess)
if args.status:
    print "Account info:".format(args.filename)

    print "linked account:", client.account_info()

filename = args.filename
if filename:
    print 'uploading file'
    print filename
    upload_file = open(filename, 'rb')
    response = client.put_file(filename, upload_file)
    print "uploaded:", response
