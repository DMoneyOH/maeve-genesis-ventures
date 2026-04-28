# Sentinel — Intelligent Change Monitoring as a Service
## MaeveGenesis Venture Business Case
**Prepared by:** Maeve (AI Infrastructure Platform)
**Date:** 2026-04-28
**Status:** Pre-seed concept — awaiting backer decision
**Repo:** https://github.com/DMoneyOH/maeve-genesis-ventures

---

## Executive Summary

Sentinel is an AI-powered change monitoring service that watches any webpage, API, document, or data source and delivers *interpreted* alerts — not raw diffs, but plain-English analysis of what changed and why it matters to the subscriber. The product is sold as a subscription ($12–25/month) targeting competitive intelligence analysts, compliance professionals, indie researchers, and small business owners who need to know when something in their world changes but cannot afford enterprise monitoring tools.

The critical differentiation: every existing competitor (Visualping, Distill, PageCrawl, Fluxguard) sends you a diff. Sentinel sends you a judgment. That one word — interpreted — is the entire business model.

**Target revenue:** $500/month (MRR) by day 60. $1,500/month by day 90.
**Build time to prototype:** 7 days.
**Ongoing human involvement post-launch:** Near zero.

---

## 1. The Problem

The web changes constantly and those changes carry real financial and competitive consequences. A competitor quietly drops their pricing. A regulatory body updates compliance language. A grant portal opens applications. A target company's careers page lists a new VP of Engineering role. A vendor buries a material change in their terms of service.

The people who act on these signals first win. The people who check manually, or don't check at all, lose.

Existing monitoring tools solve the *detection* problem. They do not solve the *interpretation* problem. A Visualping alert that says "this page changed" still requires you to read the diff, understand the context, and decide whether it matters. For someone monitoring 20 pages across multiple domains, that cognitive load becomes the new bottleneck.

**The gap:** Between "something changed" and "here's what you should do about it" — nobody lives there yet at the sub-$50/month price point.

---

## 2. Market Sizing

### TAM (Total Addressable Market)
The global website monitoring and competitive intelligence software market was valued at approximately **$2.1 billion in 2025** (MarketsandMarkets, 2025) and is growing at 15.3% CAGR through 2030. AI-augmented monitoring — the specific segment Sentinel targets — is growing at approximately 38% CAGR per BetterCloud's 2026 SaaS statistics. This places the AI monitoring TAM at roughly **$800M by 2026**.

### SAM (Serviceable Addressable Market)
Sentinel targets SMB and prosumer segments: freelancers, indie analysts, small agencies, compliance managers at companies under 200 employees, and competitive intelligence practitioners at startups. This segment represents approximately 40% of the broader market, or roughly **$320M**.

### SOM (Serviceable Obtainable Market)
A realistic 3-year target for a self-funded AI-native micro-SaaS: 0.01% of SAM = **$32,000 ARR** in year one scaling to $150,000 ARR by year three. At $25/month average subscription, year-one target is 107 paying subscribers. This is conservative and achievable.

---

## 3. Competitive Landscape

### Visualping
**Pricing:** Free (5 checks/day), $14/month Pro, $40/month Business
**Users:** 2M+ (including 85% of Fortune 500 per company claims)
**Weakness:** Delivers visual diffs and a 2–3 sentence AI summary. The AI summary is generic — it describes the change but never contextualizes it for the user's specific use case. No interpretation layer. No "why this matters to you" capability. Sentinel's interpreted alerts are structurally deeper.

### PageCrawl
**Pricing:** Free tier, $80/year Standard, higher for Ultimate
**Weakness:** Strong at price/stock monitoring but limited natural language interpretation. No user-context-aware analysis. The AI integration is surface level — summaries, not strategic interpretation.

### Fluxguard
**Pricing:** Enterprise-focused, unlisted pricing (estimated $200–500/month)
**Weakness:** Built for compliance teams at mid-to-large companies. No SMB or prosumer tier. UI is complex. Sentinel undercuts them on price and simplicity while delivering comparable AI interpretation quality.

### Distill (browser extension)
**Pricing:** Free to $14/month
**Weakness:** Browser-extension-first architecture means monitoring dies when the browser is closed. No server-side monitoring. No AI interpretation. Technically capable users' tool, not a professional service.

**The white space:** No tool in this market delivers user-context-aware interpretation at under $30/month. Sentinel owns that position.

---

## 4. Ideal Customer Profile

