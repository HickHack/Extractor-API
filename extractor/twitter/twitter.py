import tweepy

from extractor.twitter.model.follower import Follower


class TwitterExtractor(object):
    consumer_key = 'rHvRleQWXoYSIXRka0GRbJaPe'
    consumer_secret = 'FZ61mtqKr8qEAkTDr2CJyTlHPqlDla7LLGNjTo4TyJkE3PmH5H'
    access_token = '3306707327-WJNm0c7mlH77OLzQQCR9eBndACvN9qYYA8oJfic'
    access_secret = 'cc8bwd5W3QFPCXIaLJnsWxiro8OG4qp53p1g8RoXtFMHU'

    def __init__(self):
        self.api = None
        self.configure_tweepy()

    def configure_tweepy(self):
        auth = tweepy.auth.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit=True)

    def extract_followers(self, twitter_handle):
        followers = []

        try:
            if self.api.verify_credentials:
                for temp_follower in tweepy.Cursor(self.api.followers, screen_name=twitter_handle).items():
                    user_id = temp_follower.id
                    handle = temp_follower.screen_name
                    name = temp_follower.name
                    is_following = temp_follower.following
                    description = temp_follower.description
                    is_default_picture = temp_follower.default_profile_image

                    follower = Follower(user_id, handle, name, description, is_following, is_default_picture)
                    followers.append(follower.__dict__)

        except tweepy.error.TweepError as e:
            print(str(e))

        return followers






