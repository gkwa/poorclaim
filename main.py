import argparse

import jinja2
import neo4j
import yaml


def run_cypher_query(driver, query, limiter=None):
    with driver.session() as session:
        results = session.run(query).data()

    if limiter:
        results = limiter(results)

    return results


def limit_results(results, limit):
    return results[:limit] if limit else results


def report_titles(data):
    titles = [(item["title"], len(item["title"])) for item in data]
    titles.sort(key=lambda x: len(x[0]))

    for title, length in titles:
        print(f"{title} (Length: {length})")


def main():
    parser = argparse.ArgumentParser(description="read/write data.yaml")
    parser.add_argument("--titles", action="store_true", help="titles")
    args = parser.parse_args()

    driver = neo4j.GraphDatabase.driver(
        # "bolt://localhost:7687", auth=("username", "password")
        "bolt://localhost:7687",
        auth=("", ""),
    )

    # Load data from YAML into query_data
    with open("data.yaml", "r") as file:
        query_data = yaml.load(file, Loader=yaml.FullLoader)

    if args.titles:
        report_titles(query_data)
        return

    for item in query_data:
        item["results"] = run_cypher_query(
            driver,
            item["cypher_query"],
            limiter=lambda results: limit_results(results, item.get("limit")),
        )

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader("."),
    )
    template = env.get_template("template.org")

    rendered_manual = template.render(data=query_data)

    with open("manual.org", "w") as manual_file:
        manual_file.write(rendered_manual)

    driver.close()


if __name__ == "__main__":
    main()
