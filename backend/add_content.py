import streamlit
from client import get_or_create_eventloop, add_flashcard


streamlit.header("Flashcards", divider="rainbow")
with streamlit.form("add_content"):
    streamlit.write("Add Content")
    question = streamlit.text_input("Question")
    answer = streamlit.text_input("Answer")
    if streamlit.form_submit_button("Submit"):
        status, message = get_or_create_eventloop().run_until_complete(
            add_flashcard(question=question, answer=answer)
        )
        if status in range(200, 300):
            streamlit.success("Data submitted successfully!")
        else:
            streamlit.error(message)
