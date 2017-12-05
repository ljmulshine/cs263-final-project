old_users = ["realDonaldTrump", "NSAGov", "CIA", "FBI"]
with open("data/twitter_accounts.txt", "r") as f:
    raw_users = f.readlines()
f.closed
users = []
for raw_user in raw_users:
    users.append(raw_user.strip())

for user in old_users:
    try:
        users.remove(user)
    except:
        pass

user_file = "\n".join(users)
with open("data/twitter_accounts.txt", "w") as f:
    f.write(user_file + "\n")
f.closed
