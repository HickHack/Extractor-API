import tweepy
import time
import extractor.settings as settings
from extractor.model.twitter import User

credentials = settings.TWITTER['oauth']
max_friends = settings.TWITTER['limits']['max_friends']
max_friends_of_friends = settings.TWITTER['limits']['friends_of_friends']

auth = tweepy.OAuthHandler(credentials['consumer_key'], credentials['consumer_secret'])
auth.set_access_token(credentials['access_token'], credentials['access_secret'])
api = tweepy.API(auth)


def get_friends(centre, max_depth=1, current_depth=0, taboo_list=None):
    print('current depth: %d, max depth: %d' % (current_depth, max_depth))

    if taboo_list is None:
        taboo_list = []
    if current_depth == max_depth:
        print('out of depth')
        return taboo_list

    if centre in taboo_list:
        print('Already been here.')
        return taboo_list
    else:
        taboo_list.append(centre)

    try:

        if not User.exists(centre):
            print('Retrieving user details for twitter id %s' % str(centre))
            while True:
                try:
                    user = User.create(api.get_user(centre))
                    user.persist()

                    break
                except Exception as error:
                    if error[0][0]['code'] == 88:
                        print('Rate limited. Sleeping for 15 minutes.')
                        time.sleep(15 * 60 + 15)
                        continue

                    return taboo_list
        else:
            user = User.load(centre)

        # Retrieve Friends
        if not user.has_discovered_friends():
            print('No cached friends for "%s"' % user.screen_name)

            print('Retrieving friends for user "%s" (%s)' % (user.name, user.screen_name))

            # page over friends
            c = tweepy.Cursor(api.friends, id=user.id).items()

            while True:
                try:
                    friend = User.create(c.next())
                    if not User.exists(friend.id):
                        friend.persist()
                    user.add_friend(friend.id)
                    if len(user.friends_ids) >= max_friends:
                        print('Reached max no. of friends for "%s".' % user.screen_name)
                        break
                except tweepy.TweepError as error:
                    if isinstance(error, tweepy.RateLimitError):
                        print('Rate limited. Sleeping for 15 minutes.')
                        time.sleep(15 * 60 + 15)
                        continue
                    else:
                        print('Error: ' + str(error))
                        continue
                except StopIteration:
                    break
            user.persist()

        print('Found %d friends for %s' % (len(user.friends_ids), user.screen_name))

        # get friends of friends
        cd = current_depth
        if cd + 1 < max_depth:
            for fid in user.friends_ids[:max_friends_of_friends]:
                taboo_list = get_friends(fid, max_depth=max_depth,
                                         current_depth=cd + 1, taboo_list=taboo_list)

        if cd + 1 < max_depth and len(user.friends_ids) > max_friends_of_friends:
            print('Not all friends retrieved for %s.' % user.screen_name)

    except Exception as error:
        print('Error retrieving followers for user id: ', centre)
        print(error)

    return taboo_list


def run(screen_name, depth=2):

    if depth < 1 or depth > 3:
        raise Exception('Depth value %d is not valid' % depth)

    print('Max Depth: %d' % depth)

    try:
        matches = api.lookup_users(screen_names=[screen_name])

        if len(matches) == 1:
            get_friends(matches[0].id, max_depth=depth)
            return matches[0].id
    except Exception:
        raise Exception('Can\'t retrieve data for %s' % screen_name)

