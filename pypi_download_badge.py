if __name__ == "__main__":
    import requests
    import os

    cur_file_dir = os.path.dirname(os.path.abspath(__file__))
    print("Output dir: ", cur_file_dir)

    projects = ["evalplus", "nnsmith"]
    for project in projects:
        url = f"https://pypistats.org/api/packages/{project}/overall"
        response = requests.get(url)
        data = response.json()["data"]
        total_downloads = sum([x["downloads"] for x in data])
        print(f"{project}: {total_downloads}")
        badge_url = f"https://img.shields.io/badge/pip_install-{total_downloads}-white?style=social&logo=pypi&logoColor=b509ac"
        # compile it to an svg
        response = requests.get(badge_url)
        with open(os.path.join(cur_file_dir, f"{project}_pypi.svg"), "wb") as f:
            f.write(response.content)
