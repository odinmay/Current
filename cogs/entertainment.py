from discord.ext import commands
from discord import Spotify
import discord
import random
import requests
import logging
import json

magicians_images = ['https://thumbs.gfycat.com/PalatableBeautifulInganue.webp',
                    'https://thumbs.gfycat.com/FaroffDamagedIzuthrush.webp',
                    'https://thumbs.gfycat.com/ComplexMeatyItaliangreyhound.webp',
                    'https://thumbs.gfycat.com/CookedVapidBluefish.webp',
                    'https://thumbs.gfycat.com/SpectacularCostlyCricket.webp',
                    'https://thumbs.gfycat.com/BlandWeakAbalone.webp',
                    'https://thumbs.gfycat.com/OrangeQuarterlyFinwhale.webp',
                    'https://thumbs.gfycat.com/AnxiousVeneratedCattle.webp',
                    'https://thumbs.gfycat.com/DeadlyInbornAtlasmoth.webp',
                    'https://thumbs.gfycat.com/RemoteAnimatedDunlin.webp',
                    'https://thumbs.gfycat.com/GeneralFabulousAtlanticblackgoby.webp',
                    'https://thumbs.gfycat.com/ShrillHilariousBooby.webp',
                    'https://thumbs.gfycat.com/ShowyAdolescentGrosbeak.webp',
                    'https://thumbs.gfycat.com/VengefulThinHusky.webp',
                    'https://thumbs.gfycat.com/LegitimateInexperiencedFruitbat.webp',
                    'https://thumbs.gfycat.com/DownrightIdleKakarikis.webp',
                    'https://thumbs.gfycat.com/ContentGentleIchidna.webp',
                    'https://thumbs.gfycat.com/FakeUglyCricket.webp',
                    'https://thumbs.gfycat.com/ThatDeadAnole.webp',
                    'https://thumbs.gfycat.com/HotLastInchworm.webp',
                    'https://thumbs.gfycat.com/DisastrousPinkBlacklemur.webp',
                    'https://thumbs.gfycat.com/ScarceGleamingHarpseal.webp',
                    'https://thumbs.gfycat.com/VengefulAcidicAdmiralbutterfly.webp',
                    'https://thumbs.gfycat.com/JoyousWeirdKomododragon.webp',
                    'https://thumbs.gfycat.com/ShyWetCuttlefish.webp',
                    'https://thumbs.gfycat.com/WickedSlowAmurminnow.webp',
                    'https://thumbs.gfycat.com/OddballPowerfulAnnelida.webp',
                    'https://thumbs.gfycat.com/RichOpulentHagfish.webp',
                    'https://thumbs.gfycat.com/CraftyImpureCrane.webp',
                    'https://thumbs.gfycat.com/NextLivelyAuklet.webp',
                    'https://thumbs.gfycat.com/PoisedIllustriousCrossbill.webp',
                    'https://thumbs.gfycat.com/SereneDefinitiveGosling.webp',
                    'https://thumbs.gfycat.com/NiftySardonicHairstreak.webp',
                    'https://thumbs.gfycat.com/SizzlingInfiniteKodiakbear.webp',
                    'https://thumbs.gfycat.com/PessimisticGrandioseKoalabear.webp',
                    'https://thumbs.gfycat.com/CelebratedCleanCassowary.webp',
                    'https://thumbs.gfycat.com/HotElderlyGrassspider.webp',
                    'https://thumbs.gfycat.com/HotElderlyGrassspider.webp',
                    'https://thumbs.gfycat.com/RedPlaintiveBlackrhino.webp',
                    'https://thumbs.gfycat.com/SplendidUnselfishFerret.webp',
                    'https://thumbs.gfycat.com/RightBetterFireant.webp',
                    'https://thumbs.gfycat.com/YoungBraveHind.webp',
                    'https://thumbs.gfycat.com/CooperativeTallJellyfish.webp',
                    'https://thumbs.gfycat.com/SardonicNearHerculesbeetle.webp',
                    'https://thumbs.gfycat.com/NegligibleEmbellishedDaddylonglegs.webp',
                    'https://thumbs.gfycat.com/SnappyGlassDachshund.webp',
                    'https://thumbs.gfycat.com/UnluckyIdleArchaeocete.webp',
                    'https://thumbs.gfycat.com/DelectableOldBadger.webp',
                    'https://gfycat.com/hugeyellowishblackrussianterrier-the-magicians-tick-pickwick-rizwan-manji-amused',
                    'https://gfycat.com/bouncyethicalirishredandwhitesetter-the-magicians-tick-pickwick-rizwan-manji-exit',
                    'https://gfycat.com/hideousenchantedherculesbeetle-the-magicians-hale-appleman-eliot-waugh-peek',
                    'https://gfycat.com/apprehensiveshinycaiman-the-magicians-tick-pickwick-rizwan-manji',
                    'https://gfycat.com/altruisticreflectingamericanredsquirrel-the-magicians-penny-adiyodi-arjun-gupta-shocked',
                    'https://gfycat.com/rarebriskivorygull-kady-orloffdiaz-the-magicians-jade-tailor',
                    'https://gfycat.com/mintyimpureborer-olivia-taylor-dudley-the-magicians-alice-quinn',
                    'https://gfycat.com/totalcoolabalone-the-magicians-tick-pickwick-rizwan-manji-yikes',
                    'https://gfycat.com/excitablealarmeddogfish-the-magicians-tick-pickwick-but-im-a-man',
                    'https://gfycat.com/faintregularaxolotl-right-in-the-pooper-the-magicians-margo-hanson',
                    'https://gfycat.com/thismadeupiraniangroundjay-tick-pickwick-the-magicians-rizwan-manji',
                    'https://gfycat.com/joyfulinnocentbluefish-the-magicians-penny-adiyodi-arjun-gupta',
                    'https://gfycat.com/shamefulantiquecoati-the-magicians-penny-adiyodi-arjun-gupta-idiot',
                    'https://gfycat.com/acidicphysicaleasternglasslizard-i-am-so-screwed-the-magicians-penny-adiyodi',
                    'https://gfycat.com/homelyevergreenheron-lets-go-get-a-drink-the-magicians-julia-wicker',
                    'https://gfycat.com/fluffyembarrassedankole-the-magicians-penny-adiyodi-arjun-gupta-me-too',
                    'https://gfycat.com/willingconcretebasilisk-thought-we-were-going-to-bang-the-magicians',
                    'https://gfycat.com/fantasticoldfashionedauk-the-magicians-penny-adiyodi-arjun-gupta-shocked',
                    'https://gfycat.com/onlydelightfuldunlin-the-magicians-penny-adiyodi-arjun-gupta-come-on',
                    'https://gfycat.com/negativelatearieltoucan-harvey-guillen-the-magicians-distraught',
                    'https://gfycat.com/quickidioticbonobo-im-a-person-of-questionable-ethics',
                    'https://gfycat.com/shadowyenormousflamingo-the-magicians-jason-ralph-quentin',
                    'https://gfycat.com/adorablejoyouscats-the-magicians-jason-ralph-frustrated-no-no-no',
                    'https://gfycat.com/pinkgreatasianporcupine-youll-feel-better-if-you-just-drink-the-wine',
                    'https://gfycat.com/rewardingthirdcapybara-the-magicians-rick-worthy-henry-fogg',
                    'https://gfycat.com/adoreddisgustingbubblefish-kady-orloff-diaz-the-magicians-jade-tailor',
                    'https://gfycat.com/pepperyagedhorse-beauty',
                    'https://gfycat.com/rectangularjovialamethystinepython-kady-orloff-diaz-the-magicians-jade-tailor',
                    'https://gfycat.com/naturalimportantearwig-its-a-little-funny-the-magicians-penny-adiyodi',
                    'https://gfycat.com/quarterlydefinitehoneyeater-the-magicians-tick-pickwick-rizwan-manji',
                    'https://gfycat.com/tightbravehind-the-magicians-hale-appleman-lets-do-this-im-in',
                    'https://gfycat.com/welcomecheerfulflamingo-beauty',
                    'https://gfycat.com/decisivewellwornamericancrayfish-youre-so-mysterious-the-magicians',
                    'https://gfycat.com/obedientknobbyhorsechestnutleafminer-the-magicians-tick-pickwick-i-shall-not',
                    'https://gfycat.com/secondhandidiotickingsnake-now-is-the-time-the-time-is-now-tick-pickwick',
                    'https://gfycat.com/freshdistortedamurminnow-trevor-einhorn-the-magicians-josh-hoberman-420',
                    'https://gfycat.com/tinyeachabyssiniangroundhornbill-the-magicians-tick-pickwick-rizwan-manji-shrug',
                    'https://gfycat.com/shorttermhelplessjunebug-beauty',
                    'https://gfycat.com/mealyadorableamericanpainthorse-the-magicians-tick-pickwick-rizwan-manji',
                    'https://gfycat.com/watchfulconcretegalapagoshawk-beauty',
                    'https://gfycat.com/lightordinaryape-marina-andrieski-the-magicians-kacey-rohl',
                    'https://gfycat.com/madeuphatefulgrackle-weve-all-peed-in-things-we-regret-bacchus',
                    'https://gfycat.com/glassunrealisticfennecfox-this-is-bullshit-the-magicians-summer-bishil',
                    'https://gfycat.com/defenselessorganicfulmar-that-sounds-on-brand-sounds-about-right',
                    'https://gfycat.com/majesticidealisticbaldeagle-beauty',
                    'https://gfycat.com/raredenseantbear-self-awareness-the-magicians-hale-appleman',
                    'https://gfycat.com/klutzyagedamericanbulldog-trevor-einhorn-the-magicians-josh-hoberman-smug',
                    'https://gfycat.com/powerlessthirdhyracotherium-quentin-coldwater-the-magicians-jason-ralph',
                    'https://gfycat.com/madminoramphibian-sounds-like-a-personal-problem-the-magicians',
                    'https://gfycat.com/seconddetailedhamster-the-magicians-banana-phone-rick-worthy',
                    'https://gfycat.com/sphericalwidedwarfrabbit-throws-hands-up-in-the-air-quentin-coldwater',
                    'https://gfycat.com/thunderousimpolitehatchetfish-go-make-me-a-drink-the-magicians-summer-bishil',
                    'https://gfycat.com/ajarrespectfulindianpalmsquirrel-the-magicians-penny-adiyodi-arjun-gupta-wow-no',
                    'https://gfycat.com/slipperyfrightenedcivet-dont-screw-it-up-the-magicians-madisen-beaty',
                    'https://gfycat.com/apprehensivecourageousalbino-the-magicians-summer-bishil-margo-hanson-yikes',
                    'https://gfycat.com/farflungfinishedcolt-that-is-very-fuck-thats-messed-up-thats-fucked',
                    'https://gfycat.com/zigzagrecenthaddock-the-magicians-summer-bishil-margo-hanson',
                    'https://gfycat.com/hotwarmheartedcrow-now-thats-the-kind-of-man-i-need-margo-hanson',
                    'https://gfycat.com/bigrepulsiveacornweevil-the-magicians-summer-bishil-margo-hanson-urgent']


