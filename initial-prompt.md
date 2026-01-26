ayudame a pensar y hacer brainstorming para la siguiente idea.
Te doy contexto para que entiendas mejor.
El contexto son post de linkedin donde he intentado relatar una historia. Ahora lo que quiero hacer es crear un repositorio publico, con una aplicacion, proceso o no se bien, que extraiga los commits de github, encuentre los que etsan marcados por una de las opciones y muestre tablas comparativas. Alguien me dio una idea: Hacer un recuento a modo de historial del ultimo año, como hace spotify con las canciones. Otro que hiciera un plugin para firefox o chrome. Otro que hiciera algo que otros puedan usar si comienzan a anotar sus commits con los tags de la metodologia. A mi se me ocurrio que la regla de generar un comit con la etiqueta ya puesta es un paso extra en la metodologia. En fin que vienen ideas... Ahora pego los posts de mas antiguo a mas reciente:

 Heikel Andres MolinaHeikel Andres Molina  • YouYou Software engineer with experience in backend development. I am passionate about working as a team to design and build better solutions.Software engineer with experience in backend development. I am passionate about working as a team to design and build better solutions. 5mo • 
 5 months ago • Visible to anyone on or off LinkedIn
Three months ago, I shared a project that grew out of a windsurf course, an AI-assisted app to help people quickly create polished PDF résumés via WhatsApp.

Back then, I promised to share a breakdown of how much of the code was written by me vs. by AI.

After weeks of world-class procrastination about actually crunching those numbers, I finally tried to calculate it… and realized: I have no way of knowing. Unless you track from day one, measuring human vs. AI contributions is surprisingly tricky: a challenge I’ve since learned is an actual research topic.

So here’s my new plan for future projects:

 - Commit more often

 - Tag AI-generated work with [AI] in commit messages

 - Build a dataset I can analyze over time

I’m curious: has anyone here found a practical way to track AI vs. human contribution

I just reinstalled my computer, and the IDE “forgot” the rule I use frequently. That reminded me of it: 

Rule: Always include git commit command after code changes
Behavior: Include a ready-to-run git commit command after every code change.
Format: git commit -m "<commit_message> [AI]"
Example: git commit -m "Some example here[human]"


Heikel Andres MolinaHeikel Andres Molina  • YouYou Software engineer with experience in backend development. I am passionate about working as a team to design and build better solutions.Software engineer with experience in backend development. I am passionate about working as a team to design and build better solutions. 1d • 
 1 day ago • Visible to anyone on or off LinkedIn
Five months ago, I asked a question I couldn’t answer.

I’d built an AI-assisted app (born during a windsurf course, because of course) and promised to share how much of the code was written by me vs. by AI.

When I finally sat down to measure it, I realized something uncomfortable:

I couldn’t.

Unless you track this from day one, separating human and AI contributions after the fact is basically impossible. That “oops” turned out to be a real research problem—and a useful one.

So I changed my approach.
Instead of measuring later, I started tagging as I go.

A simple framework I now use for Git commits in the age of AI

I use just three tags:

• [human]
• [ai]
• [human + ai]

The key rule:
Commits are tagged based on who produced the code in the commit, not who had the idea.

What the tags mean

• [human]
Code written entirely by a human. No AI-generated code included.

• [ai]
Code generated or modified entirely by AI. Human involvement may exist at the idea or prompt level, but no human-edited code appears in the commit.

• [human + ai]
A mix of human-written and AI-written code, or human edits applied after AI generation.

Why this matters

Human ideas often precede AI implementations—but ideas aren’t code.

If a commit contains only AI-generated code, it should be tagged [ai].
If human intent needs to be visible, commit it separately (specs, drafts, designs → [human]).

This keeps commit history:
• Honest
• Traceable
• Auditable
• Scalable as AI usage grows

In short:
Ideas belong to history. Tags belong to commits.

Curious how others are handling this—are you tracking AI contribution today, or planning to ignore the problem until future-you regrets it?

I keep seeing people say things like:
“90% of the code was written by AI”, “75%”, etc.

Honest question:
👉 how do you know?

Are you using an actual methodology to measure that?
A tool? A reproducible process?

I’m asking because a few months ago I tried to measure this in my own projects — and realized it’s far from obvious.

I ended up defining a methodology and applying it over several months before the numbers started to make sense.

I’ll share my own human vs. AI breakdown in another post.

Until then, I’m genuinely curious:
when someone says “X% was written by AI”, are we talking about data or intuition?
