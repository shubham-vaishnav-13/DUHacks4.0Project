// Load the autocompletion extension
ace.require("ace/ext/language_tools");

var editor = ace.edit("editor");

// Ensure Ace is fully loaded before setting value
setTimeout(() => {
    editor.setTheme("ace/theme/dracula");
    editor.session.setMode("ace/mode/javascript"); // Default language
    editor.setValue("Darshan", -1);  // ✅ Ensures initial value
    editor.clearSelection(); // ✅ Prevents text selection
    console.log("✅ Initial Value Set:", editor.getValue()); // Debugging
}, 100); 

// Enable autocompletion
editor.setOptions({
    enableBasicAutocompletion: true,
    enableLiveAutocompletion: true,
    enableSnippets: true
});

// Ensure the editor resets to "Darshan" when language changes
document.getElementById("language").addEventListener("change", function () {
    let mode = {
        c: "ace/mode/c_cpp",
        cpp: "ace/mode/c_cpp",
        javascript: "ace/mode/javascript",
        python: "ace/mode/python",
    }[this.value];

    editor.session.setMode(mode);

    // ✅ Reset editor value after changing language
    setTimeout(() => {
        editor.setValue("Darshan", -1);
        editor.clearSelection();
        console.log("✅ Value after language change:", editor.getValue()); // Debugging
    }, 100);
});

// Change theme dynamically
document.getElementById("theme").addEventListener("change", function () {
    editor.setTheme("ace/theme/" + this.value);
});

// Increase font size
function increaseFontSize() {
    let currentSize = editor.getFontSize();
    editor.setFontSize(parseInt(currentSize) + 2);
}

// Decrease font size
function decreaseFontSize() {
    let currentSize = editor.getFontSize();
    editor.setFontSize(parseInt(currentSize) - 2);
}

// Save Code
function saveCode() {
    let code = editor.getValue();
    let language = document.getElementById("language").value;
    fetch('/save_code/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: code, language: language })
    })
    .then(response => response.json())
    .then(data => {
        let message = document.createElement("p");
        message.classList.add("p-2", "rounded", "mt-2");
        if (data.success) {
            message.innerHTML = "✅ Code Saved Successfully!";
            message.classList.add("bg-green-500");
        } else {
            message.innerHTML = "❌ Error Saving Code: " + data.error;
            message.classList.add("bg-red-500");
        }
        document.getElementById("buttons").insertAdjacentElement("afterend", message);
        setTimeout(() => { message.remove(); }, 3000);
    });
}

// Export Code as Text File
function exportCode() {
    let blob = new Blob([editor.getValue()], {
        type: "text/plain;charset=utf-8",
    });
    saveAs(blob, "code.txt");
}

// Run Code
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

// Resize editor dynamically
function resizeEditor() {
    let newHeight = window.innerHeight * 0.7; // 70% of viewport height
    document.getElementById("editor").style.height = newHeight + "px";
    editor.resize();
}

// Resize on load and window resize
window.onload = resizeEditor;
window.onresize = resizeEditor;

// ✅ Debugging: Log when page loads
window.onload = function () {
    console.log("✅ Page Loaded. Ace Editor initialized.");
    console.log("✅ Current Editor Value:", editor.getValue());
};
