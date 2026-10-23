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
    cell.textContent = values[i];
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

  for (var j = 0; j < data.symbols.length; j++) {
    addRow(symbolBody, [data.symbols[j].identifier, data.symbols[j].value], '', -1);
  }

  consoleBox.textContent = data.console;
  statusBox.textContent = data.tokens.length + ' lexemes, ' + data.errors + ' error(s)';
}

// (5-5) Execute button
function execute() {
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/run');
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.onreadystatechange = function () {
    if (xhr.readyState !== 4) {
      return;
    }
    if (xhr.status !== 200) {
      consoleBox.textContent = 'Server error (' + xhr.status + '). Make sure the Flask server is running.';
      return;
    }
    showResult(JSON.parse(xhr.responseText));
  };
  xhr.send(JSON.stringify({ code: editor.value }));
}

runBtn.onclick = execute;
