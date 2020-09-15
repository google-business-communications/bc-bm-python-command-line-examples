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
Command Line Agent Sample. It makes various API calls using the
included Python Business Communications library to create, update,
retrieve, and list agents stored in the Google Business Messages
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
    Agent,
    BotRepresentative,
    BusinessMessagesAgent,
    BusinessMessagesEntryPointConfig,
    BusinesscommunicationsBrandsAgentsCreateRequest,
    BusinesscommunicationsBrandsAgentsDeleteRequest,
    BusinesscommunicationsBrandsAgentsGetRequest,
    BusinesscommunicationsBrandsAgentsListRequest,
    BusinesscommunicationsBrandsAgentsPatchRequest,
    ConversationStarters,
    ConversationalSetting,
    Hours,
    HumanRepresentative,
    MessagingAvailability,
    OfflineMessage,
    OpenUrlAction,
    Phone,
    PrivacyPolicy,
    SuggestedAction,
    SuggestedReply,
    Suggestion,
    SupportedAgentInteraction,
    TimeOfDay,
    WelcomeMessage
)

SCOPES = ['https://www.googleapis.com/auth/businesscommunications']
SERVICE_ACCOUNT_FILE = './resources/bc-agent-service-account-credentials.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

client = BusinesscommunicationsV1(credentials=credentials)

agents_service = BusinesscommunicationsV1.BrandsAgentsService(client)

def main():
    '''
    Initiates the Agent Sample that makes multiple requests against
    the Business Communications API. The requests this sample
    makes are:
        - Creates a test agent
        - Gets an agent
        - Updates the agent's display name
        - Updates the agent's logo
        - Updates the agent's welcome message
        - Updates the available hours for an agent
        - Lists agents for a brand
        - Delete the created agent
    '''

    if (len(sys.argv) < 2 or re.search('brands/\\S+', sys.argv[1]) is None):
        print('Usage: <BRAND_NAME>')
        return

    brand_name = sys.argv[1]

    should_delete_agent = True

    # Check arguments, if NO-DELETE is passed in, the agent will not be deleted
    if len(sys.argv) == 3 and sys.argv[2] == 'NO-DELETE':
        should_delete_agent = False

    print('Agent script for brand - ' + brand_name)

    print_header('Create Agent')
    new_agent = create_agent(brand_name)

    time.sleep(3)

    print_header('Get Agent Details')
    agent = get_agent(new_agent.name)

    time.sleep(3)

    print_header('Updating Agent Display Name')
    updated_agent = update_agent_display_name(agent, 'Newly Edited Agent Test')

    time.sleep(3)

    print_header('Updating Agent Logo URL')
    new_logo_url = 'https://developers.google.com/business-communications/images/logo-guidelines/do-logo-alt.png'
    updated_agent = update_agent_logo(agent, new_logo_url)

    time.sleep(3)

    print_header('Updating Agent Welcome Message')
    conversational_settings = updated_agent.businessMessagesAgent.conversationalSettings
    updated_welcome_message = WelcomeMessage(text='The updated welcome message!')
    conversational_settings.additionalProperties[0].value.welcomeMessage = updated_welcome_message
    updated_agent = update_conversational_settings(agent, conversational_settings)

    time.sleep(3)

    print_header('Updating Agent Primary Interaction Available Hours')
    existing_hours = updated_agent.businessMessagesAgent.primaryAgentInteraction.botRepresentative.botMessagingAvailability.hours
    existing_hours[0].startTime = TimeOfDay(hours=8, minutes=0)
    supported_agent_interaction = updated_agent.businessMessagesAgent.primaryAgentInteraction
    supported_agent_interaction.botRepresentative.botMessagingAvailability.hours = existing_hours
    update_primary_interaction(updated_agent, supported_agent_interaction)

    time.sleep(3)

    print_header('List Agents')
    list_agents(brand_name)

    if should_delete_agent:
        time.sleep(3)

        print_header('Deleting Agent');
        delete_agent(agent.name)

