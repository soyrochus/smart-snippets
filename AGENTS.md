

Refactor chat-peek.py so that

- function format_markdown  adds a horizontal line after a block of interacition between User and AI to make it more clear where the conversation delimiters are.

- function format_ascii generates truly coloured, rich formatting of the markdown.  Not just "bold". Different colours for 
- **User:** heading
- **AI:** header
    - common markdown elements, not just "bold"

- function  format_html should convert the output of format_markdown to html using a library. Add this library or other dependencies to 

- explain in the README that the project is not just intended to explain the capabilities of OpenAI but to demonstrate the power of vibecoding (explain what that is). Explain that we use Codex (https://platform.openai.com/docs/codex) , ChatGPT and Github Copilot