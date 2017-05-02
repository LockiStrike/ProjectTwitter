import tweepy
from flask import Flask, request, render_template, redirect, session, jsonify, json, make_response
from requests_oauthlib import OAuth1Session
from db import DB
import requests
import os
from pprint import pprint

from data_file import consumer_token, consumer_secret

app = Flask(__name__)
app.secret_key = "123"


def get_image_by_url(url):
    filename = 'temp.jpg'
    request1 = requests.get(url, stream=True)
    if request1.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request1:
                image.write(chunk)
        return filename
        # api.update_with_media(filename, status=message)
        # os.remove(filename)
    else:
        print("Unable to download image")
        return None


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
        return redirect(authorization_url)
        # return render_template('index.html', url=authorization_url)
    else:
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
        auth.set_access_token(resource_owner_key, resource_owner_secret
        answer = {'token': resource_owner_key, 'sec ret': resource_owner_secret}
        return jsonify(**answer)
        # there must be redirect to our site
        # return redirect("https://0137c6d0.ngrok.io/send")


        # session['user_key'] = resource_owner_key
        # session['user_secret'] = resource_owner_secret


@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.get_json() is not None:
        content = request.get_json()
        auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
        auth.set_access_token(content['token'], content['secret'])
        api = tweepy.API(auth)
        post_id = str(api.update_status(content['text']).id)
        db = DB()
        db.insert_post_id(post_id, content['token'], content['secret'])
        return str(post_id)
    else:
        return "dumb"

    # auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    # auth.set_access_token(session['user_key'], session['user_secret'])


    # text = "another te1235st"
    # post_id = str(api.update_status(text).id)
    # db.insert_post_id(post_id, session['user_key'], session['user_secret'])

    # api.update_status(request.json['text'])
    # api.get_user()
    # post_id = api.update_status(request.json['text']).id
    # kartinka = open('/home/lockistrike/Desktop/images.jpg', 'rb')
    # kartinka = get_image_by_url('http://www.telegraph.co.uk/content/dam/Travel/galleries/travel/activityandadventure/The-worlds-most-beautiful-mountains/mountains-Alpamayo_3374089a-large.jpg')
    # api.update_with_media(kartinka)

    # if api.get_status(db.fetch_post_ids(session['user_key'], session['user_secret'])):
    #     return type(api.get_status(db.fetch_post_ids(session['user_key'], session['user_secret'])))
    # else:
    #     return "1"
    # return str(post_id)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    db = DB()
    content = request.get_json()
    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(content['token'], content['secret'])
    api = tweepy.API(auth)
    if api.destroy_status(content['post_id']):
        db.delete_post_id(content['post_id'])
        return "done"
    else:
        return "something went wrong"


    # db = DB()
    # ids = db.fetch_post_ids(session['user_key'], session['user_secret'])
    # body = {'id': str(ids[-1][0]), 'token': session['user_key'], 'secret': session['user_secret']}
    # headers = {'Content-Type': 'application/json'}
    # requests.post(url='https://0137c6d0.ngrok.io/delete123', data={"text": '123'})
    # requests.get(url='https://0137c6d0.ngrok.io/delete123', params="123")
    # auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    # auth.set_access_token(session['user_key'], session['user_secret'])
    # api = tweepy.API(auth)
    # api.destroy_status(ids[-1][0])
    # return str(api.get_status(ids[-1][0]))


@app.route('/delete123', methods=['GET', 'POST'])
def test():
    # token = request.json['token']
    # secret = request.json['secret']
    # post_id = request.json['id']
    # auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    # auth.set_access_token(token, secret)
    # api = tweepy.API(auth)
    # api.destroy_status(post_id)
    content = request.get_json()
    db = DB()
    if db.delete_post_id(content['post_id']):
        return "done"
    else:
        return "post not found"
    # if request.json['text']:
    #     return "1"
    # else:
    #     return "2"

if __name__ == '__main__':
    app.run()
