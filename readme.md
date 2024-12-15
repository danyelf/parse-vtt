# Concept

Convert the  .vtt file generated by Google Meet to human-readable (and copy-pastable!) transcript.

Google's Meet output .vtt looks like this. Note that the blank lines in the middle of the paragraphs, which  -- interestingly -- aren't legal WebVTT.

This script:
1- Removes those blank lines.
2- consolidates passages together
3- generates a human-readable output that is easier to copy and paste.

Note that human conversation isn't great here -- people talk over themselves. With more effort, I could have tried to do something to show the interruptions better. But this gets me through today, and my goal of making a transcript I can copy/paste out of.


```
00:00:08.000 --> 00:00:12.000
(Danyel Fisher)
I wanted to start with first is just a little bit of background so we know who we're talking

00:00:12.000 --> 00:00:16.000
(Danyel Fisher)
to. Um what is your uh

00:00:16.000 --> 00:00:20.000
(Danyel Fisher)
background?
-
 
(Dana Bettinger)
Safaria wise or lifewise

00:00:20.000 --> 00:00:24.000
(Danyel Fisher)
Um let's go with uh Jewish wise do you
-
 
(Dana Bettinger)
or Jewish
```

which has the data, but what I want is more:

```
Danyel Fisher (00:00:08.000)
I wanted to start with first is just a little bit of background so we know who we're talking to. Um what is your uh background?
 
Dana Bettinger (00:090:16.000)
Safaria wise or lifewise? or Jewish

Danyel Fisher (00:00:20.000)
Um let's go with uh Jewish wise do you
 ```

