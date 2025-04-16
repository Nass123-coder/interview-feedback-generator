import React, { useState } from 'react';
import axios from 'axios';

const InterviewUploader = () => {
  const [file, setFile] = useState(null);
  const [feedback, setFeedback] = useState(null);

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post('http://localhost:5000/upload', formData);
      const json = JSON.parse(res.data.json);  // because backend returns stringified JSON
      setFeedback(json);
    } catch (err) {
      console.error(err);
      alert('Upload or analysis failed.');
    }
  };

  return (
    <div className="p-4">
      <input type="file" accept="audio/*" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload}>Upload & Analyze</button>

      {feedback && (
        <div className="mt-4">
          <h2>📝 Feedback</h2>
          <pre>{JSON.stringify(feedback, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default InterviewUploader;
