chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "classifyImage") {
      classifyImage(message.imageUrl).then(category => {
        sendResponse({ category });
      });
      return true; // async 응답을 위해 true 반환
    }
  });
  
  async function classifyImage(imageUrl) {
    const apiEndpoint = "https://vertex-ai.googleapis.com/v1/projects/YOUR_PROJECT_ID/locations/YOUR_LOCATION/models/YOUR_MODEL:predict";
    const apiKey = "YOUR_API_KEY";
  
    const payload = {
      instances: [{ content: imageUrl }]
    };
  
    const response = await fetch(apiEndpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${apiKey}`
      },
      body: JSON.stringify(payload)
    });
  
    const result = await response.json();
    // Vertex AI 결과에서 카테고리 추출
    const category = result.predictions[0].displayNames[0];
    return category;
  }
  