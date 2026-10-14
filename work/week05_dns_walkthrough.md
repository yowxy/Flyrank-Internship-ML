# DNS walkthrough — what happens between typing an address and seeing my site

**What DNS is, in one line.** DNS (the Domain Name System) is the internet's phone book:
it translates human names like `yourname.netlify.app` into the IP address of the
computer that actually serves the site. Nothing on my site loads until that lookup
succeeds — every link, image, and page starts with this question: "which machine
holds this name?"

**What a CNAME record is.** A CNAME ("canonical name") is one line in that phone book
that says: "this name is an alias — go ask that other name instead." Example: I could
point `www.mysite.com` at `yourname.netlify.app` with a CNAME. It does not contain an
IP address itself; it just forwards the lookup to the host's name, so if Netlify or
GitHub Pages moves my site to a new machine, my alias still works because their name
follows the move. (The bare root like `mysite.com` usually needs an A/ALIAS record
with a real IP instead — CNAMEs live on subdomains like `www`.)

**The full trip, step by step.** Say someone types my site address and hits enter:

1. **Browser cache check.** The browser first asks itself: "did I look this up a minute
   ago?" If yes and the answer hasn't expired, it skips the whole trip.
2. **Resolver.** Otherwise it asks a *resolver* — usually run by the visitor's ISP or a
   public service like 1.1.1.1. The resolver does the legwork; the browser just waits.
3. **Root → nameserver chain.** The resolver walks down the hierarchy: it asks a root
   server "who handles `.app`?", gets pointed to the `.app` nameserver, asks it "who
   handles `yourname.netlify.app`?", and gets pointed to the host's nameserver
   (Netlify's, or GitHub's for Pages). Each step returns a referral, not the answer.
4. **Record.** At the host's nameserver, the resolver finally reads the actual *record*:
   an A/AAAA record holding an IP, or a CNAME saying "ask this other name instead"
   (then it follows that alias to its IP). The host created these records when I
   deployed and named the site.
5. **Response + connection.** The resolver hands the IP back to the browser, which opens
   an encrypted (HTTPS) connection to that machine and asks for the page. The host
   answers with my `index.html`. The resolver caches the answer so the next visitor's
   lookup is instant.

**Why this matters for my site.** My portfolio will live on a host's free subdomain
(`yourname.github.io/portfolio/` or `yourname.netlify.app`), so the host owns the
nameserver and the records — I just claimed a readable name. If I later buy a custom
domain, the only new work is DNS: add a CNAME (or A record) at my registrar pointing
to the host, and the five steps above start landing on the same files. The site itself
doesn't move; only the phone-book entry does.