### Primary ICP: The Competitive Intelligence Practitioner at a Startup
- **Who:** Head of Product, Founder, or Growth Lead at a Series A–B SaaS startup (5–50 employees)
- **Pain:** Needs to track 10–30 competitor pages (pricing, features, job listings, blog posts) but can't justify a $2,000/month enterprise CI tool or dedicate analyst time to manual checks
- **Job to be done:** "Tell me the moment my biggest competitor changes their pricing or ships a new feature so I can respond before our next sales call"
- **Willingness to pay:** $25/month is a rounding error in a startup's tool budget. This is a no-approval-needed purchase.
- **Where to find them:** r/startups, r/SaaS, Product Hunt, Indie Hackers, Lenny's Newsletter community

### Secondary ICP: The Compliance Manager at a Professional Services Firm
- **Who:** Compliance officer, legal ops manager, or risk analyst at an insurance agency, accounting firm, or fintech company under 200 employees
- **Pain:** Must track regulatory updates from government portals, vendor terms, and industry body pages. Currently either checks manually or pays for a $500/month enterprise tool
- **Job to be done:** "Alert me when the CFPB, SEC, or any of our top 5 vendors update language that affects our compliance posture — and tell me what actually changed"
- **Willingness to pay:** $25/month. This is risk management; they spend more on coffee for the compliance team.

### Tertiary ICP: The Indie Researcher / Investigative Writer
- **Who:** Newsletter writer, investigative journalist, or market researcher tracking government pages, corporate filings, and public data sources
- **Pain:** 24/7 manual surveillance of dozens of sources is impossible; existing tools give diffs, not insight
- **Willingness to pay:** $12–15/month (budget-sensitive but high-value use case)

---

## 5. The Product

### Core Features (MVP)
1. **Monitor configuration** — User specifies URL, monitoring frequency (hourly/daily/weekly), and a plain-English context prompt: *"I'm watching this competitor's pricing page. Alert me when prices change, tiers are added/removed, or trial terms shift."*
2. **Intelligent change detection** — Python scraper + SQLite diff engine detects meaningful content changes (filters CSS, cookie banners, dynamic timestamps, and other noise)
3. **Context-aware interpretation** — Changed content + user's context prompt → Claude → structured alert: what changed, what it might signal, and a suggested response action
4. **Multi-channel delivery** — Telegram (immediate), Gmail digest (daily summary), Supabase dashboard (historical record)
5. **Subscription management** — Vercel frontend, Supabase auth, Stripe for billing

### Tiers
| Tier | Price | Monitors | Check Frequency | Interpretation |
|------|-------|----------|-----------------|----------------|
| Scout | $12/mo | 5 | Daily | Standard |
| Analyst | $20/mo | 20 | Hourly | Advanced + context |
| Intelligence | $35/mo | Unlimited | 15-min | Full + action recommendations |

### Sample Alert Output
```
SENTINEL ALERT — 2026-04-28 14:32 ET
Monitor: Acme Corp Pricing Page
Context you set: "Watch for price changes or tier restructuring"

WHAT CHANGED:
The "Professional" tier price increased from $79/month to $99/month.
The "Starter" tier was removed entirely. New entry point is now $49/month 
(previously $29/month).

WHAT THIS LIKELY MEANS:
Acme is moving upmarket. Removing the $29 Starter tier eliminates low-value 
churn and repositions them away from SMB. The 25% price increase on Professional 
suggests they're testing price sensitivity after a recent funding round.

SUGGESTED ACTION:
This is a competitive opening in the SMB segment Acme just abandoned. Consider 
a targeted campaign this week positioning your Starter tier against their new 
$49 entry point.

View change: [dashboard link]
```

---

## 6. Technical Architecture

### Stack
| Component | Technology | Purpose |
|-----------|-----------|---------|
| Scraping | Python + requests/playwright | Page content retrieval |
| Diff engine | Python difflib + SQLite | Change detection and storage |
| Interpretation | Claude API (claude-sonnet-4-20250514) | Context-aware analysis |
| Scheduling | systemd timers (WSL2) + GitHub Actions failover | Autonomous execution |
| Frontend | Vercel (Next.js) | Monitor config, dashboard, billing |
| Database | Supabase (PostgreSQL) | Users, monitors, alert history |
| Payments | Stripe | Subscription billing |
| Notifications | Telegram bot + Gmail API | Alert delivery |
| Auth | Supabase Auth | User management |

### Autonomous Operation Loop
```
systemd timer fires (every 15 min for premium, hourly for standard)
  → Python scraper fetches all monitors due for check
  → Content stored to SQLite, diffed against last snapshot
  → If meaningful change detected:
      → Claude API: content diff + user context → interpreted alert
      → Telegram: immediate push notification
      → Supabase: alert logged to history
  → Nightly: Gmail digest of all daily alerts per user
  → Weekly: Supabase generates usage report, Stripe billing confirmed
```

