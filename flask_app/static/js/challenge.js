const emptyContent = {
  assignment: "",
  title: "",
  code: "",
  solution: "",
  hint: "",
  feedback: "",
  challengeId: "",
  attempt: "",
  p_language: "",
  language: "",
  difficulty: "",
  length: "",
  description: "",
  updated_at: ""
}

let currentContent = emptyContent

function clearContent() {
  currentContent = emptyContent
}

function ensureCorrectQuery(name, variable) {
  const url = new URL(window.location.href);
  const params = url.searchParams;

  if (params.get(name) !== variable) {
    params.set(name, variable); // Add or update the 'repo' parameter
    window.history.replaceState({}, '', url); // Update the URL without reloading the page
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

    ensureCorrectQuery("challengeId", "");

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
        .replace("§TITLE§", "§§§§§")
        .replace("§CODE§", "§§§§§")
        .replace("§SOLUTION§", "§§§§§")
        .replace("§HINT§", "§§§§§")
        .replace("§ID§", "§§§§§")
        .replace("§END§", "§§§§§")
      var pLanguage = document.getElementById('pLanguage').value
      if (content.includes("```" + pLanguage)) {
        content = content.replace("```" + pLanguage, "").replace("```", "")
      }
      var splitted = content.split("§§§§§")
      const lSplit = splitted.length
      currentContent.assignment = splitted[0]
      currentContent.title = lSplit > 1 ? splitted[1] : "";
      currentContent.code = lSplit > 2 ? splitted[2] : "";
      currentContent.solution = lSplit > 3 ? splitted[3] : "";
      currentContent.hint = lSplit > 4 ? splitted[4] : "";
      if (lSplit > 5) {
        currentContent.challengeId = splitted[5];
        ensureCorrectQuery('challengeId', currentContent.challengeId);
      }
    }

    let done = false;
    var chunk = ""

    while (!done) {
      const {value, done: streamDone} = await stream.read();
      done = streamDone;

      if (value) {
        chunk = value
        totalResponse += chunk;

        if (totalResponse.includes('§END§')) {
          break;
        }

        if (totalResponse.includes("§TITLE§") && currentBlock === "assignment") {
          splitContent();
          assignContent();
          currentBlock = "title";
        } else if (totalResponse.includes("§CODE§") && currentBlock === "title") {
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
    console.log(totalResponse)
    splitContent();
    assignContent();
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

        feedbackDiv.innerHTML = marked.parse(totalResponse.replace('§END§', ''));
        if (totalResponse.includes('§END§')) {
          currentContent.feedback = totalResponse.replace('§END§', '');
          break;
        }

      }
    }
  } catch (error) {
    console.error('Fetch error:', error);
  }
}

function deleteChallenge(challengeId) {
  fetch('/challenge/delete/' + challengeId, {
    method: 'POST',
    body: JSON.stringify({}),
    headers: {
      'Content-Type': 'application/json'
    }
  }).then(response => {
    if (response.ok) {
      location.reload();
    } else {
      console.log('Error deleting challenge:', response.json().data);
    }
  });
}

function updateCharCount() {
  const input = document.getElementById('description');
  const charCount = document.getElementById('charCount');
  charCount.textContent = `${input.value.length}/200`;
}

function showSolution() {
  attempt = editor.getValue();
  editor.session.setValue(currentContent.solution, -1);
  document.getElementById('showSolution').style.display = 'none';
  document.getElementById('hideSolution').style.display = 'block';
  document.getElementById('codeTitle').innerHTML = 'Possible Solution';
  editor.setReadOnly(true);
}

function hideSolution() {
  editor.session.setValue(attempt, -1);
  document.getElementById('showSolution').style.display = 'block';
  document.getElementById('hideSolution').style.display = 'none';
  document.getElementById('codeTitle').innerHTML = 'Your Code';
  editor.setReadOnly(false);
}

function toggleHint() {
  var hint = document.getElementById('hint');
  hint.style.display = hint.style.display === 'none' ? 'block' : 'none';
  var hintButton = document.getElementById('getHint');
  hintButton.innerHTML = hint.style.display === 'none' ? 'Show Hint' : 'Hide Hint';
}

function updatePLanguage() {
  var selection = $('option:selected').attr('value');
  selection = ['c', 'cpp'].includes(selection) ? 'c_cpp' : selection;
  var mode = 'ace/mode/' + selection;
  editor.getSession().setMode(mode);
}

function appendToEditorContent(extraCode) {
  const lastRow = editor.session.getLength() - 1;
  const lastColumn = editor.session.getLine(lastRow).length;
  editor.session.insert({row: lastRow, column: lastColumn}, extraCode);
}