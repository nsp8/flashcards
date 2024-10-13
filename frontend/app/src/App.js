// src/App.js
import React, { useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [flashcards, setFlashcards] = useState([]);
  const [newFlashcard, setNewFlashcard] = useState({ question: "", answer: "" });

  useEffect(() => {
    fetchFlashcards();
  }, []);

  const fetchFlashcards = async () => {
    const response = await axios.get("http://127.0.0.1:8000/flashcards/");
    setFlashcards(response.data);
  };

  const handleInputChange = (e) => {
    setNewFlashcard({
      ...newFlashcard,
      [e.target.name]: e.target.value,
    });
  };

  const addFlashcard = async () => {
    await axios.post("http://127.0.0.1:8000/flashcards/", newFlashcard);
    fetchFlashcards(); // Refresh the list
  };

  return (
    <div className="App">
      <h1>Flashcard App</h1>
      <div>
        <input
          type="text"
          name="question"
          placeholder="Enter Question"
          value={newFlashcard.question}
          onChange={handleInputChange}
        />
        <input
          type="text"
          name="answer"
          placeholder="Enter Answer"
          value={newFlashcard.answer}
          onChange={handleInputChange}
        />
        <button onClick={addFlashcard}>Add Flashcard</button>
      </div>
      <h2>Flashcards:</h2>
      <ul>
        {flashcards.map((flashcard) => (
          <li key={flashcard.id}>
            <strong>{flashcard.question}</strong>: {flashcard.answer}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
