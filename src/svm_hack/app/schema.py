

from collections import namedtuple


UserInfo = namedtuple(
    "UserInfo",
    [
        "age",
        "time_horizon",
        "revenues",
        "expenses",
        "invest_percent",
        "reaction_to_loss",
    ],
)
