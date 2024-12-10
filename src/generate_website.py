import pathlib
import subprocess

from string import Template

import pandas as pd

HTML_TEMPLATE = Template(
    """<html>
  <head>
     <title>$title</title>
     <description>PCC Bibframe Interoperability Group (BIG) DCTap-to-SHACL</description>
     <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
  </head>
  <body class="container">
    <h1>$title</h1>
    $body
    <footer>
     Version $version.  
     Github Repository <a href="https://github.com/bf-interop/DCTap/">https://github.com/bf-interop/DCTap/</a>
    </footer>
  </body>
</html>"""
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
        dctap_html_files.append((html_filename, dctap_title))
        html_path = parent / html_filename
        dctap_to_html(dctap, dctap_title, html_path, version)
    index_html_path = parent / "index.html"
    index_html_body = "<ul>\n"
    for dctap in sorted(dctap_html_files):
        index_html_body += f"""<li><a href="{dctap[0]}">{dctap[1]}</a></li>\n"""
    index_html_body += "</ul>\n"
    with index_html_path.open("w+") as fo:
        index_html = HTML_TEMPLATE.substitute(
            title=folder_path.stem, body=index_html_body, version=version
        )
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
    dctap_html = HTML_TEMPLATE.substitute(title=title, body=table_html, version=version)
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
            all_dctap_dirs.append((row_html_filename, row.name))
            dctap_folder_to_html(row, html_parent, version)
    # Creates Website index.html Page
    with (repo_home / "docs/index.html").open("w+") as fo:
        title = "Bibframe Interoperability Group (BIG) DCTap"
        home_html_body = "<ul>\n"
        for row in sorted(all_dctap_dirs):
            home_html_body += f"""<li><a href="{row[0]}">{row[1]}</a></li>\n"""
        home_html_body += "</ul>\n"
        home_html = HTML_TEMPLATE.substitute(
            title=title, body=home_html_body, version=version
        )
        fo.write(home_html)


if __name__ == "__main__":
    script_path = pathlib.Path(__file__)
    repo_home = script_path.parent.parent
    print("Starting Generation of DCTap Website")
    main(repo_home)
    print("Finished Website Generation")
