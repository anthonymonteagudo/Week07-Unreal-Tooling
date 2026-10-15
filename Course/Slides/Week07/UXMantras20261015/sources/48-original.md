
![[Pasted image 20261015021640.png]]

![[Pasted image 20261015021652.png]]

![[Pasted image 20261015022110.png]]

![[Pasted image 20261015022155.png]]

![[Pasted image 20261015022220.png]]

![[Pasted image 20261015022339.png]]

![[Pasted image 20261015022411.png]]

![[Pasted image 20261015022434.png]]

![[Pasted image 20261015022458.png]]

One of the ways that you do this is that you work to separate primary and secondary actions.

And you heard this from me previously Economy, clarity, focus is created by differentiating primary

actions.

So if we have two options, save and cancel right out of the box in bootstrap, for example, just to

pick on something right out of the box, every interaction is a button, okay?

In most templates in most libraries.

So if you have choices, save, cancel whatever they're buttons, they're blue buttons, they're the

default style.

And what happens is typically the design development teams will leave those defaults.

What do you think happens as a result of that?

And I'm sure some of you are saying it to yourself.

What happens is a lot of times people hit cancel when they mean to hit save.

And in cases where the state isn't saved, where the data isn't saved within that session, and believe

me, there are a lot of them, despite what you may think, they lose all their stuff and they have

to start again.

That is bad, that's destructive, and it ensures that people probably will not try a second time if

you piss them off.

So the better way to treat this is like this.

The primary action is always a button.

It's got the most contrast.

It takes up more visual space.

It's distinct.

The secondary action is text.

It's not a button, it's not anything resembling a button.

There is no question visually that here's the primary thing you're here to do.

Here's the secondary thing you're here to do.

That kind of differentiation is really, really important for ease of use, for efficiency and for accuracy.

The same principle applies when there are tertiary or even quaternary actions.

So if we have three options, we can create a file, We can save a draft of an existing file, or we

can cancel what we're doing.

In that case, we still treat them as three distinct things, but we work to establish a hierarchy where

the primary action is still the most important that will look like this.

The create button again because it's blue, because it's solid, because it has the most contrast is

the primary action.

Save draft is the secondary action.

So it is still a button shape which makes it more important then cancel.

But it's all gray.

It's what we call I've heard this referred to as a ghost button.

It's white, it's got gray text, gray outline still there.

Very subtle, very simple, but it still reads like a button.

And finally, the tertiary action is cancel.

It's just text.

Do you see how the visual hierarchy decreases from primary to tertiary?

So think about that.

Every single screen you design, when there are multiple interactive controls, multiple interactive

cues work to differentiate the primary action.

Sometimes if you do nothing but this in an enterprise application, ease of use skyrockets accuracy

and completing forms skyrockets.

And even just getting people to go through the workflow and do all the things they're supposed to do

often increases as well.

This is a very big deal.

Let's look at an example where content is again mixed with controls.

Interactive things are mixed with non interactive things, and flat design is taken to sort of a ridiculous

extreme.

Now, from a visual design standpoint, this is nice to look at.

It's very well designed.

It's attractive.

However, there are some very serious flaws in what they've done, and I'd like to walk you through

those.

First of all, this whole details looks like a button, right?

It's got a rectangle around it and it looks like a button, but it's not its content, it's a headline.

It doesn't do anything.

You can tap or click on this all day long and you'll get nothing.

So the customization hole details, those are both just headlines and they are visually treated like

buttons.

This is someone being clever for the sake of being clever.

All they care about is what it looks like.

Well, that looks pretty good.

I'm going to do that.

But it sends the wrong signal to people who are trying to use it.

That's the first thing.

The second thing is that these controls previous next add to cart, they're indistinct.

Same goes for the dropdown menus.

They're very subtle.

They're barely there and there's nothing about them that signifies clearly that they do something.

Well, people figure it out.

Yes, but because of the extreme subtlety here, people will confuse what's interactive and what's not,

and they won't be able to quickly and easily act on this.

So how do we fix that?

Well, we do a couple of things.

Number one, we use common conventions.

There's no reason for a previous and next button convention for pagination is this you got an arrow

on the left to go back and an arrow on the right to go forward.

And in between you've got the number of screens that are there.

So again, don't reinvent the wheel.

Stick with convention.

Those buttons are unnecessary and all they do is compete with the other elements on the page.

That's first.

Second, increase the contrast in these dropdowns to separate and emphasize them as interactive controls.

Make them stand out a little more from the background so that it's clear.

Also, we added a border and some padding to this add to cart button to separate and emphasize that

it's an interactive control when a button spans the entire width of a column of a space in the grid,

it doesn't look like a button anymore.

It looks like a decoration.

It looks like a headline background.

All right.

So that extra space, that enclosure around the button makes sure that we read it as a button.

And finally, you will notice that we changed those headlines up, their whole details, customization.

We remove that rule.

So now there's no question that that's just a headline.

It's just a category call out.

This is an example of clear separation between what's content and what's interactive control.

So we look at them side by side.

Here's where we were, here's where we are.

Do you see the difference?

There is no question in that second option, what is interactive and what isn't?

Because the core action which is add to Cart is very clear.

Those dropdowns stand out.

The headlines are not competing with anything else that previous.

Next isn't competing with anything else.

We can focus on the product we're buying and the action we're taking right now.

So UI design mantra number 18 is that you should always be working to separate content from controls.