

from pydantic import BaseModel


class UserForm(BaseModel):
    name: str
    age: str
    initial_capital: str
    desired_strategy: str
    investing_timeline: str


class Plots(BaseModel):
    crypto_plot: str
    stock_plot: str
    gold_plot: str