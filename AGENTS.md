
In src/bicameral_agent you find  a "bicameral agent" agent in Python, following these requirements: The agent must autonomously break down complex tasks, decide when to use tools, and recursively invoke itself to solve subtasks, all orchestrated by prompt instructions. The information it will get from an externally defined prompt (in the test case coming from /system_prompt.txt)

The current implementation has a incomplete working verion. 

Fully implement all the tool used in run_orchestrator so a full agentic workflow which can run continously until the stop condition. 


Implement in system_prompt.txt a simple english language excsersise:

You are a concise English-grammar coach. 
1️⃣ Show the base sentence, 
2️⃣ ask learner for negative & question forms, 
3️⃣ evaluate accuracy, 
4️⃣ give one-line explanation if wrong, 5️⃣ stop after both are correct.

Change the prompt where needed to have the agent follow the flow completely autonously, interacting with the userr.

