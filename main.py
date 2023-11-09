# flake8: noqa E501

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
        "title": "list distict node types",
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
        "title": "If I were to make Thai Curry, what ingredients do I need?",
        "query_comment": "",
        "results_comment": "",
        "cypher_query": textwrap.dedent(
            """

MATCH (r:Recipe {name: 'Vegan Thai Red Curry'})-[:CONTAINS]->(p:Product)
MATCH (p)-[:PURCHASE_AT]->(s:Store)
RETURN s.name AS StoreName, COLLECT(DISTINCT p.name) AS Ingredients
;

            """
        ),
    },
    {
        "title": "order products by type",
        "query_comment": "",
        "results_comment": "",
        "cypher_query": textwrap.dedent(
            """
MATCH (p:Product)-[:PURCHASE_AT]->(s:Store)
RETURN p.name AS ProductName, s.name AS StoreName, p.type as Type
ORDER BY toLower(p.type)
;

            """
        ),
    },
    {
        "title": "get products that i've not yet assiged a type to",
        "query_comment": "",
        "results_comment": "",
        "cypher_query": textwrap.dedent(
            """
MATCH (p:Product)
WHERE p.type IS NULL
RETURN p.name
;

            """
        ),
    },
    {
        "title": "something about urls",
        "query_comment": "",
        "results_comment": "",
        "cypher_query": textwrap.dedent(
            """
MATCH (r:Recipe)-[c:CONTAINS]->(p:Product)
WHERE id(p) IS NULL
RETURN r.name AS RecipeName, c.quantity AS Quantity, c.urls AS RecipeUrls
;

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
        "title": "list the brand of the product too",
        "query_comment": "",
        "results_comment": "",
        "cypher_query": textwrap.dedent(
            """
MATCH (p:Product)
OPTIONAL MATCH (p)-[:PURCHASE_AT]->(s:Store)
RETURN p.name AS ProductName, p.type AS Type, COALESCE(p.brand, '') AS Brand, COLLECT(DISTINCT s.name) AS AvailableAtStores
;

            """
        ),
    },
    {
        "title": "products whose names contain non-alphanum sorted randomly to prevent boredom while cleaning data",
        "query_comment": "",
        "results_comment": "",
        "cypher_query": textwrap.dedent(
            """
MATCH (p:Product)
WHERE p.name =~ ".*[^a-zA-Z0-9 ].*"
RETURN p.name AS ProductName
ORDER BY RAND()
;

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
        "title": "list all properties across all objects sorted case insensetively",
        "query_comment": "",
        "results_comment": "",
        "cypher_query": textwrap.dedent(
            """
MATCH (n)
UNWIND keys(n) AS propertyName
RETURN DISTINCT propertyName
ORDER BY toLower(propertyName)
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
        "title": "products that have a store associated",
        "query_comment": "",
        "results_comment": "",
        "cypher_query": textwrap.dedent(
            """
MATCH (p:Product)-[:PURCHASE_AT]->(s:Store)
RETURN p.name AS ProductName, s.name AS StoreName, p.type as Type
;
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
    {
        "title": "products that don't have a store associated with them",
        "query_comment": "",
        "results_comment": "",
        "cypher_query": textwrap.dedent(
            """
MATCH (p:Product)
WHERE NOT (p)-[:PURCHASE_AT]->(:Store)
RETURN p.name AS ProductName
;
            """
        ),
    },
    {
        "title": "if I were to make recipe Chicken Teriyaki Recipe, then what stores need I visit to get products i'd need for recipe",
        "query_comment": "",
        "results_comment": "",
        "cypher_query": textwrap.dedent(
            """
MATCH (r:Recipe {name: 'Tomatillo Salsa Verde'})-[:CONTAINS]->(p:Product)
MATCH (p)-[:PURCHASE_AT]->(s:Store)
RETURN s.name AS StoreName, COLLECT(DISTINCT p.name) AS Ingredients
;
            """
        ),
    },
    {
        "title": "if i would like to make a particular recipe, then what stores do I need to visit?",
        "query_comment": "",
        "results_comment": "",
        "cypher_query": textwrap.dedent(
            """
MATCH (r:Recipe)
WHERE r.name IN ['Vietnamese Spring Rolls (Gỏi Cuốn)']
WITH r
MATCH (r)-[:CONTAINS]->(p:Product)
OPTIONAL MATCH (p)-[:PURCHASE_AT]->(s:Store)
WITH p, COLLECT(DISTINCT s) AS stores
RETURN COLLECT(DISTINCT p.name) AS Ingredients,
       [store IN stores | CASE WHEN store IS NOT NULL THEN store.name ELSE 'Unknown' END] AS Stores
ORDER BY [store IN Stores | toLower(store)]
;
            """
        ),
    },
    {
        "title": "if i would like to make 2 recipes, then what stores do I need to visit?",
        "query_comment": "",
        "results_comment": "",
        "cypher_query": textwrap.dedent(
            """
MATCH (r:Recipe)
WHERE r.name IN ['Vietnamese Spring Rolls (Gỏi Cuốn)','Tom Yum Goong']
WITH r
MATCH (r)-[:CONTAINS]->(p:Product)
OPTIONAL MATCH (p)-[:PURCHASE_AT]->(s:Store)
WITH p, COLLECT(DISTINCT s) AS stores
RETURN COLLECT(DISTINCT p.name) AS Ingredients,
       [store IN stores | CASE WHEN store IS NOT NULL THEN store.name ELSE 'Unknown' END] AS Stores
ORDER BY [store IN Stores | toLower(store)]
;
            """
        ),
    },
    {
        "title": "I want to make a recipe and travel to the fewest number of stores",
        "query_comment": """
If I would like to make a particular recipe, then what stores do I
need to visit and sort products by stores so I don't have to leave
and return because I didn't realize there were two products from the same store

Also, make sure that if a recipe has an item that is not assigned
to a store by the PURCAHSE_AT relation, then the store field
appears empty as opposed to not seeing the product at all
""",
        "results_comment": "",
        "cypher_query": textwrap.dedent(
            """
MATCH (r:Recipe {name: 'Korean Sesame Noodles'})-[:CONTAINS]->(p:Product)
OPTIONAL MATCH (p)-[:PURCHASE_AT]->(s:Store)
WITH p, COLLECT(DISTINCT s) AS stores
RETURN COLLECT(DISTINCT p.name) AS Ingredients,
       [store IN stores | CASE WHEN store IS NOT NULL THEN store.name ELSE 'Unknown' END] AS Stores
ORDER BY [store IN Stores | toLower(store)]
;

            """
        ),
    },
    {
        "title": "list the products that aren't marked with a purchase location",
        "query_comment": "",
        "results_comment": "",
        "cypher_query": textwrap.dedent(
            """
MATCH (product:Product)
WHERE NOT (product)-[:PURCHASE_AT]->(:Store)
WITH product
ORDER BY rand()
LIMIT 10
RETURN product.name AS ProductName
ORDER BY ProductName
;

            """
        ),
    },
    {
        "title": "some recipes point to the same product multiple times by mistake",
        "query_comment": "",
        "results_comment": "",
        "cypher_query": textwrap.dedent(
            """
MATCH (p:Product)-[:CONTAINS]->(i:Ingredient)
WITH p, COLLECT(i) AS ingredients
WHERE SIZE(ingredients) > 1
RETURN p, ingredients
;

            """
        ),
    },
    {
        "title": "find products whose type contains vegetable",
        "query_comment": "",
        "results_comment": "",
        "cypher_query": textwrap.dedent(
            """
MATCH (p:Product)
WHERE toLower(p.type) CONTAINS 'vegetable'
RETURN p.name AS ProductName, p.type AS Type
;

            """
        ),
    },
    {
        "title": "find products whose type contains peas",
        "query_comment": "",
        "results_comment": "",
        "cypher_query": textwrap.dedent(
            """
MATCH (p:Product)
WHERE toLower(p.type) CONTAINS 'pea'
RETURN p.name AS ProductName, p.type AS Type
;
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