# helper Functions #

def translate_sindarin(text):
    url = 'https://api.funtranslations.com/translate/sindarin.json'
    querystring = {'text': text}
    response = requests.get(url, params=querystring)
    try:
        return response.json()['contents']['translated']
    except KeyError:
        return response.json()['error']['message']


def pull_joke():
    url = "https://joke3.p.rapidapi.com/v1/joke"
    headers = {
        'x-rapidapi-host': "joke3.p.rapidapi.com",
        'x-rapidapi-key': "006adefbccmshf086e0b885be71bp1c8a29jsnbf24cc6763f4"
    }
    response = requests.request("GET", url, headers=headers)
    return response.json()['content']


def pull_chucknorris():
    req = requests.get('https://api.chucknorris.io/jokes/random')
    return req.json()['value']


def scryfall(card_name):
    url = 'https://api.scryfall.com/cards/search'
    querystring = {'q': card_name}
    response = requests.request('GET', url, params=querystring)
    try:
        return json.loads(response.text)['data'][0]['image_uris']['normal']
    except:
        return 'Card not in either database'


def scryfall_art(card_name):
    url = 'https://api.scryfall.com/cards/search'
    querystring = {'q': card_name}
    response = requests.request('GET', url, params=querystring)
    try:
        return json.loads(response.text)['data'][0]['image_uris']['art_crop']
    except:
        return 'Cropped card art unavailable for this card sorry.'


