import streamlit as st
import openai


def get_openai_client(api_key, endpoint):
    openai.api_type = 'azure'
    openai.api_key = api_key
    openai.api_version = '2023-12-01-preview'
    openai.api_base = endpoint
    return openai


def gpt_function(client, ksb_desc, extra_instruction=''):
#     user_content = f"""
#     Create a Job Description for
#     Required Skills: {skills}.
#     Experience: {experience}
#     Job Role: {job_role}
# """
    user_content = f"""{ksb_desc}\n
###
{"Additional instruction:" if extra_instruction else ""}
{extra_instruction}"""

    conversation = [{"role": "system", "content": f"""your job is to generate around 3-7 questions based on the "description" from user.
    
                                    - The questions has to be questioning considering you are asking it to assess a content which is given by an auther
                                    - Question always should be asking like "Does the content Explain this...", "Does the content include ..." or "Does the author of the content eplains...."
                                    - If user has added an extra instructions then priorities that
                                    
                                    examples:
                                    1.  "description" : "Explain the principles and process of setting a budget to produce content."
                                         "generated questions":
                                            Does the content EXPLAIN how the organisation sets a budget?
                                            Does the content EXPLAIN how the organisation sets budgets? i.e for each campaign or an overall yearly budget
                                            Does the content EXPLAIN what the principles of a budget are?
                                            Does the content EXPLAIN why you have a budget?
                                            Does the content EXPLAIN what the budget helps to achieve? 
                                            Does the content EXPLAIN what could happen if there were no budget/s? 
                                            Does the content INCLUDE EVIDENCE of a workplace budget?
                                        
                                    2. "Description" : "Describe and show developing and maintaining effective working relationships with clients, colleagues and suppliers, establishing and using professional contacts."
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

    input_list = ["Enter your KSB Description", "Additional instruction (Optional)"]

    # job_role = st.text_input(input_list[2])
    # experience = st.text_input(input_list[1])
    ksb_desc = st.text_input(input_list[0])
    extra_instruction = st.text_area(input_list[1])

    # if not skills:
    #     skills = "None"

    if ksb_desc and openai_api_key and openai_endpoint:
        if st.button("Submit"):
            with st.spinner("Let the magic happen ...."):
                output = gpt_function(client, ksb_desc, extra_instruction)
                st.markdown(output, unsafe_allow_html=True)


if __name__ == "__main__":
    main()