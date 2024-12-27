import React, { useState } from 'react';
import QuizCard from './components/QuizCard';
import ExampleDialog from './components/ExampleDialog';
import './styles.css';

function App() {
  const [channelId, setChannelId] = useState('');
  const [quiz, setQuiz] = useState(null);
  const [examples, setExamples] = useState([]);

  const fetchQuiz = async () => {
    const response = await fetch(`/api/quiz?channelId=${channelId}`);
    const data = await response.json();
    setQuiz(data.quiz);
    setExamples(data.examples);
  };

  return (
    <div className="app-container">
      <h1>YouTube Speaking Practice</h1>
      <div className="input-section">
        <input
          type="text"
          placeholder="Enter YouTube Channel ID"
          value={channelId}
          onChange={(e) => setChannelId(e.target.value)}
        />
        <button onClick={fetchQuiz}>Fetch Quiz</button>
      </div>
      {quiz && <QuizCard quiz={quiz} />}
      {examples.length > 0 && <ExampleDialog examples={examples} />}
    </div>
  );
}

export default App;
