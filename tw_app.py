from flask import Flask, request, render_template, redirect, session
from data_file import consumer_token, consumer_secret, user, password
from requests_oauthlib import OAuth1Session
import tweepy
import mysql.connector

app = Flask(__name__)
app.secret_key = "123"

def db_connect():
    """Connect to MySQL database"""

    try:
        connect = mysql.connector.connect(host='localhost',
                                          database='TwDb',
                                          user=user,
                                          password=password)
        if connect.is_connected():
            print("connected to MySQL")

    except BaseException as e:
        print(e)

    finally:
        connect.close()



@app.route('/')
def hello_world():
    if request.full_path == "/?":
        oauth = OAuth1Session(consumer_token, consumer_secret)
        request_token_url = 'https://api.twitter.com/oauth/request_token'

        fetch_response = oauth.fetch_request_token(request_token_url)
        resource_owner_key = fetch_response.get('oauth_token')
        session['key'] = resource_owner_key

        resource_owner_secret = fetch_response.get('oauth_token_secret')
        session['secret'] = resource_owner_secret

        base_authorization_url = 'https://api.twitter.com/oauth/authorize'
        authorization_url = oauth.authorization_url(base_authorization_url)
        return render_template('index.html', url=authorization_url)
    else:
        # oauth = session['oauth']
        oauth = OAuth1Session(consumer_token, consumer_secret)
        resource_owner_key = session['key']
        resource_owner_secret = session['secret']
        redirect_response = request.full_path
        oauth_response = oauth.parse_authorization_response(redirect_response)
        verifier = oauth_response.get('oauth_verifier')
        access_token_url = 'https://api.twitter.com/oauth/access_token'
        oauth = OAuth1Session(consumer_token,
                              client_secret=consumer_secret,
                              resource_owner_key=resource_owner_key,
                              resource_owner_secret=resource_owner_secret,
                              verifier=verifier,
                              )
        oauth_tokens = oauth.fetch_access_token(access_token_url)
        resource_owner_key = oauth_tokens.get('oauth_token')
        resource_owner_secret = oauth_tokens.get('oauth_token_secret')
        auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
        auth.set_access_token(resource_owner_key, resource_owner_secret)
        session['user_key'] = resource_owner_key
        session['user_secret'] = resource_owner_secret
        return redirect("https://5edefb2e.ngrok.io/tweeting")


@app.route('/tweeting')
def tweeting():
    return render_template('authorized.html', answer=request.json)


@app.route('/send', methods=['POST'])
def send():
    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(session['user_key'], session['user_secret'])
    api = tweepy.API(auth)
    # api.update_status(request.json['text'])
    # api.get_user()
    return str(api.get_user())

if __name__ == '__main__':
    app.run()
