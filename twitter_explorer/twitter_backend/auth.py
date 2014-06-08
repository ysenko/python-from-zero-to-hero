"""Twitter authentication related utilities."""


import logging
import tweepy


def get_authorized_api(access_token_key, access_token_secret, consumer_key, consumer_secret):
    """Return an API object initialized with the given token and secret.

    :Parameters:
        - `access_token_key`: Twitter OAuth access token key received during
          OAuth authorization.
        - `access_token_secret`: Twitter OAuth access token secret key received
          during OAuth authorization.
        - `consumer_key`: twitter app consumer key.
        - `consumer_secret`: twitter app consumer secret.

    :Return:
        Instance of tweepy.API or None in case of invalid credentials.
    """
    logging.info('Initializing Twitter API.')
    tweepy_auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    tweepy_auth.set_access_token(access_token_key, access_token_secret)
    try:
        api = tweepy.API(tweepy_auth)
        api.me()
    except tweepy.TweepError as error:
        api = None
        logging.error('An error occurred while login to Twitter', exc_info=error)

    if api is not None:
        logging.info('Twitter API is ready.')

    return api


def get_access_token(consumer_key, consumer_secret):
    """Utility which allows to get Twitter access token. Should not be used in prod."""
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    redirect_url = auth.get_authorization_url()
    print ('Please open this URL in browser and grant access. Then copy verification code and paste it here.\n%s\n'
           % (redirect_url,))
    code = raw_input('Verification code: ')
    auth.get_access_token(code)
    print
    print 'Access token key: %s' % (auth.access_token.key,)
    print 'Access token secret: %s' % (auth.access_token.secret,)
