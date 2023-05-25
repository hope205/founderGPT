import os
import streamlit as st
from streamlit_chat import message
from utils import semantic_search
import prompts
import openai



# Setting page title and header
st.set_page_config(page_title="BF-AI", page_icon=":robot_face:")
st.markdown("<h1 style='text-align: center;'>Founder'sGPT</h1>", unsafe_allow_html=True)
st.caption("Ask me any question from FoundersConnect show")



# Initialise session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content":  prompts.system_message}
    ]



st.sidebar.title("Sidebar")
clear_button = st.sidebar.button("Clear Conversation", key="clear")



if clear_button:
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.session_state['messages'] = [
        {"role": "system", "content": prompts.system_message}
    ]



# Generate response to user prompt
def generate_response(prompt):
    

    # Perform semantic search and format results
    search_results = semantic_search(prompt, top_k=3)
    context = " "
    context += f"Snippet from: {search_results}\n\n"
    # context += f"{search_results}"
   

    # Generate human prompt template and convert to API message format
    query_with_context = prompts.human_template.format(query= prompt, context=context)

    # # Convert chat history to a list of messages
    # messages = construct_messages(st.session_state.history)
    st.session_state['messages'].append({"role": "user", "content": query_with_context})

    # Run the LLMChain
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages= st.session_state['messages'])
    # print(messages)

    # Parse response
    bot_response = response["choices"][0]["message"]["content"]
    
    
    st.session_state['messages'].append({"role": "assistant", "content": bot_response})
    
    
    return bot_response


# container for chat history
response_container = st.container()
# container for text box
container = st.container()




with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        output = generate_response(user_input)
        
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)
      

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
