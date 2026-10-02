import json
from pathlib import Path
from decimal import Decimal
from django.conf import settings
from django.core.management.base import BaseCommand,CommandError
from django.contrib.auth.models import User,Group,Permission
from django.db import transaction
from movies.models import Genre,Movie
from rentals.models import Customer,Coupon

DETAILS={
1:('terminator','James Cameron',107,'A killer from the future arrives in Los Angeles, setting off a relentless chase that will decide the fate of humanity.'),
2:('titanic','James Cameron',194,'Two young people from different worlds meet aboard an ocean liner. Before disaster strikes, they choose a love beyond social boundaries.'),
3:('godfather','Francis Ford Coppola',175,'Power, loyalty and the cost of family. Michael is drawn into the world he once tried to leave behind.'),
4:('dark-knight','Christopher Nolan',152,'Gotham faces a new threat. As chaos becomes a weapon, its protector must decide what he is willing to sacrifice.'),
5:('matrix','Lana & Lilly Wachowski',136,'If the world around you were an illusion, would you choose to wake up? One decision sends Neo in search of the truth.'),
6:('spirited-away','Hayao Miyazaki',125,'Chihiro enters a world of spirits. Working in a mysterious bathhouse, she learns courage, independence and the importance of remembering who she is.'),
7:('silence','Jonathan Demme',118,'A young FBI trainee seeks clues from a dangerous prisoner. Each conversation brings her closer to the truth and deeper into the human mind.'),
8:('forrest','Robert Zemeckis',142,'An earnest man moves through extraordinary times, showing how kindness and quiet determination can shape a remarkable life.'),
9:('pulp','Quentin Tarantino',154,'Intersecting stories in Los Angeles bring together chance encounters, dark humour and unexpected turns.'),
10:('inception','Christopher Nolan',148,'A team of dream infiltrators must plant an idea. As the dream deepens, the boundary between imagination and reality begins to blur.'),
11:('fight','David Fincher',139,'An office worker with insomnia meets a mysterious stranger. Their search for an escape soon spirals out of control.'),
12:('gladiator','Ridley Scott',155,'A general becomes a gladiator, fighting for dignity in the arena and a final reckoning with his past.'),
13:('saving','Steven Spielberg',169,'A squad crosses a war zone to find one soldier. Along the way, its members confront the weight of duty and the value of a life.'),
14:('interstellar','Christopher Nolan',169,'With Earth becoming uninhabitable, explorers travel through a wormhole to find a new home. Time, gravity and love meet among the stars.'),
}
class Command(BaseCommand):
    help='Import the original catalog and create local demo accounts without resetting existing stock or passwords.'
    def add_arguments(self,parser):
        parser.add_argument('--accounts',action='store_true')
        parser.add_argument('--only-empty',action='store_true')
    @transaction.atomic
    def handle(self,*args,**options):
        if options.get('only_empty') and Movie.objects.exists():
            self.stdout.write('Movies already exist. Existing data is preserved; demo movies will not be reimported.')
            return
        data=json.loads((settings.BASE_DIR/'movies/fixtures/catalog.json').read_text())
        for pk,name in data['genres']:Genre.objects.get_or_create(pk=pk,defaults={'name':name})
        for pk,title,year,stock,rate,gid in data['movies']:
            art,director,runtime,synopsis=DETAILS[pk]
            Movie.objects.get_or_create(pk=pk,defaults={'title':title,'release_year':year,'number_in_stock':stock,'total_quantity':stock,'daily_rate':Decimal(str(rate)),'genre_id':gid,'barcode':str(1000000000+pk),'artwork':art,'director':director,'runtime':runtime,'synopsis':synopsis})
            Movie.objects.filter(pk=pk,synopsis='').update(artwork=art,director=director,runtime=runtime,synopsis=synopsis)
        Coupon.objects.get_or_create(code='WELCOME10',defaults={'name':'Welcome · 10% off rental fees','percent':10})
        manager,_=Group.objects.get_or_create(name='Manager');cashier,_=Group.objects.get_or_create(name='Cashier')
        manager.permissions.set(Permission.objects.filter(Q_FOR_MANAGER()))
        cashier.permissions.set(Permission.objects.filter(codename__in=['view_movie','view_genre']))
        if options['accounts']:
            if not settings.DEBUG:raise CommandError('Demo accounts can only be created locally with DEBUG=1.')
            for username,group,phone in [('manager',manager,'+490000000001'),('cashier',cashier,'+490000000002'),('demo',None,'+490000000003')]:
                if not User.objects.filter(username=username).exists():
                    u=User.objects.create_user(username,password='VidlyDemo!2026',is_staff=group is not None)
                    if group:u.groups.add(group)
                    Customer.objects.create(user=u,full_name={'manager':'Demo manager','cashier':'Demo cashier','demo':'Alex · Demo customer'}[username],phone=phone,email=f'{username}@example.com')
                    self.stdout.write(f'Created {username} / VidlyDemo!2026 (local demo only)')
                else:self.stdout.write(f'{username} already exists. The current password is unchanged.')
        self.stdout.write(self.style.SUCCESS('Movies, genres and coupons are ready.'))

def Q_FOR_MANAGER():
    from django.db.models import Q
    return Q(content_type__app_label='rentals',codename__in=['view_coupon','add_coupon','change_coupon','delete_coupon']) | Q(content_type__app_label='movies',codename__in=['view_genre','add_genre','change_genre','view_movie'])
