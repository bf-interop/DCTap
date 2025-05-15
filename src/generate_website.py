import pathlib
import subprocess

import pandas as pd

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader("src/templates"),
    autoescape=select_autoescape(
        default_for_string=False,
    ),
)


def _get_latest_version():
    latest_version = -1
    try:
        latest_version_subprocess = subprocess.run(
            ["git", "rev-list", "--tags", "--max-count=1"], capture_output=True
        )
        latest_version_hash = latest_version_subprocess.stdout.strip().decode("utf-8")
        tag_subprocess = subprocess.run(
            ["git", "describe", "--tags", latest_version_hash], capture_output=True
        )
        latest_version = tag_subprocess.stdout.strip().decode("utf-8")
    except Exception as e:
        print(f"Failed to retrieve latest tag {e}")
    return latest_version


def dctap_folder_to_html(folder_path: pathlib.Path, parent: pathlib.Path, version: str):
    """
    Iterates through DCTap folder and generates HTML files for each DCTap TSV
    and then generates index.html file for the folder
    """
    dctap_html_files = []
    for dctap in folder_path.iterdir():
        if dctap.suffix != ".tsv":
            continue
        html_filename = f"{dctap.stem}.html"
        dctap_title = f"""{dctap.stem.replace("_", " ")} DCTap"""
        dctap_html_files.append({"url": html_filename, "name": dctap_title})
        html_path = parent / html_filename
        dctap_to_html(dctap, dctap_title, html_path, version)
    index_html_path = parent / "index.html"
    dctap_index_template = env.get_template("dctap_index.html")
    index_html = dctap_index_template.render(
        title=folder_path.stem,
        dctap_dirs=sorted(dctap_html_files, key=lambda x: x["name"]),
        version=version,
    )
    with index_html_path.open("w+") as fo:
        fo.write(index_html)


def dctap_to_html(
    dctap: pathlib.Path, title: str, html_path: pathlib.Path, version: str
):
    """
    Converts tsv into Pandas dataframe, generates HTML table, and saves
    to HTML file.
    """
    dctap_df = pd.read_csv(dctap, sep="\t")
    table_html = dctap_df.to_html(justify="center", na_rep="", index=False)
    table_html = table_html.replace('class="dataframe"', 'class="table table-bordered"')
    dctap_template = env.get_template("dctap.html")
    dctap_html = dctap_template.render(
        title=title, dctap_table=table_html, version=version
    )
    with html_path.open("w+") as fo:
        fo.write(dctap_html)


def main(repo_home: pathlib.Path):
    version = _get_latest_version()
    all_dctap_dirs = []
    for row in repo_home.iterdir():
        if row.is_dir() and "DCTAP" in row.name:
            row_html_filename = row.name.replace(" ", "_")
            html_parent = repo_home / "docs" / row_html_filename
            html_parent.mkdir(parents=True, exist_ok=True)
            all_dctap_dirs.append({"url": row_html_filename, "name": row.name})
            dctap_folder_to_html(row, html_parent, version)
    # Creates Website index.html Page
    index_template = env.get_template("index.html")
    home_html = index_template.render(
        title="Bibframe Interoperability Group (BIG) DCTAP",
        dctap_dirs=all_dctap_dirs,
        version=version,
    )
    with (repo_home / "docs/index.html").open("w+") as fo:
        fo.write(home_html)


if __name__ == "__main__":
    script_path = pathlib.Path(__file__)
    repo_home = script_path.parent.parent
    print("Starting Generation of DCTap Website")
    main(repo_home)
    print("Finished Website Generation")
