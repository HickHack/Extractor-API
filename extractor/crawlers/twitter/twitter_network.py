import networkx as nx
from extractor.model.twitter import User


def process_friends(seed_id, edges=None, depth=0, max_depth=3):
    if edges is None:
        edges = []

    if User.exists(seed_id):
        user = User.load(seed_id)
    else:
        return edges

    for friend_id in user.friends_ids:
        if not User.exists(friend_id):
            continue

        edges.append([seed_id, friend_id])

        if depth + 1 < max_depth:
            process_friends(friend_id, edges, depth + 1, max_depth)

    return edges


def generate_graph(seed_id):
    edges = process_friends(seed_id)
    graph = nx.DiGraph()
    root_uuid = None

    for (follower_id, followee_id) in edges:
        if User.exists(follower_id) and User.exists(followee_id):
            follower = User.load(follower_id)
            followee = User.load(followee_id)

            graph.add_node(follower.id, follower.get_attributes())
            graph.add_node(followee.id, followee.get_attributes())
            graph.add_edge(follower.id, followee.id)

            if follower_id == seed_id:
                root_uuid = follower.uuid

    return graph, root_uuid

