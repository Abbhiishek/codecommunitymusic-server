from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from django.core.cache import cache
from  datetime import datetime
import json
import random


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
# end point to list all the users /allusers

quotes = [
    {
       "id":"5a6ce86e2af929789500e7e4",
       "author":"Edsger W. Dijkstra",
       "en":"Computer Science is no more about computers than astronomy is about telescopes."
    },
    {
       "id":"5a6ce86e2af929789500e7d7",
       "author":"Edsger W. Dijkstra",
       "en":"Simplicity is prerequisite for reliability."
    },
    {
       "id":"5a6ce86d2af929789500e7ca",
       "author":"Edsger W. Dijkstra",
       "en":"The computing scientist’s main challenge is not to get confused by the complexities of his own making."
    },
    {
       "id":"5a6ce86f2af929789500e7f3",
       "author":"Edsger W. Dijkstra",
       "en":"If debugging is the process of removing software bugs, then programming must be the process of putting them in."
    },
    {
       "id":"5a6ce86e2af929789500e7d9",
       "author":"Edsger W. Dijkstra",
       "en":"A program is like a poem: you cannot write a poem without writing it. Yet people talk about programming as if it were a production process and measure „programmer productivity“ in terms of „number of lines of code produced“. In so doing they book that number on the wrong side of the ledger: We should always refer to „the number of lines of code spent“."
    },
    {
       "id":"5a6ce86f2af929789500e7f8",
       "author":"Tony Hoare",
       "en":"There are two ways of constructing a software design: One way is to make it so simple that there are obviously no deficiencies, and the other way is to make it so complicated that there are no obvious deficiencies. The first method is far more difficult."
    },
    {
       "id":"5a6ce86f2af929789500e807",
       "author":"Jeff Hammerbacher",
       "en":"The best minds of my generation are thinking about how to make people click ads."
    },
    {
       "id":"5a6ce86f2af929789500e7f9",
       "author":"Edsger W. Dijkstra",
       "en":"The tools we use have a profound and devious influence on our thinking habits, and therefore on our thinking abilities."
    },
    {
       "id":"5a6ce86f2af929789500e7f5",
       "author":"Edsger W. Dijkstra",
       "en":"How do we convince people that in programming simplicity and clarity — in short: what mathematicians call \"elegance\" — are not a dispensable luxury, but a crucial matter that decides between success and failure?"
    },
    {
       "id":"5a6ce86f2af929789500e80b",
       "author":"Fred Brooks",
       "en":"Adding manpower to a late software project makes it later."
    },
    {
       "id":"5a6ce86f2af929789500e809",
       "author":"Michael Stal",
       "en":"Sometimes there is a silver bullet for boosting software engineering productivity. But you need to shoot the right person."
    },
    {
       "id":"5a6ce86f2af929789500e815",
       "author":"Fred Brooks",
       "en":"Nine women can't make a baby in one month."
    },
    {
       "id":"5a6ce86f2af929789500e81a",
       "author":"Jeff Sickel",
       "en":"Deleted code is debugged code."
    },
    {
       "id":"5a6ce86f2af929789500e826",
       "author":"Ken Thompson",
       "en":"When in doubt, use brute force."
    },
    {
       "id":"5a6ce86f2af929789500e814",
       "author":"Fred Brooks",
       "en":"When a task cannot be partitioned because of sequential constraints, the application of more effort has no effect on the schedule. The bearing of a child takes nine months, no matter how many women are assigned."
    },
    {
       "id":"5a6ce86f2af929789500e816",
       "author":"Fred Brooks",
       "en":"If each part of the task must be separately coordinated with each other part, the effort increases as n(n-1)/2. Three workers require three times as much pairwise intercommunication as two; four require six times as much as two."
    },
    {
       "id":"5a6ce86f2af929789500e818",
       "author":"Fred Brooks",
       "en":"Having a system architect is the most important single step toward conceptual integrity. After teaching a software engineering laboratory more than 20 times, I came to insist that student teams as small as four people choose a manager and a separate architect."
    },
    {
       "id":"5a6ce86f2af929789500e80f",
       "author":"Fred Brooks",
       "en":"The programmer, like the poet, works only slightly removed from pure thought-stuff. He builds his castles in the air, from air, creating by exertion of the imagination. Few media of creation are so flexible, so easy to polish and rework, so readily capable of realizing grand conceptual structures."
    },
    {
       "id":"5a6ce86f2af929789500e821",
       "author":"Fred Brooks",
       "en":"The first false assumption that underlies the scheduling of systems programming is that all will go well, i.e., that each task will hike only as long as it \"ought\" to take. A large programming effort, however, consists of many tasks, some chained end-to-end. The probability that each will go well becomes vanishingly small."
    },
    {
       "id":"5a6ce86f2af929789500e81e",
       "author":"Donald Knuth",
       "en":"We should forget about small efficiencies, say about 97% of the time: premature optimization is the root of all evil. Yet we should not pass up our opportunities in that critical 3%."
    },
    {
       "id":"5a6ce86f2af929789500e824",
       "author":"Ken Thompson",
       "en":"One of my most productive days was throwing away 1,000 lines of code."
    },
    {
       "id":"5a6ce86f2af929789500e825",
       "author":"Grace Hopper",
       "en":"One accurate measurement is worth more than a thousand expert opinions."
    },
    {
       "id":"5a6ce86f2af929789500e80d",
       "author":"Fred Brooks",
       "en":"What one programmer can do in one month, two programmers can do in two months."
    },
    {
       "id":"5a6ce86f2af929789500e82e",
       "author":"Rick Osborne",
       "en":"Always code as if the guy who ends up maintaining your code will be a violent psychopath who knows where you live."
    },
    {
       "id":"5a6ce86f2af929789500e830",
       "author":"John Ousterhout",
       "en":"A program that produces incorrect results twice as fast is infinitely slower."
    },
    {
       "id":"5a6ce86f2af929789500e828",
       "author":"Poul Anderson",
       "en":"I have yet to see any problem, however complicated, which when looked at in the right way, did not become more complicated."
    },
    {
       "id":"5a6ce86f2af929789500e82a",
       "author":"Robert C. Martin",
       "en":"Cleaning code does NOT take time. NOT cleaning code does take time."
    },
    {
       "id":"5a6ce86f2af929789500e837",
       "author":"David Gelernter",
       "en":"Beauty is more important in computing than anywhere else in technology because software is so complicated. Beauty is the ultimate defense against complexity."
    },
    {
       "id":"5a6ce86f2af929789500e833",
       "author":"Edward V. Berard",
       "en":"Walking on water and developing software from a specification are easy if both are frozen."
    },
    {
       "id":"5a6ce86f2af929789500e836",
       "author":"Brian Kernighan",
       "en":"Debugging is twice as hard as writing the code in the first place. Therefore, if you write the code as cleverly as possible, you are, by definition, not smart enough to debug it."
    },
    {
       "id":"5a6ce86f2af929789500e838",
       "author":"Brian Kernighan",
       "en":"Controlling complexity is the essence of computer programming."
    },
    {
       "id":"5a6ce86f2af929789500e83f",
       "author":"Chris Wenham",
       "en":"Debugging time increases as a square of the program’s size."
    },
    {
       "id":"5a6ce86f2af929789500e82c",
       "author":"Seymour Cray",
       "en":"The trouble with programmers is that you can never tell what a programmer is doing until it’s too late."
    },
    {
       "id":"5a6ce86f2af929789500e843",
       "author":"Ron Jeffries",
       "en":"Code never lies, comments sometimes do."
    },
    {
       "id":"5a6ce86f2af929789500e845",
       "author":"Laurence J. Peter",
       "en":"Some problems are so complex that you have to be highly intelligent and well informed just to be undecided about them."
    },
    {
       "id":"5a6ce86f2af929789500e841",
       "author":"Poul-Henning Kamp",
       "en":"Make a guess, double the number, and then move to the next larger unit of time. This rule scales tasks in a very interesting way: a one-minute task explodes by a factor of 120 to take two hours. A one-hour job explodes by \"only\" a factor 48 to take two days, while a one-day job grows by a factor of 14 to take two weeks."
    },
    {
       "id":"5a6ce86f2af929789500e847",
       "author":"Albert Einstein",
       "en":"I have no special talent. I am only passionately curious."
    },
    {
       "id":"5a6ce86f2af929789500e849",
       "author":"Robert C. Martin",
       "en":"The proper use of comments is to compensate for our failure to express ourself in code."
    },
    {
       "id":"5a6ce86f2af929789500e852",
       "author":"Rob Pike",
       "en":"When there is no type hierarchy you don’t have to manage the type hierarchy."
    },
    {
       "id":"5a6ce86f2af929789500e856",
       "author":"Steve Jobs",
       "en":"Everybody should learn to program a computer, because it teaches you how to think."
    },
    {
       "id":"5a6ce86f2af929789500e84f",
       "author":"Chris Sacca",
       "en":"Simplicity is hard to build, easy to use, and hard to charge for. Complexity is easy to build, hard to use, and easy to charge for."
    },
    {
       "id":"5a6ce8702af929789500e85a",
       "author":"Bill Gates",
       "en":"Measuring programming progress by lines of code is like measuring aircraft building progress by weight."
    },
    {
       "id":"5a6ce8702af929789500e85e",
       "author":"William Wulf",
       "en":"More computing sins are committed in the name of efficiency (without necessarily achieving it) than for any other single reason - including blind stupidity."
    },
    {
       "id":"5a6ce8702af929789500e860",
       "author":"Edsger W. Dijkstra",
       "en":"Testing can be a very effective way to show the presence of bugs, but it is hopelessly inadequate for showing their absence."
    },
    {
       "id":"5a6ce8702af929789500e864",
       "author":"Albert Einstein",
       "en":"Imagination is more important than knowledge."
    },
    {
       "id":"5a6ce8702af929789500e862",
       "author":"Buckminster Fuller",
       "en":"When I am working on a problem I never think about beauty. I think only how to solve the problem. But when I have finished, if the solution is not beautiful, I know it is wrong."
    },
    {
       "id":"5a6ce86f2af929789500e84b",
       "author":"Sean Parent",
       "en":"Good code is short, simple, and symmetrical - the challenge is figuring out how to get there."
    },
    {
       "id":"5a6ce8702af929789500e868",
       "author":"Linus Torvalds",
       "en":"If you think your users are idiots, only idiots will use it."
    },
    {
       "id":"5a6ce8702af929789500e872",
       "author":"Albert Einstein",
       "en":"Once you stop learning you start dying."
    },
    {
       "id":"5a6ce8702af929789500e884",
       "author":"Kevlin Henney",
       "en":"No code is faster than no code."
    },
    {
       "id":"5a6ce8702af929789500e86c",
       "author":"Richard P. Gabriel",
       "en":"Over half of the time you spend working on a project is spent thinking, and no tool, no matter how advanced, can think for you."
    },
    {
       "id":"5a6ce8702af929789500e86e",
       "author":"Edsger W. Dijkstra",
       "en":"We could, for instance, begin with cleaning up our language by no longer calling a bug a bug but by calling it an error. It is much more honest because it squarely puts the blame where it belongs, viz. with the programmer who made the error. The animistic metaphor of the bug that maliciously sneaked in while the programmer was not looking is intellectually dishonest as it disguises that the error is the programmer's own creation. The nice thing of this simple change of vocabulary is that it has such a profound effect: while, before, a program with only one bug used to be \"almost correct\", afterwards a program with an error is just \"wrong\"."
    },
    {
       "id":"5a6ce8702af929789500e88b",
       "author":"Stewart Brand",
       "en":"Once a new technology starts rolling, if you’re not part of the steamroller, you’re part of the road."
    },
    {
       "id":"5a6ce8702af929789500e887",
       "author":"John Gall (author)",
       "en":"A complex system that works is invariably found to have evolved from a simple system that worked. The inverse proposition also appears to be true: A complex system designed from scratch never works and cannot be made to work."
    },
    {
       "id":"5a6ce8702af929789500e889",
       "author":"Henry Petroski",
       "en":"The most amazing achievement of the computer software industry is its continuing cancellation of the steady and staggering gains made by the computer hardware industry."
    },
    {
       "id":"5a6ce8702af929789500e88e",
       "author":"Carl Friedrich Gauss",
       "en":"I am never satisfied until I have said as much as possible in a few words, and writing briefly takes far more time than writing at length."
    },
    {
       "id":"5a6ce8702af929789500e890",
       "author":"Bjarne Stroustrup",
       "en":"There are only two kinds of languages: the ones people complain about and the ones nobody uses."
    },
    {
       "id":"5a6ce8702af929789500e892",
       "author":"Pamela Zave",
       "en":"The purpose of software engineering is to control complexity, not to create it."
    },
    {
       "id":"5a6ce8702af929789500e89a",
       "author":"Dennis Ritchie",
       "en":"Unix is simple. It just takes a genius to understand its simplicity."
    },
    {
       "id":"5a6ce8702af929789500e89c",
       "author":"Dennis Ritchie",
       "en":"A language that doesn’t have everything is actually easier to program in than some that do."
    },
    {
       "id":"5a6ce8702af929789500e8a2",
       "author":"Richard Feynman",
       "en":"What I cannot build, I do not understand."
    },
    {
       "id":"5a6ce8702af929789500e8a6",
       "author":"Albert Einstein",
       "en":"Any intelligent fool can make things bigger, more complex, and more violent. It takes a touch of genius – and a lot of courage – to move in the opposite direction."
    },
    {
       "id":"5a6ce8702af929789500e898",
       "author":"Lawrence Flon",
       "en":"There is no programming language, no matter how structured, that will prevent programmers from making bad programs."
    },
    {
       "id":"5a6ce8702af929789500e8a8",
       "author":"Martin Fowler",
       "en":"Any fool can write code that a computer can understand. Good programmers write code that humans can understand."
    },
    {
       "id":"5a6ce8702af929789500e894",
       "author":"Joe Armstrong (programmer)",
       "en":"The problem with object-oriented languages is they’ve got all this implicit environment that they carry around with them. You wanted a banana but what you got was a gorilla holding the banana and the entire jungle."
    },
    {
       "id":"5a6ce8702af929789500e86a",
       "author":"Ken Thompson",
       "en":"You can’t trust code that you did not totally create yourself."
    },
    {
       "id":"5a6ce8702af929789500e8a4",
       "author":"Albert Einstein",
       "en":"A clever person solves a problem. A wise person avoids it."
    },
    {
       "id":"5a6ce8702af929789500e8ac",
       "author":"Bjarne Stroustrup",
       "en":"The most important single aspect of software development is to be clear about what you are trying to build."
    },
    {
       "id":"5a6ce8702af929789500e8aa",
       "author":"Jonathan Shewchuk",
       "en":"The only sin is to make a choice without knowing you are making one."
    },
    {
       "id":"5a6ce8702af929789500e8b0",
       "author":"Ryan Singer",
       "en":"So much complexity in software comes from trying to make one thing do two things."
    },
    {
       "id":"5a6ce8702af929789500e8b2",
       "author":"P. J. Plauger",
       "en":"Hofstadter's Law: It always takes longer than you expect, even when you take into account Hofstadter's Law."
    },
    {
       "id":"5a6ce8702af929789500e8b6",
       "author":"John Johnson",
       "en":"First, solve the problem. Then, write the code."
    },
    {
       "id":"5a6ce8702af929789500e8b4",
       "author":"Doug Linder",
       "en":"A good programmer is someone who looks both ways before crossing a one-way street."
    },
    {
       "id":"5a6ce8702af929789500e8b8",
       "author":"David Wheeler (computer scientist)",
       "en":"Compatibility means deliberately repeating other people’s mistakes."
    },
    {
       "id":"5a6ce8702af929789500e8ba",
       "author":"Jeremy S. Anderson",
       "en":"There are two major products that come out of Berkeley: LSD and UNIX. We don't believe this to be a coincidence."
    },
    {
       "id":"5a6ce8702af929789500e8bc",
       "author":"Edsger W. Dijkstra",
       "en":"The competent programmer is fully aware of the strictly limited size of his own skull; therefore he approaches the programming task in full humility, and among other things he avoids clever tricks like the plague"
    },
    {
       "id":"5a6ce8702af929789500e8ae",
       "author":"Joshua Bloch",
       "en":"When in doubt, leave it out."
    },
    {
       "id":"5a6ce8702af929789500e8be",
       "author":"Linus Torvalds",
       "en":"I will, in fact, claim that the difference between a bad programmer and a good one is whether he considers his code or his data structures more important. Bad programmers worry about the code. Good programmers worry about data structures and their relationships."
    },
    {
       "id":"5a6ce8702af929789500e8ce",
       "author":"Albert Einstein",
       "en":"Never memorize something that you can look up."
    },
    {
       "id":"5a6ce8702af929789500e8cc",
       "author":"Richard Hamming",
       "en":"Mathematicians stand on each others' shoulders and computer scientists stand on each others' toes."
    },
    {
       "id":"5a72399510263e0c45cb6cfa",
       "author":"Edsger W. Dijkstra",
       "en":"LISP has assisted a number of our most gifted fellow humans in thinking previously impossible thoughts."
    },
    {
       "id":"5a6ce8702af929789500e8c6",
       "author":"Bjarne Stroustrup",
       "en":"An organisation that treats its programmers as morons will soon have programmers that are willing and able to act like morons only."
    },
    {
       "id":"5a82224c89919d0004b357ce",
       "author":"Anonymous",
       "en":"The button is working, only, it cannot be seen."
    },
    {
       "id":"5a8225ee89919d0004b357d0",
       "author":"Douglas Crockford",
       "en":"Don't worry about anything. Just do what you can and be the best you can be."
    },
    {
       "id":"5a82b607fc716e0004373f53",
       "author":"Tom DeMarco",
       "en":"The business of software building isn't really high-tech at all. It's most of all a business of talking to each other and writing things down."
    },
    {
       "id":"5a6ce8702af929789500e8ca",
       "author":"Paul Graham (programmer)",
       "en":"In programming the hard part isn’t solving problems, but deciding what problems to solve."
    },
    {
       "id":"5a82cd0efc716e0004373f56",
       "author":"Tom DeMarco",
       "en":"The manager's function is not to make people work, but to make it possible for people to work."
    },
    {
       "id":"5a82c90cfc716e0004373f55",
       "author":"Tom DeMarco",
       "en":"People under pressure don’t work better; they just work faster."
    },
    {
       "id":"5a8946eda578110004299a3b",
       "author":"Donald Knuth",
       "en":"My main conclusion after spending ten years of my life working on the TEX project is that software is hard. It’s harder than anything else I’ve ever had to do."
    },
    {
       "id":"5a82cd5ffc716e0004373f57",
       "author":"Donald Knuth",
       "en":"Science is what we understand well enough to explain to a computer. Art is everything else we do."
    },
    {
       "id":"5a896544a12a0e0004c76124",
       "author":"Donald Knuth",
       "en":"We have seen that computer programming is an art, because it applies accumulated knowledge to the world, because it requires skill and ingenuity, and especially because it produces objects of beauty."
    },
    {
       "id":"5a82cd91fc716e0004373f58",
       "author":"Donald Knuth",
       "en":"Email is a wonderful thing for people whose role in life is to be on top of things. But not for me; my role is to be on the bottom of things. What I do takes long hours of studying and uninterruptible concentration."
    },
    {
       "id":"5a8e9b5884a8f2000482568b",
       "author":"Kevlin Henney",
       "en":"Less code equals less bugs."
    },
    {
       "id":"5a91370b2141d30004b42e58",
       "author":"Charles Babbage",
       "en":"As soon as an Analytical Engine exists, it will necessarily guide the future course of science."
    },
    {
       "id":"5a9137d72141d30004b42e59",
       "author":"Charles Babbage",
       "en":"The errors which arise from the absence of facts are far more numerous and more durable than those which result from unsound reasoning respecting true data."
    },
    {
       "id":"5a9138442141d30004b42e5a",
       "author":"Charles Babbage",
       "en":"We have already mentioned what may, perhaps, appear paradoxical to some of our readers, — that the division of labour can be applied with equal success to mental as to mechanical operations, and that it ensures in both the same economy of time."
    },
    {
       "id":"5a9139472141d30004b42e5b",
       "author":"Charles Babbage",
       "en":"On two occasions I have been asked [by members of Parliament]: \"Pray, Mr. Babbage, if you put into the machine wrong figures, will the right answers come out?\" I am not able rightly to apprehend the kind of confusion of ideas that could provoke such a question."
    },
    {
       "id":"5a91be60346ab3000418a760",
       "author":"Edsger W. Dijkstra",
       "en":"As long as there were no machines, programming was no problem at all; when we had a few weak computers, programming became a mild problem, and now we have gigantic computers, programming has become an equally gigantic problem."
    },
    {
       "id":"5a91e12fc4240c0004265950",
       "author":"Edsger W. Dijkstra",
       "en":"The use of COBOL cripples the mind; its teaching should, therefore, be regarded as a criminal offense."
    },
    {
       "id":"5a91d1c1c4240c000426594f",
       "author":"Edsger W. Dijkstra",
       "en":"If you want more effective programmers, you will discover that they should not waste their time debugging, they should not introduce the bugs to start with."
    },
    {
       "id":"5a91e150c4240c0004265951",
       "author":"Edsger W. Dijkstra",
       "en":"It is practically impossible to teach good programming to students that have had a prior exposure to BASIC: as potential programmers they are mentally mutilated beyond hope of regeneration."
    },
    {
       "id":"5a91e27ec4240c0004265953",
       "author":"Edsger W. Dijkstra",
       "en":"A picture may be worth a thousand words, a formula is worth a thousand pictures."
    },
    {
       "id":"5a91e224c4240c0004265952",
       "author":"Edsger W. Dijkstra",
       "en":"I mean, if 10 years from now, when you are doing something quick and dirty, you suddenly visualize that I am looking over your shoulders and say to yourself \"Dijkstra would not have liked this\", well, that would be enough immortality for me."
    },
    {
       "id":"5a91bc8f346ab3000418a75f",
       "author":"Edsger W. Dijkstra",
       "en":"Don't blame me for the fact that competent programming will be too difficult for \"the average programmer\" — you must not fall into the trap of rejecting a surgical technique because it is beyond the capabilities of the barber in his shop around the corner."
    },
    {
       "id":"5a91e37bc4240c0004265955",
       "author":"John von Neumann",
       "en":"Young man, in mathematics you don't understand things. You just get used to them."
    },
    {
       "id":"5a91e40ec4240c0004265957",
       "author":"Dennis Ritchie",
       "en":"C is quirky, flawed, and an enormous success."
    },
    {
       "id":"5a91e2d0c4240c0004265954",
       "author":"Edsger W. Dijkstra",
       "en":"It is not the task of the University to offer what society asks for, but to give what society needs."
    },
    {
       "id":"5a895d1ba5f8bf3df4485d1d",
       "author":"Donald Knuth",
       "en":"By understanding a machine-oriented language, the programmer will tend to use a much more efficient method; it is much closer to reality."
    },
    {
       "id":"5a91e459c4240c0004265958",
       "author":"Dennis Ritchie",
       "en":"Another danger is that commercial pressures of one sort or another will divert the attention of the best thinkers from real innovation to exploitation of the current fad, from prospecting to mining a known lode."
    },
    {
       "id":"5a91e51dc4240c0004265959",
       "author":"Bjarne Stroustrup",
       "en":"Within C++, there is a much smaller and cleaner language struggling to get out."
    },
    {
       "id":"5a91e560c4240c000426595a",
       "author":"Bjarne Stroustrup",
       "en":"Anybody who comes to you and says he has a perfect language is either naïve or a salesman."
    },
    {
       "id":"5a91e60dc4240c000426595b",
       "author":"Alan Turing",
       "en":"A man provided with paper, pencil, and rubber, and subject to strict discipline, is in effect a universal machine."
    },
    {
       "id":"5a91e6a3c4240c000426595c",
       "author":"Alan Turing",
       "en":"The idea behind digital computers may be explained by saying that these machines are intended to carry out any operations which could be done by a human computer."
    },
    {
       "id":"5a91e779c4240c000426595d",
       "author":"Alan Turing",
       "en":"Machines take me by surprise with great frequency."
    },
    {
       "id":"5a933b4c8e7b510004cba4be",
       "author":"Bjarne Stroustrup",
       "en":"Maybe \"just one little global variable\" isn't too unmanageable, but that style leads to code that is useless except to its original programmer."
    },
    {
       "id":"5a933c3d8e7b510004cba4bf",
       "author":"Linus Torvalds",
       "en":"I'm doing a free operating system (just a hobby, won't be big and professional like GNU)."
    },
    {
       "id":"5a933cac8e7b510004cba4c0",
       "author":"Linus Torvalds",
       "en":"If you need more than 3 levels of indentation, you're screwed anyway, and should fix your program."
    },
    {
       "id":"5a933f078e7b510004cba4c1",
       "author":"Linus Torvalds",
       "en":"An infinite number of monkeys typing into GNU Emacs would never make a good program."
    },
    {
       "id":"5a9340258e7b510004cba4c3",
       "author":"Linus Torvalds",
       "en":"If Microsoft ever does applications for Linux it means I've won."
    },
    {
       "id":"5a933f6f8e7b510004cba4c2",
       "author":"Linus Torvalds",
       "en":"See, you not only have to be a good coder to create a system like Linux, you have to be a sneaky bastard too ;-)"
    },
    {
       "id":"5a9342048e7b510004cba4c6",
       "author":"Linus Torvalds",
       "en":"Really, I'm not out to destroy Microsoft. That will just be a completely unintentional side effect."
    },
    {
       "id":"5a9341788e7b510004cba4c5",
       "author":"Linus Torvalds",
       "en":"Talk is cheap. Show me the code."
    },
    {
       "id":"5a9340e08e7b510004cba4c4",
       "author":"Tom Cargill",
       "en":"The first 90 percent of the code accounts for the first 90 percent of the development time. The remaining 10 percent of the code accounts for the other 90 percent of the development time."
    },
    {
       "id":"5a93467e8e7b510004cba4c8",
       "author":"Kent Beck",
       "en":"I'm not a great programmer; I'm just a good programmer with great habits."
    },
    {
       "id":"5a9348828e7b510004cba4c9",
       "author":"Bill Gates",
       "en":"There's only one trick in software, and that is using a piece of software that's already been written."
    },
    {
       "id":"5a93d5a36a584e0004a4a612",
       "author":"Steve Jobs",
       "en":"You can't just ask customers what they want and then try to give that to them. By the time you get it built, they'll want something new."
    },
    {
       "id":"5a93d6b26a584e0004a4a614",
       "author":"Steve Jobs",
       "en":"What a computer is to me is it's the most remarkable tool that we have ever come up with. It's the equivalent of a bicycle for our minds."
    },
    {
       "id":"5a93eb796a584e0004a4a617",
       "author":"Marijn Haverbeke",
       "en":"Programming, it turns out, is hard. The fundamental rules are typically simple and clear. But programs built on top of these rules tend to become complex enough to introduce their own rules and complexity. You’re building your own maze, in a way, and you might just get lost in it."
    },
    {
       "id":"5a93d8036a584e0004a4a615",
       "author":"Steve Jobs",
       "en":"I'm convinced that about half of what separates the successful entrepreneurs from the non-successful ones is pure perseverance. It is so hard."
    },
    {
       "id":"5a93da0d6a584e0004a4a616",
       "author":"Steve Jobs",
       "en":"A lot of companies hire people to tell them what to do. We hire people to tell us what to do."
    },
    {
       "id":"5a93ebdc6a584e0004a4a618",
       "author":"Marijn Haverbeke",
       "en":"Computers themselves can do only stupidly straightforward things. The reason they are so useful is that they do these things at an incredibly high speed."
    },
    {
       "id":"5a93ed3d6a584e0004a4a619",
       "author":"Marijn Haverbeke",
       "en":"A program is a building of thought. It is costless to build, it is weightless, and it grows easily under our typing hands. But without care, a program’s size and complexity will grow out of control, confusing even the person who created it."
    },
    {
       "id":"5a93edc56a584e0004a4a61a",
       "author":"Marijn Haverbeke",
       "en":"There are many terrible mistakes to make in program design, so go ahead and make them so that you understand them better."
    },
    {
       "id":"5a93fd14e49ad10004edb860",
       "author":"Donald Knuth",
       "en":"People think that computer science is the art of geniuses but the actual reality is the opposite, just many people doing things that build on each other, like a wall of mini stones."
    },
    {
       "id":"5a94040fe49ad10004edb862",
       "author":"Jamie Zawinski",
       "en":"Professionalism has no place in art, and hacking is art. Software Engineering might be science; but that's not what I do. I'm a hacker, not an engineer."
    },
    {
       "id":"5a940c14e49ad10004edb864",
       "author":"Quarry worker's creed",
       "en":"We who cut mere stones must always be envisioning cathedrals."
    },
    {
       "id":"5a9405d7e49ad10004edb863",
       "author":"Roy Fielding",
       "en":"Communication must be stateless in nature, such that each request from client to server must contain all of the information necessary to understand the request, and cannot take advantage of any stored context on the server."
    },
    {
       "id":"5a942ea0ee7ed5000496b16f",
       "author":"Kent Beck",
       "en":"When you feel the need to write a comment, first try to refactor the code so that any comment becomes superfluous."
    },
    {
       "id":"5a942dc4ee7ed5000496b16e",
       "author":"Kent Beck",
       "en":"When you find you have to add a feature to a program, and the program's code is not structured in a convenient way to add the feature, first refactor the program to make it easy to add the feature, then add the feature."
    },
    {
       "id":"5a942fc3ee7ed5000496b171",
       "author":"Martin Fowler",
       "en":"There are few things more frustrating or time wasting than debugging. Wouldn't it be a hell of a lot quicker if we just didn't create the bugs in the first place?"
    },
    {
       "id":"5a942fa3ee7ed5000496b170",
       "author":"Martin Fowler",
       "en":"With testing, I know straight away when I added a bug. That lets me fix the bug immediately, before it can crawl off and hide."
    },
    {
       "id":"5a942fd8ee7ed5000496b172",
       "author":"Martin Fowler",
       "en":"I think one of the most valuable rules is avoid duplication."
    },
    {
       "id":"5a942ffbee7ed5000496b173",
       "author":"Martin Fowler",
       "en":"Often designers do complicated things that improve the capacity on a particular hardware platform when it might actually be cheaper to buy more hardware."
    },
    {
       "id":"5a9430a4ee7ed5000496b175",
       "author":"John Carmack",
       "en":"The situation is so much better for programmers today - a cheap used PC, a linux CD, and an internet account, and you have all the tools necessary to work your way to any level of programming skill you want to shoot for."
    },
    {
       "id":"5a94303bee7ed5000496b174",
       "author":"John Carmack",
       "en":"If you want to set off and go develop some grand new thing, you don't need millions of dollars of capitalization. You need enough pizza and Diet Coke to stick in your refrigerator, a cheap PC to work on, and the dedication to go through with it."
    },
    {
       "id":"5a9430ceee7ed5000496b176",
       "author":"John Carmack",
       "en":"Story in a game is like a story in a porn movie. It's expected to be there, but it's not that important."
    },
    {
       "id":"5a9430fbee7ed5000496b177",
       "author":"Paul Graham (programmer)",
       "en":"The best thing software can be is easy, but the way to do this is to get the defaults right, not to limit users' choices."
    },
    {
       "id":"5a943207ee7ed5000496b178",
       "author":"Paul Graham (programmer)",
       "en":"The most important thing is to be able to think what you want, not to say what you want."
    },
    {
       "id":"5a943233ee7ed5000496b17a",
       "author":"Paul Graham (programmer)",
       "en":"It's not so important what you work on, so long as you're not wasting your time."
    },
    {
       "id":"5a943216ee7ed5000496b179",
       "author":"Paul Graham (programmer)",
       "en":"The top 5% of programmers probably write 99% of the good software."
    },
    {
       "id":"5a943244ee7ed5000496b17b",
       "author":"Paul Graham (programmer)",
       "en":"There are few sources of energy so powerful as a procrastinating grad student."
    },
    {
       "id":"5a943267ee7ed5000496b17d",
       "author":"Bill Gates",
       "en":"Your most unhappy customers are your greatest source of learning."
    },
    {
       "id":"5a9432a9ee7ed5000496b17e",
       "author":"Bill Gates",
       "en":"We're no longer in the days where everything is super well crafted. But at the heart of the programs that make it to the top, you'll find that the key internal code was done by a few people who really know what they were doing."
    },
    {
       "id":"5a943301ee7ed5000496b181",
       "author":"Ward Cunningham",
       "en":"What is simplicity? Simplicity is the shortest path to a solution."
    },
    {
       "id":"5a943316ee7ed5000496b182",
       "author":"Ward Cunningham",
       "en":"Putting a new feature into a program is important, but refactoring so new features can be added in the future is equally important."
    },
    {
       "id":"5a94333dee7ed5000496b183",
       "author":"Albert Einstein",
       "en":"A new idea comes suddenly and in a rather intuitive way. But intuition is nothing but the outcome of earlier intellectual experience."
    },
    {
       "id":"5a9433d2ee7ed5000496b184",
       "author":"Ludwig Wittgenstein",
       "en":"The limits of my language mean the limits of my world."
    },
    {
       "id":"5a9434dcee7ed5000496b187",
       "author":"Alan Perlis",
       "en":"If you have a procedure with 10 parameters, you probably missed some."
    },
    {
       "id":"5a943438ee7ed5000496b185",
       "author":"George Boole",
       "en":"That language is an instrument of human reason, and not merely a medium for the expression of thought, is a truth generally admitted."
    },
    {
       "id":"5a9434edee7ed5000496b188",
       "author":"Alan Perlis",
       "en":"A language that doesn't affect the way you think about programming, is not worth knowing."
    },
    {
       "id":"5a943501ee7ed5000496b189",
       "author":"Alan Perlis",
       "en":"Simplicity does not precede complexity, but follows it."
    },
    {
       "id":"5a943514ee7ed5000496b18a",
       "author":"Alan Perlis",
       "en":"A year spent in artificial intelligence is enough to make one believe in God."
    },
    {
       "id":"5a943538ee7ed5000496b18c",
       "author":"Alan Perlis",
       "en":"The best book on programming for the layman is Alice in Wonderland, but that's because it's the best book on anything for the layman."
    },
    {
       "id":"5a94351fee7ed5000496b18b",
       "author":"Alan Perlis",
       "en":"Dealing with failure is easy: Work hard to improve."
    },
    {
       "id":"5a943485ee7ed5000496b186",
       "author":"Alan Perlis",
       "en":"A programming language is low level when its programs require attention to the irrelevant."
    },
    {
       "id":"5a9435d7ee7ed5000496b190",
       "author":"James Gleick",
       "en":"Computer programs are the most intricate, delicately balanced and finely interwoven of all the products of human industry to date."
    },
    {
       "id":"5a9435fbee7ed5000496b191",
       "author":"Edsger W. Dijkstra",
       "en":"The effective exploitation of his powers of abstraction must be regarded as one of the most vital activities of a competent programmer."
    },
    {
       "id":"5a943579ee7ed5000496b18e",
       "author":"Alan Perlis",
       "en":"Fools ignore complexity. Pragmatists suffer it. Some can avoid it. Geniuses remove it."
    },
    {
       "id":"5a943675ee7ed5000496b193",
       "author":"Hal Abelson",
       "en":"Programs must be written for people to read, and only incidentally for machines to execute."
    },
    {
       "id":"5a943612ee7ed5000496b192",
       "author":"Mark Gibbs",
       "en":"No matter how slick the demo is in rehearsal, when you do it in front of a live audience, the probability of a flawless presentation is inversely proportional to the number of people watching, raised to the power of the amount of money involved."
    },
    {
       "id":"5a956c50e648470004c69e0d",
       "author":"Nathaniel Borenstein",
       "en":"It should be noted that no ethically-trained software engineer would ever consent to write a DestroyBaghdad procedure. Basic professional ethics would instead require him to write a DestroyCity procedure, to which Baghdad could be given as a parameter."
    },
    {
       "id":"5a956e55e648470004c69e10",
       "author":"Jef Raskin",
       "en":"When we don’t understand a process, we fall into magical thinking about results."
    },
    {
       "id":"5a956de5e648470004c69e0f",
       "author":"John Carmack",
       "en":"Low-level programming is good for the programmer’s soul."
    },
    {
       "id":"5a956edfe648470004c69e11",
       "author":"Edsger W. Dijkstra",
       "en":"Simplicity and elegance are unpopular because they require hard work and discipline to achieve and education to be appreciated."
    },
    {
       "id":"5a956f87e648470004c69e12",
       "author":"Ted Nelson",
       "en":"A user interface should be so simple that a beginner in an emergency can understand it within 10 seconds."
    },
    {
       "id":"5a956dcce648470004c69e0e",
       "author":"Ted Nelson",
       "en":"Learning to program has no more to do with designing interactive software than learning to touch type has to do with writing poetry."
    },
    {
       "id":"5a95a672cb1a4d0004b2987f",
       "author":"Alan Perlis",
       "en":"Every program has (at least) two purposes: the one for which it was written and another for which it wasn't."
    },
    {
       "id":"5a95a6a3cb1a4d0004b29881",
       "author":"Alan Perlis",
       "en":"In man-machine symbiosis, it is man who must adjust: The machines can't."
    },
    {
       "id":"5a95a686cb1a4d0004b29880",
       "author":"Alan Perlis",
       "en":"One man's constant is another man's variable."
    },
    {
       "id":"5a9432bcee7ed5000496b17f",
       "author":"Bill Gates",
       "en":"Success is a lousy teacher. It seduces smart people into thinking they can't lose."
    },
    {
       "id":"5a95a760cb1a4d0004b29883",
       "author":"Alan Perlis",
       "en":"It is easier to change the specification to fit the program than vice versa."
    },
    {
       "id":"5a95a6f3cb1a4d0004b29882",
       "author":"Alan Perlis",
       "en":"I think it is inevitable that people program poorly. Training will not substantially help matters. We have to learn to live with it."
    },
    {
       "id":"5a95d22e7700780004d51dbb",
       "author":"Henry Ford",
       "en":"If we’d asked the customers what they wanted, they would have said “faster horses”."
    },
    {
       "id":"5a95d2487700780004d51dbc",
       "author":"David Parnas",
       "en":"I have found that the reason a lot of people are interested in artificial intelligence is the same reason a lot of people are interested in artificial limbs: they are missing one."
    },
    {
       "id":"5a95d2a57700780004d51dbd",
       "author":"Leslie Lamport",
       "en":"A distributed system is one in which the failure of a computer you didn’t even know existed can render your own computer unusable."
    },
    {
       "id":"5a95d3a37700780004d51dbe",
       "author":"Ward Cunningham",
       "en":"It’s all talk until the code runs."
    },
    {
       "id":"5a95d4127700780004d51dbf",
       "author":"Jan L. A. van de Snepscheut",
       "en":"In theory, there is no difference between theory and practice. But, in practice, there is."
    },
    {
       "id":"5a95d4977700780004d51dc2",
       "author":"Ellen Ullman",
       "en":"We build our computer systems the way we build our cities: over time, without a plan, on top of ruins."
    },
    {
       "id":"5a95d55e7700780004d51dc3",
       "author":"Eric S. Raymond",
       "en":"The next best thing to having good ideas is recognizing good ideas from your users."
    },
    {
       "id":"5a95d43e7700780004d51dc0",
       "author":"Joel Spolsky",
       "en":"Good software, like good wine, takes time."
    },
    {
       "id":"5a95d5bf7700780004d51dc4",
       "author":"Eric S. Raymond",
       "en":"Lisp is worth learning for the profound enlightenment experience you will have when you finally get it; that experience will make you a better programmer for the rest of your days, even if you never actually use Lisp itself a lot."
    },
    {
       "id":"5a95d4577700780004d51dc1",
       "author":"Filipe Fortes",
       "en":"Debugging is like being the detective in a crime movie where you are also the murderer."
    },
    {
       "id":"5a95d8a87700780004d51dc7",
       "author":"Dennis Ritchie",
       "en":"What we wanted to preserve was not just a good environment in which to do programming, but a system around which fellowship could form."
    },
    {
       "id":"5a95d7b47700780004d51dc6",
       "author":"Marvin Minsky",
       "en":"Once the computers got control, we might never get it back."
    },
    {
       "id":"5a95e89f7700780004d51dc9",
       "author":"Jef Raskin",
       "en":"A computer shall not waste your time or require you to do more work than is strictly necessary."
    },
    {
       "id":"5a95fcd17700780004d51dcb",
       "author":"George Boole",
       "en":"Of the many forms of false culture, a premature converse with abstractions is perhaps the most likely to prove fatal to the growth of a masculine vigour of intellect."
    },
    {
       "id":"5a95dae97700780004d51dc8",
       "author":"Ken Thompson",
       "en":"C++ certainly has its good points. But by and large I think it's a bad language. It does a lot of things half well and it’s just a garbage heap of ideas that are mutually exclusive. It’s way too big, way too complex. And it’s obviously built by a committee."
    },
    {
       "id":"5a95fce07700780004d51dcc",
       "author":"George Boole",
       "en":"No matter how correct a mathematical theorem may appear to be, one ought never to be satisfied that there was not something imperfect about it until it also gives the impression of being beautiful."
    },
    {
       "id":"5a96009b7700780004d51dcf",
       "author":"Ada Lovelace",
       "en":"The Analytical Engine does not occupy common ground with mere 'calculating machines.' It holds a position wholly its own, and the considerations it suggests are more interesting in their nature."
    },
    {
       "id":"5a96001a7700780004d51dce",
       "author":"Ada Lovelace",
       "en":"The science of operations, as derived from mathematics more especially, is a science of itself, and has its own abstract truth and value."
    },
    {
       "id":"5a9601017700780004d51dd1",
       "author":"Ada Lovelace",
       "en":"In the case of the Analytical Engine, we have undoubtedly to lay out a certain capital of analytical labour in one particular line, but this is in order that the engine may bring us in a much larger return in another line."
    },
    {
       "id":"5a9600ae7700780004d51dd0",
       "author":"Ada Lovelace",
       "en":"We may say most aptly that the Analytical Engine weaves algebraical patterns just as the Jacquard loom weaves flowers and leaves."
    },
    {
       "id":"5a9602227700780004d51dd2",
       "author":"George Boole",
       "en":"The design of the following treatise is to investigate the fundamental laws of those operations of the mind by which reasoning is performed; to give expression to them in the symbolical language of a Calculus, and upon this foundation to establish the science of Logic and construct its method."
    },
    {
       "id":"5a967d572ba98a0004b6294f",
       "author":"John von Neumann",
       "en":"Any one who considers arithmetical methods of producing random digits is, of course, in a state of sin. For, as has been pointed out several times, there is no such thing as a random number."
    },
    {
       "id":"5a9602757700780004d51dd3",
       "author":"George Boole",
       "en":"There is not only a close analogy between the operations of the mind in general reasoning and its operations in the particular science of Algebra, but there is to a considerable extent an exact agreement in the laws by which the two classes of operations are conducted."
    },
    {
       "id":"5a967e9c2ba98a0004b62950",
       "author":"John von Neumann",
       "en":"A large part of mathematics which becomes useful developed with absolutely no desire to be useful, and in a situation where nobody could possibly know in what area it would become useful."
    },
    {
       "id":"5a96b8e2d6959500047aecae",
       "author":"Friedrich Bauer",
       "en":"Software engineering is the part of computer science which is too difficult for the computer scientist."
    },
    {
       "id":"5a96b909d6959500047aecaf",
       "author":"Grady Booch",
       "en":"The amateur software engineer is always in search of magic, some sensational method or tool whose application promises to render software development trivial. It is the mark of the professional software engineer to know that no such panacea exist."
    },
    {
       "id":"5a96b980d6959500047aecb0",
       "author":"Grady Booch",
       "en":"Good people with a good process will outperform good people with no process every time."
    },
    {
       "id":"5a96b998d6959500047aecb1",
       "author":"Grady Booch",
       "en":"The entire history of software engineering is that of the rise in levels of abstraction."
    },
    {
       "id":"5a96b9ead6959500047aecb2",
       "author":"Hal Abelson",
       "en":"The reason that we think computer science is about computers is pretty much the same reason that the Egyptians thought geometry was about surveying instruments: when some field is just getting started and you don't really understand it very well, it's very easy to confuse the essence of what you're doing with the tools that you use."
    },
    {
       "id":"5a96b7abd6959500047aecad",
       "author":"Alan Kay",
       "en":"Most software today is very much like an Egyptian pyramid with millions of bricks piled on top of each other, with no structural integrity, but just done by brute force and thousands of slaves."
    },
    {
       "id":"5a96ba01d6959500047aecb3",
       "author":"Bill Gates",
       "en":"Is studying computer science the best way to prepare to be a programmer? No. the best way to prepare is to write programs, and to study great programs that other people have written."
    },
    {
       "id":"5a96ba30d6959500047aecb4",
       "author":"Richard Feynman",
       "en":"Computer science differs from physics in that it is not actually a science. It does not study natural objects. Rather, computer science is like engineering; it is all about getting something to do something."
    },
    {
       "id":"5a96ba45d6959500047aecb5",
       "author":"Richard Hamming",
       "en":"The purpose of computing is insight, not numbers."
    },
    {
       "id":"5a96bb2dd6959500047aecb7",
       "author":"Albert Einstein",
       "en":"All of our exalted technological progress, civilization for that matter, is comparable to an axe in the hand of a pathological criminal."
    },
    {
       "id":"5a96bbaed6959500047aecb8",
       "author":"Arthur C. Clarke",
       "en":"When a distinguished but elderly scientist states that something is possible, they are almost certainly right. When they state that something is impossible, they are very probably wrong."
    },
    {
       "id":"5a96ba93d6959500047aecb6",
       "author":"Dennis Ritchie",
       "en":"Computer science research is different from these more traditional disciplines. Philosophically it differs from the physical sciences because it seeks not to discover, explain, or exploit the natural world, but instead to study the properties of machines of human creation."
    },
    {
       "id":"5a96bbc3d6959500047aecb9",
       "author":"Arthur C. Clarke",
       "en":"Any sufficiently advanced technology is indistinguishable from magic."
    },
    {
       "id":"5a96bd31d6959500047aecba",
       "author":"Joseph Yoder (computer scientist)",
       "en":"While much attention has been focused on high-level software architectural patterns, what is, in effect, the de-facto standard software architecture is seldom discussed: the Big Ball of Mud."
    },
    {
       "id":"5a96bd7ed6959500047aecbb",
       "author":"Joseph Yoder (computer scientist)",
       "en":"All too many of our software systems are, architecturally, little more than shantytowns."
    },
    {
       "id":"5a96be8ed6959500047aecbe",
       "author":"Joseph Yoder (computer scientist)",
       "en":"Managing a large project is a qualitatively different problem from managing a small one, just as leading a division of infantry into battle is different from commanding a small special forces team."
    },
    {
       "id":"5a96bf70d6959500047aecc2",
       "author":"Joseph Yoder (computer scientist)",
       "en":"When you build a prototype, there is always the risk that someone will say \"that's good enough, ship it\". One way to minimize the risk of a prototype being put into production is to write the prototype in using a language or tool that you couldn't possibly use for a production version."
    },
    {
       "id":"5a96bec9d6959500047aecbf",
       "author":"Joseph Yoder (computer scientist)",
       "en":"Sadly, architecture has been undervalued for so long that many engineers regard life with a Big Ball of Mud as normal."
    },
    {
       "id":"5a96bf99d6959500047aecc3",
       "author":"Joseph Yoder (computer scientist)",
       "en":"The real problem with throwaway code comes when it isn't thrown away."
    },
    {
       "id":"5a96c01dd6959500047aecc4",
       "author":"Joseph Yoder (computer scientist)",
       "en":"Sometimes it’s just easier to throw a system away, and start over."
    },
    {
       "id":"5a96c299d6959500047aecc5",
       "author":"Eric S. Raymond",
       "en":"Computer science education cannot make anybody an expert programmer any more than studying brushes and pigment can make somebody an expert painter."
    },
    {
       "id":"5a96c3b6d6959500047aecc7",
       "author":"Randall E. Stross",
       "en":"The best programmers are not marginally better than merely good ones. They are an order-of-magnitude better, measured by whatever standard: conceptual creativity, speed, ingenuity of design, or problem-solving ability."
    },
    {
       "id":"5a96c380d6959500047aecc6",
       "author":"Alan Kay",
       "en":"I invented the term 'Object-Oriented', and I can tell you I did not have C++ in mind."
    },
    {
       "id":"5a96c44cd6959500047aecc9",
       "author":"Linus Torvalds",
       "en":"Most good programmers do programming not because they expect to get paid or get adulation by the public, but because it is fun to program."
    },
    {
       "id":"5a97def55f624c00046e2103",
       "author":"Alan Perlis",
       "en":"Educators, generals, dieticians, psychologists, and parents program. Armies, students, and some societies are programmed."
    },
    {
       "id":"5a96c431d6959500047aecc8",
       "author":"L. Peter Deutsch",
       "en":"To iterate is human, to recurse divine."
    },
    {
       "id":"5a97dee55f624c00046e2102",
       "author":"Alan Perlis",
       "en":"For all its power, the computer is a harsh taskmaster. Its programs must be correct, and what we wish to say must be said accurately in every detail."
    },
    {
       "id":"5a97e0755f624c00046e2104",
       "author":"John Locke",
       "en":"The acts of the mind, wherein it exerts its power over simple ideas, are chiefly these three: 1. Combining several simple ideas into one compound one, and thus all complex ideas are made. 2. The second is bringing two ideas, whether simple or complex, together, and setting them by one another so as to take a view of them at once, without uniting them into one, by which it gets all its ideas of relations. 3. The third is separating them from all other ideas that accompany them in their real existence: this is called abstraction, and thus all its general ideas are made."
    },
    {
       "id":"5a97efdaccdfe50004febf35",
       "author":"Gerald Weinberg",
       "en":"When program developers are not territorial about their code and encourage others to look for bugs and potential improvements, progress speeds up dramatically."
    },
    {
       "id":"5a97f196ccdfe50004febf37",
       "author":"Anonymous",
       "en":"The best thing about a boolean is even if you are wrong, you are only off by a bit."
    },
    {
       "id":"5a97f307ccdfe50004febf39",
       "author":"Richard E. Pattis",
       "en":"When debugging, novices insert corrective code; experts remove defective code."
    },
    {
       "id":"5a97f324ccdfe50004febf3a",
       "author":"Douglas Crockford",
       "en":"It turns out that style matters in programming for the same reason that it matters in writing. It makes for better reading."
    },
    {
       "id":"5a97f363ccdfe50004febf3b",
       "author":"Douglas Crockford",
       "en":"Computer programs are the most complex things that humans make."
    },
    {
       "id":"5a97f4e1ccdfe50004febf3d",
       "author":"Douglas Crockford",
       "en":"Most programming languages contain good parts and bad parts. I discovered that I could be better programmer by using only the good parts and avoiding the bad parts."
    },
    {
       "id":"5a97f510ccdfe50004febf3e",
       "author":"Douglas Crockford",
       "en":"Good architecture is necessary to give programs enough structure to be able to grow large without collapsing into a puddle of confusion."
    },
    {
       "id":"5a97f539ccdfe50004febf3f",
       "author":"Douglas Crockford",
       "en":"JavaScript is the world's most misunderstood programming language."
    },
    {
       "id":"5a97f5f2ccdfe50004febf41",
       "author":"Douglas Crockford",
       "en":"In JavaScript, there is a beautiful, elegant, highly expressive language that is buried under a steaming pile of good intentions and blunders."
    },
    {
       "id":"5a97f552ccdfe50004febf40",
       "author":"Douglas Crockford",
       "en":"Software is usually expected to be modified over the course of its productive life. The process of converting one correct program into a different correct program is extremely challenging."
    },
    {
       "id":"5a97f8c1ccdfe50004febf42",
       "author":"Eric S. Raymond",
       "en":"Every good work of software starts by scratching a developer’s personal itch."
    },
    {
       "id":"5a9801011878b40004879f55",
       "author":"Anonymous",
       "en":"You can have the project: Done On Time. Done On Budget. Done Properly - Pick two."
    },
    {
       "id":"5a9801871878b40004879f56",
       "author":"Andy Hunt (author)",
       "en":"No one in the brief history of computing has ever written a piece of perfect software. It's unlikely that you'll be the first."
    },
    {
       "id":"5a9801f61878b40004879f57",
       "author":"Steve Wozniak",
       "en":"Never trust a computer you can’t throw out a window."
    },
    {
       "id":"5a9800cd1878b40004879f54",
       "author":"Alan Kay",
       "en":"The best way to predict the future is to invent it."
    },
    {
       "id":"5a9802611878b40004879f58",
       "author":"Martin Fowler",
       "en":"If you can get today’s work done today, but you do it in such a way that you can’t possibly get tomorrow’s work done tomorrow, then you lose."
    },
    {
       "id":"5a9803171878b40004879f5a",
       "author":"Alan Turing",
       "en":"Codes are a puzzle. A game, just like any other game."
    },
    {
       "id":"5a9802cb1878b40004879f59",
       "author":"Damian Conway",
       "en":"Documentation is a love letter that you write to your future self."
    },
    {
       "id":"5a95d17b7700780004d51dba",
       "author":"Bdale Garbee",
       "en":"Life is too short to run proprietary software."
    },
    {
       "id":"5a98075b1878b40004879f5d",
       "author":"Martin Fowler",
       "en":"W​henever I have to think to understand what the code is doing, I ask myself if I can refactor the code to make that understanding more immediately apparent."
    },
    {
       "id":"5a9803931878b40004879f5b",
       "author":"David Leinweber",
       "en":"If you give someone a program, you will frustrate them for a day; if you teach them how to program, you will frustrate them for a lifetime."
    },
    {
       "id":"5a9803be1878b40004879f5c",
       "author":"Mario Fusco",
       "en":"The code you write makes you a programmer. The code you delete makes you a good one. The code you don't have to write makes you a great one."
    },
    {
       "id":"5a98080e1878b40004879f5f",
       "author":"Addy Osmani",
       "en":"First do it, then do it right, then do it better."
    },
    {
       "id":"5a9808401878b40004879f60",
       "author":"John Carmack",
       "en":"The cost of adding a feature isn’t just the time it takes to code it. The cost also includes the addition of an obstacle to future expansion. The trick is to pick the features that don’t fight each other."
    },
    {
       "id":"5a9808b71878b40004879f62",
       "author":"George Carrette",
       "en":"First learn computer science and all the theory. Next develop a programming style. Then forget all that and just hack."
    },
    {
       "id":"5a98090a1878b40004879f64",
       "author":"Anders Hejlsberg",
       "en":"Just because people tell you it can't be done, that doesn't necessarily mean that it can't be done. It just means that they can't do it."
    },
    {
       "id":"5a98096c1878b40004879f65",
       "author":"Dennis Ritchie",
       "en":"The only way to learn a new programming language is by writing programs in it."
    },
    {
       "id":"5a980ec71878b40004879f66",
       "author":"Manny Lehman (computer scientist)",
       "en":"An evolving system increases its complexity unless work is done to reduce it."
    },
    {
       "id":"5a985b7ae93441000489b948",
       "author":"Robert C. Martin",
       "en":"No matter how slow you are writing clean code, you will always be slower if you make a mess."
    },
    {
       "id":"5a985bc7e93441000489b949",
       "author":"Rob Pike",
       "en":"Fancy algorithms are slow when n is small, and n is usually small."
    },
    {
       "id":"5a985c91e93441000489b94a",
       "author":"Manuel Blum",
       "en":"The only difference between a FA [finite automata] and a TM [Turing machine] is that the TM, unlike the FA, has paper and pencil. Think about it. It tells you something about the power of writing."
    },
    {
       "id":"5a985e7ae93441000489b94c",
       "author":"Alan Perlis",
       "en":"Within a computer, natural language is unnatural."
    },
    {
       "id":"5a985db5e93441000489b94b",
       "author":"Brian Cantwell Smith",
       "en":"Just because you've implemented something doesn't mean you understand it."
    },
    {
       "id":"5a9807b41878b40004879f5e",
       "author":"Douglas Crockford",
       "en":"That hardly ever happens is another way of saying 'it happens'."
    },
    {
       "id":"5a9860abe93441000489b94f",
       "author":"Donald Knuth",
       "en":"Beware of bugs in the above code; I have only proved it correct, not tried it."
    },
    {
       "id":"5a986366e93441000489b951",
       "author":"Ivan Sutherland",
       "en":"A display connected to a digital computer gives us a chance to gain familiarity with concepts not realizable in the physical world. It is a looking glass into a mathematical wonderland."
    },
    {
       "id":"5a9911bb8cdbad0004955d02",
       "author":"Ralph Johnson (computer scientist)",
       "en":"Before software can be reusable it first has to be usable."
    },
    {
       "id":"5a9912938cdbad0004955d04",
       "author":"Gordon Bell",
       "en":"The cheapest, fastest, and most reliable components are those that aren’t there."
    },
    {
       "id":"5a9912248cdbad0004955d03",
       "author":"Anonymous",
       "en":"In order to understand recursion, one must first understand recursion."
    },
    {
       "id":"5a9995789128a800040c7dfa",
       "author":"Don Norman",
       "en":"The hardest part of design is keeping features out."
    },
    {
       "id":"5a986021e93441000489b94e",
       "author":"Luciano Ramalho",
       "en":"Premature abstraction is as bad as premature optimization."
    },
    {
       "id":"5a9995d29128a800040c7dfc",
       "author":"Fred Brooks",
       "en":"Much of the essence of building a program is in fact the debugging of the specification."
    },
    {
       "id":"5a9997389128a800040c7dfd",
       "author":"Elon Musk",
       "en":"Any product that needs a manual to work is broken."
    },
    {
       "id":"5a9995b89128a800040c7dfb",
       "author":"Kevlin Henney",
       "en":"The act of describing a program in unambiguous detail and the act of programming are one and the same."
    },
    {
       "id":"5a9997929128a800040c7dfe",
       "author":"Elon Musk",
       "en":"I think you should always bear in mind that entropy is not on your side."
    },
    {
       "id":"5a9997d79128a800040c7dff",
       "author":"Elon Musk",
       "en":"The path to the CEO's office should not be through the CFO's office, and it should not be through the marketing department. It needs to be through engineering and design."
    },
    {
       "id":"5a9999f39128a800040c7e00",
       "author":"Elon Musk",
       "en":"People are mistaken when they think that technology just automatically improves. It does not automatically improve. It only improves if a lot of people work very hard to make it better, and actually it will, I think, by itself degrade, actually."
    },
    {
       "id":"5a9a9c372bad9600044b6fb4",
       "author":"Elon Musk",
       "en":"With artificial intelligence we are summoning the demon."
    },
    {
       "id":"5a9a9f7e2bad9600044b6fb6",
       "author":"Elon Musk",
       "en":"AI is a fundamental risk to the existence of human civilization."
    },
    {
       "id":"5a9aa21b2bad9600044b6fba",
       "author":"Terry Winograd",
       "en":"The main activity of programming is not the origination of new independent programs, but in the integration, modification, and explanation of existing ones."
    },
    {
       "id":"5a9aaff32bad9600044b6fbd",
       "author":"Tim Berners-Lee",
       "en":"Cool URIs don't change."
    },
    {
       "id":"5a9aaf8e2bad9600044b6fbc",
       "author":"Tim Berners-Lee",
       "en":"I don't believe in the sort of eureka moment idea. I think it's a myth. I'm very suspicious that actually Archimedes had been thinking about that problem for a long time."
    },
    {
       "id":"5a9ab0372bad9600044b6fbf",
       "author":"Tim Berners-Lee",
       "en":"When I invented the web, I didn't have to ask anyone's permission."
    },
    {
       "id":"5a9aa01d2bad9600044b6fb7",
       "author":"Elon Musk",
       "en":"We need to be super careful with AI. Potentially more dangerous than nukes."
    },
    {
       "id":"5a9ab1802bad9600044b6fc1",
       "author":"Tim Berners-Lee",
       "en":"I invented the Web just because I needed it, really, because it was so frustrating that it didn't exit."
    },
    {
       "id":"5a9ab1ac2bad9600044b6fc2",
       "author":"Tim Berners-Lee",
       "en":"To be a hacker - when I use the term - is somebody who is creative and does wonderful things."
    },
    {
       "id":"5a9ab1fa2bad9600044b6fc3",
       "author":"Tim Berners-Lee",
       "en":"The Domain Name Server (DNS) is the Achilles heel of the Web."
    },
    {
       "id":"5a9ab3f52bad9600044b6fc4",
       "author":"Vannevar Bush",
       "en":"Two centuries ago Leibnitz invented a calculating machine which embodied most of the essential features of recent keyboard devices, but it could not then come into use. The economics of the situation were against it."
    },
    {
       "id":"5a9ab4a82bad9600044b6fc5",
       "author":"Vannevar Bush",
       "en":"Whenever logical processes of thought are employed, there is an opportunity for the machine."
    },
    {
       "id":"5a9ab8f42bad9600044b6fc6",
       "author":"Vannevar Bush",
       "en":"If scientific reasoning were limited to the logical processes of arithmetic, we should not get very far in our understanding of the physical world. One might as well attempt to grasp the game of poker entirely by the use of the mathematics of probability."
    },
    {
       "id":"5a9ac42b2bad9600044b6fc7",
       "author":"Ward Cunningham",
       "en":"Shipping first time code is like going into debt. A little debt speeds development so long as it is paid back promptly with a rewrite. The danger occurs when the debt is not repaid. Every minute spent on not-quite-right code counts as interest on that debt. Entire engineering organizations can be brought to a stand-still under the technical debt load."
    },
    {
       "id":"5a9ac4852bad9600044b6fc8",
       "author":"Martin Fowler",
       "en":"Like a financial debt, the technical debt incurs interest payments, which come in the form of the extra effort that we have to do in future development because of the quick and dirty design choice."
    },
    {
       "id":"5a9ac5942bad9600044b6fc9",
       "author":"Steve McConnell",
       "en":"One of the important implications of technical debt is that it must be serviced. If the debt grows large enough, eventually the company will spend more on servicing its debt than it invests in increasing the value of its other assets."
    },
    {
       "id":"5a9ab0622bad9600044b6fc0",
       "author":"Tim Berners-Lee",
       "en":"What's very important from my point of view is that there is one web. Anyone that tries to chop it into two will find that their piece looks very boring."
    },
    {
       "id":"5a9b0b112bad9600044b6fca",
       "author":"René Descartes",
       "en":"Thus it is observable that the buildings which a single architect has planned and executed, are generally more elegant and commodious than those which several have attempted to improve."
    },
    {
       "id":"5a9b0b752bad9600044b6fcb",
       "author":"Danny Hillis",
       "en":"Computers are the most complex objects we human beings have ever created, but in a fundamental sense they are remarkably simple."
    },
    {
       "id":"5a9b0bb22bad9600044b6fcd",
       "author":"Danny Hillis",
       "en":"The magic of a computer lies in its ability to become almost anything you can imagine, as long as you can explain exactly what that is."
    },
    {
       "id":"5a9b0b9a2bad9600044b6fcc",
       "author":"Danny Hillis",
       "en":"The computer is not just an advanced calculator or camera or paintbrush; rather, it is a device that accelerates and extends our processes of thought."
    },
    {
       "id":"5a9b0bce2bad9600044b6fce",
       "author":"Danny Hillis",
       "en":"With the right programming, a computer can become a theater, a musical instrument, a reference book, a chess opponent. No other entity in the world except a human being has such an adaptable, universal nature."
    },
    {
       "id":"5a9b0c2f2bad9600044b6fcf",
       "author":"Danny Hillis",
       "en":"Anyone who has ever written a program knows that telling a computer what you want it to do is not as easy as it sounds. Every detail of the computer’s desired operation must be precisely described. For instance, if you tell an accounting program to bill your clients for the amount that each owes, then the computer will send out a weekly bill for $0.00 to clients who owe nothing."
    },
    {
       "id":"5a9b0c4b2bad9600044b6fd0",
       "author":"Danny Hillis",
       "en":"A skilled programmer is like a poet who can put into words those ideas that others find inexpressible."
    },
    {
       "id":"5a9b0c6b2bad9600044b6fd1",
       "author":"Danny Hillis",
       "en":"Every computer language has its Shakespeares, and it is a joy to read their code. A well-written computer program possesses style, finesse, even humor—and a clarity that rivals the best prose."
    },
    {
       "id":"5a9b0c932bad9600044b6fd2",
       "author":"Danny Hillis",
       "en":"It turns out that there is no algorithm for examining a program and determining whether or not it is fatally infected with an endless loop. Moreover, it’s not that no one has yet discovered such an algorithm; rather, no such algorithm is possible."
    },
    {
       "id":"5a9b0cc62bad9600044b6fd3",
       "author":"Danny Hillis",
       "en":"The class of problems that are computable by a digital computer apparently includes every problem that is computable by any kind of device."
    },
    {
       "id":"5a9b0d662bad9600044b6fd5",
       "author":"Hal Abelson",
       "en":"The programs we use to conjure processes are like a sorcerer's spells. They are carefully composed from symbolic expressions in arcane and esoteric programming languages that prescribe the tasks we want our processes to perform."
    },
    {
       "id":"5a9b10db2bad9600044b6fd7",
       "author":"Fred Brooks",
       "en":"Human beings are not accustomed to being perfect, and few areas of human activity demand it. Adjusting to the requirement for perfection is, I think, the most difficult part of learning to program."
    },
    {
       "id":"5a9b131f2bad9600044b6fd9",
       "author":"Fred Brooks",
       "en":"Because of optimism, we usually expect the number of bugs to be smaller than it turns out to be. Therefore testing is usually the most mis-scheduled part of programming."
    },
    {
       "id":"5a9b0d9c2bad9600044b6fd6",
       "author":"Danny Hillis",
       "en":"One of the greatest joys in computer programming is discovering a new, faster, more efficient algorithm for doing something — particularly if a lot of well-respected people have come up with worse solutions."
    },
    {
       "id":"5a9b13442bad9600044b6fda",
       "author":"Fred Brooks",
       "en":"False scheduling to match the patron's desired date is much more common in our discipline than elsewhere in engineering."
    },
    {
       "id":"5a9b14c12bad9600044b6fdb",
       "author":"Robert L. Glass",
       "en":"The best programmers are up to 28 times better than the worst programmers, according to “individual differences” research. Given that their pay is never commensurate, they are the biggest bargains in the software field."
    },
    {
       "id":"5a9b154e2bad9600044b6fdc",
       "author":"Fred Brooks",
       "en":"Sackman, Erickson, and Grant were measuring performance of a group of experienced programmers. Within just this group the ratios between the best and worst performances averaged about 10:1 on productivity measurements and an amazing 5:1 on program speed and space measurements!"
    },
    {
       "id":"5a9b15cb2bad9600044b6fdd",
       "author":"Fred Brooks",
       "en":"Conceptual integrity is the most important consideration in system design. It is better to have a system omit certain anomalous features and improvements, but to reflect one set of design ideas, than to have one that contains many good but independent and uncoordinated ideas."
    },
    {
       "id":"5a9b15e52bad9600044b6fde",
       "author":"Fred Brooks",
       "en":"The separation of architectural effort from implementation is a very powerful way of getting conceptual integrity on very large projects."
    },
    {
       "id":"5a9b16122bad9600044b6fdf",
       "author":"Fred Brooks",
       "en":"The general tendency is to over-design the second system, using all the ideas and frills that were cautiously sidetracked on the first one."
    },
    {
       "id":"5a9b16922bad9600044b6fe2",
       "author":"Fred Brooks",
       "en":"The management question, therefore, is not whether to build a pilot system and throw it away. You will do that. The only question is whether to plan in advance to build a throwaway, or to promise to deliver the throwaway to customers."
    },
    {
       "id":"5a9b17542bad9600044b6fe4",
       "author":"Fred Brooks",
       "en":"Program building is an entropy-decreasing process, hence inherently metastable. Program maintenance is an entropy-increasing process, and even its most skillful execution only delays the subsidence of the system into unfixable obsolescence."
    },
    {
       "id":"5a9b16792bad9600044b6fe1",
       "author":"Fred Brooks",
       "en":"Chemical engineers learned long ago that a process that works in the laboratory cannot be implemented in a factory in only one step."
    },
    {
       "id":"5a9b17f92bad9600044b6fe7",
       "author":"Fred Brooks",
       "en":"First, we must observe that the anomaly is not that software progress is so slow but that computer hardware progress is so fast. No other technology since civilization began has seen six orders of magnitude price-performance gain in 30 years."
    },
    {
       "id":"5a9b17a22bad9600044b6fe6",
       "author":"Fred Brooks",
       "en":"Coding is \"90 percent finished\" for half of the total coding time. Debugging is \"99 percent complete\" most of the time."
    },
    {
       "id":"5a9b18102bad9600044b6fe8",
       "author":"Fred Brooks",
       "en":"The complexity of software is an essential property, not an accidental one. Hence descriptions of a software entity that abstract away its complexity often abstract away its essence."
    },
    {
       "id":"5a9b189c2bad9600044b6fea",
       "author":"Fred Brooks",
       "en":"Study after study shows that the very best designers produce structures that are faster, smaller, simpler, cleaner, and produced with less effort. The differences between the great and the average approach an order of magnitude."
    },
    {
       "id":"5a9b18d52bad9600044b6fec",
       "author":"Fred Brooks",
       "en":"A programming systems product takes about nine times as much effort as the component programs written separately for private use."
    },
    {
       "id":"5a9b190a2bad9600044b6fed",
       "author":"Fred Brooks",
       "en":"My rule of thumb is 1/3 of the schedule for design, 1/6 for coding, 1/4 for component testing, and 1/4 for system testing."
    },
    {
       "id":"5a9b18bf2bad9600044b6feb",
       "author":"Fred Brooks",
       "en":"First, my wife, my colleagues, and my editors find me to err far more often in optimism than in pessimism. I am, after all, a programmer by background, and optimism is an occupational disease of our craft."
    },
    {
       "id":"5a9b19232bad9600044b6fee",
       "author":"Fred Brooks",
       "en":"Because we are uncertain about our scheduling estimates, we often lack the courage to defend them stubbornly against management and customer pressure."
    },
    {
       "id":"5a9b19422bad9600044b6fef",
       "author":"Fred Brooks",
       "en":"Adding people to a software project increases the total effort necessary in three ways: the work and disruption of repartitioning itself, training the new people, and added intercommunication."
    },
    {
       "id":"5a9b195a2bad9600044b6ff0",
       "author":"Fred Brooks",
       "en":"Very good professional programmers are ten times as productive as poor ones, at same training and two-year experience level."
    },
    {
       "id":"5a9b198a2bad9600044b6ff2",
       "author":"Fred Brooks",
       "en":"Programming increases goes as a power of program size."
    },
    {
       "id":"5a9b1abf2bad9600044b6ff7",
       "author":"Daniel T. Barry",
       "en":"Various studies indicate that the optimal team size is between 2 and 5, with 3 being the mode. With more than 5 team members, team management begins to dominate the work."
    },
    {
       "id":"5a9b1ce02bad9600044b6ff8",
       "author":"Daniel T. Barry",
       "en":"A stupid error is an algorithmically avoidable error. Mainly, you are stupid if you let an error that a program can detect go undetected."
    },
    {
       "id":"5a9b19dd2bad9600044b6ff4",
       "author":"Fred Brooks",
       "en":"All repairs tend to destroy structure, to increase the entropy and disorder of a system."
    },
    {
       "id":"5a9b1d7d2bad9600044b6ffa",
       "author":"Thomas J. Watson",
       "en":"I think there is a world market for maybe five\ncomputers."
    },
    {
       "id":"5a9b1e082bad9600044b6ffb",
       "author":"Ken Olsen",
       "en":"There is no reason anyone would want a computer in their home."
    },
    {
       "id":"5a9b1eb02bad9600044b6ffc",
       "author":"Michael A. Jackson",
       "en":"The beginning of wisdom for a programmer is to recognize the difference between getting his program to work and getting it right."
    },
    {
       "id":"5a9b1ece2bad9600044b6ffd",
       "author":"Michael A. Jackson",
       "en":"Two things are known about requirements:\n1. They will change!\n2. They will be misunderstood!"
    },
    {
       "id":"5a9b1f362bad9600044b6fff",
       "author":"Daniel T. Barry",
       "en":"Every time you improve process, work becomes harder."
    },
    {
       "id":"5a9b1f592bad9600044b7000",
       "author":"Daniel T. Barry",
       "en":"There is never enough time to do it right, but there is always enough time to fix it or to do it over."
    },
    {
       "id":"5a8e9be284a8f2000482568c",
       "author":"Rich Skrenta",
       "en":"The more code you have, the more places there are for bugs to hide."
    },
    {
       "id":"5a97f062ccdfe50004febf36",
       "author":"Gerald Weinberg",
       "en":"If builders built houses the way programmers built programs, the first woodpecker to come along would destroy civilization."
    },
    {
       "id":"5a9aa1db2bad9600044b6fb9",
       "author":"Terry Winograd",
       "en":"The techniques of artificial intelligence are to the mind what bureaucracy is to human social interaction."
    },
    {
       "id":"5a9b1f692bad9600044b7001",
       "author":"Daniel T. Barry",
       "en":"Code is expensive to change, but design is cheaper to change, and requirements are even cheaper to change."
    },
    {
       "id":"5a9b1f822bad9600044b7002",
       "author":"Daniel T. Barry",
       "en":"The cost to repair an error goes up dramatically as project moves towards completion and beyond."
    },
    {
       "id":"5a9b1f252bad9600044b6ffe",
       "author":"Daniel T. Barry",
       "en":"A team of highly competent programmers who are also highly territorial, egotistical politicians will fail while a team of equally competent programmers, who are also egoless, cooperative, team players will succeed."
    },
    {
       "id":"5a9b203c2bad9600044b7004",
       "author":"Daniel T. Barry",
       "en":"For most software, efficiency just does not matter."
    },
    {
       "id":"5a9b214b2bad9600044b7005",
       "author":"Harlan Mills",
       "en":"The best way to know that you have found the last bug is never to find the first bug."
    },
    {
       "id":"5a9b21cb2bad9600044b7008",
       "author":"Harlan Mills",
       "en":"An interactive debugger is an outstanding example of what is not needed - it encourages trial-and-error hacking rather than systematic design, and also hides marginal people barely qualified for precision programming."
    },
    {
       "id":"5a9b22a02bad9600044b7009",
       "author":"Daniel T. Barry",
       "en":"Thoroughly testing a program is impossible (requires unbounded number of test cases); so try to choose test cases that will expose all errors. That’s very difficult, especially since we do not know what all the errors are, and if we did, we would not need the test cases!"
    },
    {
       "id":"5a9b21a12bad9600044b7007",
       "author":"Harlan Mills",
       "en":"The only way for errors to occur in a program is by being put there by the author. No other mechanisms are known."
    },
    {
       "id":"5a9b22c72bad9600044b700b",
       "author":"Daniel T. Barry",
       "en":"Reliable computations are obtainable from buggy programs, which after all, are the only kind of programs there are."
    },
    {
       "id":"5a9b22ed2bad9600044b700c",
       "author":"David Parnas",
       "en":"I can build a reliable system with thousands of bugs, if you let me choose my bugs carefully."
    },
    {
       "id":"5a9b231d2bad9600044b700d",
       "author":"Daniel T. Barry",
       "en":"Ed Adams of IBM found that 80% of the reliability problems are caused by only 2% of the defects."
    },
    {
       "id":"5a9b23502bad9600044b700e",
       "author":"Jim Horning",
       "en":"Hardware is the part you can replace. Software is the part you have to keep, because it’s so expensive and nobody understands it any more."
    },
    {
       "id":"5a9b23dc2bad9600044b7011",
       "author":"Daniel T. Barry",
       "en":"Any technological or managerial scheme to force documentation can be subverted by unwilling programmers."
    },
    {
       "id":"5a9b23b02bad9600044b700f",
       "author":"Jim Horning",
       "en":"Good judgement comes from experience. Experience comes from bad judgement."
    },
    {
       "id":"5a9c649eff6af300049e6b59",
       "author":"John McCarthy (computer scientist)",
       "en":"Machines as simple as thermostats can be said to have beliefs."
    },
    {
       "id":"5a9b253f2bad9600044b7016",
       "author":"Tony Parisi (software developer)",
       "en":"A framework can provide 90% of the features we need quickly — giving us a false sense of confidence early in the development cycle — and then be frustratingly hard when it comes to implementing the last 10%."
    },
    {
       "id":"5a9c6502ff6af300049e6b5a",
       "author":"John McCarthy (computer scientist)",
       "en":"Mental qualities peculiar to human-like motivational structures, such as love and hate, will not be required for intelligent behavior, but we could probably program computers to exhibit them if we wanted to."
    },
    {
       "id":"5a9d2f8c607c5100044dff77",
       "author":"Richard Stallman",
       "en":"I have met bright students in computer science who have never seen the source code of a large program. They may be good at writing small programs, but they can't begin to learn the different skills of writing large ones if they can't see how others have done it."
    },
    {
       "id":"5a9c65d6ff6af300049e6b5b",
       "author":"John McCarthy (computer scientist)",
       "en":"Program designers have a tendency to think of the users as idiots who need to be controlled. They should rather think of their program as a servant, whose master, the user, should be able to control it."
    },
    {
       "id":"5a9d3007607c5100044dff79",
       "author":"Richard Stallman",
       "en":"In fact, in the 1980s I often came across newly graduated computer science majors who had never seen a real program in their lives. They had only seen toy exercises, school exercises, because every real program was a trade secret."
    },
    {
       "id":"5a9d31fa607c5100044dff7c",
       "author":"Richard Stallman",
       "en":"I figure that since proprietary software developers use copyright to stop us from sharing, we cooperators can use copyright to give other cooperators an advantage of their own: they can use our code."
    },
    {
       "id":"5a9d2eb2607c5100044dff75",
       "author":"Richard Stallman",
       "en":"I consider that the golden rule requires that if I like a program I must share it with other people who like it. Software sellers want to divide the users and conquer them, making each user agree not to share with others. I refuse to break solidarity with other users in this way."
    },
    {
       "id":"5a9d33ae607c5100044dff7d",
       "author":"Richard Stallman",
       "en":"The free software community rejects the “priesthood of technology”, which keeps the general public in ignorance of how technology works; we encourage students of any age and situation to read the source code and learn as much as they want to know."
    },
    {
       "id":"5a9d3532607c5100044dff7e",
       "author":"Richard Stallman",
       "en":"The most powerful programming language is Lisp. If you don't know Lisp (or its variant, Scheme), you don't know what it means for a programming language to be powerful and elegant. Once you learn Lisp, you will understand what is lacking in most other languages."
    },
    {
       "id":"5a9d36a4607c5100044dff7f",
       "author":"Richard Stallman",
       "en":"Programming is programming. If you get good at programming, it doesn't matter which language you learned it in, because you'll be able to do programming in any language."
    },
    {
       "id":"5a9dc5de6744730004f6a1e6",
       "author":"Maurice Wilkes",
       "en":"It was on one of my journeys between the EDSAC room and the punching equipment the realization came over me with full force that a good part of the remainder of my life was going to be spent in finding errors in my own programs."
    },
    {
       "id":"5a9dc65d6744730004f6a1e8",
       "author":"Maurice Wilkes",
       "en":"Since 1954, the raw speed of computers, as measured by the time it takes to do an addition, increased by a factor of 10,000. That means an algorithm that once took 10 minutes to perform can now be done 15 times a second."
    },
    {
       "id":"5a9dc8e76744730004f6a1e9",
       "author":"Richard Hamming",
       "en":"Typing is no substitute for thinking."
    },
    {
       "id":"5a9d530a1a29250004e946df",
       "author":"Donald Knuth",
       "en":"A programmer who subconsciously views himself as an artist will enjoy what he does and will do it better."
    },
    {
       "id":"5a9dc9c26744730004f6a1ea",
       "author":"Richard Hamming",
       "en":"Perhaps the central problem we face in all of computer science is how we are to get to the situation where we build on top of the work of others rather than redoing so much of it in a trivially different way."
    },
    {
       "id":"5a9dcace6744730004f6a1eb",
       "author":"Richard Hamming",
       "en":"Any unwillingness to learn mathematics today can greatly restrict your possibilities tomorrow."
    },
    {
       "id":"5aa28cf31dcf530004c4bf64",
       "author":"Charles Simonyi",
       "en":"Really good programs live forever."
    },
    {
       "id":"5a9dccdd6744730004f6a1ec",
       "author":"Richard Hamming",
       "en":"In science if you know what you are doing you should not be doing it. In engineering if you do not know what you are doing you should not be doing it."
    },
    {
       "id":"5aa28d721dcf530004c4bf65",
       "author":"Butler Lampson",
       "en":"In handling resources, strive to avoid disaster rather than to attain an optimum."
    },
    {
       "id":"5aa28ea11dcf530004c4bf67",
       "author":"John Warnock",
       "en":"As with most projects, the last two percent takes fifty percent of the time."
    },
    {
       "id":"5aa299fbe7e86700048f0279",
       "author":"Gary Kildall",
       "en":"It's fun to sit at a terminal and let the code flow. It sounds strange, but it just comes out my brain; once I'm started, I don't have to think about it."
    },
    {
       "id":"5aa29b16e7e86700048f027a",
       "author":"Gary Kildall",
       "en":"I think programming is very much a religious experience for a lot of people."
    },
    {
       "id":"5aa28c251dcf530004c4bf63",
       "author":"Charles Simonyi",
       "en":"What is programming? Some people call it a science, some people call it an art, some people call it a skill. I think it has aspects of all three."
    },
    {
       "id":"5aa29bfee7e86700048f027b",
       "author":"Bill Gates",
       "en":"If you ever talk to a great programmer, you'll find he knows his tools like an artist knows his paintbrushes."
    },
    {
       "id":"5aa29c76e7e86700048f027c",
       "author":"Bill Gates",
       "en":"Our goals are very simple. We're going to create the software that puts a computer on every desk and in every home."
    },
    {
       "id":"5aa2a019e7e86700048f027f",
       "author":"Dan Bricklin",
       "en":"The most important part of writing a program is designing the data structures."
    },
    {
       "id":"5aa2a0ace7e86700048f0280",
       "author":"Bob Frankston",
       "en":"Ideas don't disappear. They change form, they merge with other ideas."
    },
    {
       "id":"5aa2a355e7e86700048f0284",
       "author":"Peter Roizen",
       "en":"I care not only what the code says but how it looks."
    },
    {
       "id":"5aa2a2f1e7e86700048f0283",
       "author":"Ray Ozzie",
       "en":"Programming is the ultimate field for someone who likes to tinker."
    },
    {
       "id":"5aa2a3fde7e86700048f0286",
       "author":"Bob Carr",
       "en":"Programming can be addictive."
    },
    {
       "id":"5aa2a3b3e7e86700048f0285",
       "author":"Bob Carr",
       "en":"From an artistic standpoint, the best software comes from the realm of intuition."
    },
    {
       "id":"5aa2a602e7e86700048f0287",
       "author":"Andy Hertzfeld",
       "en":"Then Apple went public toward the end of 1980. All of a sudden, all these people I was working with were millionaires."
    },
    {
       "id":"5aa2a68ce7e86700048f0288",
       "author":"Toru Iwatani",
       "en":"I'm interested in creating images that communicate with people."
    },
    {
       "id":"5aa31172bb93c00004d9a6f6",
       "author":"Charles Simonyi",
       "en":"I think the best way to supervise is by personal example and by frequent code reviews."
    },
    {
       "id":"5aa3181fbb93c00004d9a6f8",
       "author":"Butler Lampson",
       "en":"There are some basic techniques to control complexity. Fundamentally, I divide and conquer, break things down, and try to write reasonably precise descriptions of what each piece is supposed to do."
    },
    {
       "id":"5aa311f9bb93c00004d9a6f7",
       "author":"Charles Simonyi",
       "en":"The efficiency of the code decreases with an increase in the number of people working on the program. The most efficient programs are written by a single person."
    },
    {
       "id":"5aa30d4abb93c00004d9a6f5",
       "author":"Charles Simonyi",
       "en":"I'll bet you that from ten feet away I can tell if a program is bad. I might not guarantee that it is good, but if it looks bad from ten feet, I can guarantee you that it wasn't written with care."
    },
    {
       "id":"5aa44e197832df00040ac9b7",
       "author":"Butler Lampson",
       "en":"Nobody knows how to build really complicated hardware systems, so designing hardware tends to be simpler. Software is much more complicated."
    },
    {
       "id":"5aa4511b7832df00040ac9b8",
       "author":"Butler Lampson",
       "en":"A beautiful program is like a beautiful theorem: It does the job elegantly."
    },
    {
       "id":"5aa456667832df00040ac9b9",
       "author":"John Warnock",
       "en":"To be successful, you want to surround yourself with very talented folks whose skills blend very well. That’s the secret of success."
    },
    {
       "id":"5aa459d77832df00040ac9bc",
       "author":"Gary Kildall",
       "en":"I start with drawing the data structures, and I spend a lot of time thinking about them. I also think about what the program has to go through before I start writing code."
    },
    {
       "id":"5aa456d87832df00040ac9ba",
       "author":"John Warnock",
       "en":"Don’t go into a two-year development with nothing coming out in the middle. Have something come out every two months, so you can evaluate, regroup, and restart."
    },
    {
       "id":"5aa459767832df00040ac9bb",
       "author":"Gary Kildall",
       "en":"If you learn how to solve problems, you can go through life and do pretty well."
    },
    {
       "id":"5aa45f317832df00040ac9c0",
       "author":"Bill Gates",
       "en":"A great programmer thinks about the program on a constant basis, whether driving or eating. That method takes an incredible amount of mental energy."
    },
    {
       "id":"5aa4601c7832df00040ac9c1",
       "author":"Bill Gates",
       "en":"The really great programs I've written have all been ones that I have thought about for a huge amount of time before I ever wrote them."
    },
    {
       "id":"5aa461667832df00040ac9c2",
       "author":"Bill Gates",
       "en":"There is an amazing commonality in the types of difficulties you run into. In design reviews, I really enjoy being able to provide advice, based on programs that I have done."
    },
    {
       "id":"5a9b16b92bad9600044b6fe3",
       "author":"Fred Brooks",
       "en":"The fundamental problem with program maintenance is that fixing a defect has a substantial (20-50 percent) chance of introducing another. So the whole process is two steps forward and one step back."
    },
    {
       "id":"5aa5c874d1481c4acc43aa71",
       "author":"Addy Osmani",
       "en":"Really care about the tools you use because they are what make you your best."
    },
    {
       "id":"5aa63f3a42fbc6000481ca0d",
       "author":"Michael Hawley",
       "en":"What I like about programming is that it really helps you think about how we communicate, how we think, how logic works, how creative arts work."
    },
    {
       "id":"5aa6de2101c2c400048eb9a8",
       "author":"Douglas Crockford",
       "en":"One of the things I’ve been pushing is code reading. I think that is the most useful thing that a community of programmers can do for each other—spend time on a regular basis reading each other’s code."
    },
    {
       "id":"5aa6dd2101c2c400048eb9a7",
       "author":"Douglas Crockford",
       "en":"I think the best way to make JavaScript better would be to\nmake it smaller. If we could just get it down to what it does really well and remove the features that add little or no value, it’s actually a better language."
    },
    {
       "id":"5aa6e0d101c2c400048eb9a9",
       "author":"Douglas Crockford",
       "en":"Readability of code is now my first priority. It’s more important than being fast, almost as important as being correct, but I think being readable is actually the most likely way of making it correct."
    },
    {
       "id":"5aa6e37801c2c400048eb9aa",
       "author":"Douglas Crockford",
       "en":"Part of what makes programming difficult is most of the time we’re doing stuff we’ve never done before."
    },
    {
       "id":"5aa6e8ac01c2c400048eb9ab",
       "author":"Douglas Crockford",
       "en":"I think of myself as a writer. Sometimes I write in English and sometimes I write in JavaScript."
    },
    {
       "id":"5aa63e0642fbc6000481ca0c",
       "author":"Jaron Lanier",
       "en":"People should be able to speak and breathe programs just like they talk now."
    },
    {
       "id":"5aa9a89904c8cd0004d472c4",
       "author":"Joe Armstrong (programmer)",
       "en":"If you start removing things, if you get to the point where if you were to remove anything more it would not work any more — at this point it is beautiful."
    },
    {
       "id":"5aa8307a94bd610da89b3340",
       "author":"Buckminster Fuller",
       "en":"Humanity is acquiring all the right technology for all the wrong reasons."
    },
    {
       "id":"5aa9aa9f04c8cd0004d472c5",
       "author":"Simon Peyton Jones",
       "en":"I characterize functional programming as a radical and elegant attack on the whole enterprise of writing programs."
    },
    {
       "id":"5aab9d9617c21b0004913edc",
       "author":"Marijn Haverbeke",
       "en":"Size almost always involves complexity, and complexity confuses programmers. Confused programmers, in turn, introduce mistakes (bugs) into programs."
    },
    {
       "id":"5aab9ade17c21b0004913edb",
       "author":"Marijn Haverbeke",
       "en":"Flaws in computer programs are usually called bugs. It makes programmers feel good to imagine them as little things that just happen to crawl into our work. In reality, of course, we put them there ourselves."
    },
    {
       "id":"5aac2850c2138a00046e9183",
       "author":"L. Peter Deutsch",
       "en":"When I was at what I would consider the peak of my abilities, I had extremely trustworthy intuition. I would do things and they would just turn out right."
    },
    {
       "id":"5aac2af1c2138a00046e9185",
       "author":"L. Peter Deutsch",
       "en":"Every now and then I feel a temptation to design a programming language but then I just lie down until it goes away."
    },
    {
       "id":"5aac2cf9c2138a00046e9186",
       "author":"L. Peter Deutsch",
       "en":"Language systems stand on a tripod. There’s the language, there’s the libraries, and there are the tools. And how successful a language is depends on a complex interaction between those three things."
    },
    {
       "id":"5aac29e1c2138a00046e9184",
       "author":"L. Peter Deutsch",
       "en":"I would make a strong case that programming languages have not improved qualitatively in the last 40 years. There is no programming language in use today that is qualitatively better than Simula-67."
    },
    {
       "id":"5aac303cc2138a00046e9188",
       "author":"Gottfried Wilhelm Leibniz",
       "en":"Instead of the progression of tens, I have for many years used the simplest progression of all, which proceeds by twos, having found that it is useful for the perfection of the science of numbers."
    },
    {
       "id":"5aac2e8fc2138a00046e9187",
       "author":"L. Peter Deutsch",
       "en":"I never in my wildest dreams would have predicted the evolution of the Internet. And I never would’ve predicted the degree to which corporate influence over the Internet has changed its character over time."
    },
    {
       "id":"5aac3a57610d7d0004066303",
       "author":"Ken Thompson",
       "en":"I’ve never been a lover of existing code. Code by itself almost rots and it’s gotta be rewritten. Even when nothing has changed, for some reason it rots."
    },
    {
       "id":"5aac39b1610d7d0004066302",
       "author":"Ken Thompson",
       "en":"Modern programming scares me in many respects. It confuses me to read a program which you must read top-down. It says “do something.” And you go find “something.” And you read it and it says, “do something else” and you go find something and it says, “do something else” and it goes back to the top maybe. And nothing gets done. It’s just relegating the problem to a deeper and deeper level."
    },
    {
       "id":"5aa9a7b304c8cd0004d472c3",
       "author":"Richard Hamming",
       "en":"I always spend a day a week learning new stuff. That means I spend 20% more of my time than my colleagues learning new stuff. Now 20% at compound interest means that after four and a half years I will know twice as much as them."
    },
    {
       "id":"5aad68d17632ba0004ec84ae",
       "author":"Donald Knuth",
       "en":"I’ll use dirty tricks for two reasons. One is, if it’s really going to give me a performance improvement. Or sometimes just for pure pleasure. In any case, I document it; I don’t just put it in there."
    },
    {
       "id":"5aac3aa3610d7d0004066304",
       "author":"Ken Thompson",
       "en":"I’ll throw away code as soon I want to add something to it and I get the feeling that what I have to do to add it is too hard."
    },
    {
       "id":"5aad69767632ba0004ec84af",
       "author":"Donald Knuth",
       "en":"The problem is that coding isn’t fun if all you can do is call things out of a library, if you can’t write the library yourself."
    },
    {
       "id":"5aad6d0d7632ba0004ec84b0",
       "author":"Donald Knuth",
       "en":"I make mistakes because I’m always operating at my limit. If I only stay in comfortable territory all the time, that’s not so much fun."
    },
    {
       "id":"5aad6dfa7632ba0004ec84b1",
       "author":"Donald Knuth",
       "en":"I’ve got this need to program. I wake up in the morning with sentences of a literate program. Before breakfast — I’m sure poets must feel this — I have to go to the computer and write this paragraph and then I can eat and I’m happy."
    },
    {
       "id":"5aad71337632ba0004ec84b2",
       "author":"Donald Knuth",
       "en":"The more varieties of different kinds of notations are still useful — don’t only read the people who code like you."
    },
    {
       "id":"5ab6e0d632a9950004a2efc2",
       "author":"Ted Nelson",
       "en":"The good news about computers is that they do what you tell them to do. The bad news is that they do what you tell them to do."
    },
    {
       "id":"5aa6e99001c2c400048eb9ac",
       "author":"Douglas Crockford",
       "en":"Mathematics is important in programming, but it’s just one of a lot of things that are important. If you overemphasize the math then you underemphasize stuff which might be even more important, such as literacy."
    },
    {
       "id":"5aac3b37610d7d0004066305",
       "author":"Ken Thompson",
       "en":"Documenting is very, very hard; it’s time-consuming. To do it right, you’ve got to do it like programming. You’ve got to deconstruct it, put it together in nice ways, rewrite it when it’s wrong. People don’t do that."
    },
    {
       "id":"5ab6e20132a9950004a2efc6",
       "author":"Ted Nelson",
       "en":"Making things easy is hard."
    },
    {
       "id":"5ab6e9e132a9950004a2efc7",
       "author":"Richard Moore (engineer)",
       "en":"The difference between theory and practice is that in theory, there is no difference between theory and practice."
    },
    {
       "id":"5ab6ea2a32a9950004a2efc8",
       "author":"Jim Coplien",
       "en":"You should name a variable using the same care with which you name a first-born child."
    },
    {
       "id":"5acca81fe01bb40004668819",
       "author":"Robert C. Martin",
       "en":"The ratio of time spent reading versus writing is well over 10 to 1. We are constantly reading old code as part of the effort to write new code."
    },
    {
       "id":"5b579bb420e9780004ba9ac3",
       "author":"Kyle Simpson",
       "en":"There's nothing more permanent than a temporary hack."
    },
    {
       "id":"5b6d73d6b3f09f0004d9275f",
       "author":"Gottfried Wilhelm Leibniz",
       "en":"As numbers are reduced to the simplest principles, like 0 and 1, a wonderful order is apparent throughout."
    },
    {
       "id":"5ab6e1ad32a9950004a2efc4",
       "author":"Ted Nelson",
       "en":"In my second year in graduate school, I took a computer course and that was like lightening striking."
    },
    {
       "id":"5ab6e13932a9950004a2efc3",
       "author":"Ted Nelson",
       "en":"They were saying computers deal with numbers. This was absolutely nonsense. Computers deal with arbitrary information of any kind."
    },
    {
       "id":"5ab6e1dd32a9950004a2efc5",
       "author":"Ted Nelson",
       "en":"Right now you are a prisoner of each application you use. You have only the options that were given you by the developer of that application."
    },
    {
       "id":"5a6ce86f2af929789500e83d",
       "author":"Ray Ozzie",
       "en":"Complexity kills. It sucks the life out of developers, it makes products difficult to plan, build and test, it introduces security challenges and it causes end-user and administrator frustration."
    },
    {
       "id":"5a6ce8702af929789500e882",
       "author":"Niklaus Wirth",
       "en":"Software gets slower faster than hardware gets faster."
    },
    {
       "id":"5a6ce8702af929789500e89e",
       "author":"David Parnas",
       "en":"A computer is a stupid machine with the ability to do incredibly smart things, while computer programmers are smart people with the ability to do incredibly stupid things. They are, in short, a perfect match."
    },
    {
       "id":"5a6ce8702af929789500e8c4",
       "author":"Anonymous",
       "en":"A few months writing code can save you a few hours in design."
    },
    {
       "id":"5a72f8251ac5f022282e4125",
       "author":"Edsger W. Dijkstra",
       "en":"Are you quite sure that all those bells and whistles, all those wonderful facilities of your so called powerful programming languages, belong to the solution set rather than the problem set?"
    },
    {
       "id":"5a91e3a1c4240c0004265956",
       "author":"John von Neumann",
       "en":"If people do not believe that mathematics is simple, it is only because they do not realize how complicated life is."
    },
    {
       "id":"5a933a408e7b510004cba4bb",
       "author":"Bjarne Stroustrup",
       "en":"C makes it easy to shoot yourself in the foot; C++ makes it harder, but when you do it blows your whole leg off."
    },
    {
       "id":"5a933a668e7b510004cba4bc",
       "author":"Bjarne Stroustrup",
       "en":"If you think it's simple, then you have misunderstood the problem."
    },
    {
       "id":"5a9342458e7b510004cba4c7",
       "author":"Rob Pike",
       "en":"Object-oriented design is the roman numerals of computing."
    },
    {
       "id":"5a93d61c6a584e0004a4a613",
       "author":"Steve Jobs",
       "en":"It is hard to think that a $2 billion company with 4,300-plus people couldn't compete with six people in blue jeans."
    },
    {
       "id":"5a93ffbae49ad10004edb861",
       "author":"Jamie Zawinski",
       "en":"Some people, when confronted with a problem, think ‘I know, I’ll use regular expressions.’ Now they have two problems."
    },
    {
       "id":"5a943255ee7ed5000496b17c",
       "author":"Bill Gates",
       "en":"Sometimes we do get taken by surprise. For example, when the Internet came along, we had it as a fifth or sixth priority."
    },
    {
       "id":"5a9432f0ee7ed5000496b180",
       "author":"Ward Cunningham",
       "en":"It was a turning point in my programming career when I realized that I didn't have to win every argument."
    },
    {
       "id":"5a9435b6ee7ed5000496b18f",
       "author":"Vint Cerf",
       "en":"And programming computers was so fascinating. You create your own little universe, and then it does what you tell it to do."
    },
    {
       "id":"5a943552ee7ed5000496b18d",
       "author":"Joshua Bloch",
       "en":"The cleaner and nicer the program, the faster it's going to run. And if it doesn't, it'll be easy to make it fast."
    },
    {
       "id":"5a9436dcee7ed5000496b194",
       "author":"Philip Greenspun",
       "en":"SQL, Lisp, and Haskell are the only programming languages that I've seen where one spends more time thinking than typing."
    },
    {
       "id":"5a95a610cb1a4d0004b2987e",
       "author":"Alan Perlis",
       "en":"It is better to have 100 functions operate on one data structure than to have 10 functions operate on 10 data structures."
    },
    {
       "id":"5a95d1077700780004d51db9",
       "author":"Brian Kernighan",
       "en":"The most effective debugging tool is still careful thought, coupled with judiciously placed print statements."
    },
    {
       "id":"5a95d7637700780004d51dc5",
       "author":"Marvin Minsky",
       "en":"Computer languages of the future will be more concerned with goals and less with procedures specified by the programmer."
    },
    {
       "id":"5a95fe167700780004d51dcd",
       "author":"Alan Turing",
       "en":"A computer would deserve to be called intelligent if it could deceive a human into believing that it was human."
    },
    {
       "id":"5a96be3ed6959500047aecbd",
       "author":"Joseph Yoder (computer scientist)",
       "en":"The way to arrest entropy in software is to refactor it."
    },
    {
       "id":"5a96bf21d6959500047aecc0",
       "author":"Joseph Yoder (computer scientist)",
       "en":"Reviews and pair programming provide programmers with something their work would not otherwise have: an audience. Sunlight, it is said is a powerful disinfectant. An immediate audience of one's peers provides immediate incentives to programmers to keep their code clear and comprehensible, as well as functional."
    },
    {
       "id":"5a97f2c0ccdfe50004febf38",
       "author":"John Romero",
       "en":"You might not think that programmers are artists, but programming is an extremely creative profession. It's logic-based creativity."
    },
    {
       "id":"5a97f4c5ccdfe50004febf3c",
       "author":"Douglas Crockford",
       "en":"JavaScript is the only language that I'm aware of that people feel they don't need to learn before they start using it."
    },
    {
       "id":"5a9808951878b40004879f61",
       "author":"Addy Osmani",
       "en":"Be humble, communicate clearly, and respect others. It costs nothing to be kind, but the impact is priceless."
    },
    {
       "id":"5a9808dc1878b40004879f63",
       "author":"Pete Cordell",
       "en":"Telling a programmer there's already a library to do X is like telling a songwriter there's already a song about love."
    },
    {
       "id":"5a980f551878b40004879f68",
       "author":"Stan Kelly-Bootle",
       "en":"Should array indices start at 0 or 1? My compromise of 0.5 was rejected without, I thought, proper consideration."
    },
    {
       "id":"5a985fd2e93441000489b94d",
       "author":"Edsger W. Dijkstra",
       "en":"The purpose of abstraction is not to be vague, but to create a new semantic level in which one can be absolutely precise."
    },
    {
       "id":"5a9a9e792bad9600044b6fb5",
       "author":"Elon Musk",
       "en":"There certainly will be job disruption. Because what's going to happen is robots will be able to do everything better than us."
    },
    {
       "id":"5a9860dbe93441000489b950",
       "author":"John Carmack",
       "en":"Sometimes, the elegant implementation is a function. Not a method. Not a class. Not a framework. Just a function."
    },
    {
       "id":"5a9aa0f72bad9600044b6fb8",
       "author":"Marvin Minsky",
       "en":"Artificial intelligence is the science of making machines do things that would require intelligence if done by men."
    },
    {
       "id":"5a9aaf682bad9600044b6fbb",
       "author":"Tim Berners-Lee",
       "en":"I just had to take the hypertext idea and connect it to the TCP and DNS ideas and — ta-da!— the World Wide Web."
    },
    {
       "id":"5a9b0d552bad9600044b6fd4",
       "author":"Hal Abelson",
       "en":"A computational process is indeed much like a sorcerer's idea of a spirit. It cannot be seen or touched. It is not composed of matter at all. However, it is very real. It can perform intellectual work. It can answer questions. It can affect the world by disbursing money at a bank or by controlling a robot arm in a factory."
    },
    {
       "id":"5a9b17792bad9600044b6fe5",
       "author":"Fred Brooks",
       "en":"One must assume that there will be lots of bugs, and plan an orderly procedure for snaking them out."
    },
    {
       "id":"5a9b19662bad9600044b6ff1",
       "author":"Fred Brooks",
       "en":"To achieve conceptual integrity, a design must proceed from one mind or a small group of agreeing minds."
    },
    {
       "id":"5a9b1d152bad9600044b6ff9",
       "author":"Tom DeMarco",
       "en":"The very best technology never has as much impact as girlfriend or boyfriend trouble."
    },
    {
       "id":"5a9b19952bad9600044b6ff3",
       "author":"Fred Brooks",
       "en":"Maintenance cost is strongly affected by the number of users. More users find more bugs."
    },
    {
       "id":"5a9b1f8c2bad9600044b7003",
       "author":"Daniel T. Barry",
       "en":"Most errors are introduced during requirements specification!"
    },
    {
       "id":"5a9b21892bad9600044b7006",
       "author":"Harlan Mills",
       "en":"Programming is similar to a game of golf. The point is not getting the ball in the hole but how many strokes it takes."
    },
    {
       "id":"5a9b22b42bad9600044b700a",
       "author":"Daniel T. Barry",
       "en":"A number of studies have shown testing not very effective at finding bugs."
    },
    {
       "id":"5a9b23cd2bad9600044b7010",
       "author":"Daniel T. Barry",
       "en":"The key to keeping software costs down is to write code that is easily modified."
    },
    {
       "id":"5a9b24492bad9600044b7014",
       "author":"Daniel T. Barry",
       "en":"The notions of correctness in mathematics and programs are different. A mathematical model must be consistent; it need not match reality (be correct), and it need not be complete (in the formal sense). A program model must be consistent; it must match reality; and it must be complete (in the sense that it reacts gracefully to all inputs)."
    },
    {
       "id":"5a9b23ed2bad9600044b7012",
       "author":"Daniel T. Barry",
       "en":"Programming is at least as difficult as developing a mathematical theory."
    },
    {
       "id":"5a9d2fc8607c5100044dff78",
       "author":"Richard Stallman",
       "en":"In 1971 when I joined the staff of the MIT Artificial Intelligence lab, all of us who helped develop the operating system software, we called ourselves hackers. We were not breaking any laws, at least not in doing the hacking we were paid to do. We were developing software and we were having fun. Hacking refers to the spirit of fun in which we were developing software."
    },
    {
       "id":"5a9dc6316744730004f6a1e7",
       "author":"Maurice Wilkes",
       "en":"By June 1949 people had begun to realize that it was not so easy to get programs right as at one time appeared."
    },
    {
       "id":"5aa28dd71dcf530004c4bf66",
       "author":"Butler Lampson",
       "en":"Everything should be made as simple as possible. But to do that you have to master complexity."
    },
    {
       "id":"5aa29df5e7e86700048f027d",
       "author":"Wayne Ratliff",
       "en":"If I had followed my heart instead of advice, dBASE would be much closer to perfection today."
    },
    {
       "id":"5aa29e43e7e86700048f027e",
       "author":"Wayne Ratliff",
       "en":"Programming is a little bit like the army. Now that I'm out, it's neat to have had the experience."
    },
    {
       "id":"5aa2a20ce7e86700048f0282",
       "author":"Jonathan Sachs",
       "en":"I don't like using any tools or programs I didn't write myself or that I don't have some control over."
    },
    {
       "id":"5aa2a15fe7e86700048f0281",
       "author":"Bob Frankston",
       "en":"If you cannot explain a program to yourself, the chance of the\ncomputer getting it right is pretty small."
    },
    {
       "id":"5aa45ab57832df00040ac9bd",
       "author":"Gary Kildall",
       "en":"I don't comment on the code itself because I feel that properly written code is very much self-documented."
    },
    {
       "id":"5aa45bcf7832df00040ac9be",
       "author":"Gary Kildall",
       "en":"When a program is clean and neat, nicely structured, and consistent, it can be beautiful."
    },
    {
       "id":"5aa6db5d01c2c400048eb9a6",
       "author":"Douglas Crockford",
       "en":"JavaScript, purely by accident, has become the most popular programming language in the world."
    },
    {
       "id":"5aac2669c2138a00046e9182",
       "author":"L. Peter Deutsch",
       "en":"Software is a discipline of detail, and that is a deep, horrendous fundamental problem with software."
    },
    {
       "id":"5aac309cc2138a00046e9189",
       "author":"Gottfried Wilhelm Leibniz",
       "en":"Even in the games of children there are things to interest the greatest mathematician."
    }
 ]

