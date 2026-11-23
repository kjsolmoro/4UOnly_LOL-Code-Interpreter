// (OwO)==================================================================
//  JAVASCRIPT LOGIC
// (OwO)==================================================================

var editor = document.getElementById('editor');
var fileInput = document.getElementById('fileInput');
var fileName = document.getElementById('fileName');
var tokenBody = document.getElementById('tokenBody');
var symbolBody = document.getElementById('symbolBody');
var consoleBox = document.getElementById('console');
var statusBox = document.getElementById('status');
var runBtn = document.getElementById('runBtn');

function clearBody(body) {
  while (body.firstChild) {
    body.removeChild(body.firstChild);
  }
}

function addRow(body, values, extraClass, lineColumn) {
  var row = document.createElement('tr');
  if (extraClass) {
    row.className = extraClass;
  }
  for (var i = 0; i < values.length; i++) {
    var cell = document.createElement('td');
    cell.textContent = values[i];   // textContent so a YARN like "<b>" is never read as HTML
    if (lineColumn === i) {
      cell.className = 'line';
    }
    row.appendChild(cell);
  }
  body.appendChild(row);
}

// (1u1) File explorer -> (2n2) text editor
var overlay = document.getElementById('overlay');
var dropZone = document.getElementById('dropZone');
var dropMsg = document.getElementById('dropMsg');
var skipBtn = document.getElementById('skipBtn');

function readFile(file) {
  if (!file) {
    return;
  }
  var reader = new FileReader();
  reader.onload = function (event) {
    editor.value = event.target.result;
    fileName.textContent = file.name;
    overlay.style.display = 'none';
    dropMsg.textContent = '';
  };
  reader.onerror = function () {
    dropMsg.textContent = 'Could not read that file.';
  };
  reader.readAsText(file);
}

fileInput.onchange = function () {
  readFile(fileInput.files[0]);
  fileInput.value = '';
};

dropZone.onclick = function () {
  fileInput.click();
};

dropZone.ondragover = function (event) {
  event.preventDefault();
  dropZone.className = 'drop over';
};

dropZone.ondragleave = function () {
  dropZone.className = 'drop';
};

dropZone.ondrop = function (event) {
  event.preventDefault();
  dropZone.className = 'drop';
  readFile(event.dataTransfer.files[0]);
};

skipBtn.onclick = function () {
  overlay.style.display = 'none';
};

// (3_3) tokens, (4u4) symbol table, (6) console
function showResult(data) {
  clearBody(tokenBody);
  clearBody(symbolBody);

  for (var i = 0; i < data.tokens.length; i++) {
    var t = data.tokens[i];
    var cls = '';
    if (t.classification === 'Unidentified') {
      cls = 'bad';
    }
    addRow(tokenBody, [t.lexeme, t.classification, t.line], cls, 2);
  }

  // symbols is [] when there are lexical/syntax errors, so the table is simply cleared
  for (var j = 0; j < data.symbols.length; j++) {
    var s = data.symbols[j];
    var shown = s.value;
    if (s.type === 'YARN') {
      shown = '"' + s.value + '"';   // so "12" and 12 look different
    }
    addRow(symbolBody, [s.identifier, shown, s.type], '', -1);
  }

  // always REPLACE the console text: every response holds the full output so far
  consoleBox.textContent = data.console;
  statusBox.textContent = data.tokens.length + ' lexemes, ' + data.errors + ' error(s)';
}

// (5-5) Execute button
// GIMMEH: the server is stateless. When it hits a GIMMEH with no input left it
// answers with need_input = <variable name>. We ask the user, save the answer,
// and run the whole program again with the longer inputs list.
var collectedInputs = [];

function sendRun() {
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/run');
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.onreadystatechange = function () {
    if (xhr.readyState !== 4) {
      return;
    }
    if (xhr.status !== 200) {
      consoleBox.textContent = 'Server error (' + xhr.status + '). Make sure the Flask server is running.';
      runBtn.disabled = false;
      return;
    }

    var data = JSON.parse(xhr.responseText);
    showResult(data);

    if (data.need_input) {
      // let the page paint the partial output before the dialog blocks it
      setTimeout(function () {
        var answer = prompt('GIMMEH ' + data.need_input + ':');
        if (answer === null) {
          consoleBox.textContent += '\n\n(Input cancelled)';
          runBtn.disabled = false;
          return;
        }
        collectedInputs.push(answer);
        sendRun();
      }, 50);
      return;
    }

    runBtn.disabled = false;
  };
  xhr.send(JSON.stringify({ code: editor.value, inputs: collectedInputs }));
}

function execute() {
  collectedInputs = [];     // fresh run, forget old answers
  runBtn.disabled = true;   // no double-clicks while a run is in progress
  sendRun();
}

runBtn.onclick = execute;