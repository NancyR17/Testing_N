Subject: Kubernetes CronJob for Automated Log Space Deletion

Problem Addressed
We needed to automate the cleanup of old log files from specific Kubernetes pods to prevent disk space exhaustion. A key challenge was that these logs are inside the pods (not on Persistent Volume Claims - PVCs), meaning a standard CronJob couldn't directly access them for cleanup.

Solution Overview
I've implemented a robust Kubernetes CronJob solution that leverages the following components to effectively manage log disk space:

Custom Docker Image (e.g., d2admcraacr521.azurecr.io/add/phm/earth-log-cleaner:v1.4):

Purpose: A standard Kubernetes CronJob container (like busybox or alpine) does not include the kubectl utility, which is essential for interacting with other pods. This custom image is built to include kubectl and the core log cleaning
script (clean_pod_storage.sh).

Benefit: This allows the CronJob's pod to "reach into" and execute commands within the target application pods.

clean_pod_storage.sh (Shell Script):

Execution: This script runs inside the CronJob's pod.

Functionality: It uses kubectl exec to run a find command within the target application pods (specifically, those identified by the
label app.kubernetes.io/instance=earth-algorithm-execution-client). This find command then identifies and deletes old log files from their internal storage.

RBAC (Role-Based Access Control - ServiceAccount, Role, RoleBinding):

Purpose: To adhere to the principle of least privilege, specific Kubernetes RBAC configurations are set up.
Components:

ServiceAccount (pod-cleaner-sa): Provides an identity for the CronJob pod.

Role (pod-cleaner-role): Defines the precise permissions needed (e.g., list/get/watch on pods to find them, and create on pods/exec to execute commands inside them).

RoleBinding (pod-cleaner-binding): Binds the Service Account to the Role, granting the CronJob pod the necessary permissions securely.
Why this approach was chosen:
No PVCs: Since the target application pods do not utilize PVCs, direct volume mounting or access from a simple CronJob is not feasible. kubectl exec is the only viable method to interact with their internal file systems.

Essential kubectl: The log cleaning logic directly depends on the kubectl command-line tool, which necessitates a custom Docker image to bundle it.

Security: RBAC ensures that the log cleaner CronJob has only the precise permissions required to perform its task and nothing more, enhancing overall cluster security.
This solution represents a one-time development effort to create a robust, self-contained, secure, and automated way to manage log disk space directly within our Kubernetes environment.

Deployment (One-Time Effort per Environment):
Once developed, the deployment to each environment (QA and Production) is a straightforward, one-time set of steps per environment.

For QA and Production environments, the following actions are needed:

1. Container Image Management:
2. 
3. Build the Docker Image: Build the earth-log-cleaner:v1.4 image from the provided Dockerfile.
4. 
5. Push to ACR: Push the built image to our Azure Container Registry (ACR) at d2admcraacr521.azurecr.io/add/phm/earth-log-cleaner:v1.4.
6. 
7. (Note: Ensure the tag used (e.g., v1.4) is consistent and reflects the production-ready version for the respective environment.)
2. Kubernetes RBAC Configuration:
3. 
4. Apply Service Account, Role, and RoleBinding: Apply the pod-cleaner-rbac.yaml manifest to the target namespace in the Kubernetes cluster for the respective environment. This grants the necessary permissions.
5. 
6. Command: kubectl apply -f pod-cleaner-rbac.yaml -n <your-namespace-qa/prod>
3. Kubernetes CronJob Deployment:
4. 
5. Apply the CronJob Definition: Apply the cronjob.yaml manifest, which orchestrates the automated execution of the log cleaning script.
6. 
7. Command: kubectl apply -f cronjob.yaml -n <your-namespace-qa/prod>
8. 
9. (Important: Before applying, verify that the image field within cronjob.yaml correctly references the pushed image tag, and the pod selector label value is set to earth-algorithm-execution-client for that specific environment.)
After these steps are completed, the log cleaning solution will be fully operational in the respective QA and Production environments, requiring no further manual intervention for its ongoing operation.