### Key Technical Risks and Mitigations
| Risk | Mitigation |
|------|-----------|
| JavaScript-heavy sites block scrapers | Playwright headless browser for JS-dependent targets |
| Claude API costs at scale | Rate limit: max 3 Claude calls per alert batch per user per hour. Cache context prompts. |
| False positive alert fatigue | Noise filter: changes below 50 character delta ignored. Dynamic timestamps and ads excluded via pattern list. |
| Supabase/Vercel costs | Free tiers cover 0–100 users. Upgrade costs ~$50/month at 500 users — well within margin. |

### API Cost Model
At scale (200 subscribers, 20 monitors average, 1 meaningful change per monitor per day):
- 4,000 Claude API calls/day × ~500 tokens average = 2M tokens/day
- At Claude Sonnet pricing: ~$0.003/call = $12/day = $360/month
- Revenue at 200 subscribers at $20 average: $4,000/month
- **Gross margin after API costs: ~91%**

---

## 7. Go-to-Market Strategy

### No SEO Required
Sentinel's entire customer acquisition strategy avoids Google dependency.

**Phase 1 (Days 1–14): Product Hunt Launch**
A single well-executed Product Hunt launch routinely drives 500–2,000 unique visitors and 50–200 sign-ups in 24 hours for a genuinely useful tool. The demo video writes itself: competitor's pricing page, Sentinel detects a change, alert arrives in Telegram with interpretation. 60 seconds. Converts.

**Phase 2 (Days 15–30): Community seeding**
Targeted posts with a real use case demo in:
- r/startups ("I built a tool that watches competitor pages and tells you what the change means")
- r/SaaS (same)
- Indie Hackers (build-in-public thread, posted during build)
- Lenny's Newsletter Slack (competitive intelligence use case)
- The Hustle/Sam Parr communities

**Phase 3 (Days 30–60): Direct outreach**
LinkedIn DMs to heads of product at Series A startups. Message is simple: "I noticed you have 3 major competitors. Want me to show you what changed on their pricing pages in the last 30 days?" Demo closes. Convert to paid.

**Phase 4 (Day 60+): Referral loop**
Every Sentinel alert footer includes: "Know someone who needs this? They get 1 month free, you get 1 month free." No viral mechanics needed — the product already sends a notification daily.

### Pricing Rationale
Visualping's free tier allows only 5 checks per day with hour-minimum intervals, and their Pro tier runs $14/month. Sentinel enters above this with interpretation that Visualping's tier cannot match. PageCrawl Standard runs $80/year for solo users, making Sentinel's $20/month Analyst tier competitive on a per-feature basis when the interpretation layer is factored in.

---

## 8. Revenue Model and Financial Projections

### Assumptions
- Average subscription: $20/month
- Month 1: Product Hunt launch + community seeding. Target 25 paying subscribers.
- Month 2: Word of mouth + direct outreach. Target 50 paying subscribers.
- Month 3: Referral program active. Target 80 paying subscribers.
- Churn: 8%/month (conservative for early-stage SaaS)
- COGS: Claude API (~$0.05/user/day at scale) + Vercel + Supabase + Stripe fees ≈ $3/user/month

### Revenue Ramp
| Month | Subscribers | MRR | COGS | Net |
|-------|------------|-----|------|-----|
| 1 | 25 | $500 | $75 | $425 |
| 2 | 50 | $1,000 | $150 | $850 |
| 3 | 80 | $1,600 | $240 | $1,360 |
| 6 | 175 | $3,500 | $525 | $2,975 |
| 12 | 400 | $8,000 | $1,200 | $6,800 |

Daily revenue at month 2 (50 subscribers): **$33/day**. Exceeds the $20/day target by day 45.

---

## 9. Biggest Risk and Mitigation

**Risk: Alert fatigue kills retention**
The #1 churn driver for monitoring tools is irrelevant alerts. If Sentinel fires too many notifications for noise (CSS changes, cookie banner updates, timestamp rotations), users disable notifications and churn within 30 days.

**Mitigation strategy:**
1. Noise filter is built before the product launches — not as a future feature
2. User-configured sensitivity: "Only alert me if the change is significant enough to act on today"
3. Daily digest mode as default for non-urgent monitors — batches low-priority changes instead of spamming
4. Explicit alert quality feedback button on every notification. Claude learns which alert patterns users mark useful vs. noise.

**Risk: LinkedIn bans automated posting (for Ghost — see companion doc)**
For Sentinel specifically: scraping terms of service. Most major sites permit scraping of public pages for personal/research use. For commercially operated scraping at scale, mitigation is: rate limiting, respectful crawl delays, robots.txt compliance, and user-agent transparency. At 200–500 users, Sentinel's scrape volume is trivial compared to Googlebot.

---

## 10. Why Now (The 2026 Timing Argument)

Three forces converge in 2026 to make Sentinel viable as a solo AI-operated micro-SaaS:

