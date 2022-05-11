# SERVICE

## Introduction and background

This is the server-side code repository for the [SERVICE project](https://serviceproject.org.uk) (<u>S</u>ocial and <u>E</u>motional <u>R</u>esilience for the <u>V</u>ulnerable <u>I</u>mpacted by the <u>C</u>OVID-19 <u>E</u>mergency). SERVICE is the successor to the earlier *COVID-Stretch* project.

SERVICE attempts to monitor (and, eventually, improve) the emotional state of vulnerable (primarily elderly) people who have been forced into isolation by crises such as the 2020-22 COVID-19 pandemic. It consists of a mobile app which runs on client Android and iOS devices, and this backend server. The user is asked to regularly enter a record of their wellbeing, including answers to a few questions about activities they've performed during the last logged period (nominally a day). These records are uploaded to the server running this software (via its API), where the project researchers (and eventually clinical support staff involved with the clients) can observe and monitor them. The plan is that eventually we'll be able to use machine learning and medical advice to provide suggestions for activities and pastimes that are likely to positively reinforce the clients' state of mind. In addition, the monitored data can serve as a status warning or alert to the key workers who supervise the isolated clients, helping them know who needs help most urgently.

The code in this repository is a mixed bag. The project has grown organically, rather than having a fixed specification in mind from the beginning, and consequently the code is replete with retcons, patches, replacements, stubs of unused ideas, and abortive attempts at extensions which ran out of resources. The programming team has changed multiple times, leading to an uneven mix of styles and approaches. The server environment has changed multiple times, leading to several hacks and workarounds for issues that in many cases no longer need hacks or workarounds, but because things could have changed back, we had to leave them in. It's all a bit chaotic. It uses multiple different methods of achieving similar goals, even in cases where, with a bit of rationalisation, we could drop either one in favour of the other. Similarly, there are traces left of experiments which failed, but with a bit of work they could be tidied up and removed.

That said, in its current form, it works fairly stably. The server can be run either locally or in a Docker/Kubernetes container (the latter being the recommendation for anything serious), and the API will accept requests from the corresponding client app or another client program as documented.

You can find out more about SERVICE at the [SERVICE project website](https://serviceproject.org.uk).

You can find out more about Django, the underlying web content engine that the SERVICE server uses, in [the Django documentation](https://docs.djangoproject.com).

[Back to README.md](README.md)

Next: [Setting up a server](ServerSetup.md)
