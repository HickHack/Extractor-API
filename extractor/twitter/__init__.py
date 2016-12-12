import json

from extractor.twitter.model.follower import Follower
from extractor.twitter.twitter import TwitterExtractor

handle = 'RiTech9'
extractor = TwitterExtractor()
followers = extractor.extract_followers(handle)

print(len(followers))
f = open('followers.json', 'w')
f.write(json.dumps(followers))
f.close()
