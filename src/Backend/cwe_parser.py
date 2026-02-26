import xml.etree.ElementTree as ET

def parse_cwe_hierarchy(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    ns = {'cwe': 'http://cwe.mitre.org/cwe-7'}
    graph = {}

    # Build the graph: map each CWE ID to its related CWE IDs (parent/child)
    for weakness in root.findall(".//cwe:Weakness", ns):
        source_id = weakness.get("ID")
        graph.setdefault(source_id, set())

        for related in weakness.findall(".//cwe:Related_Weakness", ns):
            related_id = related.get("CWE_ID")
            nature = related.get("Nature")

            if nature in ["ChildOf", "ParentOf"]:
                graph[source_id].add(related_id)
                graph.setdefault(related_id, set()).add(source_id)  # Bidirectional

    return graph



def parse_cwe_relations(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    ns = {'cwe': 'http://cwe.mitre.org/cwe-7'}

    parent_map = {}   # key = child, value = set of parents
    child_map = {}    # key = parent, value = set of children

    for weakness in root.findall(".//cwe:Weakness", ns):
        source_id = weakness.get("ID")
        for related in weakness.findall(".//cwe:Related_Weakness", ns):
            target_id = related.get("CWE_ID")
            nature = related.get("Nature")

            if nature == "ChildOf":
                parent_map.setdefault(source_id, set()).add(target_id)
                child_map.setdefault(target_id, set()).add(source_id)

    return parent_map, child_map


def get_all_parents(cwe_id, parent_map):
    """Recursively return all ancestors of a CWE."""
    visited = set()
    def dfs(cwe):
        for parent in parent_map.get(cwe, []):
            if parent not in visited:
                visited.add(parent)
                dfs(parent)
    dfs(cwe_id)
    return sorted(visited)

def get_all_children(cwe_id, child_map, visited=None):
    if visited is None:
        visited = set()
    if cwe_id in visited:
        return set()

    visited.add(cwe_id)

    children = child_map.get(cwe_id, set())
    all_descendants = set(children)
    for child in children:
        all_descendants |= get_all_children(child, child_map, visited)
    return all_descendants

def get_related_cwes(graph, start_id):
    visited = set()
    result = []

    def dfs(cwe_id):
        if cwe_id in visited:
            return
        visited.add(cwe_id)
        result.append(cwe_id)
        for neighbor in graph.get(cwe_id, []):
            dfs(neighbor)

    dfs(start_id)
    return sorted(result)

# Example usage
if __name__ == "__main__":
    cwe_xml_path = "cwec_v4.17.xml"  # Path to your CWE XML file
    cwe_graph = parse_cwe_hierarchy(cwe_xml_path)
    parent_map, child_map = parse_cwe_relations(cwe_xml_path)
    input_cwe = "691"  # For example, CWE-3
    # print(f"Parents {parent_map[input_cwe]}")
    print(f"Child {child_map[input_cwe]}")
    print(get_all_children(input_cwe,child_map))

    # for i in range(1000):
    #     related_cwes = get_related_cwes(cwe_graph, str(i))
    #     target_cwe= str(i)
    #     print(f"All related CWEs to CWE-{i}:")
    #     print("------OLD------")
    #     for cwe in related_cwes:
    #         print(f"CWE-{cwe}")
    #     print(f"----All parents of CWE-{target_cwe}:------")
    #     for p in get_all_parents(target_cwe, parent_map):
    #         print(f"  CWE-{p}")

    #     print(f"\n------------All children of CWE-{target_cwe}:-------")
    #     for c in get_all_children(target_cwe, child_map):
    #         print(f"  CWE-{c}")
