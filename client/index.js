 const BASE_URL = "http://localhost:8000/api/v1";

    // Tab Switching Function
    function switchTab(index) {
      const tabs = document.querySelectorAll('.tab');
      const contents = document.querySelectorAll('.tab-content');

      tabs.forEach((tab, i) => {
        tab.classList.toggle('active', i === index);
        contents[i].classList.toggle('active', i === index);
      });
    }

    // Text Question Function
    async function sendTextQuestion() {
  const question = document.getElementById("textQuestion").value;
  const language = document.getElementById("textLanguage").value;
  const responseBox = document.getElementById("textResponse");
  const stagesBox = document.getElementById("textStages");
  const loadingEl = document.getElementById("textLoading");

  if (!question.trim()) {
    responseBox.innerText = "Please enter a question first.";
    stagesBox.style.display = "none";
    return;
  }

  // Reset UI
  responseBox.innerText = "";
  stagesBox.innerText = "";
  stagesBox.style.display = "none";

  // Show loading
  loadingEl.classList.remove("hidden");

  try {
    const response = await fetch(`${BASE_URL}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, language, auto_stage_detection: true })
    });

    const data = await response.json();

    // Hide loading
    loadingEl.classList.add("hidden");

    responseBox.innerText = data.answer || "No response";

    // Show detected stages if they exist
// Show detected stages if they exist
if (Array.isArray(data.detected_stages) && data.detected_stages.length > 0) {
  stagesBox.innerHTML = ""; // clear container
  stagesBox.style.display = "block";

  // Add "Question Stage" title
  const stageTitle = document.createElement("div");
  stageTitle.className = "stage-title";
  stageTitle.innerText = "Question Stage";
  stagesBox.appendChild(stageTitle);

  data.detected_stages.forEach(stage => {
    const cleanStage = stage
      .replace(/^[0-9]+_?/, "")   // remove numbers
      .replace(/_/g, " ")         // replace underscores
      .trim();

    const badge = document.createElement("span");
    badge.className = "stage-badge";
    badge.innerText = cleanStage;

    stagesBox.appendChild(badge);
  });
} else {
  stagesBox.style.display = "none";
}

  } catch (err) {
    loadingEl.classList.add("hidden");
    responseBox.innerText = "Error while contacting the server.";
    stagesBox.style.display = "none";
    console.error(err);
  }
}


    // Image Analysis Function
    async function sendImageQuestion() {
      const question = document.getElementById("imageQuestion").value;
      const language = document.getElementById("imageLanguage").value;
      const file = document.getElementById("imageInput").files[0];
      const responseBox = document.getElementById("imageResponse");

      if (!file) {
        responseBox.innerText = "⚠️ Please select an image for analysis";
        return;
      }

      responseBox.innerText = "⏳ Analyzing your image...";

      const formData = new FormData();
      formData.append("question", question);
      formData.append("language", language);
      formData.append("image", file);

      try {
        const response = await fetch(`${BASE_URL}/chat-with-image`, {
          method: "POST",
          body: formData
        });

        const data = await response.json();
        responseBox.innerText = data.answer || "❌ No results received";
      } catch (error) {
        responseBox.innerText = "❌ Connection error: " + error.message;
      }
    }

    // File Analysis Function
    async function sendFileQuestion() {
      const question = document.getElementById("fileQuestion").value;
      const language = document.getElementById("fileLanguage").value;
      const file = document.getElementById("fileInput").files[0];
      const responseBox = document.getElementById("fileResponse");

      if (!file) {
        responseBox.innerText = "⚠️ Please select a document for analysis";
        return;
      }

      responseBox.innerText = "⏳ Analyzing your document...";

      const formData = new FormData();
      formData.append("question", question);
      formData.append("language", language);
      formData.append("file", file);

      try {
        const response = await fetch(`${BASE_URL}/chat-with-file`, {
          method: "POST",
          body: formData
        });

        const data = await response.json();
        responseBox.innerText = data.answer || "❌ No results received";
      } catch (error) {
        responseBox.innerText = "❌ Connection error: " + error.message;
      }
    }

    // Scroll Animation
    function handleScrollAnimation() {
      const elements = document.querySelectorAll('.fade-in');
      elements.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const elementVisible = 150;
        
        if (elementTop < window.innerHeight - elementVisible) {
          element.classList.add('visible');
        }
      });
    }

    // Smooth Scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      });
    });

    // Event Listeners
    window.addEventListener('scroll', handleScrollAnimation);
    window.addEventListener('load', handleScrollAnimation);

    // Initialize animations on load
    document.addEventListener('DOMContentLoaded', function() {
      handleScrollAnimation();
    });