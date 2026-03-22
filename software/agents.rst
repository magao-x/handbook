Using AI Agents
======================================

AI Policy
-----------------------
You are encouraged to use AI to help you write code.  However, you are still responsible for the physics and engineering.  The following guidelines are intended to ensure that we write code that helps MagAO-X achieve its goals, but that we also learn about how the universe works and document what we learn.

Standard Workflow
----------------------
You must still follow the standard workflow using feature branches, testing from your home directory, and pull-request to get reviewed before merging.

AGENTS.md
---------------------------
At the top level of the MagAO-X repo there is a file named `AGENTS.md`_.  This file contains a set of guidelines for an AI agent to
follow.  While `AGENTS.md`_ is supposed to be a standard name, in practice you should always remind your agent to refer to that file.

.. _AGENTS.md: https://github.com/magao-x/MagAOX/blob/dev/AGENTS.md

If you develop a new rule while working with AI, ask it to update `AGENTS.md`_ and include it in your feature branch.

Plans
--------------------------
The current best practice is to use AI in planning mode.  Describe your problem and ask the AI to create a plan.  Then iterate on the
plan as needed, keeping the planning document (see below) up to date.  Once you are happy with the plan, then have the agent implement it.

Planning Documents
~~~~~~~~~~~~~~~~~~~~~~~~~
In the MagAO-X repo there is now a folder called `agents/plans`_.  One thing that has proven useful is to write your specifications in a
new file there.  Then your prompt to the AI is simply to review that file, make a plan, and write out the plan to that same file.  The
intention is that you then commit that file as part of your feature development.  The benefit to this practice will be that we now have
a record of the engineering you did to create the feature.

.. _agents/plans: https://github.com/magao-x/MagAOX/tree/dev/agents/plans

Blast Radius -- Follow the Rules
----------------------------------------
It is incredibly easy to "change all the things", or "fix all the bugs", with AI.  AI agents are always willing to work, and often ask
to go further if they recognize more problems.  Try to avoid this.  We consider it good engineering practice to make small focused
changes and test them, and slowly expand.  This is why it is crucial to follow the development guidelines and our git-branch-PR workflow
so that we can maintain some semblance of traceability and recoverability.
