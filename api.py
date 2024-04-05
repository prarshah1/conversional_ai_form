import os
import psycopg2
import streamlit as st
from langchain.chains import ConversationChain, create_tagging_chain_pydantic
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.memory import MongoDBChatMessageHistory
from langchain.prompts.prompt import PromptTemplate
from streamlit_chat import message
from dotenv import load_dotenv
from dashboard_info import DashboardInfo

load_dotenv()
# setup up mongodb client

# setup openai
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

llm = None

_DEFAULT_TEMPLATE = """
You are an interactive conversational chatbot collecting specs for dashboard creation.
Your goal is to collect user information in a conversational and non-intrusive manner, one piece at a time.
When asking for details, explain why you need them, and be persuasive yet empathetic.
Build rapport by transitioning into small talk when appropriate, but aim to gather data smoothly as the conversation progresses.
If a user hesitates or is unsure, provide reassurance, offer alternatives, and if the user wishes to correct or update their details, be flexible and handle it trustworthily, be polite.
If no information is needed, thank the user and tell them their dashboard is ready.

Conversation Workflow:
1. Explain the need for collecting information.
2. Ask for one piece of information from the 'ask_for' list.
3. If the user provides the information, confirm it empathetically and move to the next piece when appropriate.
4. If the user hesitates, offer reassurance, and smoothly transition into small talk or other topics.
5. When the 'ask_for' list is empty, thank the user and offer further assistance.
6. Remember not to use greetings or list questions; keep it conversational.
7. Don't revel information to the user unless they ask for it.
8. Strictly don't use AI: and bot: kind of prefix in output.

Previous conversation:
{history}
Recent user input:
{input}
Information to ask for (do not ask as a list):
### ask_for list: ask_for_list
Available information of user: avl_info_list

"""
if "user_information" not in st.session_state:
    st.session_state['dashboard_specs'] = DashboardInfo()


def update_customer_table(session_id: object, data: object) -> object:
    st.session_state['dashboard_specs'] = st.session_state['dashboard_specs'].add(data)


# form_chain = None


# Define a function to check which fields are empty
def check_what_is_empty(user_personal_details: object) -> object:
    ask_for = []
    for field, value in user_personal_details.dict().items():
        if value in [None, "", 0]:
            ask_for.append(field)
    return ask_for


# Define a function to update the non-empty details
def add_non_empty_details(current_details: DashboardInfo, new_details: DashboardInfo) -> object:
    non_empty_details = {k: v for k, v in new_details.dict().items() if v not in [None, ""]}
    updated_details = current_details.copy(update=non_empty_details)
    return updated_details


def conversation_chat(input: object, session_id: object, llm=llm) -> object:
    # if session_id:
    #     existing_info_from_db = check_details_from_db(session_id)
    #     existing_info_of_user = DashboardInfo(**existing_info_from_db)
    # else:
    existing_info_of_user = DashboardInfo()

    # message_history = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    form_chain = create_tagging_chain_pydantic(DashboardInfo, llm)
    extractions = form_chain.run(input)  # Extract information using your NER chain
    existing_info_of_user = add_non_empty_details(existing_info_of_user, extractions)
    existing_info_of_str = ", ".join(f"{k}={v}" for k, v in existing_info_of_user.dict().items() if v not in [None, ""])
    ask_for = check_what_is_empty(existing_info_of_user)
    update_customer_table(session_id, existing_info_of_user.dict())
    memories = ConversationBufferMemory(k=3)

    PROMPT = PromptTemplate(
        input_variables=["history", "input"],
        template=_DEFAULT_TEMPLATE.replace("ask_for_list", f"{ask_for}").replace("avl_info_list",
                                                                                 f"{existing_info_of_str}"),
        )
    conversation = ConversationChain(
        llm=llm,
        verbose=False,
        prompt=PROMPT,
        memory=memories,
    )

    conv = conversation.predict(input=input)
    # message_history.add_user_message(input)
    # message_history.add_ai_message(conv)

    return conv


st.title("LearnTube ChatBot🧑🏽‍")


# add field to sidebar gpt_token and session_id

def initialize_session_state():
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello! Ask me anything about 🤗"]

    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hey! 👋"]

    if 'session_id' not in st.session_state:
        st.session_state['session_id'] = None


def display_chat_history(session_id: object, llm):
    if not session_id:
        st.warning("Please enter a session ID in the sidebar")
        return

    reply_container = st.container()
    container = st.container()
    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_input("Question:", placeholder="Ask about you want to learn", key='input')
            submit_button = st.form_submit_button(label='Send')

        if submit_button and user_input:
            output = conversation_chat(user_input, session_id=session_id, llm=llm)
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)

    if st.session_state['generated']:
        with reply_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="thumbs")
                message(st.session_state["generated"][i], key=str(i), avatar_style="fun-emoji")


def main():
    initialize_session_state()
    with st.sidebar:
        with st.form(key='sidebar_form'):
            session_id = st.text_input("Session ID", value=st.session_state.get('session_id', ''))
            gpt_token = st.text_input("GPT Token", value='')
            submit_button = st.form_submit_button(label='Update')

        if submit_button:
            st.session_state['session_id'] = session_id
            if gpt_token:  # You'd typically not want to store the API key in session_state for security reasons
                os.environ["OPENAI_API_KEY"] = gpt_token

    if gpt_token:
        os.environ["OPENAI_API_KEY"] = gpt_token
        global llm
        llm = ChatOpenAI(temperature=0)
    display_chat_history(st.session_state['session_id'], llm=llm)


if __name__ == "__main__":
    main()
