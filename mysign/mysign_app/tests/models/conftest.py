import os

import pytest
from dotenv import find_dotenv, load_dotenv


@pytest.fixture(autouse=True)
def setup():
    load_dotenv(find_dotenv())
    # os.environ['POSTGRES_DATABASE'] = "test"
    #
    # print(os.environ)
