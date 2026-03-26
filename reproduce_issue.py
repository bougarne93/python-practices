
import sys
import os
sys.path.append(os.getcwd())

# Mock database connection before importing services
from unittest.mock import AsyncMock, patch, MagicMock

# Import components
from app.security.jwt import create_access_token
from app.core.security import get_current_user
import asyncio

async def test():
    # 1. Créer un token comme dans /auth/login
    user_id = 1
    token = create_access_token({"sub": str(user_id)})
    print(f"DEBUG: Token généré: {token}")
    
    # 2. Simuler l'appel à /auth/me qui utilise get_current_user
    credentials = MagicMock()
    credentials.credentials = token
    
    # On mock UserSQLService.get_user pour éviter d'avoir besoin d'une vraie DB
    with patch("app.services.user_sql_service.UserSQLService.get_user", new_callable=AsyncMock) as mock_get_user:
        mock_get_user.return_value = MagicMock(id=user_id, name="Test User")
        
        try:
            user = await get_current_user(credentials)
            print(f"RÉSULTAT: Utilisateur récupéré avec succès: {user.name}")
        except Exception as e:
            print(f"RÉSULTAT: Erreur lors du décodage: {e}")
            if hasattr(e, 'detail'):
                print(f"Détail de l'erreur: {e.detail}")

if __name__ == "__main__":
    asyncio.run(test())
