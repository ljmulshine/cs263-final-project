new_users = ["realDonaldTrump", "NSAGov", "CIA", "FBI"]
user_file = "\n".join(new_users)
with open("data/twitter_accounts2.txt", "w") as f:
    f.write(user_file)
f.closed
print "Updating twitter accounts to check:"
print user_file
