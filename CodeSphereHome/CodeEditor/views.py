from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from StudentManage.models import CodeFile
import subprocess
import json
import os


@login_required
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
                compile_result = subprocess.run(compile_command, capture_output=True, text=True)
                if compile_result.stderr:
                    return JsonResponse({"output": compile_result.stderr})
                command = ["./" + output_file]
            elif language == "cpp":
                output_file = "temp.out"
                compile_command = ["g++", file_name, "-o", output_file]
                compile_result = subprocess.run(compile_command, capture_output=True, text=True)
                if compile_result.stderr:
                    return JsonResponse({"output": compile_result.stderr})
                command = ["./" + output_file]
            elif language == "javascript":
                command = ["node", file_name]

            result = subprocess.run(command, input=custom_input, text=True, capture_output=True)

            output = result.stdout if result.stdout else result.stderr

            # Cleanup
            os.remove(file_name)
            if language in ["c", "cpp"] and os.path.exists("temp.out"):
                os.remove("temp.out")

            return JsonResponse({"output": output})

        except Exception as e:
            return JsonResponse({"output": str(e)})

    return JsonResponse({"output": "Invalid request method"})


@csrf_exempt
@login_required
def save_code(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            code = data.get("code")
            language = data.get("language")
            user = request.user

            file_name = f"{user.username}_code.{language}"
            file_path = f"code_files/{file_name}"

            # Save file locally
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)

            # Save to the model
            CodeFile.objects.create(
                student=user,
                file_name=file_name,
                file=file_path,
                file_type=language,
                subject="General"
            )

            return JsonResponse({"success": True, "message": "Code saved successfully!"})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request method"})
