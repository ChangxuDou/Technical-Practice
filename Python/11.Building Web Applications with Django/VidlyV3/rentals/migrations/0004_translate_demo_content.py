from django.db import migrations
import re

# Exact matches for the built-in catalog and demonstration text. User edits stay intact.
KNOWN_TEXT = {'来自未来的追杀者抵达洛杉矶。一场关于命运、机器与人类生存的追逐就此展开。': 'A killer from the future arrives in Los Angeles, setting '
                                         'off a relentless chase that will decide the fate of '
                                         'humanity.',
 '一艘驶向新世界的巨轮，让两个不同阶层的年轻人相遇。在命运转折之前，他们选择勇敢相爱。': 'Two young people from different worlds meet aboard '
                                               'an ocean liner. Before disaster strikes, they '
                                               'choose a love beyond social boundaries.',
 '一个家族的权力、责任与代价。迈克尔逐渐走进自己曾经拒绝的世界。': 'Power, loyalty and the cost of family. Michael is drawn into '
                                    'the world he once tried to leave behind.',
 '哥谭的秩序受到挑战。当混乱成为武器，守护城市的人必须面对艰难的选择。': 'Gotham faces a new threat. As chaos becomes a weapon, its '
                                       'protector must decide what he is willing to sacrifice.',
 '如果眼前的世界并不真实，你是否愿意醒来？一次选择，让尼奥踏上寻找真相的旅程。': 'If the world around you were an illusion, would you '
                                           'choose to wake up? One decision sends Neo in search of '
                                           'the truth.',
 '少女千寻误入神灵的世界。在陌生的汤屋里，她学会勇气、独立，以及记住自己的名字。': 'Chihiro enters a world of spirits. Working in a '
                                            'mysterious bathhouse, she learns courage, '
                                            'independence and the importance of remembering who '
                                            'she is.',
 '年轻探员向一位危险的囚犯寻求线索。每一次对话，都在逼近真相与人心的边界。': 'A young FBI trainee seeks clues from a dangerous '
                                         'prisoner. Each conversation brings her closer to the '
                                         'truth and deeper into the human mind.',
 '一个始终真诚的人，走过时代的喧嚣。他的人生告诉我们，简单的坚持也能拥有非凡的力量。': 'An earnest man moves through extraordinary times, '
                                              'showing how kindness and quiet determination can '
                                              'shape a remarkable life.',
 '几段交错的洛杉矶故事，把偶然、黑色幽默与意想不到的转折连接在一起。': 'Intersecting stories in Los Angeles bring together chance '
                                      'encounters, dark humour and unexpected turns.',
 '潜入梦境的团队接到一个特殊任务：植入一个念头。当梦层层展开，现实的边界开始松动。': 'A team of dream infiltrators must plant an idea. As '
                                             'the dream deepens, the boundary between imagination '
                                             'and reality begins to blur.',
 '一位失眠的上班族遇见神秘的陌生人。寻找出口的过程，逐渐失去控制。': 'An office worker with insomnia meets a mysterious stranger. '
                                     'Their search for an escape soon spirals out of control.',
 '从将军到角斗士，他在竞技场中寻找尊严，也迎来与旧日命运的最后对决。': 'A general becomes a gladiator, fighting for dignity in the '
                                      'arena and a final reckoning with his past.',
 '一支小队深入战场，寻找一个士兵。漫长的任务中，每个人都在思考生命与责任的重量。': 'A squad crosses a war zone to find one soldier. Along '
                                            'the way, its members confront the weight of duty and '
                                            'the value of a life.',
 '当地球不再适合生存，一支探索队穿越虫洞，寻找人类的新家园。时间、引力与爱，在星海深处交汇。': 'With Earth becoming uninhabitable, explorers '
                                                  'travel through a wormhole to find a new home. '
                                                  'Time, gravity and love meet among the stars.',
 '初次相遇 · 租金 9 折': 'Welcome · 10% off rental fees',
 '演示店长': 'Demo manager',
 '演示收银员': 'Demo cashier',
 'Alex · 演示客户': 'Alex · Demo customer',
 '已创建采购单，等待到货验收。': 'Purchase order created. Awaiting delivery and inspection.',
 '电影已验收入库，可以前往电影馆租借。': 'This movie has arrived and is now available in the catalog.',
 '想看这部关于语言与时间的科幻电影。': 'I would like to watch this science-fiction film about language and time.',
 '首批两份已验收': 'The first two copies have been inspected.',
 '演示电影供应商': 'Demo film supplier'}


def translate_existing(apps, schema_editor):
    alias = schema_editor.connection.alias
    Group = apps.get_model('auth', 'Group')
    User = apps.get_model('auth', 'User')
    for old_name, new_name in [('店长', 'Manager'), ('收银员', 'Cashier')]:
        old = Group.objects.using(alias).filter(name=old_name).first()
        if old is None:
            continue
        new = Group.objects.using(alias).filter(name=new_name).first()
        if new is None:
            old.name = new_name
            old.save(using=alias, update_fields=['name'])
        else:
            new.permissions.add(*old.permissions.all())
            for user in User.objects.using(alias).filter(groups=old):
                user.groups.add(new)
            old.delete(using=alias)
    fields = [('movies','Movie','synopsis'), ('rentals','Customer','full_name'),
              ('rentals','Coupon','name'), ('rentals','MovieWish','manager_note'),
              ('rentals','WishRequest','note'), ('rentals','StockReceipt','note'),
              ('rentals','PurchaseOrder','supplier')]
    for app, model, field in fields:
        Model = apps.get_model(app, model)
        for old, new in KNOWN_TEXT.items():
            Model.objects.using(alias).filter(**{field:old}).update(**{field:new})
    Ledger = apps.get_model('rentals','Ledger')
    for entry in Ledger.objects.using(alias).all().iterator():
        text = entry.note
        if re.fullmatch(r'顾客模拟支付 [0-9a-f-]{36}',text):
            text = text.replace('顾客模拟支付','Customer simulated payment')
        elif re.fullmatch(r'VL[0-9]+ 归还结算',text):
            text = text.replace('归还结算','Return settlement')
        if text != entry.note:
            Ledger.objects.using(alias).filter(pk=entry.pk).update(note=text)
    PointsEntry = apps.get_model('rentals','PointsEntry')
    for entry in PointsEntry.objects.using(alias).all().iterator():
        text = entry.note
        match = re.fullmatch(r'充值赠送：每 €([0-9.]+) 得 ([0-9]+) 积分',text)
        if match:
            text = f'Top-up reward: every €{match[1]} awards {match[2]} points'
        elif text == '余额退款：按原充值赠送积分比例累计扣回':
            text = 'Balance refund: original top-up rewards reversed proportionally'
        if text != entry.note:
            PointsEntry.objects.using(alias).filter(pk=entry.pk).update(note=text)


class Migration(migrations.Migration):
    dependencies = [('rentals','0003_english_interface'), ('movies','0005_english_interface')]
    operations = [migrations.RunPython(translate_existing, migrations.RunPython.noop)]
