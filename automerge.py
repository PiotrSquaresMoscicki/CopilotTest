# This script is used by a CI/CD system (such as TeamCity or Jenkins) to merge
# automatically all commits from one stream to another in a Perforce server.
# If a cimmit to a child stream is detected the job will start and will execute
# this script. The script is executed for the workspace create dfom the parent
# stream as this is the only way to submit changes to the parent stream. The
# script will then merge all changes from the child stream to the parent stream
# (including child imports) and submit them to the parent stream (including
# parent imports). Imports are also taken into consideration because each child
# import stream is a child of one of imports in the parent stream. Example
# streams are:
#
# parent:
#   root - //depot/parent
#   parent - none; it's a mainline stream
#   imports:
#     - //depot2/import1
#     - //depot2/import2
#     - //depot3/import3
# child:
#   root - //depot/child
#   parent - //depot/parent
#   imports:
#     - //depot2/import1_child
#     - //depot2/import2_child
#     - //depot3/import3_child
#
# import1_child:
#   root - //depot2/import1_child
#   parent - //depot2/import1
#   imports - none
# import2_child:
#   root - //depot2/import2_child
#   parent - //depot2/import2
#   imports - none
# import3_child:
#   root - //depot3/import3_child
#   parent - //depot3/import3
#   imports - none
#
# The script makes sure to intehrate changelists one by one (not all at once)
# and to submit them one by one (not all at once). Thanks to that we can copy
# the description of the merged commit and paste it to the merge commit
# description. The merge description will also get a prefix contining the
# merged changelist number and the name of the child stream.
#
# After performing "p4 integrate ..." step for each child - parent stream pair
# the script will resolve files using "accept merge" option (p4 resolve -am)
# and submit the changes to the parent stream. If automatic resolve fails the
# script will stop and will not submit any changes - instead it will try to get
# information about how to resolce conflicts from the web server. If there is
# no infoamtaion on the server on how to resolve a conflict the script will
# send a slack message and notify the server about existing conflicts. Then it
# will stop execution (without revrting changes) and will wait for the next run
# of the job. The next run of the job will try to resolve conflicts again. If
# the server will contain the information about existing conflicts the script
# will use this information to resolce conflicts accepting source or target
# files (depending on the information from the server). If the coflict needs a
# manual merge to resolve a conflict it is possible for the user to log in to a
# machine where the job was executed and to resolve the conflict manually.
# After resolving the conflict the user can run the script again to submit the
# changes to the parent stream.

