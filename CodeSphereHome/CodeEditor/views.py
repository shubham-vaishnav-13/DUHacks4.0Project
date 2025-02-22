from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import subprocess
import tempfile
import os
import json
# Create your views here.


def editor(request):
    return render(request, "Editor/editor.html")


@csrf_exempt
def runCode(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            language = data.get("language")
            code = data.get("code")
            custom_input = data.get("input", "")

            file_extension = {
                "python": "py",
                "c": "c",
                "cpp": "cpp",
                "javascript": "js"
            }.get(language, None)

            if not file_extension:
                return JsonResponse({"output": "Unsupported language"})

            file_name = f"temp.{file_extension}"
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(code)

            command = []
            if language == "python":
                command = ["python", file_name]
            elif language == "c":
                output_file = "temp.out"
                compile_command = ["gcc", file_name, "-o", output_file]
                subprocess.run(compile_command, capture_output=True, text=True)
                command = ["./" + output_file]
            elif language == "cpp":
                output_file = "temp.out"
                compile_command = ["g++", file_name, "-o", output_file]
                subprocess.run(compile_command, capture_output=True, text=True)
                command = ["./" + output_file]
            elif language == "javascript":
                command = ["node", file_name]

            result = subprocess.run(
                command, input=custom_input, text=True, capture_output=True)

            output = result.stdout if result.stdout else result.stderr

            # Cleanup
            os.remove(file_name)
            if language in ["c", "cpp"] and os.path.exists("temp.out"):
                os.remove("temp.out")

            return JsonResponse({"output": output})

        except Exception as e:
            return JsonResponse({"output": str(e)})

    return JsonResponse({"output": "Invalid request method"})
