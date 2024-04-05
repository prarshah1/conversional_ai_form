
# Chatbot Conversational Form
Chatbot Conversational Form is a demo project that simplifies creating interactive forms using a chatbot-style interface for tasks like surveys, questionnaires, and feedback forms.

## Features
- Collect User Information: The chatbot gathers user information in a natural and non-intrusive manner. It explains why it needs specific details from a predefined list.

- Empathetic Explanation: The chatbot kindly explains why it requests information, creating a user-friendly experience.

- Rapport Building: The chatbot engages in small talk to build rapport with users, maintaining a friendly atmosphere.

- Handling User Hesitation: The chatbot provides reassurance and alternatives if users hesitate, making corrections easy.

- Thankful and Supportive: When the task is complete, the chatbot expresses gratitude and offers further assistance.

- Conversation Workflow: The chatbot follows a clear and engaging conversation structure, avoiding list questions.

- Privacy and User-Centric: The chatbot prioritizes user comfort and data privacy.



## Tech Functionality
Used langchain's ConversationChain for chatbot and create_tagging_chain_pydantic for extract and validation of user input.


## Installation

To get started with Chatbot Conversational Form, you'll need Python 3.7+ installed. You can install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

Run the main script to start the application:
```bash
streamlit run api_1.py 
```

Provide gpt_token(OPENAI_API_KEY) in streamlit secrets. 


## Enhancement
- Improve dashboard requirements
- Introduce llm firewall to only talk topical questions and add security rails. 
