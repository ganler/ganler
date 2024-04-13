import requests


def make_badge(project, downloads):
    if downloads >= 1000:
        downloads = f"{(downloads / 1000):.1f}".rstrip(".0") + "k"
    badge_url = f"https://img.shields.io/badge/pip_install-{downloads}-white?style=social&logo=pypi&logoColor=b509ac"
    response = requests.get(badge_url)
    with open(os.path.join(cur_file_dir, f"{project}_pypi.svg"), "wb") as f:
        f.write(response.content)


def _get_total_downloads_pypi_stat(project):
    url = f"https://pypistats.org/api/packages/{project}/overall"
    response = requests.get(url)
    data = response.json()["data"]
    return sum([x["downloads"] for x in data])


def get_total_downloads(project):
    from google.cloud import bigquery

    client = bigquery.Client()

    # Get all download counts
    query_job = client.query(
        f"""
    SELECT COUNT(*) AS num_downloads
    FROM `bigquery-public-data.pypi.file_downloads`
    WHERE file.project = '{project}'
    AND DATE(timestamp)
        BETWEEN '2022-09-10'
        AND CURRENT_DATE()"""
    )

    results = list(query_job.result())  # Waits for job to complete.
    assert len(results) == 1
    return results[0].num_downloads


if __name__ == "__main__":
    import os

    cur_file_dir = os.path.dirname(os.path.abspath(__file__))
    print("Output dir: ", cur_file_dir)

    projects = ["evalplus", "nnsmith"]
    for project in projects:
        total_downloads = get_total_downloads(project)
        print(f"{project}: {total_downloads}")
        make_badge(project, total_downloads)
