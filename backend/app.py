import streamlit
from delete_content import handle_deletion

if "clear_bank" not in streamlit.session_state:
    streamlit.session_state.clear_bank = False

add_content_page = streamlit.Page(
    "add_content.py", title="Add", icon=":material/post_add:"
)

show_content_page = streamlit.Page(
    "show_content.py", title="Flashcards", icon=":material/preview:"
)

pages = streamlit.navigation(
    {
        "Show Content": [show_content_page],
        "Add Content": [add_content_page],
    }
)

handle_deletion()
pages.run()
