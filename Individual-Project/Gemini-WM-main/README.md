# Assessing Working Memory Capacity of Large Language Models (LLMs) Using N-back Tasks

![image](https://github.com/user-attachments/assets/f968575a-00be-4453-bc62-5d9237fa26fe)

This is a code and dataset repository for the paper "**[Working Memory Capacity of ChatGPT: An Empirical Study](https://arxiv.org/abs/2305.03731)**", which has been accepted by AAAI 2024 Conference on Artificial Intelligence.

## Overview

We created a dataset to test the working memory capacity of language models. We chose the N-back task because it is widely used in cognitive science as a measure of working memory capacity. To create the N-back task dataset, we generated 50 blocks of trials for $N = \{1, 2, 3\}$, respectively. Each block contains 24 trials, including 8 match trials and 16 nonmatch trials. The dataset for each block is stored in a text file. The first line in the text file is the letter presented on every trial. The second line is the condition corresponding to every letter in the first line ('m': this is a match trial; '-': this is a nonmatch trial). We have created many versions of the N-back task, including verbal ones and spatial ones.

## Prompt Example

Here we focus on the base version of verbal N-back tasks. We use the following format of prompts for $N = \{1, 2, 3\}$:

```
User:
Instruction: as a language model, you are asked to perform a 1-back task. A letter will be presented on every trial. Your task is to respond with 'm' whenever the letter presented is the same as the previous letter, and '-' whenever the letter presented is different from the previous letter. A strict rule is that you must not output anything other than 'm' or '-'. Now begins the task.

User:
{letter}
Model:
{-}(because this is the first letter)

User:
{letter}
Model:
{m/-}

...
```

Similar prompts are used for 2-back and 3-back tasks, where the model compares the current letter with the letter two or three trials ago, respectively.

## Metrics

We use exact match of the extraction results to calculate the hit rate, false alarm rate, and accuracy. $d'$ (detection sensitivity) is calculated as the $z$ score of hit rate minus the $z$ score of false alarm rate. In the case where the hit rate or false alarm rate is equal to either 0 or 1, they will be adjusted by 0.01 to handle the problem of $z$ score being infinite.

---

## Reproduction with Google Gemini API

This repository has been adapted to run experiments using the **Google Gemini API** (OpenAI-compatible interface). The original paper used ChatGPT (gpt-3.5-turbo); you can reproduce similar working memory capacity patterns with Gemini models.

### Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Key:**
   - Set the environment variable:
     ```bash
     export GEMINI_API_KEY="your-gemini-api-key"
     ```
   - Or edit `llm_client.py` and set `API_KEY` directly.
   - Get your API key from [Google AI Studio](https://aistudio.google.com/apikey).

3. **Run experiments:**
   - Navigate to the `experiments/` directory.
   - Run the desired Jupyter notebook, e.g.:
     - `verbal.ipynb` — base verbal N-back task
     - `verbal_with_noise.ipynb` — verbal task with noise
     - `verbal_with_feedback.ipynb` — verbal task with feedback
     - `verbal_think_by_step.ipynb` — verbal task with chain-of-thought reasoning
     - `spatial_3*3.ipynb` — spatial N-back task (3×3 grid)
     - `spatial_4*4.ipynb`, `spatial_5*5.ipynb`, `spatial_7*7.ipynb` — spatial tasks with larger grids
     - `spatial_abstraction.ipynb` — spatial task with abstract reasoning

### Default Model

The default model is `gemini-3-flash-preview`. You can change it in `llm_client.py` by modifying `DEFAULT_MODEL` (e.g., to `gemini-1.5-flash` or `gemini-1.5-pro` for better stability under high load).

### Results

Experimental results are saved in the `results/` directory (e.g., `all_trials_verbal.json`). Figures are generated in the `figures/` directory.

---

## Project Structure

```
├── llm_client.py          # Unified LLM client (Gemini API, OpenAI-compatible)
├── requirements.txt       # Python dependencies
├── experiments/           # Jupyter notebooks for each task variant
├── results/               # Saved trial data (JSON)
├── figures/               # Generated plots
└── letters/               # Letter sequences for verbal N-back tasks
```

---

## Citation

If you use this code or dataset, please cite the original paper:

```bibtex
@inproceedings{gong2024working,
  title={Working Memory Capacity of ChatGPT: An Empirical Study},
  author={Gong, Dongyu and Wan, Xingchen and Wang, Dingmin},
  booktitle={AAAI Conference on Artificial Intelligence},
  year={2024}
}
```
