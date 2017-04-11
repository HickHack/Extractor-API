from extractor.persistence.bulk_loader import BulkLoader
from extractor.persistence.connector import Driver
from extractor.image_generator import ImageGenerator
from extractor.model.network import Network
import api.utils as utils


def load(graph, root_id, job, label, rel):

    try:
        loader = BulkLoader()
        driver = Driver()

        image_gen = ImageGenerator(graph)
        network = Network(job.name, job.id, utils.generate_timestamp(),
                          len(graph.nodes()), job.type.description, image_gen.get_image_ref())
        query = loader.get_query(graph, label, rel)
        driver.link_graph_to_user(job.user_id, root_id, network.__dict__, query, label)
    except Exception as error:
        raise Exception('Import failed.')
