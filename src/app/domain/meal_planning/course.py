import math
from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class Course:
    """Represents a Recipe reference within a Menu."""

    recipe_id: UUID | str
    portions: int | str = 1

    def __post_init__(self) -> None:
        try:
            raw_recipe_id = str(self.recipe_id)
            recipe_id = UUID(raw_recipe_id)
        except TypeError, ValueError:
            raise ValueError("Ungültige Rezept-ID")
        try:
            raw_portions = str(self.portions).replace(",", ".")
            float_portions = float(raw_portions)
            if math.isnan(float_portions) or math.isinf(float_portions):
                raise ValueError("Ungültige Anzahl Portionen")
            portions = int(float_portions)
            if float_portions != portions:
                raise ValueError("Ungültige Anzahl Portionen")
        except TypeError, ValueError:
            raise ValueError("Ungültige Anzahl Portionen")
        if portions <= 0:
            raise ValueError("Ungültige Anzahl Portionen")
        object.__setattr__(self, "recipe_id", recipe_id)
        object.__setattr__(self, "portions", portions)
