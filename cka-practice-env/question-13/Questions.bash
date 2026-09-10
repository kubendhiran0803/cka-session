# Question 13
# Create a Pod with multiple containers named multi-container-playground in Namespace default:
# - It should have a volume attached and mounted into each container.
# - Container c1 with image nginx:1-alpine, name of the node should be available as env var MY_NODE_NAME
# - Container c2 with image busybox:1 should write date to date.log in shared volume
# - Container c3 with image busybox:1 should tail -f date.log from shared volume to stdout
