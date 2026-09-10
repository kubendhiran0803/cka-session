# Question 4
# Do the following in Namespace default:
# - Create a Pod named ready-if-service-ready of image nginx:1-alpine
# - Configure a LivenessProbe which simply executes command true
# - Configure a ReadinessProbe which checks if the url http://service-am-i-ready:80 is reachable. You can use wget -T2 -O- http://service-am-i-ready:80 for this.
# - Start the Pod and confirm it isn't ready because of the ReadinessProbe.
# Then:
# - Create a second Pod named am-i-ready of image nginx:1-alpine with label id: cross-server-ready
# - The already existing Service service-am-i-ready should now have that second Pod as endpoint.
# - Now the first Pod should be in ready state, check that.
