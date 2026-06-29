from storage import Storage
db = Storage()
print(f"👥 Пользователей: {len(db.users)}")
for id, user in enumerate(db.users.values(), 1):
    print(f"{id}. {user.login} (ID: {user.user_id})")