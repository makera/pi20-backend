from dataclasses import dataclass

from models import BaseModel


@dataclass
class FoodKind(BaseModel):
    icon: str
    name: str


if __name__ == '__main__':
    food = FoodKind(icon='plate', name='Dinner', id=None)
    food._create_table()
    food.save()
    print(food)
    food.name = 'Launch'
    food.save()
    print(food)
    foods = FoodKind.fetch_all()
    print(foods)
