# Examples

These invented examples demonstrate edits, not factual claims about real systems. Each rewrite uses only information present in its original.

## Cut the preamble

Before:

> Here's the thing: the parser accepts duplicate keys and keeps the last value. It's worth noting that earlier values are discarded. Let that sink in.

After:

> The parser accepts duplicate keys, keeps the last value, and discards earlier values.

## Replace a dramatic contrast

Before:

> This isn't a rendering problem. It's a subscription problem. The view subscribes only after the first event has already arrived.

After:

> The view subscribes after the first event arrives.

## Keep uncertainty

Before:

> It's worth noting that retries may possibly contribute to some of the duplicate charges. We haven't checked the payment provider's logs yet.

After:

> Retries may explain some duplicate charges. We haven't checked the payment provider's logs.

The uncertainty and evidence gap remain.

## Make a vague claim concrete

Before:

> The implications of this change are significant. Users must now provide a region when creating a workspace. Existing workspaces keep their current region.

After:

> Users must provide a region when creating a workspace. Existing workspaces keep their current region.

No new evidence is needed to replace the opening claim.

## Combine repeated openings

Before:

> We will compare the two parsers on the same inputs. We will record differences in output. We will publish those differences with the benchmark results.

After:

> We will compare the two parsers on the same inputs and publish output differences with the benchmark results.

## Preserve an unknown actor

Before:

> It was observed that the configuration file had been deleted. The investigation has not established who deleted it.

After:

> The configuration file was deleted; we do not know who deleted it.

Passive voice preserves what is known.

## Remove an invented label

Before:

> This creates what we might call the "configuration drift trap": the dashboard updates the setting, but the worker keeps using its startup value.

After:

> The dashboard updates the setting, but the worker keeps using its startup value.

## Preserve the author's position

Before:

> And yes, since we're being honest, I prefer the simpler API. It lets callers create a session in one call instead of three. That's the real story here.

After:

> I prefer the simpler API because callers can create a session in one call instead of three.
