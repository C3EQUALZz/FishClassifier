import json
from dataclasses import dataclass
import pathlib


@dataclass
class NeuralNetwork:
    network_image: str
    network_name: str
    network_description: str
    network_status: str
    unread_messages: int
    is_active: bool


class NeuralNetworks:
    def __init__(self, networks_file: pathlib.Path) -> None:
        self.networks: list[NeuralNetwork] = []
        self.load_users_from_file(networks_file)

    def load_users_from_file(self, file_path: pathlib.Path) -> None:
        with open(file_path, 'r') as f:
            users_data = json.load(f)

        self.networks.extend(map(lambda user_data: NeuralNetwork(**user_data), users_data))
