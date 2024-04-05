import os
import streamlit as st
from langchain.chains import ConversationChain, create_tagging_chain_pydantic
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
from dashboard_info import DashboardInfo
from langchain.prompts import PromptTemplate

load_dotenv()

# setup openai
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
st.set_page_config(page_title='Conversation AI Form')
st.title('🦜🔗 Conversation AI Form')

_FIRST_MESSAGE = "Hello there!, How can I help you today?"
_DEFAULT_TEMPLATE = """
You are an interactive conversational chatbot collecting specs for dashboard creation.
Your goal is to collect information in a conversational and non-intrusive manner, one piece at a time from ask_for list.
Build rapport by transitioning into small talk when appropriate, but aim to gather data smoothly as the conversation progresses.
If a user hesitates or is unsure, provide reassurance, offer alternatives, and if the user wishes to correct or update their details, be flexible and handle it trustworthily, be polite.
Be polite and nice, continue the ongoing conversation using previous conversation.

Conversation Workflow:
1. Ask for only one piece of information from the 'ask_for' list, mostly the first one.
2. If the user provides the information, confirm it empathetically and move to the next piece when appropriate.
3. When the 'ask_for' list is empty, tell to user to feel free to add or alter any existing information and thank them.
4. Remember not to use greetings or list questions; keep it conversational.
5. Don't revel information to the user unless they ask for it.
6. Strictly don't use AI: and bot: kind of prefix in output, dont greet(dont say Hi or hello, or .., continue the previous conversation).

Previous conversation:
{history}

Recent user input:
{input}

Information to ask for (do not ask as a list):
### ask_for list: ask_for_list

"""

if "dashboard_specs" not in st.session_state:
    st.session_state.dashboard_specs = DashboardInfo()

if "llm" not in st.session_state:
    st.session_state.llm = ChatOpenAI(temperature=0)

if "memories" not in st.session_state:
    st.session_state.memories = ConversationBufferMemory(k=5)

if "ask_for" not in st.session_state:
    st.session_state.ask_for = list(st.session_state.dashboard_specs.__fields__.keys())

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": _FIRST_MESSAGE}
    ]

if "chain" not in st.session_state:
    st.session_state.chain = create_tagging_chain_pydantic(DashboardInfo, st.session_state.llm)

def check_what_is_empty():
    ask_for = []
    # Check if fields are empty
    for field, value in st.session_state.dashboard_specs.dict().items():
        if value in [None, "", 0]:  # You can add other 'empty' conditions as per your requirements
            print(f"Field '{field}' is empty.")
            ask_for.append(f'{field}')
    return ask_for


def add_non_empty_details(new_details: DashboardInfo):
    non_empty_details = {k: v for k, v in new_details.dict().items() if v not in [None, ""]}
    for field in non_empty_details.keys():
        new_field_value = eval(f"new_details.{field}")
        existing_field_value = eval(f"st.session_state.dashboard_specs.{field}")
        if new_field_value is not None:
            if existing_field_value is None:
                exec(f"st.session_state.dashboard_specs.{field} = new_details.{field}")
            elif existing_field_value != new_field_value:
                exec(f"""st.session_state.dashboard_specs.{field} = st.session_state.dashboard_specs.{field} + ", (and) " + new_details.{field}""")
    return


def filter_response():
    res = st.session_state.chain.run(str(st.session_state.messages[:-2]))
    add_non_empty_details(res)
    st.write("\t\t\t\tLogs: RES " + str(st.session_state.dashboard_specs))
    ask_for = check_what_is_empty()
    return ask_for

def ask_for_info(ask_for=list(st.session_state.dashboard_specs.__fields__.keys()), input=""):
    global _DEFAULT_TEMPLATE
    PROMPT = PromptTemplate(
        input_variables=["history", "input"],
        template=_DEFAULT_TEMPLATE.replace("ask_for_list", str(ask_for)),
    )
    info_gathering_chain = ConversationChain(
        llm=st.session_state.llm,
        verbose=True,
        prompt=PROMPT,
        memory=st.session_state.memories,
    )
    ai_chat = info_gathering_chain.run(input=input)
    return ai_chat

def write_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

def write_message(role, content):
    with st.chat_message(role):
        st.write(f"{content}")


def main():
    if user_input := st.chat_input("Say Something..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        st.session_state.ask_for = filter_response()
        bot_question = ask_for_info(ask_for=st.session_state.ask_for,
                                    input=str(user_input))
        st.session_state.messages.append({"role": "assistant", "content": bot_question})
        write_message("assistant", bot_question)


print("Starting ...")
write_messages()
main()

