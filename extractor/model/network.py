class Network(object):

    def __init__(self, name, job_id, created_time, no_connections, type, image_url):
        self.name = name
        self.job_id = job_id
        self.created_time = created_time
        self.no_connections = no_connections
        self.type = type
        self.image_file = image_url
        self.is_trash = False

