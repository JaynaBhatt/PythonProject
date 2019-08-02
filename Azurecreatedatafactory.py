import os
import json
from datetime import datetime
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient

EAST_US2 = "eastus2"
GROUP_NAME = "azure-sample-group"


# Manage resources and resource groups - create, update and delete a resource group,
# deploy a solution into a resource group, export an ARM template. Create, read, update
# and delete a resource
#
# This script expects that the following environment vars are set:
#
# AZURE_TENANT_ID: with your Azure Active Directory tenant id or domain
# AZURE_CLIENT_ID: with your Azure Active Directory Application Client ID
# AZURE_CLIENT_SECRET: with your Azure Active Directory Application Secret
# AZURE_SUBSCRIPTION_ID: with your Azure Subscription Id
#


def run_example():
    """Resource Group management example."""
    #
    # Create the Resource Manager Client with an Application (service principal) token provider
    #
    subscription_id = os.environ.get(
        "AZURE_SUBSCRIPTION_ID", "2ac343d2-308d-442e-bf19-d1e01d5d2459"
    )  # your Azure Subscription Id

    credentials = ServicePrincipalCredentials(
        client_id='0cf22160-8a87-41db-bec0-040f94d56a18',
        secret='=bn.B6Z3R/O]b20?Gb61/1kBhr_5vq0P',
        tenant='524b0e96-35a3-46ef-ade3-a76c1936a890'
    )

    client = ResourceManagementClient(credentials, subscription_id)

    #
    # Managing resource groups
    #
    resource_group_params = {"location": "eastus2"}

    # List Resource Groups
    print("List Resource Groups")
    for item in client.resource_groups.list():
        print_item(item)

    # Create Resource group
    print("Create Resource Group")
    print_item(
        client.resource_groups.create_or_update(
            GROUP_NAME, resource_group_params)
    )

    # Modify the Resource group
    print("Modify Resource Group")
    resource_group_params.update(tags={"hello": "world"})
    print_item(
        client.resource_groups.create_or_update(
            GROUP_NAME, resource_group_params)
    )

    # Create a Key Vault in the Resource Group
    print("Create a Key Vault via a Generic Resource Put")
    key_vault_params = {
        "location": "eastus2",
        "properties": {
            "sku": {"family": "A", "name": "standard"},
            "tenantId": '524b0e96-35a3-46ef-ade3-a76c1936a890',
            "accessPolicies": [],
            "enabledForDeployment": True,
            "enabledForTemplateDeployment": True,
            "enabledForDiskEncryption": True,
        },
    }
    client.resources.create_or_update(
        GROUP_NAME,
        "Microsoft.KeyVault",
        "",
        "vaults",
        # Suffix random string to make vault name unique
        "azureSampleVault" + datetime.utcnow().strftime("-%H%M%S"),
        "2015-06-01",
        key_vault_params,
    )

    # List Resources within the group
    print("List all of the resources within the group")
    for item in client.resources.list_by_resource_group(GROUP_NAME):
        print_item(item)

    # Export the Resource group template
    print("Export Resource Group Template")
    print(
        json.dumps(
            client.resource_groups.export_template(
                GROUP_NAME, ["*"]).template, indent=4
        )
    )
    print("\n\n")

    # Delete Resource group and everything in it
    print("Delete Resource Group")
    delete_async_operation = client.resource_groups.delete(GROUP_NAME)
    delete_async_operation.wait()
    print("\nDeleted: {}".format(GROUP_NAME))


def print_item(group):
    """Print a ResourceGroup instance."""
    print("\tName: {}".format(group.name))
    print("\tId: {}".format(group.id))
    print("\tLocation: {}".format(group.location))
    print("\tTags: {}".format(group.tags))
    print_properties(group.properties)


def print_properties(props):
    """Print a ResourceGroup properties instance."""
    if props and props.provisioning_state:
        print("\tProperties:")
        print("\t\tProvisioning State: {}".format(props.provisioning_state))
    print("\n\n")


if __name__ == "__main__":
    run_example()