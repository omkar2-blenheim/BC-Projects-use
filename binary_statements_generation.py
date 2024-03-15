import streamlit as st
import openai


def get_openai_client(api_key, endpoint):
    openai.api_type = 'azure'
    openai.api_key = api_key
    openai.api_version = '2023-12-01-preview'
    openai.api_base = endpoint
    return openai


def gpt_function(client, ksb, ksb_desc, extra_instruction=''):
#     user_content = f"""
#     Create a Job Description for
#     Required Skills: {skills}.
#     Experience: {experience}
#     Job Role: {job_role}
# """
    user_content = f"""
    KSB: {ksb}
    Description:{ksb_desc}
###
{"Additional instruction:" if extra_instruction else ""}
{extra_instruction}"""

    conversation = [{"role": "system", "content": f"""your job is to generate around 3-7 questions based on the "description" and "KSB" from user.
                                    KSB is Knowledge, Skills and Behavior
                                    Knowledge: Refers to the information and understanding that an individual possesses in a particular subject or domain. It involves facts, concepts, theories, and procedures acquired through learning and experience.
                                    Skills: Represent the ability to perform specific tasks or activities effectively and efficiently. Skills are developed through practice and experience, and they encompass practical know-how, techniques, and competencies.
                                    Behavior: Describes the actions, conduct, and attitudes demonstrated by an individual in various situations. It encompasses how a person interacts with others, makes decisions, and approaches tasks, reflecting their values, attitudes, and personality traits.
                                    
                                    Actions:
                                        - Understand the user's description thoroughly
                                        - Understand the KSB based on above explanation
                                        - Then generate the questions line by line
                                        
                                    Instructions to generate the question:
                                    - The questions has to be questioning considering you are asking it to assess a content which is given by an auther
                                    - Questions going assess users 
                                    - Question always should be asking like "Does the content Explain this...", "Does the content include ..." or "Does the author of the content eplains...."
                                    - If user has added an extra instructions then priorities that
                                    
                                    examples:
                                    
                                    1.  "KSB": Knowledge
                                        "Description" : "Explain the principles and process of setting a budget to produce content."
                                         "generated questions":
                                            Does the content EXPLAIN how the organisation sets a budget?
                                            Does the content EXPLAIN how the organisation sets budgets? i.e for each campaign or an overall yearly budget
                                            Does the content EXPLAIN what the principles of a budget are?
                                            Does the content EXPLAIN why you have a budget?
                                            Does the content EXPLAIN what the budget helps to achieve? 
                                            Does the content EXPLAIN what could happen if there were no budget/s? 
                                            Does the content INCLUDE EVIDENCE of a workplace budget?
                                        
                                    2.  "KSB": SKill
                                        "Description" : "Describe and show developing and maintaining effective working relationships with clients, colleagues and suppliers, establishing and using professional contacts."
                                        "Generated questions":
                                        Does the author SHOW evidence of emails, messages on Teams and other similar communication tools. 
                                        Does the content SHOW strong narrative around these examples in how this helps to develop and maintain good working relationships.
                                        Does the content EXPLAIN ALL examples shown. 
                                        Does the content of all examples shown EXPLAIN clients, colleagues and suppliers.
                                        Does the author of the content SHOW evidence of working together as a team.
                                        Does the content EXPLAIN ALL examples shown. 
                                        Does the content SHOW evidence of an example linked to colleagues and at least one example linked to someone other than a colleague.
                                        Does the content include an EXAMPLE of how can you show ways of maintaining positive working relationships with your customers or clients? 
                                    
                                    
                                    """},
                    {"role": "user", "content": f"{user_content}"}]

    response = client.ChatCompletion.create(
        messages=conversation,
        engine="gpt-35-turbo",
        temperature=0
    )
    text_response = response.choices[0].message.content

    return text_response


def main():
    st.title("A step to Automate KSB binary statements")
    description = """
    #### About the App
    ###### This app generates binary statements based on the KSB description provided.
    """
    st.markdown(description, unsafe_allow_html=True)

    st.sidebar.title("Azure OpenAI API Key")
    openai_api_key = st.sidebar.text_input("Enter your Azure OpenAI API Key", type="password")
    openai_endpoint = 'https://bc-api-management-uksouth.azure-api.net'
    client = get_openai_client(openai_api_key, openai_endpoint)

    input_list = ["KSB", "Enter your KSB Description", "Additional instruction (Optional)"]

    # job_role = st.text_input(input_list[2])
    # experience = st.text_input(input_list[1])

    ksb = st.selectbox(input_list[0], ['Knowledge', 'Skills', 'Behavior'])
    ksb_desc = st.text_input(input_list[1])
    extra_instruction = st.text_area(input_list[2])

    # if not skills:
    #     skills = "None"

    if ksb_desc and openai_api_key and openai_endpoint:
        if st.button("Submit"):
            with st.spinner("Let the magic happen ...."):
                output = gpt_function(client, ksb=ksb, ksb_desc=ksb_desc, extra_instruction=extra_instruction)
                st.markdown(output, unsafe_allow_html=True)


if __name__ == "__main__":
    main()