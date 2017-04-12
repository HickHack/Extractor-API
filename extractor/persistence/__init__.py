from extractor.persistence.bulk_loader import BulkLoader
from extractor.persistence.connector import Driver
from extractor.image_generator import ImageGenerator
from extractor.model.network import Network
import api.utils as utils


def load(graph, root_uuid, job, label, rel):
    loader = BulkLoader()
    driver = Driver()

    if root_uuid is not None:
        image_gen = ImageGenerator(graph)
        network = Network(job.name, job.id, utils.generate_timestamp(),
                          len(graph.nodes()), job.type.description, image_gen.get_image_ref())
        query = loader.get_query(graph, label, rel)
        driver.link_graph_to_user(job.user_id, root_uuid, network.__dict__, query, label)
    else:
        raise Exception('root uuid can not be None')
