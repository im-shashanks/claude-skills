So I am in pursuit of creating a coding setup/framework, called shaktra, using claude code features like rules, skills, mcp, hooks,
  etc. This framework will have opinionated workflow using different main agents and subagents in tandem to create industry          
  standard, reliable, production code. This framework/setup is going to follow agile methodology in some ways. Now, we don't have to
  work on everything from scratch there is already a version of it I have been using. However, that setup was just built without much
  planning and therefore, it has gotten very bloated, messy, and things have been added on to pre-existing items haphazardly. Its  
  currently very difficult to maintain. Therefore, I would like to take this opportunity to build this setup very carefuly         
  scrutinizing everything and in a very maintainable way. At the end, There is a potential for us to even package this setup as a  
  plugin to be distributed. To start off lets go extremely carefully step by step. Lets begin by analyzing the existing framework
  (Forge) on different dimensions - how is everything laid out, how does the framework function, what are the messy parts, what are  
  the current gaps, what is the flow and many more dimensions. In order to do this First come up with list of questions(dimensions),
  that will help you understand the framework at its core, then spawn any number of subagents, I believe you'll need a min of 5, but
  you decide on the max, to extensively explore the framework around those areas you identified. You should only be orchestrating the
  work through the subagents and aggregate the info at the end if required. The subagents should be able to write to the files about
  their analysis, and each sub-agent should be extremely focused on specific areas of exploration. I want this exploratio to be  
  extensive and you should get over 90% of info about the framework looking at the end analysis. Use the docs/Forge-analysis folder
  to store the analsys by subagents. The framework location is at ~/workspace/applications/forge-claudify. Ask any questions before   
  proceeding with this extensive task. You DO NOT need to save the contents from forge-claudify, in the future, we can directly        
  reference that repo to get the content, for now only focus on understanding how everything works, and how we can utilize it in our   
  case. 