# influence-tree

## Setup

### Environment Setup

This project uses conda for environment management. To set up the environment:

1. Make sure you have conda installed. If not, you can download it from [here](https://docs.conda.io/en/latest/miniconda.html).

2. Create the environment from the `environment.yml` file:
   ```bash
   conda env create -f environment.yml
   ```

3. Activate the environment:
   ```bash
   conda activate influence-tree
   ```

### API Key Configuration

This project uses the OpenAI API. To configure your API key:

1. Create a `.env` file in the project root directory
2. Add your OpenAI API key to the file:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

The script builds a musical influence tree using breadth-first search:

```bash
python build_tree.py --max_calls 10
```

### Key Features

- **Persistent Storage**: Results are saved to `influence_results.json` between runs
- **Incremental Processing**: Subsequent runs continue from where previous runs left off
- **Duplicate Prevention**: Each musician is only queried once
- **Command Line Control**:
  - `--max_calls`: Set maximum number of LLM calls per run (default: 10)

### Output

The script creates two main data structures:
1. `musicians`: Dictionary with detailed information about each musician
2. `influence_graph`: Mapping of musicians to their direct influences

Results are automatically saved to `influence_results.json` after each run.