from model.follower import Follower
from extractor.twitter import TwitterExtractor


handle = 'graham.murr'
extractor = TwitterExtractor()
followers = extractor.extract_followers(handle)

file = open('twitter_followers.txt', 'w+')
for follower in followers:
    file.write('%s\t%s\t%s\t%s\t%s' % (follower.handle, follower.name, follower.description,
                                       follower.is_following, follower.is_default_picture))

    print('%s\t%s\t%s\t%s\t%s' % (follower.handle, follower.name, follower.description,
                                  follower.is_following, follower.is_default_picture))