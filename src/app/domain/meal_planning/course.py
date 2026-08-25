from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class Course:
    """Represents a Recipe reference within a Menu."""

    recipe_id: UUID
    portions: int = 1

    def __post_init__(self) -> None:
        if self.portions <= 0:
            raise ValueError("INVALID ARGUMENT: Course portions must be positive.")
        if self.recipe_id is None or not isinstance(self.recipe_id, UUID):
            raise ValueError("INVALID ARGUMENT: Course must refer to a valid recipe.")
