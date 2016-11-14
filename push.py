from subprocess import call
message = input("Commit message: ")
call(["git", "add", "."])
call(["git", "commit", "-m %s" %(message)])
call(["git", "pull", "origin", "Sagit"])
call(["git", "push", "origin", "Sagit"])