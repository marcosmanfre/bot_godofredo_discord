import discord
from discord.ext import commands, tasks
import datetime
from decouple import config
import ffmpeg
from discord import FFmpegPCMAudio


intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!",intents=intents)


#remover comando 'help' nativo
bot.remove_command('help')

#eventos de bot conectado
@bot.event
async def on_ready():
    print(f'Estou conectado como {bot.user}!')

#no momento em que o usuário entra no servidor, recebe a mensagem de bem vindo com o link para as regras.
@bot.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = f'Seja Bem-Vindo {member.mention} ao {guild.name}! por favor, leias as regras no link abaixo e digite !help para saber mais!'
        embed = discord.Embed(title="Regras", url="https://discord.com/channels/1025003694409908266/1025029590466445333/1025385560963031040")
        await guild.system_channel.send(to_send)
        await guild.system_channel.send(embed=embed)


#quando a mensagem é editada, aparece o que foi editado.
@bot.event
async def on_message_edit(before, after):
    await before.channel.send(
        f'{before.author} editou a mensagem.\n'
        f'Antes: {before.content}\n'
        f'Depois: {after.content}'
    )

#comando para o bot entrar no canal de voz, somente depois que o usuário estiver no canal de voz, tocar e música e sair do canal de voz.
@bot.command()
async def entrar(ctx):
    if (ctx.author.voice):
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send("Entrou no canal de voz")
    else:
        await ctx.send("Você precisa entrar em um canal de voz para eu conseguir conectar.")


@bot.command()
async def sair(ctx):
    await ctx.voice_client.disconnect()
    await ctx.send("Saiu do canal de voz")


@bot.command()
async def play(ctx):
    guild = ctx.guild
    voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)
    audio_source = discord.FFmpegPCMAudio('sounds_rickroll.mp3')
    if not voice_client.is_playing():
        voice_client.play(audio_source, after=None)

#calculadora com argumentos.
@bot.command(name="calcular", help="Requer argumento, ex: 2 * 3 + 5")
async def calcular(ctx, *expressao):
    expressao = "".join(expressao)
    print(expressao)
    resposta = eval(expressao)

    await ctx.send("A resposta é: " + str(resposta))

  
#Embed com as regras do servidor.
@bot.command()
async def regras(ctx):
    embed = discord.Embed(
        title='REGRAS',
        description='Bem vindo ao Servidor do Marcos. Ao entrar neste servidor, você concordou com todas as regras listadas abaixo. ',
        color=discord.Colour.red()
    )
    embed.set_thumbnail(url='https://abrir.link/I7jLs')

    embed.add_field(
        name='1 - Tenha bom senso, seja educado(a) e tenha respeito. ',
        value='Mantenha a comunidade agradável e segura para todos os membros. Ataques pessoais, ofensas gratuitas, comentários obscenos, assédios, ameaças, perseguição, discursos de ódio, discriminações ou difamação de qualquer natureza não serão tolerados.',
        inline=False
    )

    embed.add_field(
        name='2 - Respeite a faixa etária.',
        value='Não publique conteúdo adulto, sugestivo, violento, e não apropriado para menores. Isso serve para "memes" e "brincadeiras" também.',
        inline=False
    )

    embed.add_field(
        name='3 - Não publique seus dados pessoais.',
        value='Nunca publique informações pessoais suas ou de outros usuários, número de telefone, CPF, RG, e-mail, etc.',
        inline=False
    )

    embed.add_field(
        name='4 - Respeite os Termos de Uso.',
        value='Não faça nada que vá contra os Termos de Uso do Discord.',
        inline=False
    )

    embed.add_field(
        name='5 - Evite spams, publicações excessivas.',
        value='Não publique várias vezes a mesma coisa ou mensagens parecidas',
        inline=False
    )
    embed.add_field(
        name='6 - Sobre Phishing e scamming',
        value='Qualquer tentativa de enganar outros usuários, seja através de sites, geradores de moedas, conversas suspeitas, serão levadas bem a sério. ',
        inline=False
    )

    await ctx.send(embed=embed)


#digita oi e o bot responde
@bot.command(name="oi")
async def send_hello(ctx):
    name = ctx.author.name
    response = "Olá, " + name
    await ctx.send(response)


#envia uma mensagem no privado do usuário, precisa estar habilidado no discord para receber a mensagem.
@bot.command(name="privado")
async def send_dm(ctx):
    try:
        await ctx.author.send(f"Olá, estou te enviando essa mensagem para lembrar de se inscrever no canal!!!")

    except discord.error.Forbidden:
        await ctx.send("Habilite para receber mensagem de qualquer servidor! caso contrario, não consigo te mandar mensagem!")


