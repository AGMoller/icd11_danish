import json
import os
from typing import Dict, List

import requests
from dotenv import load_dotenv

from file_handling import read_json, save_json

load_dotenv()


class ICD11_Client:
    def __init__(
        self,
        api_version: str = "v2",
        linearization: str = "mms",
        release_id: str = "2022-02",
    ) -> None:
        self.CLIENT_ID = os.environ["CLIENT_ID"]
        self.CLIENT_SECRET = os.environ["CLIENT_SECRET"]
        self.api_version = api_version
        self.linearization = linearization
        self.release_id = release_id

    def get_node(self, id: str) -> Dict:
        """Returns the node with the given id"""

        uri = f"https://id.who.int/icd/release/11/{self.release_id}/{self.linearization}/{id}"

        r = requests.get(uri, headers=self._get_headers(), verify=True)

        return json.loads(r.text)

    def get_icd11_taxonomy(self) -> List[Dict]:
        """Returns the ICD11 taxonomy"""

        has_crawled = dict()

        root = icd11_client.basic_information_linearization()

        data: List[Dict] = [root]

        has_crawled[root["@id"].split("/")[-1]] = True

        queue = root["child"]

        counter = 0
        while queue:
            # pop the first element
            node_uri = queue.pop(0)

            # get the node id
            _id = node_uri.split("/")[-1]
            if _id in ["unspecified", "other"]:
                _id = node_uri.split("/")[-2]

            # check if we already crawled this node
            if _id in has_crawled:
                continue

            # get the node
            try:
                node = icd11_client.get_node(_id)
                data.append(node)
            except:
                print(f"Error: {node_uri}")
                continue

            # add children to the queue
            if "child" in node:
                queue.extend(node["child"])

            # mark that we crawled this node
            has_crawled[_id] = True

            counter += 1
            if counter % 100 == 0:
                print(f"Crawled {counter} nodes")

        return data

    def basic_information_linearization(
        self, release_id: str = "2022-02"
    ) -> Dict[str, str]:
        """Returns the basic information of the ICD11 release"""

        uri = f"https://id.who.int/icd/release/11/{release_id}/mms"

        r = requests.get(uri, headers=self._get_headers(), verify=True)

        return json.loads(r.text)

    def basic_information(
        self,
        uri: str = "https://id.who.int/icd/entity?releaseId=2022-02",
    ) -> Dict[str, str]:
        """Returns the basic information of the ICD11 release"""

        r = requests.get(uri, headers=self._get_headers(), verify=True)

        return json.loads(r.text)

    def _get_headers(self) -> Dict[str, str]:
        """Returns the headers for the API call
        Based on: https://github.com/ICD-API/Python-samples/blob/master/sample.py
        """

        # setting variables
        token_endpoint: str = "https://icdaccessmanagement.who.int/connect/token"
        client_id: str = self.CLIENT_ID
        client_secret: str = self.CLIENT_SECRET
        scope: str = "icdapi_access"
        grant_type: str = "client_credentials"

        # define payload
        payload: Dict[str, str] = {
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": scope,
            "grant_type": grant_type,
        }

        # make request
        r = requests.post(token_endpoint, data=payload, verify=True).json()
        token: str = r["access_token"]

        # HTTP header fields to set
        headers = {
            "Authorization": "Bearer " + token,
            "Accept": "application/json",
            "Accept-Language": "en",
            "API-Version": "v2",
        }

        return headers


if __name__ == "__main__":

    icd11_client = ICD11_Client()

    # root = icd11_client.basic_information_linearization()

    data = icd11_client.get_icd11_taxonomy()

    save_json("data/icd11_taxonomy.json", data)

    # data = [root]

    # chapters = root["child"]

    # to_crawl = chapters

    # node = icd11_client.get_node("1719389232")

    a = 1
