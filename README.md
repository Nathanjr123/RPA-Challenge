# Template: Python - Browser automation with Playwright

This template leverages the new [Python framework](https://github.com/robocorp/robocorp), incorporating libraries from the same project. It's designed to provide a structured Python project with built-in logging and task control, eliminating the need to deal with underlying Python configurations. The environment includes commonly used libraries, streamlining your automation workflow. Browser automation is achieved seamlessly with `robocorp-browser` using Playwright.

👉 Explore other available templates via our tooling and on our [Portal](https://robocorp.com/portal/tag/template).

## Running

### Prerequisites
- Install [Robocorp CLI (RCC)](https://github.com/robocorp/rcc?tab=readme-ov-file#getting-started).
- Ensure you have a valid Robocorp Cloud account and API key.

### Setup
1. Clone this repository to your local machine.
2. Navigate to the project directory.

### Configuration
- Customize the search phrase and news category in the `solve_challenge` task in the `tasks.py` file.

### Execution
1. Open a terminal or command prompt.
2. Run the following command to execute the automation:
3. Sit back and relax while the bot handles the automation process.

### Results
🚀 After executing the bot, review the `log.html` located in the `output` folder for detailed logs.

## Dependencies

We strongly recommend managing your dependencies in the [conda.yaml](conda.yaml) file to control your Python environment and dependencies effectively.

<details>
<summary>🙋‍♂️ "Why not just pip install...?"</summary>

Think of [conda.yaml](conda.yaml) as an upgraded version of requirements.txt. With `conda.yaml`, you have full control over your Python environment, ensuring repeatability and consistency across different machines. By using `conda.yaml`:
- Avoid "Works on my machine" scenarios.
- Eliminate the need to manage Python installations on various machines.
- Specify the exact Python version your automation will run on.
- No more dependency resolution issues with pip.
- Access the entire [conda-forge](https://prefix.dev/channels/conda-forge) ecosystem seamlessly.

> Explore further with [these](https://github.com/robocorp/rcc/blob/master/docs/recipes.md#what-is-in-condayaml) resources.

</details>
<br/>

## Object-Oriented Model

The automation is structured around an object-oriented model, primarily consisting of the following components:
- `NewsProcessor`: Responsible for processing news data.
- `Browser`: Manages browser automation tasks.
- `solve_challenge`: The main task to solve the RPA challenge.

## Customization

### Changing Search Phrase and News Category

You can customize the search phrase and news category by modifying the `search_phrase` and `news_category` variables in the `solve_challenge` task located in the `tasks.py` file. Simply update these variables with the desired values before executing the automation.

### Modifying Automation Logic

If you need to adjust the automation logic or behavior, you can make changes directly in the `NewsProcessor` class within the `tasks.py` file. Here, you can add, remove, or modify methods to suit your requirements.

## What now?

🚀 Go ahead and tackle those challenges!

Start writing Python automation code and remember that AI/LLMs out there are becoming increasingly proficient at generating Python code tailored to specific requirements.

👉 Give [Robocorp ReMark 💬](https://chat.robocorp.com) a try.

For more information, refer to:
- [Robocorp Documentation](https://robocorp.com/docs)
- [Portal](https://robocorp.com/portal) for additional examples
- Follow our main [robocorp repository](https://github.com/robocorp/robocorp) for updates on libraries and frameworks.

