![[Pasted image 20261015015749.png]]

![[Pasted image 20261015015900.png]]

![[Pasted image 20261015015949.png]]

![[Pasted image 20261015020018.png]]

![[Pasted image 20261015020038.png]]

![[Pasted image 20261015020126.png]]

![[Pasted image 20261015020207.png]]

![[Pasted image 20261015020247.png]]

![[Pasted image 20261015020304.png]]

![[Pasted image 20261015020429.png]]

![[Pasted image 20261015020504.png]]

![[Pasted image 20261015020548.png]]

Now let's use some of those principles to fix a really cluttered UI.

This is a beautiful example of what typically passes for state of the art in enterprise software.

I hate that term with a passion.

Number one, it's an old term.

Number two, it's still being used as if what we're looking at here is some sort of modern marvel of

interface design and efficiency, which it most certainly isn't.

This is riddled with visual clutter, and we're going to fix that.

So here's our starting point.

Okay, here's the interface as it is.

You can see that there's a lot going on here.

There's a lot of information jammed together tightly.

It's all very small and very tight and it's all blending into each other.

There's no clear differentiation between things.

So the first thing we're going to do is we're going to increase the negative space.

If you look at this, all those areas of magenta that I just highlighted, look at the randomness.

Remember what I've told you about alignment and proximity in particular.

There is no consistency in the distances between items.

There's no clear separation that groups these things.

This is one group.

This is one group, this is one group.

It's sort of all runs together because the negative space is very haphazard.

We're going to change that.

We're going to make it more purposeful.

When you increase the padding just about everywhere, you start to get clearer chunks, groups of information,

which makes it easier to quickly bounce and scan and look at what's here.

So here's what we did in this instance.

We increased the container margins on all four sides, everywhere, every single area, every single

container, more space inside the margins.

We also increased the margins after each paragraph and line height, extra space start to separate those

things.

We also increase the padding inside containers, cells, fields, buttons.

Any type of enclosure here has a lot more padding, a lot more air inside it.

That again, allows us to focus on the label.

If you even look at those buttons at the top, save refresh edit mode, close the air between the edge

of the button and the word itself.

The label goes a long way in allowing people to sort of quickly read and understand.

Second thing we're going to do is remove all the unnecessary rules and containers.

If you take a look at this, look at all the outlines on these containers, everything has a rule around

it, which because of the way that they're using color and because of the contrast here is really,

for the most part, unnecessary.

Those rules aren't really doing anything.

They're not separating anything.

They're not really helping us move through this.

They're just extra visual noise.

They're unnecessary.

So we're going to take them out, See the difference?

All those groups still hold together the chunks of information, the left hand navigation, that information

tree in the middle, those tabs in the center, the grid based data towards the bottom.

They are still holding together as chunks.

Without those rules, we still see separate sections without those rules.

So what we did here is we removed any unnecessary rules that we could find.

Instead, we used negative space and alignment to create those visual groups, just like we learned

very early on in this course, we removed the rules from existing enclosures that already have background

colors, areas like that, left hand blue vertical navigation, the sub navigation, the hierarchical

tree next to it, the tabs next to that.

Okay, the rules are unnecessary.

When you have a background color that's already defining a shape, the rule isn't necessary.

We also used color instead of rules wherever possible.

If we can differentiate by color, if we can differentiate by shade, you want to do that first?

We visually separated the navigation areas, made a very distinct change between what's navigation and

what's content.

We also lightened any rules that must be used.

Okay.

And a couple of cases here, like the rules around the fields, for example, or for instance, the

separation on that tree menu.

You can see there's a white rule around that box.

All right.

We changed it from a harder, dark gray rule to a light rule.

It's barely there, but it does help separate things.

So if we have to if we feel like we have to use a rule to visually separate something, you make sure

that it's contrast is much, much, much lower than the content that it delineates.

Next, we're going to separate labels from content and tables and forms.

If you take a look at this interface, all this text is treated the same way from the navigation at

the top to the three tiers of navigation right below it to the breadcrumb trail that happens to all

the way down in these menus.

It's all the same font.

It's the same size, it's the same case, it's all lowercase, it's the exact same color.

You have to work to visually separate labels from content controls, from content.

Okay, Interactive elements.

They should be treated visually.

Julie differently in some way when all this text is the same size, same font.

Same treatment, it makes it much harder for us to quickly get through this because we have to read

everything because it's all the same and it's all calling for our attention.

So here's what we're going to do.

We're going to change the case and or the color of navigation menu items.

We made them all caps.

If you look up at the top, at content administration, user, administration system, administration

and the subcategories below it, those are all caps now, all capital letters.

They're also lighter.

We change the shade so that they don't have as much contrast as the content text on the screen.

We also changed the case in the color of button labels.

If you look at every yellow button here, you'll see that those are all in capital letters now as well.

That starts to help separate them from the stuff we need to read and or understand.

We also made the field labels lighter than the text inside the fields.

So if you look down where it says portal display rules editor in the center, look right below that

where it says Rule collection, name, rule collection, ID those are the labels.

They should be lighter than the fields next to them so that the content in the field comes forward.

That's where our focus should be.

When the label is a gray and it recedes a little bit, that increases our ability to focus on the content,

on the stuff that we need to read, understand, act on.

And finally, we adjusted the contrast between the heading and the content container backgrounds.

In many cases, there were backgrounds behind things and the backgrounds were a little too dark, a

little too saturated, and they were competing with the labels.

You want to make sure that the headings come forward.

In the backgrounds recede.

You can see that where we have in the tabs in the center, master rule collection, rule collection,

we made those actually lighter.

They were a dark font before on a blue background.

Now there are white font on a blue background.

They come forward much more.

They're much easier to look at, much easier to read because there's more contrast between them.

Finally, we are going to separate primary, secondary and tertiary actions.

Interactivity.

Okay, Interaction choices.

So here's what we're going to do.

We're going to take these buttons in particular, there are four choices at the top.

There's four choices at the bottom.

All of these things are not equal.

You can see that they've started to sort of gray them out.

Right?

Refresh is active, close is active.

The other two are grayed out.

Add if expression at the bottom is active, the others are grayed out.

All right.

So there are some primary actions here, obviously, and there are some secondary actions.

The design, the treatment of those buttons should reflect that level of priority, that level of importance.

So what we're going to do is we're going to make the primary action always a high contrast button.

It is always the yellow button and it always appears to the far left the primary thing that it's very

likely the user is going to do on the screen is always the first thing.

It's always a button, it's always yellow.

The secondary or tertiary actions appear next to it.

On the right has low contrast buttons or text links.

You see how we treated those other buttons.

They're grayed out, they're simpler.

They don't have any color attached to them and where possible, you make them text links instead of

buttons.

If you can get away with that.

The contrast of tertiary actions or quaternary actions should decrease gradually for items of less importance.

If you compare the buttons at the top to the buttons at the bottom, look at the bottom where it says

Add if expression.

Look at those other two buttons.

They are still higher.

Contrast the ability to move an item up or move an item down.

Those are secondary actions.

They should sort of come forward a little bit.

Compare that to the top.

Okay, where we have refresh edit mode close.

Those are technically quaternary actions.

They're not nearly as important as those other things.

They won't be used as often as those other things.

So we treat those differently.

Contrast decreases, they're of less importance.

Finally, unrelated functions should also have a different visual appearance and be separated in proximity.

So anytime actions are unrelated, you want to take care to separate them with negative space from the

unrelated actions that may be sharing the same similar space.

So what I hope you're getting here is UI design mantra 18, which is that simpler is better.