def scryfall_price(card_name):
    url = 'https://api.scryfall.com/cards/search'
    querystring = {'q': card_name}
    response = requests.request('GET', url, params=querystring)
    try:
        prices = json.loads(response.text)['data'][0]['prices']
        price_list = list(prices.items())
        msg = f'{price_list[0][0]} : {price_list[0][1]} \n{price_list[1][0]} : {price_list[1][1]}'
        return msg
    except:
        return 'Card price not in either database'


def pull_mtgio_card(card_name):
    url = 'https://api.magicthegathering.io/v1/cards'
    querystring = {'name': card_name}
    response = requests.request('GET', url, params=querystring)
    try:
        return response.json()['cards'][0]['imageUrl']
    except:
        return scryfall(card_name)


def pull_movie(movie):
    url = f"https://imdb-internet-movie-database-unofficial.p.rapidapi.com/film/{movie}"
    headers = {
        'x-rapidapi-host': "imdb-internet-movie-database-unofficial.p.rapidapi.com",
        'x-rapidapi-key': "006adefbccmshf086e0b885be71bp1c8a29jsnbf24cc6763f4"
    }
    response = requests.request("GET", url, headers=headers).json()

    embedMsg = discord.Embed(title=f"{str(movie).title()} | {response['rating']}/10",
                             description=f"{response['plot']}",
                             url=response['trailer']['link'],
                             color=0x00C7FF
                             )
    embedMsg.set_image(url=response['poster'])


    return embedMsg
    # return '\n'.join(
    #     [response['poster'], , 'Rating ' + response['rating'], response['trailer']['link']])


