from app.models.user import User, UserUpdate

# Ce service représente la logique métier (business logic).
# Il gère les utilisateurs indépendamment de l'API.
class UserService:

    # "Fake database" en mémoire
    users_db = {}

    @classmethod
    def create_user(cls, user: User):
        """
        Ajoute l'utilisateur dans la base (en mémoire)
        """
        cls.users_db[user.id] = user
        return user

    @classmethod
    def get_user(cls, user_id: int):
        """
        Récupère un utilisateur par ID.
        Retourne None si l'utilisateur n'existe pas.
        """
        return cls.users_db.get(user_id)

    @classmethod
    def get_all_users(cls):
        return list(cls.users_db.values())

    @classmethod
    def update_user(cls, user_id: int, data: UserUpdate):
        user = cls.get_user(user_id)

        if not user:
            return None

        updated_data = user.model_copy(update=data.model_dump(exclude_unset=True))

        cls.users_db[user_id] = updated_data
        return updated_data

    @classmethod
    def delete_user(cls, user_id: int):
        return cls.users_db.pop(user_id, None)
