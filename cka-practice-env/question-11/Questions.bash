# Question 11
# Create Namespace secret and implement the following in it:
# - Create Pod secret-pod with image busybox:1. kept running by sleep 1d
# - Create the existing Secret /course/11/secret1.yaml and mount it read-only into the Pod at /tmp/secret1
# - Create a new Secret called secret2 which should contain user=user1 and pass=1234. These entries should be available inside the Pod as env vars APP_USER and APP_PASS
