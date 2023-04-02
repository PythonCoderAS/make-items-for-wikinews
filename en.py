# English Wikinews 
import locale
locale.setlocale(locale.LC_ALL, 'en_US.utf8')
import pywikibot
from pywikibot import pagegenerators
import mwparserfromhell
import datetime
import random
rand_hash = "{:x}".format(random.randrange(0, 2**48))
site = pywikibot.Site("en", "wikinews")
repo = site.data_repository()
instance_val = pywikibot.ItemPage(repo, "Q17633526")
lang_val = pywikibot.ItemPage(repo, "Q1860")
cat = pywikibot.Category(site,'Category:Published')
gen = pagegenerators.CategorizedPageGenerator(cat)
for page in gen:
    # print(page.title())
    if page.namespace().id != 0:
        continue
    try:
        item = pywikibot.ItemPage.fromPage(page)
    except pywikibot.exceptions.NoPageError:
        parsed = mwparserfromhell.parse(page.text)
        date = [item for item in parsed.filter_templates(recursive=False) if item.name.matches("date")]
        if not date:
            continue
        date_obj = datetime.datetime.strptime(str(date[0].get(1)), "%B %d, %Y")
        data = {"labels": {"en": page.title()}, "descriptions": {"en": "Wikinews article"}, "sitelinks": {"enwikinews": {"site": "enwikinews", "title": page.title()}}}
        instance_claim = pywikibot.Claim(repo, "P31")
        instance_claim.setTarget(instance_val)
        lang_claim = pywikibot.Claim(repo, "P407")
        lang_claim.setTarget(lang_val)
        date_claim = pywikibot.Claim(repo, "P577")
        date_claim.setTarget(pywikibot.WbTime(year=date_obj.year, month=date_obj.month, day=date_obj.day, site=repo))
        title_claim = pywikibot.Claim(repo, "P1476")
        title_claim.setTarget(pywikibot.WbMonolingualText(page.title(), "en"))
        data["claims"] = [obj.toJSON() for obj in [instance_claim, lang_claim, date_claim, title_claim]]
        new_item = pywikibot.ItemPage(repo)
        new_item.editEntity(data, summary=f"Creating item for Wikinews article ([[:toolforge:editgroups/b/CB/{rand_hash}|details]])")
        print(f"Created item {new_item.getID()}")