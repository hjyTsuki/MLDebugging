SAMPLES_PROMPT = """
Please review the task_func function for errors. Begin by reading the provided instructions to understand the intended behavior of the function. Ensure the code aligns with the requirements and identify any issues. Correct any errors found and provide the revised code.

Input format
<instruct>: Code requirements and expected functionality
<bug_code>: The original (bugged) version of the code.

Please output only the debugged code under the label <corrected_code>, without any additional text or comments:
Output Format Example
<corrected_code>
import ……
def task_func(……
</corrected_code>

Samples:
{}
"""