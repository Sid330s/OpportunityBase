#!/bin/bash

# Set AWS profile if needed (Optional)
# export AWS_PROFILE=your-profile

# Sync the folders from S3 to the current working directory (repo root)
aws s3 cp s3://opbase/ResumeYAMLs/ ./ResumeYAMLs/ --recursive
aws s3 cp s3://opbase/Resumes/ ./Resumes/ --recursive
aws s3 cp s3://opbase/jobs.yml ./jobs.yml

echo "Folders downloaded successfully!"
