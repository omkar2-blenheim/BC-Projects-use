import streamlit as st
import openai


def get_openai_client(api_key, endpoint):
    openai.api_type = 'azure'
    openai.api_key = api_key
    openai.api_version = '2023-12-01-preview'
    openai.api_base = endpoint
    return openai


def gpt_function(client, ksb_desc):
#     user_content = f"""
#     Create a Job Description for
#     Required Skills: {skills}.
#     Experience: {experience}
#     Job Role: {job_role}
# """
    user_content = ksb_desc
    conversation = [{"role": "system", "content": """You are a Job Description generate around 3-7 questions based on the description entered by the user
                                    - All generated question has to be precise and each question should relate to the description given
                                    - there is no restriction on number of questions generation it can be between 3 and 7.
                                    
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
    st.title("KSB binary statement generator")
    description = """
    #### About the App
    ###### This app generates binary statements based on the KSB description provided.
    """
    st.markdown(description, unsafe_allow_html=True)

    st.sidebar.title("Azure OpenAI API Key")
    openai_api_key = st.sidebar.text_input("Enter your Azure OpenAI API Key", type="password")
    openai_endpoint = 'https://bc-api-management-uksouth.azure-api.net'
    client = get_openai_client(openai_api_key, openai_endpoint)

    input_list = ["Enter your KSB Description"]

    # job_role = st.text_input(input_list[2])
    # experience = st.text_input(input_list[1])
    ksb_desc = st.text_input(input_list[0])

    # if not skills:
    #     skills = "None"

    if ksb_desc and openai_api_key and openai_endpoint:
        if st.button("Submit"):
            with st.spinner("Let the magic happen ...."):
                output = gpt_function(client, ksb_desc)
                st.markdown(output, unsafe_allow_html=True)


if __name__ == "__main__":
    main()