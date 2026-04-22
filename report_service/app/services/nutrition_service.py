from app.schemas.user_dto import UserCreate, UserResponse


class NutritionService:
    def __init__(self):
        self.users = []
        self.products = []
        self.meals = []
        self._u_counter = 1
        self._p_counter = 1
        self._m_counter = 1

    # Logic for Users
    def create_user(self, data: UserCreate) -> UserResponse:
        user = UserResponse(id=self._u_counter, **data.model_dump())
        self.users.append(user)
        self._u_counter += 1
        return user


# Singleton instance
nutrition_service = NutritionService()