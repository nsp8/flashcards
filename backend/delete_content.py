import streamlit
from client import get_or_create_eventloop, remove_all_flashcards


@streamlit.dialog("Confirm")
def confirm_dialog():
    streamlit.write("Are you sure you want to delete everything?")
    if streamlit.button("Yes"):
        streamlit.session_state.clear_bank = True
        streamlit.rerun()


def handle_deletion():
    with streamlit.sidebar:
        if streamlit.button(
            "Delete everything",
            icon=":material/delete_forever:",
            use_container_width=True
        ):
            confirm_dialog()
            streamlit.write(streamlit.session_state.clear_bank)
            if streamlit.session_state.clear_bank:
                status, message = get_or_create_eventloop().run_until_complete(
                    remove_all_flashcards()
                )
                if status in range(200, 300):
                    streamlit.success("Data submitted successfully!")
                else:
                    streamlit.error(message)
