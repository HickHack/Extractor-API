import matplotlib as plt
import matplotlib.pyplot as plt
import networkx as nx
import extractor.settings as settings
import string
import random
import time
import os

image_path = settings.GENERAL['generated_image_path']


class ImageGenerator(object):

    def __init__(self, graph):
        self._graph = graph
        self._filename = self._generate_filename()

        self._configure_plot()
        self._generate_plot()

    def get_image_ref(self):
        return self._filename

    def _generate_filename(self):
        random.seed(time.time())
        filename = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(70)) + '.png'

        return filename

    def _generate_plot(self):
        graph_pos = nx.spring_layout(self._graph)

        nx.draw(self._graph, graph_pos, node_color='#A0CBE2',
                edge_color='#B0C23E', width=2, edge_cmap=plt.cm.Blues, with_labels=False, block=False)

        plt.savefig(os.path.join(image_path, self._filename), format="PNG", transparent=True)

    def _configure_plot(self):
        plt.show(block=False)
        plt.figure(figsize=(5, 5))



