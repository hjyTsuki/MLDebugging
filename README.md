# ✨MLDebugging
<div>
<img src="./assets/log.png" width="96%">
</div>

This is the code repository for the paper: MLDebugging: Towards Benchmarking Code Debugging Across Multi-Library Scenarios. **ACL 2025 Findings**.

## 💡Evaluation

We have open-sourced the dataset, and it is available for download on Hugging Face.

```python
from datasets import load_dataset

# Login using e.g. `huggingface-cli login` to access this dataset
ds = load_dataset("Tsukihjy/MLDeugging")
```

Our evaluation code can be run by following the provided steps：

```bash
pip install -r requirements-eval.txt
cd eval
python evaluate.py your/path/to/results.jsonl
```

## 🛠️Data Collection

![](D:\Research\MLDebug\MLDebugging\assets\pipeline.png)

Illustration of the MLDebugging Dataset Construction Process



## 💬 Contact

If you have any questions or suggestions, please create a GitHub issue or email [JinYang Huang](hjy.tsuki@gmail.com).