class Entertainment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.strikes = 0

    @commands.command(name='8ball')
    async def _8ball(self, ctx, *, question):
        """Ask it a question!"""
        responses = ["It is certain.",
                     "It is decidedly so.",
                     "Without a doubt.",
                     "Yes - definitely.",
                     "You may rely on it.",
                     "As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes.",
                     "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Very doubtful."]
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

    @commands.command(aliases=['coin'])
    async def flip(self, ctx):
        """Whats the most you ever lost in a coin toss?"""
        await ctx.send(random.choice(['Heads', 'Tails']))

    @commands.command()
    async def joke(self, ctx, user: discord.Member = None):
        """Tells a joke"""
        user = user or ctx.author
        await ctx.send(pull_joke())

    @commands.command(aliases=['chuck norris', 'chucknorris', 'norris'])
    async def chuck(self, ctx, user: discord.Member = None):
        """Tells a Chuck Noris FACT."""
        user = user or ctx.author
        await ctx.send(pull_chucknorris())

    @commands.command(aliases=['magic', 'magician'])
    async def magicians(self, ctx):
        """Displays random Magicians gif"""
        await ctx.send(random.choice(magicians_images))

    @commands.command()
    async def mtg(self, ctx, *, card):
        """Magic The Gathering card data from magicthegathering.io/scryfall"""
        async with ctx.message.channel.typing():
            await ctx.send(pull_mtgio_card(card))
            await ctx.send(scryfall_price(card))

    @commands.command()
    async def mtg_art(self, ctx, *, card):
        """Magic The Gathering card art from magicthegathering.io/scryfall"""
        async with ctx.message.channel.typing():
            await ctx.send(scryfall_art(card))

    @commands.command()
    async def movie(self, ctx, *, movie):
        """Displays a movies plot/rating/trailer"""
        await ctx.send(pull_movie(movie))

    @commands.command()
    async def sindarin(self, ctx, *, text):
        """Translates message into Elvish(Sindarin)"""
        await ctx.send(translate_sindarin(text))

    @commands.command()
    async def spotify(self, ctx, user: discord.Member = None):
        """Shares what you are listening to on Spotify"""
        user = user or ctx.author
        for activity in user.activities:
            if isinstance(activity, Spotify):
                await ctx.send(
                    f"{user} is listening to {activity.title} by {activity.artist} {activity.album_cover_url}")

    @commands.command(aliases=['defelcts'])
    async def deflect(self, ctx) -> str:
        """Displays a random deflect gif"""
        await ctx.send(random.choice(
            ['https://media2.giphy.com/media/l1KVaixq8xLxoHEti/giphy.gif',
             'https://media4.giphy.com/media/3ohjUQ81edgmV8Gu40/giphy.gif',
             'https://i.imgur.com/zPSpCpD.gif',
             'https://thumbs.gfycat.com/EllipticalSophisticatedHorsemouse-size_restricted.gif',
             'https://media.tenor.com/images/8ea0b658e77683528a151deef9154e94/tenor.gif',
             'https://media.tenor.com/images/0802de3dbf808ae7f1e13185f5bcb15a/tenor.gif',
             'https://media3.giphy.com/media/9dhFwjb4adknC/giphy.gif']))


def setup(bot):
    bot.add_cog(Entertainment(bot))
