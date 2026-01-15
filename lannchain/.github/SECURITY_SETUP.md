# GitHub Actions Security Setup

## Required Secrets

To run the CI/CD pipeline successfully, you need to configure the following secrets in your GitHub repository:

1. **ALIBABA_REGISTRY_USERNAME**
   - Your Alibaba Cloud Container Registry username
   - Typically: `liudenny527`

2. **ALIBABA_REGISTRY_PASSWORD** 
   - Your Alibaba Cloud Container Registry password or access token
   - Used for authentication when pushing/pulling images

## How to Configure Secrets

1. Navigate to your GitHub repository
2. Go to **Settings** tab
3. Click on **Secrets and variables** in the left sidebar
4. Select **Actions** 
5. Click **New repository secret** 
6. Add each secret with the exact names mentioned above

## Pipeline Permissions

The workflow includes the following permissions:
- `contents: read` - To read repository contents
- `packages: write` - To push Docker images to the registry  
- `security-events: write` - To upload security scan results

## Troubleshooting

If you encounter permission errors:
1. Verify that the secrets are correctly configured
2. Ensure your GitHub account has appropriate permissions to manage secrets
3. Check that the Alibaba Cloud registry credentials are valid