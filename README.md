# Pakistan News Hub — free automatic news website

This is a static website that can be hosted for free with GitHub Pages. A GitHub Actions workflow fetches RSS headline metadata roughly hourly and updates `articles.json`. The page displays the headlines and links readers to the original publisher.

## Included files
- `index.html` — responsive news website, category filters, search, and headline cards
- `fetch_news.py` — fetches RSS metadata from Google News searches and BBC World RSS
- `.github/workflows/update-news.yml` — scheduled update (hourly) and manual run
- `articles.json` — starter empty data file; the first workflow run fills it

## Publish with free GitHub Pages
1. Sign in or create a free account at https://github.com/.
2. Click **New repository**. Name it `pakistan-news-hub`. Choose **Public**. Create the repository.
3. Upload the contents of this ZIP (not the ZIP file itself) to the repository root. Ensure `.github/workflows/update-news.yml` is included; if the browser upload doesn't preserve hidden folders, create the workflow file in GitHub using **Add file → Create new file** and name it `.github/workflows/update-news.yml`.
4. Open **Actions**. If GitHub asks you to enable workflows, enable them. Open **Update news headlines** and click **Run workflow**. Check that the run succeeds.
5. Open **Settings → Pages**. Under **Build and deployment**, select **Deploy from a branch**, choose `main` and `/(root)`, then save.
6. After the Pages deployment completes, your site will be at `https://YOUR-USERNAME.github.io/pakistan-news-hub/`. It may take a few minutes to appear.
7. Test the website and check that headline cards link to their source.

## Free vs. paid/external features
### Works without paying
- Static website hosting and a `github.io` subdomain through GitHub Pages (subject to GitHub's current plan and usage rules)
- Responsive layout, search across loaded headlines, Pakistan/World category filters
- Scheduled RSS fetch using GitHub Actions, with a manual “Run workflow” option
- Headline titles, brief feed descriptions where supplied, dates, publisher labels, and links

### Needs external services or more work
- Custom `.com` domain: usually requires paying a registrar.
- Newsletter collection and email delivery: not included; connect an email marketing provider and publish a privacy notice.
- Contact form, user accounts, comments, admin dashboard, analytics, push notifications: need a third-party service or backend.
- Automatic full-article rewriting, translation, and fact-checking: not included and should not be represented as verified automation.
- Ad revenue: requires an ad network approval, policy-compliant original content, traffic, and payout eligibility; not instant income.
- Live RSS display: the page reads the generated `articles.json`. Updates depend on the GitHub Actions workflow succeeding; schedule delays or feed changes may interrupt it.

## Editorial and copyright cautions
- This site links to sources; it does not republish full articles or source images.
- RSS headline/metadata reuse terms vary by publisher, especially for commercial use. Check each source's terms and get permission where required. This starter uses feed metadata and source links; it is not a blanket licence for commercial republication.
- The BBC's terms allow personal use of its RSS feed with attribution and without changing the feed/branding, but business use requires permission. Check the current terms before commercial use.
- Google News RSS is an aggregator feed; confirm the final article publisher by opening the link.
- Do not label a story “verified” merely because it appears in an RSS feed. Verify important claims, dates, and corrections.
- GitHub Actions may have fair-use limits. Hourly runs are an example; if they hit limits, reduce the frequency.
- Never upload secrets or API keys to a public repository.

## Troubleshooting
- If the page has no headlines, go to **Actions → Update news headlines → Run workflow** and inspect the logs.
- If the workflow fails because no feed items were fetched, one or more upstream feeds may be unavailable. Edit `FEEDS` in `fetch_news.py` to use another permitted RSS source.
- If Pages shows a 404, confirm the repository's Pages source is `main` and `/(root)`, and wait a few minutes.
- If the site is public, anything in this repository is public too.
