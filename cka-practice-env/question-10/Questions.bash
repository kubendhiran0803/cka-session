# Question 10
# There is a backup Job which needs to be adjusted to use a PVC to store backups.
# Create a StorageClass named local-backup which uses provisioner: rancher.io/local-path and volumeBindingMode: WaitForFirstConsumer.
# The StorageClass should keep a PV retained even if a bound PVC is deleted.
# Adjust the Job at /course/10/backup.yaml to use a PVC which requests 50Mi storage and uses the new StorageClass.
