from ..library import Cog, command, Context, deps, Member, Embed, Colour, Container, MessageFlags, ActionRow, Button, TextDisplay, MessageInteraction, ButtonStyle, Message

class SellItem(Cog):
    searches: dict[int, tuple[deps.Search | deps.ShopItem, int, int, Member]] = {}
        
    async def on_error(self, message: Message, embed: Embed, membed_id: int):
        await message.reply(embed=embed)
        self.searches.pop(member_id, None)
        
    async def on_success(self, m, item: deps.ShopItem, author_id):
        _, count, price, member = self.searches[author_id]
        try:
            await member.send(components=[
                Container(
                    TextDisplay('# Запрос на покупку!'),
                    TextDisplay(f'Пользователь <@{author_id}> ({author_id}) хочет, чтобы вы приобрели у него {count} штук предмета {item.name} за {deps.bamount(price)}{deps.Currency(deps.MAIN_CURRENCY_ID).symbol} ({deps.bamount(int(price / count))}{deps.Currency(deps.MAIN_CURRENCY_ID).symbol} за единицу)'),
                    ActionRow(
                        Button(label='Принять', style=ButtonStyle.green, custom_id=f'SellItem accept {author_id}'),
                        Button(label='Отказать', style=ButtonStyle.red, custom_id=f'SellItem decline {author_id}')
                    )
                )
            ], flags=MessageFlags(is_components_v2=True))
            self.searches[author_id] = (item, count, price, member)
            await m.channel.send(embed=Embed(
                title='Успешно!',
                description='Сообщение было успешно доставлено, ожидайте ответа',
                color=Colour.green()
            ))
        except:
            await m.channel.send(embed=Embed(
                title='Ошибка',
                description='По какой-то причине сообщение не было доставлено',
                color=Colour.red()
            ))
    
    @command('sell-item')
    async def sell_item(self, ctx: Context, member: Member, count: int, price_raw: str, *, item_name: str = ''):
        author_inventory = [item.item for item in ctx.author.get_inventory().values() if (item.amount >= count) and item_name.lower().strip() in item.item.name.lower()]
        price_raw = price_raw.replace(',', '')
        price = int(price_raw.split('e')[0]) * 10 ** int(price_raw.split('e')[1]) if 'e' in price_raw else int(price_raw)
        
        if member.id == ctx.author.id:
            return await ctx.send(embed=Embed(
                title='Ошибка',
                description='Вы не можете продавать вещи самому себе',
                color=Colour.red()
            ))
        
        if count <= 0:
            return await ctx.send(embed=Embed(
                title='Ошибка',
                description='Количество передаваемых предметов не может быть меньше или равно нулю',
                color=Colour.red()
            ))
        if price <= 0:
            return await ctx.send(embed=Embed(
                title='Ошибка',
                description='Вы не можете указать цену меньше или равную нулю. Для передачи денег используйте `!pay` а для доставки предмета используйте `!give`',
                color=Colour.red()
            ))
        
        if len(author_inventory) == 0:
            return await ctx.send(embed=Embed(
                title='Ошибка',
                description='Предмета с таким названием нет, либо его недостаточно в вашем инвентаре',
                color=Colour.red()
            ))
        
        self.searches[ctx.author.id] = (author_inventory[0], count, price, member)
        if len(author_inventory) == 1:
            await self.on_success(ctx, author_inventory[0], ctx.author.id)
        else:
            success = deps.EventHandler(coro_event=self.on_success)
            error = deps.EventHandler(coro_event=self.on_error)
            items_map = {item.name: item for item in author_inventory}
            s = deps.Search('Поиск предмета', items_map, ctx.author.id, success, error)
            self.searches[ctx.author.id] = (s, count, price, member)
            await s.send_label(ctx)
            
    @Cog.listener('on_message')
    async def sell_item_messaegs(self, m):
        for s_arr in self.searches.values():
            if isinstance(s_arr[0], deps.Search):
                await s_arr[0].on_message_handler(m)
            
    @Cog.listener('on_button_click')
    async def accept_deccept_handler(self, interaction: MessageInteraction):
        data = interaction.data.custom_id
        if not data and not data.startswith('SellItem'): return
            
        data_splited = data.split()
        author = await deps.main_guild.fetch_member(int(data_splited[2]))
        
        if data_splited[1] == 'accept':
            item, count, price, member = self.searches[author.id]
            member_balance = interaction.author.get_balance()
            member_inv = interaction.author.get_inventory()
            author_balance = author.get_balance()
            author_inv = author.get_inventory()
            if not deps.MAIN_CURRENCY_ID in member_balance:
                member_balance[deps.MAIN_CURRENCY_ID] = 0
            if member_balance[deps.MAIN_CURRENCY_ID].amount < price:
                return await interaction.response.send_message('У вас недостаточно денежных средств', ephemeral=True)
            if not item.id in author_inv or author_inv[item.id].amount < count:
                return await interaction.response.send_message('У владельца предложения недостаточно предметов', ephemeral=True)
            member_balance[deps.MAIN_CURRENCY_ID] -= price
            member_inv[item.id] = (member_inv[item.id].amount if item.id in member_inv else 0) + count
            
            author_balance[deps.MAIN_CURRENCY_ID] = (author_balance[deps.MAIN_CURRENCY_ID].amount if deps.MAIN_CURRENCY_ID in author_balance else 0) + price
            author_inv[item.id] -= count
            
            await interaction.response.defer(with_message=False)
            await interaction.author.send(f'Вы успешно получили {count} шт. {item.name} за {deps.bamount(price)}{deps.Currency(deps.MAIN_CURRENCY_ID).symbol}')
            await author.send(f'{member.mention} ({member.id}) принял ваше предложение. Вы отдали {count} шт. {item.name} и получили {deps.bamount(price)}{deps.Currency(deps.MAIN_CURRENCY_ID).symbol}')
            await interaction.message.delete()
        
        elif data_splited[1] == 'decline':
            _, _, _, member = self.searches[author.id]
            await interaction.message.delete()
            await author.send(f'{member.mention} ({member.id}) отказался от вашего предложения')
        
        self.searches.pop(author.id, None)
                
            