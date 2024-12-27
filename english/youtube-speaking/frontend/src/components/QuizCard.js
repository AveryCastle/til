import React, { useState } from 'react';

function QuizCard({ quiz }) {
  const [showAnswer, setShowAnswer] = useState(false);

  return (
    <div className="quiz-card">
      <h2>Quiz</h2>
      <p>{showAnswer ? quiz.answer : quiz.question}</p>
      <button onClick={() => setShowAnswer(!showAnswer)}>
        {showAnswer ? 'Show Question' : 'Show Answer'}
      </button>
    </div>
  );
}

export default QuizCard;
