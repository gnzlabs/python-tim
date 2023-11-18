from dataclasses import dataclass
from typing import List


@dataclass
class Configuration:

    plugins: List[str]
