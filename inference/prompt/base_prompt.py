BUG_PROMPT = """
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
"""

BUG_PROMPT_CoT = """
Please review the task_func function for errors. Begin by reading the provided instructions to understand the intended behavior of the function. Ensure the code aligns with the requirements and identify any issues. Correct any errors found and provide the revised code.

Input format
<instruct>: Code requirements and expected functionality
<bug_code>: The original (bugged) version of the code.

Let's think Step by Step to Solve this problem.
Please output the final answer at the end, enclosed in markdown format, without any additional text or comments.
Final answer Output Format Example
```python
import ……
def task_func(……
```
"""

BUG_PROMPT_Reasoning = """
Please review the task_func function for errors. Begin by reading the provided instructions to understand the intended behavior of the function. Ensure the code aligns with the requirements and identify any issues. Correct any errors found and provide the revised code.

Input format
<instruct>: Code requirements and expected functionality
<bug_code>: The original (bugged) version of the code.

Please output the final answer at the end, enclosed in markdown format, without any additional text or comments.
Final answer output Format Example:
```python
import ……
def task_func(……
```
"""

RUNTIME_PROMPT = """
Please review the task_func function for errors. Begin by reading the provided instructions to understand the intended behavior of the function. Ensure the code aligns with the requirements and identify any issues. Correct any errors found and provide the revised code.

Input format
<instruct>: Code requirements and expected functionality
<bug_code>: The original (bugged) version of the code.
<test_case>:Test cases used to verify whether the requirements are met.
<runtime_feedback>:System error messages and other information obtained from executing the code.

Please output only the debugged code under the label <corrected_code>, without any additional text or comments:
Output Format Example
<corrected_code>
import ……
def task_func(……
</corrected_code>
"""

RUNTIME_PROMPT_RUN = """
Please review the task_func function for errors. Begin by reading the provided instructions to understand the intended behavior of the function. Ensure the code aligns with the requirements and identify any issues. Correct any errors found and provide the revised code.

Input format
<instruct>: Code requirements and expected functionality
<bug_code>: The original (bugged) version of the code.
<test_case>:Test cases used to verify whether the requirements are met.
<runtime_feedback>:System error messages and other information obtained from executing the code.

Please output only the debugged code under the label <corrected_code>, without any additional text or comments:
Output Format Example
<corrected_code>
import ……
def task_func(……
</corrected_code>
"""

RUNTIME_PROMPT_TEST = """
Please review the task_func function for errors. Begin by reading the provided instructions to understand the intended behavior of the function. Ensure the code aligns with the requirements and identify any issues. Correct any errors found and provide the revised code.

Input format
<instruct>: Code requirements and expected functionality
<bug_code>: The original (bugged) version of the code.
<test_case>:Test cases used to verify whether the requirements are met.

Please output only the debugged code under the label <corrected_code>, without any additional text or comments:
Output Format Example
<corrected_code>
import ……
def task_func(……
</corrected_code>
"""

BUG_PROMPT_IE = """
Please review the task_func function for errors. Begin by reading the provided instructions to understand the intended behavior of the function. Ensure the code aligns with the requirements and identify any issues. Correct any errors found and provide the revised code.
Check if all the libraries have been imported.
Input format
<instruct>: Code requirements and expected functionality
<bug_code>: The original (bugged) version of the code.

Please output only the debugged code under the label <corrected_code>, without any additional text or comments:
Output Format Example
<corrected_code>
import ……
def task_func(……
</corrected_code>
"""

BUG_PROMPT_RM = """
Please review the task_func function for errors. Begin by reading the provided instructions to understand the intended behavior of the function. Ensure the code aligns with the requirements and identify any issues. Correct any errors found and provide the revised code.
Please check if the code implementation meets the requirements
Input format
<instruct>: Code requirements and expected functionality
<bug_code>: The original (bugged) version of the code.

Please output only the debugged code under the label <corrected_code>, without any additional text or comments:
Output Format Example
<corrected_code>
import ……
def task_func(……
</corrected_code>
"""