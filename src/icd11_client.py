import os
from typing import Dict

import requests
from dotenv import load_dotenv
import json


load_dotenv()


class ICD11_Client:
    def __init__(self) -> None:
        self.CLIENT_ID = os.environ["CLIENT_ID"]
        self.CLIENT_SECRET = os.environ["CLIENT_SECRET"]

    def basic_information(
        self,
        uri: str = "https://id.who.int/icd/entity?releaseId=2022-02",
    ) -> Dict[str, str]:
        """Returns the basic information of the ICD11 release"""

        r = requests.get(uri, headers=self._get_headers(), verify=False)

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
        r = requests.post(token_endpoint, data=payload, verify=False).json()
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

    basic = icd11_client.basic_information()

    a = 1
