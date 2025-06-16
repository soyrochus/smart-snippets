
In src/bicameral_agent you find  a "bicameral agent" agent in Python, following these requirements: The agent must autonomously break down complex tasks, decide when to use tools, and recursively invoke itself to solve subtasks, all orchestrated by prompt instructions. The information it will get from an externally defined prompt (in the test case coming from /system_prompt.txt)

Provide answers to the following questions:

1. The current implementation works with a potent model. WIth lesser it seems to break (interrupting the loop in orchestrator)
Give me hypothesis why this is the case

2. It would seem that the current implementation is fragile. What are options to make it more robbust?

3. Would changing the orchestrator to a LangGraph implementation have any benefits?

4. Although called "Bicameral", there is not real distinction between "god voice" and "execution". What would a "real" implementatiojn look like? Woudl that strengthen the mechanism? ( I would imagine at the cost of more calls to the LLM)


Do NOT change any code. GIve me answers to the questions, please. 

