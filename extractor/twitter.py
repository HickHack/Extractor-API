from model.follower import Follower
import tweepy


class TwitterExtractor:
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
        self.api = tweepy.API(auth)

    def extract_followers(self, twitter_handle):
        followers = [Follower]

        try:
            if self.api.verify_credentials:
                for temp_follower in tweepy.Cursor(self.api.followers, screen_name=twitter_handle).items():
                    handle = temp_follower.screen_name
                    name = temp_follower.name
                    is_following = temp_follower.following
                    description = temp_follower.description
                    is_default_picture = temp_follower.default_profile_image

                    follower = Follower(handle, name, description, is_following, is_default_picture)
                    followers.append(follower)

        except tweepy.error.TweepError:
            pass
            # TODO: Log the exception

        return followers

    def log(self):
        file = open('twitter_followers.txt', 'w+')

        for follower in self.followers_list:
            file.write('%s\t%s\t%s\t%s\t%s' % (follower.handle, follower.name, follower.description,
                                               follower.is_following, follower.is_default_picture))



