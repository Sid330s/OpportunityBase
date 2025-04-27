#!/bin/bash

# Set AWS profile if needed (Optional)
# export AWS_PROFILE=your-profile

# Sync the folders from local to S3
aws s3 sync ./ResumeYAMLs/ s3://opbase/ResumeYAMLs/ --recursive
aws s3 sync ./Resumes/ s3://opbase/Resumes/ --recursive

echo "Folders uploaded successfully!"