routes = {
    "routes": {
        '/': 'GET',
        '/allusers': 'GET',
        '/getuser': 'GET',
        '/login': 'POST',
    }
}


@api_view(['GET'])
def statusOk():
      return JsonResponse({
         "message": "success",
         "data": "server is up and running"
      }, status=status.HTTP_200_OK)

@api_view(['GET'])
def getallavailableroutes(request):
    starttime = datetime.now()
    print("getallavailableroutes fetching from cache")
    list = cache.get('getallavailableroutes')
    if list is None:
        if request.method == 'GET':
            cache.set('getallavailableroutes', routes, timeout=60*1500)
            endtime = datetime.now()
            return JsonResponse({
            "message": "success",
            "time_taken": str(endtime - starttime),
            "server": "db",
            "data": routes,
        }, status=status.HTTP_200_OK)
    else:
        endtime = datetime.now()
        return JsonResponse({
            "message": "success",
            "time_taken": str(endtime - starttime),
            "data": list,
            "server": "cache server v2"
        }, status=status.HTTP_200_OK)
    



@api_view(['GET'])
def getrandomprogrammingquote(request):
    starttime = datetime.now()
    print("getrandomprogrammingquote fetching from cache")
    list = cache.get('getrandomprogrammingquote')
    if list is None:
        if request.method == 'GET':
            random_quote = random.choice(quotes)
            cache.set('getrandomprogrammingquote', random_quote, timeout=60*1500)
            endtime = datetime.now()
            return JsonResponse({
            "message": "success",
            "time_taken": str(endtime - starttime),
            "server": "db",
            "data": random_quote,
        }, status=status.HTTP_200_OK)
    else:
        endtime = datetime.now()
        return JsonResponse({
            "message": "success",
            "time_taken": str(endtime - starttime),
            "data": list,
            "server": "cache server v2"
        }, status=status.HTTP_200_OK)