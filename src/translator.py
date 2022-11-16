import warnings
from typing import Dict, List, Literal, Optional, Union

import numpy as np
from iteration_utilities import unique_everseen
from tqdm import tqdm
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from file_handling import read_json, save_json
from utils import get_device

warnings.filterwarnings("ignore")


class Translator:
    def __init__(
        self,
        model_name: str = "Helsinki-NLP/opus-mt-en-da",
        device: str = get_device(),
    ) -> None:
        self.device = device
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name, fast=True, device_map="auto"
        )
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name).to(
            self.device
        )
        self.beam_size = 5
        self.batch_size = 2

    def translate(self, text: Union[str, List[str]]) -> List[str]:

        if isinstance(text, str):
            text = [text]

        tokenized_text = self.tokenizer(text, return_tensors="pt", padding=True).to(
            self.device
        )
        translation = self.model.generate(**tokenized_text)
        translated_text = self.tokenizer.batch_decode(
            translation, skip_special_tokens=True
        )

        return translated_text


def translate_elements(data: List[Dict], translator: Translator) -> List[Dict]:
    """This function accepts a list of dictionaries as argument
    and translate all values of nested dictionaries
    """
    translated_data = []
    for element in (pbar := tqdm(data)):

        if "code" in element:
            pbar.set_description(f"Translating element {element['code']}")

        translated_element = {}
        for key, value in element.items():
            if key in [
                "title",
                "description",
                "longDefinition",
                "fullySpecifiedName",
                "codingNote",
            ]:
                translated_element[key] = {
                    "language": "da",
                    "value": translator.translate(value["@value"])[0],
                }
            elif key in ["foundationChildElsewhere", "exclusion"]:
                translated_children = []
                for child in value:
                    translated_children.append(
                        {
                            "label": {
                                "language": "da",
                                "value": translator.translate(child["label"]["@value"])[
                                    0
                                ],
                            },
                            "foundationReference": child["foundationReference"],
                            "linearizationReference": child["linearizationReference"]
                            if "linearizationReference" in child
                            else None,
                        }
                    )
                translated_element[key] = translated_children
            elif key in ["inclusion", "indexTerm"]:
                translated_children = []
                for child in value:
                    translated_children.append(
                        {
                            "label": {
                                "language": "da",
                                "value": translator.translate(child["label"]["@value"])[
                                    0
                                ],
                            },
                        }
                    )
                translated_element[key] = translated_children
            else:
                translated_element[key] = value

        translated_data.append(translated_element)

    return translated_data


if __name__ == "__main__":

    # not sure if I have duplicates here.
    data = list(unique_everseen(read_json("data/icd11_taxonomy.json")))

    translator = Translator()
    translated = translate_elements(data, translator)
    save_json("data/icd11_taxonomy_da.json", translated)

    # translator = Translator()
    # # translator.model_to_cpu()
    # texts = ["This is a test", "This is another test"]
    # print(
    #     translator.translate(
    #         [
    #             "This is a funny text that should be in Danish.",
    #             "This is another test",
    #             "Thoracolumbosacral spina bifida cystica with hydrocephalus",
    #             "This chapter includes diseases of the blood as well as diseases of blood forming organs.",
    #         ]
    #     )
    # )
