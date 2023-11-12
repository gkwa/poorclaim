import argparse
import logging

import jinja2
import neo4j
import yaml

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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


def fix_titles(data, fix_data):
    for fix_item in fix_data:
        for item in data:
            if item["title"] == fix_item["before"]:
                item["title"] = fix_item["after"]

    return data


def update_data_yaml(data):
    with open("data.yaml", "w") as file:
        yaml.dump(data, file, default_flow_style=False)


def process_query_data(query_data):
    driver = neo4j.GraphDatabase.driver(
        "bolt://localhost:7687",
        auth=("", ""),
    )

    for item in query_data:
        if not item["cypher_query"]:
            logging.warning(f"query is empty for {item['title']}, skipping...")
            continue

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

    with open("_README.org", "w") as manual_file:
        manual_file.write(rendered_manual)

    driver.close()


def main():
    parser = argparse.ArgumentParser(description="read/write data.yaml")
    parser.add_argument("--titles", action="store_true", help="titles")
    parser.add_argument("--fix-titles", action="store_true", help="fix titles")
    parser.add_argument("--verbose", action="store_true", help="logging")
    parser.add_argument("--run-neo4j", action="store_true", help="query neo4j")
    args = parser.parse_args()

    if args.verbose and not all(
        value is False for key, value in vars(args).items() if key != "verbose"
    ):
        parser.print_help()
        return

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Verbose logging enabled.")
    else:
        # If --verbose is not specified, set logging level to INFO
        logging.getLogger().setLevel(logging.INFO)

    with open("data.yaml", "r") as file:
        query_data = yaml.load(file, Loader=yaml.FullLoader)

    if args.titles:
        report_titles(query_data)

    if (
        args.fix_titles and args.verbose
    ):  # Only execute if --fix-titles and --verbose are specified
        with open("fix.yaml", "r") as fix_file:
            fix_data = yaml.load(fix_file, Loader=yaml.FullLoader)

        query_data = fix_titles(query_data, fix_data)
        update_data_yaml(query_data)

    if args.run_neo4j:
        process_query_data(query_data)


if __name__ == "__main__":
    main()
