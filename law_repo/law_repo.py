import os
import requests

class LawRepo:
    laws = {
        "OR": "https://www.fedlex.admin.ch/filestore/fedlex.data.admin.ch/eli/cc/27/317_321_377/20240101/de/xml/fedlex-data-admin-ch-eli-cc-27-317_321_377-20240101-de-xml-9.xml",
        "ZGB": "https://www.fedlex.admin.ch/filestore/fedlex.data.admin.ch/eli/cc/54/757_781_799/20240101/de/xml/fedlex-data-admin-ch-eli-cc-54-757_781_799-20240101-de-xml-7.xml",
        "BV": "https://www.fedlex.admin.ch/filestore/fedlex.data.admin.ch/eli/cc/1999/404/20240101/de/xml/fedlex-data-admin-ch-eli-cc-1999-404-20240101-de-xml-14.xml"
    }

    @classmethod
    def get_xml(cls, law):
        directory = "raw"
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_path = os.path.join(directory, f"{cls.laws[law].split('/')[-1]}")
        if not os.path.exists(file_path):
            url = cls.laws[law]
            response = requests.get(url)
            if response.status_code == 200:
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                print(f"Downloaded {law} successfully.")
            else:
                print(f"Failed to download {law}.")
        with open(file_path, 'r') as file:
            return file.read()