from services.bots import Bots
import pytest


@pytest.fixture()
def init():
    print ("Initiating Bot Sequence ...")


@pytest.mark.skip(reason="skip due to functional testing")
def test_craigbot():
    test_bot = Bots()
    test_bot.run_craigbot()
