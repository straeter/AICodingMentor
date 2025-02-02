var currentContent = {
  assignment: "",
  code: "",
  solution: "",
  hint: "",
  feedback: ""
}

function clearContent() {
  currentContent = {
    assignment: "",
    code: "",
    solution: "",
    hint: "",
    feedback: ""
  }
}


async function fetchStream(data) {
  try {
    const response = await fetch('/get_challenge', {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok || !response.body) {
      throw new Error('Network response was not ok or stream is not supported.');
    }

    const stream = response.body
      .pipeThrough(new TextDecoderStream())
      .getReader();

    var currentBlock = "assignment";
    var totalResponse = "";

    const assignmentDiv = document.getElementById('assignment');
    assignmentDiv.innerHTML = "";
    const hintDiv = document.getElementById('hint');
    hintDiv.innerHTML = "";

    clearContent();

    function assignContent() {
      splitContent(totalResponse);
      assignmentDiv.innerHTML = marked.parse(currentContent.assignment);
      editor.session.setValue(currentContent.code, -1);
      hintDiv.innerHTML = marked.parse(currentContent.hint);
    }

    function splitContent() {
      var content = totalResponse
      content = content
        .replace("§CODE§", "§§§§§")
        .replace("§SOLUTION§", "§§§§§")
        .replace("§HINT§", "§§§§§")
      var pLanguage = document.getElementById('pLanguage').value
      if (content.includes("```" + pLanguage)) {
        content = content.replace("```" + pLanguage, "").replace("```", "")
      }
      var splitted = content.split("§§§§§")
      const lSplit = splitted.length
      currentContent.assignment = splitted[0]
      currentContent.code = splitted[1]
      currentContent.solution = splitted[2]
      currentContent.hint = splitted[3]
    }

    let done = false;
    var chunk = ""

    while (!done) {
      const {value, done: streamDone} = await stream.read();
      done = streamDone;

      if (value) {
        chunk = value
        totalResponse += chunk;

        if (totalResponse.includes('&&&')) {
          break;
        }

        if (totalResponse.includes("§CODE§") && currentBlock === "assignment") {
          splitContent();
          assignContent();
          currentBlock = "code";
        } else if (totalResponse.includes("§SOLUTION§") && currentBlock === "code") {
          splitContent();
          assignContent();
          currentBlock = "solution";
        } else if (totalResponse.includes("§HINT§") && currentBlock === "solution") {
          splitContent();
          assignContent();
          currentBlock = "hint";
        } else {
          if (currentBlock === "assignment") {
            assignmentDiv.innerHTML += chunk;
          } else if (currentBlock === "code") {
            appendToEditorContent(chunk)
          } else if (currentBlock === "hint") {
            hintDiv.innerHTML += chunk;
          }
        }
      }
    }
  } catch (error) {
    console.error('Fetch error:', error);
  }
}


async function fetchFeedback(data) {
  try {
    const response = await fetch('/get_feedback', {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok || !response.body) {
      throw new Error('Network response was not ok or stream is not supported.');
    }

    const stream = response.body
      .pipeThrough(new TextDecoderStream())
      .getReader();

    var totalResponse = "";

    const feedbackDiv = document.getElementById('feedback');
    feedbackDiv.innerHTML = "";

    let done = false;
    var chunk = ""

    while (!done) {
      const {value, done: streamDone} = await stream.read();
      done = streamDone;
      if (value) {
        chunk = value
        totalResponse += chunk;

        feedbackDiv.innerHTML = marked.parse(totalResponse.replace('&&&', ''));
        if (totalResponse.includes('&&&')) {
          currentContent.feedback = totalResponse.replace('&&&', '');
          break;
        }

      }
    }
  } catch (error) {
    console.error('Fetch error:', error);
  }
}