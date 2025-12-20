for agents. That paradigm is a tighter coupling between the model and a runtime environment.
Put simply, we think code is all we need.
We used to think agents in different domains will look very different. Each
one will need its own tools and scaffolding and that means we'll have a separate agent for each use case for each domain. Well, customization is
each domain. Well, customization is still important for each domain. The
agent underneath is actually more universal than we thought.
What we realized is that code is not just a use case but the universal interface to the digital world.
After we built cloud code, we realized that cloud code is actually a general purpose agent.
Think about generating a financial report. The model can call the API to
report. The model can call the API to pull in data and do research. It can
organize that data in the file system.
It can analyze it with Python and then synthesize the insight in old file format all through code. The core
scaffolding can suddenly become as thin as just bash and file system which is great and really scalable. But we very quickly run into a different problem
and that problem is domain expertise.
Who do you want doing your taxes? Is it
going to be Mahesh, the 300 IQ mathematical genius, or is it Barry, an experienced tax professional, right? I
would pick Barry every time. I don't
want Mahesh to figure out the 2025 tax code from first principles. I need
consistent execution from from a domain expert. As agents today are a lot like
expert. As agents today are a lot like Mahes. They're brilliant, but they lack
Mahes. They're brilliant, but they lack expertise.
They can do no more slow. They can do amazing things when you really put in the effort and give proper guidance, but they're often missing the important context up front. They can't really absorb your expertise super well, and
they don't learn over time.
That's why we created agent skills.
Skills are organized collections of files that package composable procedural knowledge for agents.
In other words, they're folders. This
simplicity is deliberate. We want
something that anyone human or agent can create and use as long as they have a computer. These also work with what you
computer. These also work with what you already have. You can version them in
already have. You can version them in Git, you can throw them in Google Drive and you can zip them up and share with your team. We have used files for uh as
your team. We have used files for uh as a primitive for decades and we like them. So why change now?
them. So why change now?
Because of that skills can also include a lot of scripts as tools. Traditional
tools have pretty obvious problems. Some tools have poorly written instructions and are pretty ambiguous and when the model is struggling, it can't really make a change to the tool. So, it's just kind of stuck with a code start problem
and they always live in the context window. Code solves some of these
window. Code solves some of these issues. It's self-documenting. It is
issues. It's self-documenting. It is
modifiable and can live in the file system until they're really needed and used. Here's an example of a script
used. Here's an example of a script inside of a skill. We kept seeing Claude write the same Python script over and over again to apply styling to slides.
So we just ask cloud to save it inside of the skill as a tool for his version for his future self. Now we can just run the script and that makes everything a lot more consistent and a lot more efficient.
At this point skills can contain a lot of information and we want to protect the context window so that we can fit in hundreds of skills and make them truly composable. That's why skills are
composable. That's why skills are progressively disclosed. At runtime,
progressively disclosed. At runtime, only this metadata is shown to the model just to indicate that he has the skill.
When an agent needs to use a skill, it can read in the rest of the skill.md,
which contains the core instruction and directory for the rest of the folder.
Everything else is just organized for ease of access. So that's all skills are. They're organized folders with
are. They're organized folders with scripts as tools.
Since our launch five weeks ago, this very simple design has translated into a very quickly growing ecosystem of thousands of skills. And we've seen this be split across a couple of different
types of skills. There are foundational skills, third party skills created by partners in the ecosystem, and skills built within an enterprise and within teams.
To start, foundational skills are those that give agents new general capabilities or domain specific capabilities that it didn't have before.
We ourselves with our launch built document skills that give Claude the ability to create and edit professional quality office documents. We're also
really excited to see people like Cadence build scientific research skills that give Claude new capabilities like EHR data analysis and using common
Python bioinformatics libraries better than it could before.
We've also seen partners in the ecosystem build skills that help Claude better with their own software and their own products. Browserbase is a pretty
own products. Browserbase is a pretty good example of this. They built a skill for their open- source browser automation tooling, stage hand. And now
Claude equipped that this skill and with stage hand can now go navigate the web and use a browser more effectively to get work done.
And notion launched a bunch of skills that help claude better understand your notion workspace and do deep research over your entire workspace.
And I think where I've seen the most excitement and traction with skills is within large enterprises. These are
company and team specific skills built for an organization.
We've been talking to Fortune 100s that are using skills as a way to teach agents about their organizational best practices and the weird and unique ways that they use this bespoke internal
software.
We're also talking to really large developer productivity teams. These are teams serving thousands or even tens of thousands of developers in an organization that are using skills as a
way to deploy agents like cloud code and teach them about code style best practices and other ways that they want their developers to work internally.
So all of these different types of skills are created and consumed by different people inside of an organization or in the world. But what
they have in common is anyone can create them and they give agents the new capabilities that they didn't have before.
So, as this ecosystem has grown, we've started to observe a couple of interesting trends. First, skills are
interesting trends. First, skills are starting to get more complex. The most
basic skill today can still be a skill.md markdown file with some prompts
skill.md markdown file with some prompts and some really basic instructions, but we're starting to see skills that package software, executables, binaries,
files, code, scripts, assets, and a lot more. And a lot of the skills that are
more. And a lot of the skills that are being built today might take minutes or hours to build and put into an agent.
But we think that increasingly much like a lot of the software we use today, these skills might take weeks or months to build and be maintained.
We're also seeing that this ecosystem of skills is complementing the existing ecosystem of MCP servers that was built up over the course of this year.
Developers are using and building skills that orchestrate workflows of multiple MCP tools stitched together to do more complex things with external data and
connectivity. And in these cases, MCP
connectivity. And in these cases, MCP MCP is providing the connection to the outside world while skills are providing the expertise.
And finally, and I think most excitingly for me personally, is we're seeing skills that are being built by people that aren't technical. These are people in functions like finance, recruiting,
accounting, legal, and a lot more. Um,
and I think this is pretty early validation of our initial idea that skills help people that aren't doing coding work extend these general agents and they make these agents more
accessible for the day-to-day of what these people are working on.
So tying this all together, let's talk about how these all fit into this emerging architecture of general agents.
First, we think this architecture is converging on a couple of things. The
first is this agent loop that helps manage the the model's internal context and manages what tokens are going in and out. And this is coupled with a runtime
out. And this is coupled with a runtime environment that provides the agent with a file system and the ability to read and write code.
This agent, as many of us have done throughout this year, can be connected to MCP servers. And these are tools and data from the outside world that make the the agent more relevant and more
effective.
And now we can give the same agent a library of hundreds or thousands of skills that it can decide to pull into context only at runtime when it's
deciding to work on a particular task.
Today, giving an agent a new capability in a new domain might just involve equipping it with the right set of MCP servers and the right library of skills.
And this emerging pattern of an agent with an MCP server and a set of skills is something that's already helping us at Enthropic deploy Claude to new verticals. Just after we launched skills
verticals. Just after we launched skills 5 weeks ago, we immediately launched new offerings in financial services and life sciences. And each of these came with a
sciences. And each of these came with a set of MCP servers and a set of skills that immediately make Claude more effective for professionals in each of these domains.
We're also starting to think about some of the other open questions and areas that we want to focus on for how skills evolve in the future as they start to become more complex. We really want to
support developers, enterprises, and other skill builders by starting to treat skills like we treat software.
This means exploring testing and evaluation, better tooling to make sure that these agents are loading and triggering skills at the right time and
for the right task, and tooling to help measure the output quality of an agent equipped with the skill to make sure that's on par with what the agent is supposed to be doing.
We'd also like to focus on versioning.
as a skill evolves and the resulting agent behavior uh evolves, we want this to be uh clearly tracked and to have a clear lineage over time.
And finally, we'd also like to explore skills that can explicitly depend on and refer to either other skills, MCP servers, and dependencies and packages within the agents environment. We think
that this is going to make agents a lot more predictable in different runtime environments. and the composability of
environments. and the composability of multiple skills together will help agents like Claude elicit even more complex and relevant behavior from these agents.
Overall, these set of things should hopefully make skills easier to build and easier to integrate into agent products, even those besides claude.
Finally, a huge part of the value of skills we think is going to come from sharing and distribution. Barry and I think a lot about the future of companies that are deploying these
agents at scale. And the vision that excites us most is one of a collecting and collective and evolving knowledge base of capabilities that's curated by
people and agents inside of an organization. We think skills are a big
organization. We think skills are a big step towards this vision. They provide
the procedural knowledge for your agents to do useful things. And as you interact with an agent and give it feedback and more institutional knowledge, it starts to get better and all of the agents
inside your team and your org get better as well. And when someone joins your
as well. And when someone joins your team and starts using Claude for the first time, it already knows what your team cares about. It knows about your day-to-day and it knows about how to be most effective for the work that you're doing.
And as this grows and this ecosystem starts to develop even more, this was going to this compounding value is going to extend outside of just your organ into the broader community. So just like when someone else across the world
builds an MCP server that makes your agent more useful, a skill built by someone else in the community will help make your own agents more capable,
reliable, and useful as well.
This vision of a evolving knowledge base gets even more powerful when claw starts to create these skills. We design skills specifically as a concrete steps towards uh continuous learning.
When you first start using cloud, this standardized format gives a very important guarantee. Anything that cloud
important guarantee. Anything that cloud writes down can be used efficiently by a future version of itself. This makes the learning actually transferable.
As you build up the context skills makes the concept of memory more tangible.
They don't capture everything. They
don't capture every type of information.
Just procedural knowledge that cloud can use on specific tasks.
When you have worked with cloud for quite a while, the flexibility of skills matters even more. Cloud can acquire new capabilities instantly, evolve them as needed, and then drop the ones that
become obsolete. This is what we have
become obsolete. This is what we have always known. The power of in in context
always known. The power of in in context learning makes this a lot more cost- effective for information that change on daily basis.
Our goal is that claude on day 30 of working with you is going to be a lot better on cloud on day one. CL can
already create skills for you today using our skill creator skill and we're going to continue pushing in that direction.
We're going to conclude by comparing the agent stack to what we have already seen computing.
In a rough analogy, models are like processors. Both require massive
processors. Both require massive investment and contain immense potential, but only so useful by themselves.
Then we start building operating system.
The OS made processors far more valuable by orchestrating the processes, resources, and data around the processor. In AI, we believe that agent
processor. In AI, we believe that agent runtime is starting to play this role.
We're all trying to build the cleanest, most efficient, and most scalable uh abstractions to get the right tokens in and out of the model.
But once we have a platform, the real value comes from applications. A few
companies build uh processors and operating systems, but millions of developers like us have built software that encoded domain expertise and our unique points of view. We hope that
skills can help us open up this layer for everyone. This is where we get
for everyone. This is where we get creative and solve concrete problem for ourselves, for each other, and for the world just by putting stuff in the folder. So skills are just the starting
folder. So skills are just the starting point.
To close out, we think we're now converging on this general architecture for general agents. We've created skills as a new paradigm for shipping and sharing new capabilities. So we think
it's time to stop rebuilding agents and start building skills instead. And if
you're excited about this, come work with us and start building some skills today. Thank you.
today. Thank you.