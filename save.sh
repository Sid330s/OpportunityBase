#!/bin/bash

# Set AWS profile if needed (Optional)
# export AWS_PROFILE=your-profile

# Sync the folders from local to S3
aws s3 cp ./ResumeYAMLs/ s3://opbase/ResumeYAMLs/ --recursive
aws s3 cp ./Resumes/ s3://opbase/Resumes/ --recursive
aws s3 cp ./jobs.yml s3://opbase/jobs.yml

echo "Folders uploaded successfully!"
