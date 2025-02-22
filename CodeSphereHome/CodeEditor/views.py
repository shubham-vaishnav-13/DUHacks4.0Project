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
    if request.method == 'POST':
        data = json.loads(request.body)
        language = data.get('language')
        code = data.get('code')
        input_data = data.get('input')

        # Create temporary file to store the code
        with tempfile.NamedTemporaryFile(delete=False) as f:
            if language == 'python':
                f.write(code.encode())
                cmd = ['python', f.name]
            elif language in ['c', 'cpp']:
                f.write(code.encode())
                # Compile and run for C/C++
                compile_cmd = ['gcc', f.name, '-o', f.name + '.exe'] if language == 'c' else [
                    'g++', f.name, '-o', f.name + '.exe']
                subprocess.run(compile_cmd)
                cmd = [f.name + '.exe']
            elif language == 'javascript':
                f.write(code.encode())
                cmd = ['node', f.name]

        try:
            process = subprocess.run(
                cmd,
                input=input_data.encode() if input_data else None,
                capture_output=True,
                text=True,
                timeout=5
            )
            output = process.stdout if process.stdout else process.stderr
        except Exception as e:
            output = str(e)
        finally:
            # Cleanup
            os.unlink(f.name)
            if language in ['c', 'cpp'] and os.path.exists(f.name + '.exe'):
                os.unlink(f.name + '.exe')

        return JsonResponse({'output': output})

    return JsonResponse({'error': 'Invalid request method'})
