// Load the autocompletion extension
ace.require("ace/ext/language_tools");

var editor = ace.edit("editor");
editor.setTheme("ace/theme/dracula");
editor.session.setMode("ace/mode/js"); // Default language

// Enable autocompletion
editor.setOptions({
    enableBasicAutocompletion: true,  // Shows suggestions when pressing Ctrl + Space
    enableLiveAutocompletion: true,   // Auto-suggest while typing
    enableSnippets: true              // Use built-in code snippets
});


document
    .getElementById("language")
    .addEventListener("change", function () {
        let mode = {
            c: "ace/mode/c_cpp",
            cpp: "ace/mode/c_cpp",
            javascript: "ace/mode/javascript",
            python: "ace/mode/python",
        }[this.value];
        editor.session.setMode(mode);
    });

document.getElementById("theme").addEventListener("change", function () {
    editor.setTheme("ace/theme/" + this.value);
});

function increaseFontSize() {
    let currentSize = editor.getFontSize();
    editor.setFontSize(parseInt(currentSize) + 2);
}

function decreaseFontSize() {
    let currentSize = editor.getFontSize();
    editor.setFontSize(parseInt(currentSize) - 2);
}

function saveCode() {
    fragment = document.createElement("p");
    fragment.innerHTML = "Saved Code Successfully";
    fragment.classList.add("bg-green-500", "p-2", "rounded");
    document
        .getElementById("buttons")
        .insertAdjacentElement("afterend", fragment);
    setTimeout(() => {
        fragment.remove();
    }, 3000);
}

function exportCode() {
    let blob = new Blob([editor.getValue()], {
        type: "text/plain;charset=utf-8",
    });
    saveAs(blob, "code.txt");
}
function runCode() {
    document.getElementById("output").innerText = "Running...";
    fetch("run_code", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            language: document.getElementById("language").value,
            code: editor.getValue(),
            input: document.getElementById("custom-input").value
        })
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById("output").innerText = data.output;
        });
}

function resizeEditor() {
    let newHeight = window.innerHeight * 0.7; // 70% of viewport height
    document.getElementById("editor").style.height = newHeight + "px";
    editor.resize();
}

// Resize on load and window resize
window.onload = resizeEditor;
window.onresize = resizeEditor;