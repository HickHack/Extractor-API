import os

PROJECT_DIR = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
CACHE_DIR = os.path.join(DATA_DIR, 'cache')
TWITTER_CACHE_DIR = os.path.join(CACHE_DIR, 'twitter')
LINKEDIN_CACHE_DIR = os.path.join(CACHE_DIR, 'linkedin')

TWITTER = {
    'oauth': {
        'consumer_key': '0vKduBqsTBAHyoHhSdiMebiCl',
        'consumer_secret': 'wRKth6dJb4VtYbCmnLh4BlhGSJ6GwbnliSUq0tI7B4TZrvQrFh',
        'access_token': '3306707327-JPeaVubPJSHUJwCNRoAVWMKQH7zEFsz6sLrP54m',
        'access_secret': 'U5r07PzQP4b3oXV0fOxepZTOH6T9aeVzslcDRl8hzbShx',
    },
    'cache': {
        'users': os.path.join(TWITTER_CACHE_DIR, 'users')
    },
    'limits': {
        'max_friends': 40,
        'friends_of_friends': 40,
        'max_depth': 2
    }
}

LINKEDIN = {
    'limits': {
        'max_depth': 3,
        'retry_limit': 5,
        'request_throttle': 0
    },
    'cache': {
        'cookie_file': os.path.join(LINKEDIN_CACHE_DIR, 'parser.cookies.txt'),
    },
    'urls': {
        'home_url': 'https://www.linkedin.com/nhome/',
        'cdn_url': 'https://media.licdn.com/mpr/mpr/shrinknp_400_400',
        'contacts_url': 'https://www.linkedin.com/connected/api/v1/contacts/connections-only?start=%d&count=%d&fields=id,name,firstName,lastName,company,title,location,tags,emails,sources,displaySources,connectionDate,profileImageUrl&sort=CREATED_DESC',
        'all_connections_url': 'https://www.linkedin.com/profile/profile-v2-connections?id=%d&offset=%d&count=%d&distance=1&type=INITIAL',
        'shared_connections_url': 'https://www.linkedin.com/profile/profile-v2-connections?id=%d&offset=%d&count=%d&distance=1&type=SHARED'
    }
}

NEO4J = {
    'default': {
        'db_name': 'graph.db',
        'username': 'neo4j',
        'password': 'neo4j',
        'host': '127.0.0.1',
        'port': '7687'
    }
}

GENERAL = {
    'generated_image_path': os.path.join('/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-2]), 'exograph-server/public/img/graph')
}

