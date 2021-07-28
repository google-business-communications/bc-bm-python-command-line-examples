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

'''This sample uses the Business Communications API to list available template
survey questions.
'''

from oauth2client.service_account import ServiceAccountCredentials
from businesscommunications.businesscommunications_v1_client import (
    BusinesscommunicationsV1
)
from businesscommunications.businesscommunications_v1_messages import (
    BusinesscommunicationsSurveyQuestionsListRequest
)

SCOPES = ['https://www.googleapis.com/auth/businesscommunications']
SERVICE_ACCOUNT_FILE = './resources/bc-agent-service-account-credentials.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

client = BusinesscommunicationsV1(credentials=credentials)

survey_questions_service = BusinesscommunicationsV1.SurveyQuestionsService(client)

print(survey_questions_service.List(BusinesscommunicationsSurveyQuestionsListRequest()))
