// src/InterviewUploader.js
import React, { useState } from 'react';

function InterviewUploader() {
  const [file, setFile] = useState(null);
  const [feedback, setFeedback] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const uploadRes = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });

      const uploadData = await uploadRes.json();
      setFeedback(uploadData);  // this assumes the backend sends back the JSON directly
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  return (
    <div className="p-6 max-w-xl mx-auto">
      <form onSubmit={handleSubmit} className="space-y-4">
        <input type="file" accept="audio/*,video/*" onChange={handleFileChange} />
        <button
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Upload and Get Feedback
        </button>
      </form>

      {feedback && (
        <div className="mt-6 bg-gray-100 p-4 rounded">
          <h2 className="text-xl font-semibold mb-2">Interview Feedback:</h2>
          <pre className="whitespace-pre-wrap text-sm">{JSON.stringify(feedback, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default InterviewUploader;
