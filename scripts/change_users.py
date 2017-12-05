new_users = ["naval", "pt", "ManuKumar"]
user_file = "\n".join(new_users)
with open("data/twitter_accounts.txt", "w") as f:
    f.write(user_file + "\n")
f.closed