#buscar no google + qualquer frase
@bot.command()
async def google(ctx,*,arg):
  await ctx.send(f"https://www.google.com/search?q={arg.replace(' ', '+')}")  


#buscar no youtube + qualquer frase
@bot.command()
async def youtube(ctx,*,arg):
  await ctx.send(f"https://www.youtube.com/results?search_query={arg.replace(' ', '+')}")
  

#Botão com frases famosas utilizando o parametro discord.ui.View
class Frases(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Frase I", style=discord.ButtonStyle.red)
    async def frase1(self, interaction: discord.Integration, button: discord.ui.Button, ):
        await interaction.response.send_message("“A alegria evita mil males e prolonga a vida. - William Shakespeare”")

    @discord.ui.button(label="Frase II", style=discord.ButtonStyle.green)
    async def frase2(self, interaction: discord.Integration, button: discord.ui.Button, ):
        await interaction.response.send_message("“O conhecimento torna a alma jovem e diminui a amargura da velhice. Colhe, pois, a sabedoria. Armazena suavidade para o amanhã.” – Leonardo da Vinci")
    
    @discord.ui.button(label="Frase III", style=discord.ButtonStyle.blurple)    
    async def frase3(self, interaction: discord.Integration, button: discord.ui.Button, ):
        await interaction.response.send_message("“Tente mover o mundo – o primeiro passo será mover a si mesmo.” – Platão")
    
    @discord.ui.button(label="Frase IV", style=discord.ButtonStyle.gray)
    async def frase4(self, interaction: discord.Integration, button: discord.ui.Button, ):
        await interaction.response.send_message("“Não se pode pisar duas vezes no mesmo rio.” – Heráclito")
    
    @discord.ui.button(label="Frase V", style=discord.ButtonStyle.red)
    async def frase5(self, interaction: discord.Integration, button: discord.ui.Button, ):
        await interaction.response.send_message("“Ter fé é assinar uma folha em branco e deixar que Deus nela escreva o que quiser.” – Santo Agostinho")

@bot.command()
async def frases(ctx):
    view = Frases()
    await ctx.reply(view=view)


#Embed da seção !help, foi dessabilitado !help nativo e incluido um novo com mais detalhes e personalização.
@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title='Comandos do Godofredo o robô',
        description='Bem vindo a seção de Ajuda, aqui estão os meus comandos!!',
        color=discord.Colour.red()
    )
    embed.set_thumbnail(url='https://abrir.link/i0gJH')

    embed.add_field(
        name='!regras',
        value='Lista com as regras do servidor. (Não requer argumento)',
        inline=False
    )

    embed.add_field(
        name='!entrar - !sair - !play',
        value='Comando para o bot entrar no chat, sair e tocar uma música. (Necessário entrar em um chat de voz)',
        inline=False
    )

    embed.add_field(
        name='!calcular',
        value='Calculadora (Requer argumento, ex: 4 * 3 + 8)',
        inline=False
    )    

    embed.add_field(
        name='!frases',
        value='Lista de frases disponíveis. (Não requer argumento)',
        inline=False
    )

    embed.add_field(
        name='!oi',
        value='Enviar um oi para o bot. (Não requer argumento)',
        inline=False
    )

    embed.add_field(
        name='!privado',
        value='Recebe uma mensagem no privado. (Não requer argumento)',
        inline=False
    )

    embed.add_field(
        name='!google',
        value='faz uma pequisa no google com a frase. (Requer argumento: ex !google + frase)',
        inline=False
    )
    embed.add_field(
        name='!youtube',
        value='faz uma pesquisa no youtube com a frase. (Requer argumento: ex !youtube + frase)',
        inline=False
    )

    embed.add_field(
        name='!help',
        value='Informa os comandos disponíves. (Não requer argumento)',
        inline=False
    )
    
    await ctx.send(embed=embed)

#loop de mensagem a cada 30 minutos com data e horário atual e informação sobre o !help
@tasks.loop(seconds=1800)
async def current_time():
    now = datetime.datetime.now()
    now = now.strftime("%d/%m/%Y às %H:%M:%S")
    channel = bot.get_channel(1025003694409908269)    
    await channel.send("Data atual: " + now + " --- Digite !help para saber todos os meus comandos!")


TOKEN = config("TOKEN")  
bot.run(TOKEN)