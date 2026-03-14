import discord
from discord import app_commands
import api
import config


async def anime_autocomplete(interaction: discord.Interaction, current: str):
    animes = await api.fetch_animes()
    results = []
    current_lower = current.lower()

    for anime in animes:
        name_match = current_lower in anime['name'].lower()
        romaji_match = anime.get('romaji') and current_lower in anime['romaji'].lower()

        if name_match or romaji_match:
            if anime.get('romaji'):
                display_name = f"{anime['name']} ({anime['romaji']})"
            else:
                display_name = anime['name']

            if len(display_name) > 100:
                display_name = display_name[:97] + "..."

            results.append(discord.app_commands.Choice(name=display_name, value=anime['id']))

        if len(results) >= 25:
            break

    return results


async def show_entry_embed(interaction, anime_data, entries, season=None):
    fansubs = await api.fetch_fansubs()
    id_to_name = {f['id']: f['name'] for f in fansubs}

    if season is not None:
        filtered_entries = [e for e in entries if e['anime'] == anime_data['id'] and e['season'] == season]
    else:
        filtered_entries = [e for e in entries if e['anime'] == anime_data['id']]

    anilist_info = None
    if anime_data.get('anilist_id'):
        try:
            anilist_info = await api.fetch_anilist_data(int(anime_data['anilist_id']))
        except Exception as e:
            print(f"Error fetching AniList info: {e}")

    title = anime_data['name']
    year = ''
    poster_url = None

    if anilist_info:
        title = anilist_info['title'].get('romaji') or anilist_info['title'].get('english') or title
        year = anilist_info['startDate'].get('year')
        poster_url = anilist_info['coverImage'].get('large')

    title_embed = f"{title} ({year if year else 'Year N/A'})"

    is_movie_type = any(e.get('type', '').lower() == 'movie' for e in filtered_entries)

    if is_movie_type:
        season_text = "Movie"
    elif season is not None and season != 0:
        season_text = f"Season {season}"
    elif season == 0:
        season_text = "Special"
    else:
        season_text = ""

    if season_text:
        title_embed += f" - {season_text}"

    short_id = api.generate_short_id(str(anime_data['id']))

    embed = discord.Embed(
        title=title_embed,
        url=f"{config.DATAFANSUB_URL}/#{short_id}",
        color=config.BOT_COLOR
    )

    if poster_url:
        embed.set_thumbnail(url=poster_url)

    if filtered_entries:
        desc = ""
        for entry in filtered_entries:
            fansubs_names = [id_to_name.get(fid, fid) for fid in entry.get('fansub', [])]
            fansubs_str = ", ".join(fansubs_names) if fansubs_names else "N/A"
            desc += (
                f"**Fansub:** {fansubs_str}\n"
                f"**Status:** {entry.get('status', 'N/A')}\n"
                f"**Source:** {entry.get('source', 'N/A')}\n"
                f"**Spanish variant:** {entry.get('spanish_variant', 'N/A')}\n"
            )

            nyaa_link = entry.get('nyaa')
            nekobt_link = entry.get('nekobt')

            if nyaa_link:
                desc += f"[Nyaa]({nyaa_link}) "
            if nekobt_link:
                desc += f"[NekoBT]({nekobt_link})"

            desc += "\n\n"

        embed.description = desc
    else:
        embed.description = "No entries data available for this season or movie."

    try:
        await interaction.response.send_message(embed=embed)
    except discord.errors.InteractionResponded:
        await interaction.edit_original_response(embed=embed)


@app_commands.autocomplete(anime=anime_autocomplete)
@app_commands.command(name="datafansub", description="Search an anime on DataFansub")
async def datafansub(interaction: discord.Interaction, anime: str):
    animes = await api.fetch_animes()
    entries = await api.fetch_entries()

    selected = next((a for a in animes if a['id'] == anime), None)

    if not selected:
        await interaction.response.send_message("Anime not found.", ephemeral=True)
        return

    anime_entries = [e for e in entries if e['anime'] == selected['id']]
    is_movie = any(e.get('type', '').lower() == "movie" for e in anime_entries)

    if is_movie:
        await show_entry_embed(interaction, selected, anime_entries, season=0)
        return

    seasons_for_anime = sorted(set(e['season'] for e in anime_entries))

    if not seasons_for_anime:
        await interaction.response.send_message("No seasons available for this anime.", ephemeral=True)
        return

    options = []
    for season in seasons_for_anime:
        if season == 0:
            label = "Special"
        else:
            label = f"Season {season}"
        options.append(discord.SelectOption(label=label, value=str(season)))

    class SeasonSelect(discord.ui.Select):
        def __init__(self):
            super().__init__(placeholder="Select season...", min_values=1, max_values=1, options=options)

        async def callback(self, interaction: discord.Interaction):
            season_selected = int(self.values[0])
            await show_entry_embed(interaction, selected, anime_entries, season_selected)

    class SeasonView(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.add_item(SeasonSelect())

    await interaction.response.send_message(f"Select season for **{selected['name']}**:", view=SeasonView(), ephemeral=True)


@app_commands.command(name="ping", description="Ping the bot and show latency")
async def ping(interaction: discord.Interaction):
    latency_ms = interaction.client.latency * 1000
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Latency is approximately **{latency_ms:.2f} ms**.",
        color=config.BOT_COLOR
    )
    await interaction.response.send_message(embed=embed)


@app_commands.command(name="help", description="Shows the list of available commands")
async def help_command(interaction: discord.Interaction):
    commands_info = [
        ("/datafansub", "Search for an anime on DataFansub."),
        ("/ping", "Show the bot's latency."),
    ]

    embed = discord.Embed(
        title="Available Commands",
        description="Here are the commands you can use:",
        color=config.BOT_COLOR
    )

    for name, desc in commands_info:
        embed.add_field(name=name, value=desc, inline=False)

    await interaction.response.send_message(embed=embed, ephemeral=True)