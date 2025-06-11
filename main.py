from models import User
from pydantic import ValidationError

def register_user(data):
    try:
        user = User(**data)
        print("\n✅ Përdoruesi u regjistrua me sukses!")
        print(user.model_dump_json(indent=4))  # kjo është metoda e re në Pydantic v2
    except ValidationError as e:
        print("\n❌ Gabim gjatë regjistrimit:")
        print(e.json(indent=4))  # kjo ende funksionon për ValidationError

if __name__ == "__main__":
    # Shembull i saktë
    user_data = {
        "name": "Arta Dushi",
        "email": "arta@example.com",
        "age": 27
    }
    register_user(user_data)

    # Shembull me gabim
    bad_user_data = {
        "name": "A",
        "email": "not-an-email",
        "age": 15
    }
    register_user(bad_user_data)
