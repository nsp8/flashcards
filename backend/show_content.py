import streamlit
from client import get_or_create_eventloop, get_flashcards

streamlit.header("Flashcards", divider="rainbow")


class Pagination:
    def __init__(self, maximum: int, chunk_size: int = 10):
        self.pages = [
            (i + 1, min(i + chunk_size, maximum)) for i in range(0, maximum, chunk_size)
        ]

    def to_select_options(self) -> dict:
        return {f"{i[0]} - {i[1]}": i for i in self.pages}

    def __repr__(self):
        return str(self.pages)


status, data = get_or_create_eventloop().run_until_complete(get_flashcards())
if status == 200 and data:
    pagination = Pagination(
        maximum=len(data),
        chunk_size=streamlit.slider("Choose chunk size", 2, len(data), 10)
    )
    options = pagination.to_select_options()
    selection = streamlit.selectbox("Select group:", options.keys())
    page = options[selection]
    for card in data[page[0]-1: page[1]]:
        with streamlit.expander(card["question"]):
            streamlit.write(card["answer"])
else:
    streamlit.error("Nothing to show here!")
