new_users = ["realDonaldTrump", "NSAGov", "CIA", "FBI"]
user_file = "\n".join(new_users)
with open("data/twitter_accounts.txt", "a") as f:
    f.write(user_file + "\n")
f.closed
