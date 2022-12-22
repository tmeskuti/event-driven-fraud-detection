# Fraud Detection in GCP
This repository is used to implement an event-based fraud detection system using Infrastructure as Code. The infrastructure is fully serverless and includes the following GCP services:

- BigQuery
- Cloud Build
- Cloud Functions
- Cloud Pub/Sub
- Cloud Run
- Cloud Storage
- Firestore

## Prerequisites
To run the demo, please enable the needed APIs (each of the services listed above). If you don't, Terraform will prompt you to enable them sequentially.

### Steps
- Authenticate with your GCP project using `gcloud auth application-default login`
- Push the image to your Artifact Repository 
  - `gcloud builds submit --tag <YOUR_GCP_REGION>-docker.pkg.dev/<YOUR_GCP_PROJECT_ID>/fraud-detection/event-producer`
- Install the Terraform CLI
- Set `$GCP_CREDENTIALS` and `$GCP_PROJECT_ID` as GitHub Actions secrets

## Running the demo
1. ### Set environment variables
```bash
export TF_VAR_region=<YOUR_GCP_REGION>
export TF_VAR_project_id=<YOUR_GCP_PROJECT_ID>
```
2. ### Change the Terraform state file bucket 
- https://github.com/tmeskuti/event-driven-fraud-detection/blob/bf10748d4620285651d2ed9402315f185de6e5cd/infrastructure/main.tf#L3

3. ### Initialize the Terraform backend
```bash
cd infrastructure
terraform init
```

4. ### Run Terraform
```bash 
terraform apply
```

5. ### Run the application
- Populate the BigQuery dataset with data (most importantly the **venues** and **users** tables)
- Go to the Cloud Run console and use the generated URL to access the **producer** service
- Use the Streamlit UI to produce events

6. ### View the results
- After a certain number of events have been generated, you can check the **fraud** table to see which checkins have been deemed as fraudulent and need further investigation. Furthermore, you may choose to implement an analytics tool such as Looker Studio to produce dashboards and visualize your findings.

### Destroy the infrastructure
```bash 
terraform destroy
```