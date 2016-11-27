#Xur Helper for Destiny#

Figures out what Xur is selling, and sends an email letting you know
* Where he's at
* What he's got
* What the Trials map is for the weekend

Requires a [Bungie.net API key](https://www.bungie.net/en/Application) to grab Xur's warez.
Requires a free [SendGrid](https://sendgrid.com) API key to send the email.
Source your API keys into environment variables.

Designed to be run from Cron Fridays at 10:01 or so Pacific time.  Xur lands before that but Trials doesn't start until then.