def create_agent(brand_name):
    '''
    Creates an agent with the Business Communications API.

    Args:
        brand_name (str): The brand to be associated with the agent.

    Returns:
        agent (Agent): The newly created agent object.
    '''

    hours = [
        Hours(
            startDay=Hours.StartDayValueValuesEnum.MONDAY,
            startTime=TimeOfDay(hours=9, minutes=0),
            endDay=Hours.EndDayValueValuesEnum.FRIDAY,
            endTime=TimeOfDay(hours=17, minutes=0),
            timeZone='America/Los_Angeles'
        )
    ]

    additional_agent_interactions = [
        SupportedAgentInteraction(
            interactionType=SupportedAgentInteraction.InteractionTypeValueValuesEnum.HUMAN,
            humanRepresentative=HumanRepresentative(
                humanMessagingAvailability=MessagingAvailability(hours=hours)
            )
        )
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
        offlineMessage=OfflineMessage(text='We are currently offline, please leave a message and we will get back to you as soon as possible.'),
        conversationStarters=conversation_starters
    )

    additional_property = BusinessMessagesAgent.ConversationalSettingsValue.AdditionalProperty(
        key='en',
        value=conversational_settings
    )

    conversational_settings_value = BusinessMessagesAgent.ConversationalSettingsValue(
        additionalProperties=[additional_property]
    )

    entry_points = [BusinessMessagesEntryPointConfig(
        allowedEntryPoint=BusinessMessagesEntryPointConfig.AllowedEntryPointValueValuesEnum.LOCATION
    )]

    agent = Agent(
        displayName='Test Agent',
        businessMessagesAgent=BusinessMessagesAgent(
            defaultLocale='en',
            customAgentId='My custom agent ID', # Optional
            phone=Phone(number='+12223334444'), # Optional
            logoUrl='https://storage.googleapis.com/sample-logos/google-logo.png',
            primaryAgentInteraction=SupportedAgentInteraction(
                interactionType=SupportedAgentInteraction.InteractionTypeValueValuesEnum.BOT,
                botRepresentative=BotRepresentative(
                    botMessagingAvailability=MessagingAvailability(hours=hours)
                )
            ),
            additionalAgentInteractions=additional_agent_interactions,
            conversationalSettings=conversational_settings_value,
            entryPointConfigs=entry_points
        )
    )

    new_agent = agents_service.Create(
        BusinesscommunicationsBrandsAgentsCreateRequest(
            agent=agent,
            parent=brand_name
        )
    )
    print(new_agent)
    return new_agent

def update_agent_display_name(agent, display_name):
    '''
    Updates the agent's display name.

    Args:
        agent (Agent): The agent that needs to be updated.
        display_name (str): The new agent agent display name.

    Returns:
        updated_agent (Agent): The updated agent object.
    '''
    agent.displayName = display_name
    updated_agent = update_agent(agent, 'displayName')
    return updated_agent

def update_agent_logo(agent, logo_url):
    '''
    Updates the agent logo URL.

    Args:
        agent (Agent): The agent that needs to be updated.
        logo_url (str): The new agent agent logo URL.

    Returns:
        updated_agent (Agent): The updated agent object.
    '''
    agent.businessMessagesAgent.logoUrl = logo_url
    updated_agent = update_agent(agent, 'businessMessagesAgent.logoUrl')
    return updated_agent

def update_conversational_settings(agent, conversational_settings_value):
    '''
    Update the agent's conversational settings.

    Args:
        agent (Agent): The agent that needs to be updated.
        conversational_settings_value (ConversationalSettingsValue): The new
            conversational settings value.

    Returns:
        updated_agent (Agent): The updated agent object.
    '''

    agent.businessMessagesAgent.conversationalSettings = conversational_settings_value
    updated_agent = update_agent(agent, 'businessMessagesAgent.conversationalSettings.en')
    return updated_agent


def update_primary_interaction(agent, supported_agent_interaction):
    '''
    Updates the agent primary agent interaction.

    Args:
        agent (Agent): The agent that needs to be updated.
        supported_agent_interaction (PrimaryAgentInteraction): The new agent
            interaction for the primary interaction.

    Returns:
        updated_agent (Agent): The updated agent object.
    '''

    agent.businessMessagesAgent.primaryAgentInteraction = supported_agent_interaction
    updated_agent = update_agent(agent, 'businessMessagesAgent.primaryAgentInteraction')
    return updated_agent

def update_agent(agent, update_mask):
    '''
    Updates the saved agent with the passed in agent object for
    the fields specified in the update mask.

    Args:
        agent (Agent): The agent that needs to be updated.
        update_mask (str): A comma-separated list of fully qualified
                names of fields that are to be included in the update.

    Returns:
        updated_agent (Agent): The updated agent object.
    '''
    updated_agent = agents_service.Patch(
        BusinesscommunicationsBrandsAgentsPatchRequest(
            agent=agent,
            name=agent.name,
            updateMask=update_mask
        )
    )
    print(updated_agent)
    return updated_agent


def get_agent(agent_name):
    '''
    Based on the agent name, looks up the agent details.

    Args:
        agent_name (str): The unique identifier for the in
            'brands/BRAND_ID/agents/AGENT_ID' format.

    Returns:
        agent (Agent): The matching agent object.

    '''

    agent = agents_service.Get(BusinesscommunicationsBrandsAgentsGetRequest(
        name=agent_name
    ))
    print(agent)
    return agent

def list_agents(brand_name):
    '''
    Lists all agents for the given brand.

    Args:
        brand_name (str): The unique identifier for
            the brand in 'brands/BRAND_ID' format.

    Returns:
        agents (Agent[]): A list of the agents for the given brand.
    '''
    agents = agents_service.List(BusinesscommunicationsBrandsAgentsListRequest(
        parent=brand_name
    ))
    print(agents)
    return agents

def delete_agent(agent_name):
    '''
    Based on the agent name, deletes the agent. Only a non-verified agent can be deleted.

    Args:
        agent_name (str): The unique identifier for the in
        'brands/BRAND_ID/agents/AGENT_ID' format.
    '''
    print(agents_service.Delete(BusinesscommunicationsBrandsAgentsDeleteRequest(name=agent_name)))

if __name__ == '__main__':
    main()
