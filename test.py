from oauth2client.service_account import ServiceAccountCredentials
from businesscommunications.businesscommunications_v1_client import (
    BusinesscommunicationsV1
)
from businesscommunications.businesscommunications_v1_messages import (
    BusinesscommunicationsBrandsAgentsGetRequest,
    BusinesscommunicationsBrandsAgentsPatchRequest,
    CustomSurveyConfig,
    SurveyConfig,
    SurveyQuestion,
    SurveyResponse,
)


SCOPES = ['https://www.googleapis.com/auth/businesscommunications']
SERVICE_ACCOUNT_FILE = 'PATH_TO_SERVICE_ACCOUNT_KEY'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

client = BusinesscommunicationsV1(credentials=credentials)

agents_service = BusinesscommunicationsV1.BrandsAgentsService(client)

agent = agents_service.Get(BusinesscommunicationsBrandsAgentsGetRequest(
        name=agent_name
    ))

survey_config = SurveyConfig(
        customSurveys=SurveyConfig.CustomSurveysValue(
            additionalProperties=[SurveyConfig.CustomSurveysValue.AdditionalProperty(
                key='en',
                value=CustomSurveyConfig(customQuestions=[
                    SurveyQuestion(
                        name="Question Name 1",
                        questionContent="Does a custom question yield better survey results?",
                        questionType=SurveyQuestion.QuestionTypeValueValuesEnum.PARTNER_CUSTOM_QUESTION,
                        responseOptions=[
                            SurveyResponse(
                                content="👍",
                                postbackData="yes"
                            ),
                            SurveyResponse(
                                content="👎",
                                postbackData="no"
                            ),
                        ]),
                    SurveyQuestion(
                        name="Question Name 2",
                        questionContent="How would you rate this agent?",
                        questionType=SurveyQuestion.QuestionTypeValueValuesEnum.PARTNER_CUSTOM_QUESTION,
                        responseOptions=[
                            SurveyResponse(
                                content="⭐️",
                                postbackData="1-star"
                            ),
                            SurveyResponse(
                                content="⭐️⭐️",
                                postbackData="2-star"
                            ),
                            SurveyResponse(
                                content="⭐️⭐️⭐️",
                                postbackData="3-star"
                            ),
                            SurveyResponse(
                                content="⭐️⭐️⭐️⭐️",
                                postbackData="4-star"
                            ),
                            SurveyResponse(
                                content="⭐️⭐️⭐️⭐️⭐️",
                                postbackData="5-star"
                            ),
                        ]),
                    ])
                ),
            ]),
        templateQuestionIds=["GOOGLE_DEFINED_ASSOCIATE_SATISFACTION", "GOOGLE_DEFINED_CUSTOMER_EFFORT_ALTERNATE"]
    )

updated_agent = agents_service.Patch(
    BusinesscommunicationsBrandsAgentsPatchRequest(
        agent=agent,
        name=agent.name,
        updateMask='businessMessagesAgent.surveyConfig'
    )
)

