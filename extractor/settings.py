import os

PROJECT_DIR = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
CACHE_DIR = os.path.join(DATA_DIR, 'cache')
TWITTER_CACHE_DIR = os.path.join(CACHE_DIR, 'twitter')
LINKEDIN_CACHE_DIR = os.path.join(CACHE_DIR, 'linkedin')

TWITTER = {
    'oauth': {
        'consumer_key': 'rHvRleQWXoYSIXRka0GRbJaPe',
        'consumer_secret': 'FZ61mtqKr8qEAkTDr2CJyTlHPqlDla7LLGNjTo4TyJkE3PmH5H',
        'access_token': '3306707327-WJNm0c7mlH77OLzQQCR9eBndACvN9qYYA8oJfic',
        'access_secret': 'cc8bwd5W3QFPCXIaLJnsWxiro8OG4qp53p1g8RoXtFMHU',
    },
    'cache': {
        'users': os.path.join(TWITTER_CACHE_DIR, 'users')
    },
    'limits': {
        'max_friends': 25,
        'friends_of_friends': 25,
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
    'host': 'http://localhost:7474',
    'username': 'neo4j',
    'password': 'neo4j'
}

GENERAL = {
    'generated_image_path': os.path.join('/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-2]), 'Exograph-Server/public/img/graph')
}

