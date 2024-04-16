
import streamlit as st
import openai, os
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI
from openai import AzureOpenAI

import asyncio

################ INITIALISATION ####################
load_dotenv()



def gpt_function(endpoint, api_key, ksb, ksb_desc, extra_instruction=''):
    #     user_content = f"""
    #     Create a Job Description for
    #     Required Skills: {skills}.
    #     Experience: {experience}
    #     Job Role: {job_role}
    # """
    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version='2023-05-15'
    )
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
                                    - The questions should be formulated to assess content provided by an author, considering that they are intended for evaluation purposes.
                                    - Questions are designed to assess users' understanding.
                                    - Questions should typically be phrased as, "Does the content explain this...", "Does the content include...", or "Does the author of the content explain..."
                                    - If the user has added extra instructions, these should be prioritized.

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

    # gpt4_model_for_summarization = st.secrets["AZURE_OPENAI_MODEL"] #os.getenv("AZURE_OPENAI_MODEL")
    response = client.chat.completions.create(
        model="gpt-4-8k-0613",
        messages=conversation
    )
    return response.choices[0].message.content.strip()


async def main():
    if "openai_key" not in st.session_state:
        st.session_state.openai_key = ""

    if "endpoint" not in st.session_state:
        st.session_state.endpoint = ""

    st.header("Generate Binary Statements")

    st.title("A step to Automate KSB binary statements")

    openai_api_key = st.text_input("Enter your Azure OpenAI keys", type="password")
    if openai_api_key:
        st.session_state.openai_key = openai_api_key

    openai_endpoint = st.text_input("Enter your Azure OpenAI endpoint", type="password")
    if openai_endpoint:
        st.session_state.endpoint = openai_endpoint

    description = """
    #### About the App
    ###### This app generates binary statements based on the KSB description provided.
    """
    st.markdown(description, unsafe_allow_html=True)

    # st.sidebar.title("Azure OpenAI API Key")
    # openai_api_key = st.sidebar.text_input("Enter your Azure OpenAI API Key", type="password")

    # if 'openai_client' not in st.session_state:
    #     client = get_openai_client(openai_api_key, openai_endpoint)
    #     st.session_state["openai_client"] = client

    # client = OpenAI(openai_api_key, openai_endpoint)
    # client = get_openai_client(st.session_state.openai_key, st.session_state.endpoint)

    # st.error("Please enter valid Azure OpenAI API key and endpoint")

    input_list = ["KSB", "Enter your KSB Description", "Additional instruction (Optional)"]
    # job_role = st.text_input(input_list[2])
    # experience = st.text_input(input_list[1])

    ksb = st.selectbox(input_list[0], ['Knowledge', 'Skills', 'Behavior'])
    ksb_desc = st.text_input(input_list[1])
    extra_instruction = st.text_area(input_list[2])

    # if not skills:
    #     skills = "None"

    if ksb_desc:
        if st.button("Submit"):
            print("#Abhi ", st.session_state.openai_key, st.session_state.endpoint)
            with st.spinner("Let the magic happen ...."):
                output = gpt_function(st.session_state.endpoint, st.session_state.openai_key, ksb=ksb,
                                      ksb_desc=ksb_desc, extra_instruction=extra_instruction)
                st.markdown(output, unsafe_allow_html=True)


if __name__ == "__main__":
    asyncio.run(main())