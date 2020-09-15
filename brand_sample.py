# Copyright 2020 Google Inc. All rights reserved.

# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''This is the Business Communications Business Messages Python
Command Line Brand Sample. It makes various API calls using the
included Python Business Communications library to create, update,
retrieve, and list brands stored in the Google Business Messages
platform for the configured Cloud Project.'''

import sys
import time
from oauth2client.service_account import ServiceAccountCredentials
from shared_utils import print_header
from businesscommunications.businesscommunications_v1_client import BusinesscommunicationsV1
from businesscommunications.businesscommunications_v1_messages import (
    Brand,
    BusinesscommunicationsBrandsDeleteRequest,
    BusinesscommunicationsBrandsPatchRequest,
    BusinesscommunicationsBrandsGetRequest,
    BusinesscommunicationsBrandsListRequest)

SCOPES = ['https://www.googleapis.com/auth/businesscommunications']
SERVICE_ACCOUNT_FILE = './resources/bc-agent-service-account-credentials.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

client = BusinesscommunicationsV1(credentials=credentials)

brands_service = BusinesscommunicationsV1.BrandsService(client)

def main():
    '''
    Initiates the Brand Sample which makes multiple requests against
    the Business Communications API. The requests this sample
    makes are:
        - Create a brand
        - Gets the brand details
        - Updates the created brand's display name
        - Lists all brands available
        - Delete the created brand
    '''
    should_delete_brand = True

    # Check arguments, if NO-DELETE is passed in, the brand will not be deleted
    if len(sys.argv) == 2 and sys.argv[1] == 'NO-DELETE':
        should_delete_brand = False

    print_header('Create Brand')
    new_brand = create_brand()

    time.sleep(5)

    print_header('Get Brand Details')
    brand = get_brand(new_brand.name)

    time.sleep(3)

    print_header('Updating Brand')
    update_brand(brand, 'New Test Brand Name')

    time.sleep(3)

    print_header('List Brands')
    list_brands()

    if should_delete_brand:
        time.sleep(3)

        print_header('Deleting brand')
        delete_brand(new_brand.name)

def create_brand():
    '''
    Creates a brand with the name 'Test Brand'.

    Returns:
        brand (Brand): The brand object that was created.
    '''
    brand = brands_service.Create(Brand(displayName='Test Brand'))
    print(brand)
    return brand

def update_brand(brand, display_name):
    '''
    Updates the passed in brand object with a new display name.

    Args:
        brand (Brand): The brand to be updated.
        display_name (str): The new display name.

    Returns:
        updated_brand (Brand): The updated brand object.
    '''
    brand.displayName = display_name
    updated_brand = brands_service.Patch(
        BusinesscommunicationsBrandsPatchRequest(
            brand=brand,
            name=brand.name,
            updateMask='displayName'
        )
    )
    print(updated_brand)
    return updated_brand

def get_brand(brand_name):
    '''
    Based on the brand name, looks up the brand details.

    Args:
        brand_name (str): The unique identifier for the brand in
        'brands/BRAND_ID' format.

    Returns:
        brand (Brand): The matching brand object.
    '''
    brand = brands_service.Get(
        BusinesscommunicationsBrandsGetRequest(name=brand_name)
    )
    print(brand)
    return brand

def list_brands():
    '''
    Lists all brands for the configured Cloud project.

    Returns:
        brands (Brand[]): The list of brands for the configured Cloud project.
    '''
    brands = brands_service.List(
        BusinesscommunicationsBrandsListRequest()
    )
    print(brands)
    return brands

def delete_brand(brand_name):
    '''
    Based on the brand name, deletes the brand. Deleting a brand with
    associated agents will also result in the agents also being deleted.
    Only brands without verified agents can be deleted.

    Args:
        brand_name (str): The unique identifier for the brand in
        'brands/BRAND_ID' format.
    '''
    print(brands_service.Delete(BusinesscommunicationsBrandsDeleteRequest(name=brand_name)))

if __name__ == '__main__':
    main()
