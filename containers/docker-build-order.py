#!/usr/bin/env python3

import argparse
import dataclasses
import os


@dataclasses.dataclass
class DockerfileNode:
    path: str
    base_images: list[str]
    processed: bool = False

    def __str__(self):
        return f"{self.path}"

class GraphNode:
    def __init__(self, value):
        self.value = value
        self.edges = []
        self.isRoot = True

    def add_edge(self, node):
        self.edges.append(node)

    def remove_edge(self, node):
        self.edges.remove(node)

    def __str__(self):
        return self.value.__str__()


def create_parser():
    parser = argparse.ArgumentParser(description='Determine the order to build Docker images')
    # Add single argument that is directory to search for Dockerfiles
    parser.add_argument('directory', type=str, help='Directory to search for Dockerfiles')
    parser.add_argument('org_name', type=str, help='Organization name to filter Dockerfiles')
    return parser


def find_dockerfiles(directory):
    allowed_names = {'Dockerfile', 'Containerfile'}
    dockerfiles = []
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name in allowed_names:
                dockerfiles.append(os.path.join(root, file_name))
    return dockerfiles


def get_all_base_images_from_dockerfile(dockerfile):
    with open(dockerfile, 'r') as f:
        lines = f.readlines()
    base_images = []
    for line in lines:
        if line.startswith('FROM'):
            base_images.append(line.split()[1])
    return base_images


def get_container_name_from_path(path):
    return path.split('/')[-2]

def parse_from_dockerfile(from_line):
    """
    :param from_line:
    :return: str
    the FROM command contains `ORG/IMAGE:TAG` format
    The ORG and tar are optional
    """
    org, image, image_tag = None, None, None

    if '/' in from_line:
        org, from_line = from_line.split('/')
    if ':' in from_line:
        image, image_tag = from_line.split(':')
    else:
        image = from_line

    return org, image, image_tag



def create_build_tree(dockerfiles_nodes, org_name):

    build_order = dict() # Yeah, this is simple dictionary with image org+/image name as the keys


    # Remove all images that do not have any base_image, print them and then remove
    no_base_images = [dn for dn in dockerfiles_nodes if not dn.base_images]
    for dn in no_base_images:
        print(f'WARNING: Removing: {dn.path}')
    dockerfiles_nodes = [dn for dn in dockerfiles_nodes if dn.base_images]

    # Let's start by finding only the `FROM scratch`
    for dn in dockerfiles_nodes:
        from_image_org, from_image_name, from_image_tag = parse_from_dockerfile(dn.base_images[0])
        c_name = get_container_name_from_path(dn.path)
        if from_image_name == "scratch":
            print("Found the image from scratch adding it to the build order")
            build_order[f"{org_name}/{c_name}"] = GraphNode(dn)
            dn.processed = True

    dockerfiles_nodes = [dn for dn in dockerfiles_nodes if dn.processed == False]
    # Now let's add all the images to the build_order without checking!
    for dn in dockerfiles_nodes:
        c_name = get_container_name_from_path(dn.path)
        build_order[f"{org_name}/{c_name}"] = GraphNode(dn)
    """
    1. Deduplicate list of base_images
    2. Check if the image is in the build order 
    3. If it's in the build_order then add it to the edges of the graphNode and unset the is root
    4. If it's not in the build order then do not do that :)
    """

    for dn in dockerfiles_nodes:
        base_images_deduplicated = list(set(dn.base_images))
        for b_image in base_images_deduplicated:
            from_image_org, from_image_name, from_image_tag = parse_from_dockerfile(b_image)
            c_name = get_container_name_from_path(dn.path)
            if from_image_org:
                from_image = f"{from_image_org}/{from_image_name}"
            else:
                from_image = f"{from_image_name}"

            if from_image in build_order:
                build_order[f"{org_name}/{c_name}"].isRoot = False
                build_order[from_image].add_edge(build_order[f"{org_name}/{c_name}"])

    return build_order


def print_in_order(node: GraphNode, visited_nodes):
    my_name = get_container_name_from_path(node.value.path)
    visited_nodes = visited_nodes + [my_name]
    print("->".join(visited_nodes))
    for edge in node.edges:
        print_in_order(edge, visited_nodes)

def print_graph(nodes):
    for node in nodes.values():
        if node.isRoot:
            print_in_order(node, [])



def main():
    parser = create_parser()
    args = parser.parse_args()
    if not os.path.isdir(args.directory):
        parser.error(f'{args.directory} is not a directory')

    dockerfiles_paths = find_dockerfiles(args.directory)
    dockerfiles_nodes = []
    for docker_file in dockerfiles_paths:
        base_images = get_all_base_images_from_dockerfile(docker_file)
        dockerfiles_nodes.append(DockerfileNode(docker_file, base_images))

    for node in dockerfiles_nodes:
        print(f'Found: {node.path}: {node.base_images}')

    build_order = create_build_tree(dockerfiles_nodes, args.org_name)
    print_graph(build_order)

if __name__ == '__main__':
    main()
