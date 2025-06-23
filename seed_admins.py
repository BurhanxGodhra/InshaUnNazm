import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from datetime import datetime

# MongoDB connection string (replace with your actual password)
MONGODB_URI = "mongodb+srv://nazm-admin:nazm1447@cluster0.wcfqdle.mongodb.net/poetry_platform?retryWrites=true&w=majority"
DB_NAME = "poetry_platform"
COLLECTION_NAME = "users"

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Admin accounts to seed
ADMINS = [
    {"name": "Admin One", "email": "admin1@poetry.com", "password": "Admin123!", "role": "admin"},
    {"name": "Admin Two", "email": "admin2@poetry.com", "password": "Admin123!", "role": "admin"},
    {"name": "Admin Three", "email": "admin3@poetry.com", "password": "Admin123!", "role": "admin"},
    {"name": "Admin Four", "email": "admin4@poetry.com", "password": "Admin123!", "role": "admin"},
    {"name": "Admin Five", "email": "admin5@poetry.com", "password": "Admin123!", "role": "admin"},
]

async def seed_admins():
    try:
        # Connect to MongoDB
        client = AsyncIOMotorClient(MONGODB_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        # Seed admins
        for admin in ADMINS:
            # Check if email exists
            existing_user = await collection.find_one({"email": admin["email"]})
            if existing_user:
                print(f"Admin {admin['email']} already exists, skipping.")
                continue

            # Hash password
            hashed_password = pwd_context.hash(admin["password"])

            # Prepare user document
            user_doc = {
                "name": admin["name"],
                "email": admin["email"],
                "password": hashed_password,
                "role": admin["role"],
                "createdAt": datetime.utcnow()
            }

            # Insert user
            result = await collection.insert_one(user_doc)
            print(f"Inserted admin {admin['email']} with ID {result.inserted_id}")

        # Verify count
        admin_count = await collection.count_documents({"role": "admin"})
        print(f"Total admins in database: {admin_count}")

        # Close client
        client.close()

    except Exception as e:
        print(f"Error seeding admins: {str(e)}")

if __name__ == "__main__":
    asyncio.run(seed_admins())