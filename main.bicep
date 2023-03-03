// Setting subscription as scope
targetScope = 'subscription'

// Parameters
@description('Name of the API environment')
param environment string

@description('Azure Region where the API should be deployed')
param location string

@description('resource group name')
param resource_group_name string

resource rsg 'Microsoft.Resources/resourceGroups@2022-09-01' = {
  location: location
  name: resource_group_name
  tags: {
    Environment: environment
  }
}
