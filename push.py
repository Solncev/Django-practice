from subprocess import call
message = input("Commit message: ")
call(["git", "add", "."])
call(["git", "commit", "-m %s"]) %(message)
# call(["git", "pull", "origin", "master"])
# call(["git", "push", "origin", "master"])