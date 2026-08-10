I understand, let's create a more detailed and comprehensive Confluence-style documentation for you.

# GitLab Service Account Setup and Token Management

## 1. Prerequisites
To create and manage group-level service accounts in GitLab, your user account must hold the **Owner** role for the top-level group. Additionally, ensure your GitLab plan supports this feature if group-level capabilities are required.

## 2. Creating the Service Account
1. Navigate to the top-level group page in GitLab.
2. Locate and expand the **Settings** menu in the left-hand sidebar.
3. Select **Service accounts** from the expanded list.
4. Click on the **Add new service account** button.
5. Fill in the required name and unique username, then click **Create**.

## 3. Generating the Access Token
1. After the service account is created, locate it in the list and select the option to create a **Personal access token**.
2. Assign the appropriate permissions or scopes required for the integration, and generate the token.

## 4. Distributing and Sharing Across Pipelines
To use this token across different pipelines, store it securely as a CI/CD variable at your top-level group or within the specific projects that need access. This variable can then be called directly in your pipeline configuration files.

## 5. Security Best Practices
* Always grant the minimum required scopes for the access token.
* Rotate the tokens regularly to maintain security.
