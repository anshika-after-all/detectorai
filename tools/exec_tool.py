import subprocess, tempfile

class ExecTool:
    def run(self, code):
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".py") as f:
            f.write(code)
            path = f.name

        result = subprocess.run(["python", path], capture_output=True, text=True)
        return result.stdout + result.stderr
