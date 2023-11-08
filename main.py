import textwrap

import jinja2
import neo4j


def run_cypher_query(driver, item):
    cypher_query = item["cypher_query"]

    with driver.session() as session:
        return session.run(cypher_query).data()


driver = neo4j.GraphDatabase.driver(
    # "bolt://localhost:7687", auth=("username", "password")
    "bolt://localhost:7687",
    auth=("", ""),
)

query_data = [
    {
        "title": "list all nodes and relations",
        "query_comment": "",
        "results_comment": "",
        "cypher_query": textwrap.dedent(
            """
MATCH (n) RETURN n
            """
        ),
    },
    {
        "title": "list all properties across all objects",
        "query_comment": "",
        "results_comment": "",
        "cypher_query": textwrap.dedent(
            """
MATCH (n)
UNWIND keys(n) AS propertyName
RETURN DISTINCT propertyName
            """
        ),
    },
    {
        "title": "list all Product nodes",
        "query_comment": "",
        "results_comment": "",
        "cypher_query": textwrap.dedent(
            """
MATCH (n:Product) RETURN n
            """
        ),
    },
    {
        "title": "list distict object types",
        "query_comment": "",
        "results_comment": "",
        "cypher_query": textwrap.dedent(
            """
MATCH (n)
RETURN DISTINCT labels(n) AS objectType
ORDER BY objectType
            """
        ),
    },
    {
        "title": "list all possible Product properties",
        "query_comment": "",
        "results_comment": "",
        "cypher_query": textwrap.dedent(
            """
MATCH (n:Product)
WITH DISTINCT keys(n) AS propertyNamesList
UNWIND propertyNamesList AS propertyName
RETURN DISTINCT propertyName
ORDER BY toLower(propertyName)
            """
        ),
    },
    {
        "title": "list all properties assigned to the PURCHASE_AT relation",
        "query_comment": "",
        "results_comment": "",
        "cypher_query": textwrap.dedent(
            """
MATCH ()-[r:PURCHASE_AT]->()
UNWIND keys(r) AS propertyNames
RETURN DISTINCT propertyNames
            """
        ),
    },
    {
        "title": "list all properties across all objects sorted",
        "query_comment": "",
        "results_comment": "",
        "cypher_query": textwrap.dedent(
            """
MATCH (n)
UNWIND keys(n) AS propertyName
RETURN DISTINCT propertyName
ORDER BY propertyName
            """
        ),
    },
    {
        "title": "list all properties of all objects including relations",
        "query_comment": "",
        "results_comment": "",
        "cypher_query": textwrap.dedent(
            """
// get properties of objects:
MATCH (n)
UNWIND keys(n) AS propertyName
RETURN DISTINCT 'Node' AS type, propertyName
ORDER BY type, propertyName

// combine both sets of properties:
UNION

// get properties of relations:
MATCH ()-[r]-()
UNWIND keys(r) AS propertyNames
RETURN DISTINCT type(r) AS type, propertyNames AS propertyName
ORDER BY type, propertyName
            """
        ),
    },
    {
        "title": "list the object type its assocted with",
        "query_comment": "",
        "results_comment": "",
        "cypher_query": textwrap.dedent(
            """
MATCH (n)
UNWIND labels(n) AS label
UNWIND keys(n) AS propertyName
RETURN label, propertyName
            """
        ),
    },
    {
        "title": "list all distinct objects",
        "query_comment": "",
        "results_comment": "",
        "cypher_query": textwrap.dedent(
            """
MATCH (n)
WITH DISTINCT labels(n) AS distinctLabels, keys(n) AS propertyNames
UNWIND distinctLabels AS label
UNWIND propertyNames AS propertyName
RETURN DISTINCT label, propertyName
            """
        ),
    },
    {
        "title": "list uniquely all CONTAINS relations",
        "query_comment": "",
        "results_comment": "",
        "cypher_query": textwrap.dedent(
            """
MATCH ()-[r:CONTAINS]-()
UNWIND keys(r) AS propertyNames
RETURN DISTINCT type(r) AS type, propertyNames AS propertyName
ORDER BY type, propertyName
            """
        ),
    },
    {
        "title": "list all CONTAINS relations",
        "query_comment": "",
        "results_comment": "",
        "cypher_query": textwrap.dedent(
            """
MATCH ()-[r:CONTAINS]-()
UNWIND keys(r) AS propertyNames
RETURN type(r) AS type, propertyNames AS propertyName
ORDER BY type, propertyName
            """
        ),
    },
    {
        "title": "list all relations",
        "query_comment": "",
        "results_comment": "",
        "cypher_query": textwrap.dedent(
            """
MATCH ()-[r]-()
RETURN DISTINCT type(r) AS relationType
ORDER BY relationType
            """
        ),
    },
    {
        "title": "list all relations, not just CONTAINS and inlude relation properties",
        "query_comment": "",
        "results_comment": "",
        "cypher_query": textwrap.dedent(
            """
MATCH ()-[r]-()
UNWIND keys(r) AS propertyNames
RETURN DISTINCT type(r) AS type, propertyNames AS propertyName
ORDER BY type, propertyName


            """
        ),
    },
]

for item in query_data:
    item["results"] = run_cypher_query(driver, item)

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader("templates"),
)
template = env.get_template("template.org")

rendered_manual = template.render(data=query_data)

with open("manual.org", "w") as manual_file:
    manual_file.write(rendered_manual)

driver.close()
