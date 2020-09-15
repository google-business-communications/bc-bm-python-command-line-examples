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
Command Line location Sample. It makes various API calls using the
included Python Business Communications library to create, update,
retrieve, and list locations stored in the Google Business Messages
platform for the configured Cloud Project.'''

import re
import sys
import time
from oauth2client.service_account import ServiceAccountCredentials
from shared_utils import print_header
from businesscommunications.businesscommunications_v1_client import (
    BusinesscommunicationsV1
)
from businesscommunications.businesscommunications_v1_messages import (
    BusinesscommunicationsBrandsLocationsCreateRequest,
    BusinesscommunicationsBrandsLocationsDeleteRequest,
    BusinesscommunicationsBrandsLocationsGetRequest,
    BusinesscommunicationsBrandsLocationsListRequest,
    BusinesscommunicationsBrandsLocationsPatchRequest,
    ConversationStarters,
    ConversationalSetting,
    Location,
    LocationEntryPointConfig,
    OfflineMessage,
    OpenUrlAction,
    PrivacyPolicy,
    SuggestedAction,
    SuggestedReply,
    Suggestion,
    WelcomeMessage
)

SCOPES = ['https://www.googleapis.com/auth/businesscommunications']
SERVICE_ACCOUNT_FILE = './resources/bc-agent-service-account-credentials.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

client = BusinesscommunicationsV1(credentials=credentials)

locations_service = BusinesscommunicationsV1.BrandsLocationsService(client)

def main():
    '''
    Initiates the Location Sample which makes multiple requests against
    the Business Communications API. The requests this sample
    makes are:
        - Create a location
        - Gets a location
        - Updates a location
        - Lists locations for a brand
        - Delete the created location
    '''
    if (len(sys.argv) != 2 or re.search('brands/\\S+/agents/\\S+', sys.argv[1]) is None):
        print('Usage: <AGENT_NAME>')
        return

    agent_name = sys.argv[1]
    brand_name = agent_name[:agent_name.index('/agents/')]

    print_header('Location script for agent - ' + agent_name)

    print_header('Create Location')
    new_location = create_location(brand_name, agent_name)

    time.sleep(3)

    print_header('Get Location Details')
    location = get_location(new_location.name)

    time.sleep(3)

    # update_location will modify the agent_name associated with the location
    # NOTE: This call will fail unless the agent_name parameter is a valid value
    print_header('Updating location')
    update_location(location, '/brands/BRAND_ID/agents/AGENT_ID')

    time.sleep(3)

    print_header('List locations')
    list_locations(brand_name)

    time.sleep(3)

    print_header('Deleting location')
    delete_location(new_location.name)

def create_location(brand_name, agent_name):
    '''
    Creates a location associated with the given brand and agent.

    Args:
        brand_name (str): The brand name that this location belongs to in brands/BRAND_ID format.
        agent_name (str): The agent name to associate with this location in
            'brands/BRAND_ID/agents/AGENT_ID' format.

    Returns:
        location (Location): The newly created location object.
    '''

    # Using Googleplex for placeId sample.
    place_id = 'ChIJj61dQgK6j4AR4GeTYWZsKWw'

    location_entry_point_configs = [
        LocationEntryPointConfig(
            allowedEntryPoint=LocationEntryPointConfig.AllowedEntryPointValueValuesEnum.PLACESHEET
        ),
        LocationEntryPointConfig(
            allowedEntryPoint=LocationEntryPointConfig.AllowedEntryPointValueValuesEnum.MAPS_TACTILE
        ),
    ]

    conversation_starters = [
        ConversationStarters(
            suggestion=Suggestion(
                reply=SuggestedReply(text='Chip #1', postbackData='chip_1')
            )
        ),
        ConversationStarters(
            suggestion=Suggestion(
                reply=SuggestedReply(text='Chip #2', postbackData='chip_2')
            )
        ),
        ConversationStarters(
            suggestion=Suggestion(
                reply=SuggestedReply(text='Chip #3', postbackData='chip_3')
            )
        ),
        ConversationStarters(
            suggestion=Suggestion(
                reply=SuggestedReply(text='Chip #4', postbackData='chip_4')
            )
        ),
        ConversationStarters(
            suggestion=Suggestion(
                action=SuggestedAction(
                    text='Chip #5',
                    postbackData='chip_5',
                    openUrlAction=OpenUrlAction(url='https://www.google.com')
                )
            )
        ),
    ]

    conversational_settings = ConversationalSetting(
        privacyPolicy=PrivacyPolicy(url='https://www.company.com/privacy'),
        welcomeMessage=WelcomeMessage(text='Welcome! How can I help?'),
        offlineMessage=OfflineMessage(text='This location is currently offline, please leave a message and we will get back to you as soon as possible.'),
        conversationStarters=conversation_starters
    )

    additional_property = Location.ConversationalSettingsValue.AdditionalProperty(
        key='en',
        value=conversational_settings
    )

    conversational_settings_value = Location.ConversationalSettingsValue(
        additionalProperties=[additional_property]
    )

    location = locations_service.Create(BusinesscommunicationsBrandsLocationsCreateRequest(
        location=Location(
            agent=agent_name,
            placeId=place_id,
            conversationalSettings=conversational_settings_value,
            locationEntryPointConfigs=location_entry_point_configs
        ),
        parent=brand_name
    ))
    print(location)
    return location

def get_location(location_name):
    '''
    Based on the location name, looks up the location details.

    Args:
        location_name (str): The unique identifier for the location in
        'locations/location_ID' format.

    Returns:
        location (Location): The matching location object.
    '''
    location = locations_service.Get(
        BusinesscommunicationsBrandsLocationsGetRequest(name=location_name)
    )
    print(location)
    return location

def update_location(location, agent_name):
    '''
    Updates the agent associated with the passed in location.

    Args:
        location (Location):The location that needs to be updated.
        agent_name (str): The new agent to associate with the location.

    Returns:
        location (Location): The updated location object.
    '''
    location.agent = agent_name
    updated_location = locations_service.Patch(
        BusinesscommunicationsBrandsLocationsPatchRequest(
            location=location,
            name=location.name,
            updateMask='agent'
        )
    )
    print(updated_location)
    return updated_location


def list_locations(brand_name):
    '''
    Lists all locations for given brand.
    Args:
        brand_name (str): The unique identifier for the brand.

    Returns:
        locations (Locations[]) The list of locations associated with the brand
    '''
    locations = locations_service.List(
        BusinesscommunicationsBrandsLocationsListRequest(
            parent=brand_name
        )
    )
    print(locations)
    return locations

def delete_location(location_name):
    '''
    Based on the location name, deletes the location. Only a non-verified location can be deleted.

    Args:
        location_name (str): The unique identifier for the location in
        'locations/location_ID' format.
    '''
    print(locations_service.Delete(BusinesscommunicationsBrandsLocationsDeleteRequest(name=location_name)))

if __name__ == '__main__':
    main()