1. **AI interpretation is good enough.** Claude Sonnet's ability to understand context and generate actionable analysis crossed a quality threshold in 2025. Before this, "AI-powered monitoring" meant GPT-2 summaries that were worse than just reading the diff yourself. That's no longer true.

2. **The web is changing faster than ever.** The SaaS market is projected to surpass $315 billion in 2026, with 70% of new SaaS products incorporating AI as a core feature. This means competitor pricing, feature sets, and positioning are changing faster than any human analyst can track manually.

3. **The SMB monitoring gap is widening.** Enterprise tools (Klue, Crayon, Kompyte) now cost $15,000–50,000/year. They've moved upmarket. Tools like Visualping have stayed at the technical/visual detection layer without investing in interpretation. The $12–35/month interpreted monitoring tier is genuinely unoccupied.

---

## 11. Non-Obvious Insight

**The real customer isn't the person who reads the alert. It's the person who forwards it.**

The highest-retention Sentinel use case isn't individual users — it's the analyst or ops person who sets up monitors and then automatically forwards Telegram alerts to a Slack channel or emails them to their team. That person becomes the internal hero who always knows what the competition is doing. Their reputation becomes tied to Sentinel's reliability. Churn drops to near zero because canceling means looking less informed than before.

This means Sentinel's true retention mechanic is not the alert itself — it's the *internal distribution* of the alert. The product roadmap implication: build Slack/Teams webhook integration before the 6-month mark. The growth implication: one power user in a 10-person startup can drive 3–5 additional accounts through internal advocacy.

---

## 12. Maintenance and Monitoring (Operational Model)

### What Maeve Runs Autonomously
- Scrape scheduler (systemd + GitHub Actions failover)
- Change detection and diff computation
- Claude API calls for interpretation
- Telegram and Gmail alert delivery
- Stripe webhook processing (new subscribers, cancellations, failed payments)
- Weekly usage reports to Supabase dashboard

### What Requires Human Attention
- **Scraper failures** (Telegram alert auto-fires when error rate > 5% for any monitor)
- **Stripe payment failures** (auto-dunning via Stripe's built-in retry, Maeve emails user at 3-day failed payment mark)
- **Customer support emails** (Derek receives, responds — estimated 2–3 emails/week at 50 subscribers)
- **Monthly: review alert quality metrics** in Supabase dashboard (30 minutes/month)

### Infrastructure Cost at 100 Subscribers
| Service | Monthly Cost |
|---------|-------------|
| Vercel Pro | $20 |
| Supabase Pro | $25 |
| Claude API | ~$45 |
| Telegram (free) | $0 |
| Gmail API (free) | $0 |
| Total COGS | ~$90/month |
| Revenue (100 × $20) | $2,000/month |
| **Net margin** | **95.5%** |

---

## 13. Build Requirements

### Phase 1: Core Engine (Days 1–7)
- [ ] Python scraper with Playwright fallback for JS pages
- [ ] SQLite snapshot storage with diff computation
- [ ] Noise filter (dynamic content exclusion patterns)
- [ ] Claude interpretation engine with context prompt injection
- [ ] Telegram bot notification
- [ ] Basic systemd timer for local scheduling

### Phase 2: User-Facing Product (Days 8–14)
- [ ] Vercel Next.js frontend (monitor config, dashboard, alert history)
- [ ] Supabase auth + database schema (users, monitors, snapshots, alerts)
- [ ] Stripe subscription integration (3 tiers)
- [ ] Gmail daily digest
- [ ] GitHub Actions failover scheduler

### Phase 3: Launch Preparation (Days 15–21)
- [ ] Noise filter tuning (test on 50 real URLs)
- [ ] Onboarding flow with example monitors pre-populated
- [ ] Demo video recording
- [ ] Product Hunt listing draft
- [ ] Documentation: how to write effective context prompts

### Phase 4: Launch + Iteration (Days 22–60)
- [ ] Product Hunt launch (target day 22)
- [ ] Community seeding posts
- [ ] Alert quality feedback loop
- [ ] Slack/Teams webhook (if user demand confirmed)

**Total estimated build time (Maeve operating autonomously): 14–21 days to launch-ready prototype.**

---

## 14. Decision Criteria for Proceeding

Proceed to build if:
- Derek confirms $0 monthly spend tolerance (current stack covers it)
- Stripe account accessible for payment integration
- Willing to handle 2–3 support emails/week at launch

Do not proceed if:
- Maeve's Claude API costs during build/test phase are a concern (estimated $15–20 for testing)
- The interpretation quality doesn't clear a quality bar on first prototype test

---

*Document prepared by Maeve. Research sourced from Visualping, PageCrawl, UptimeRobot, BetterCloud, Vena, and Voxturr published data (April 2026).*
