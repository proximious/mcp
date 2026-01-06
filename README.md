# mcp
Learning how to make a MCP server for UFC fighter stats to help with betting lines.

# What is MCP server?
MCP stands for Model Context Protocol, which is a way for tools and services to talk to AI models in a structued method.

# Why is it useful?
Using a MCP, we can more safely use AI on databases and internal services (commonly automation scripts) without giving the model full access.

# What else can we do with it?
In this example, I found using a MCP for data analytics works well. We can load in CSV files, query a database, and perform analytics and our MCP server would return a structured result

# Resources used
For most of this, I googled MCP and found some websites; these are the most used ones.
I also used ChatGPT to explain error messages and write some code (annotated when it was used).

https://github.com/modelcontextprotocol (Very useful information in many different languages)

https://github.com/Greco1899/scrape_ufc_stats (Found UFC fighter/fight data)