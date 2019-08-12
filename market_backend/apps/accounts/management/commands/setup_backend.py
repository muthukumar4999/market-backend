import os

from django.core.management.base import BaseCommand

from market_backend.apps.accounts.models import User, Category, SubCategory, Media
from market_backend.env_dir.base import BASE_DIR


class Command(BaseCommand):
    base_path = BASE_DIR
    setup_path = os.path.abspath(os.path.dirname(__file__)) + '/setup/'
    help = 'Builds the Market backend pre-defined data\n' \
           'Process List:\n\r' \
           '1 - setup_admin_user\n\r'

    def setup_admin_user(self):
        username = 'admin'
        password = 'Test@123'
        u = User(username=username)
        u.set_password(password)
        u.is_superuser = True
        u.is_staff = True
        u.is_active = True
        u.user_type = User.ADMIN
        u.save()
        print(f"created a super user with username = {username}, password= {password}")

    def setup_category_data(self):
        DATA = {
            "Electronics": {
                "Temper glass": {
                    "is_picture_available": False,
                    "p_type": True,
                    "p_color": True,
                    "type": "No(s)"
                },
                "Phone Case": {
                    "is_picture_available": False,
                    "type": "No(s)",
                    "p_type": False,
                    "p_color": False
                },
                "Mobile phone": {
                    "is_picture_available": False,
                    "p_type": True,
                    "p_color": True,
                    "type": "No(s)",
                    "is_fav": True,
                    "fav_order": 1,
                }
            },
            "Electricals": {
                "Wires": {
                    "is_picture_available": False,
                    "type": "m",
                    "p_type": False,
                    "p_color": False
                },
                "Cables": {
                    "is_picture_available": False,
                    "type": "m",
                    "p_type": False,
                    "p_color": False
                }
            },
            "Groceries": {
                "Vegetables": {
                    "is_picture_available": False,
                    "p_type": True,
                    "p_color": False,
                    "type": "Kg",
                    "is_fav": True,
                    "fav_order": 2
                },
                "Fruits": {
                    "is_picture_available": False,
                    "p_type": True,
                    "p_color": False,
                    "type": "Kg",
                    "is_fav": True,
                    "fav_order": 8
                }
            },
            "Gift items": {
                "Printed mugs": {
                    "is_picture_available": True,
                    "p_type": True,
                    "p_color": True,
                    "type": "No(s)"
                },
                "Printed pillows": {
                    "is_picture_available": True,
                    "p_type": True,
                    "p_color": True,
                    "type": "No(s)"
                },
                "Printed case": {
                    "is_picture_available": True,
                    "type": "No(s)",
                    "p_type": False,
                    "p_color": False,
                    "is_fav": True,
                    "fav_order": 3
                },
                "Printed keychains": {
                    "is_picture_available": True,
                    "type": "No(s)",
                    "p_type": False,
                    "p_color": False
                },
                "Others": {
                    "is_picture_available": True,
                    "type": "No(s)",
                    "p_type": False,
                    "p_color": True
                }
            },
            "Spare parts": {
                "Engine oil": {
                    "is_picture_available": False,
                    "type": "l",
                    "p_type": False,
                    "p_color": False,
                    "is_fav": True,
                    "fav_order": 7
                },
                "Coolent oil": {
                    "is_picture_available": False,
                    "type": "l",
                    "p_type": False,
                    "p_color": False
                },
                "Break pad": {
                    "is_picture_available": False,
                    "type": "No(s)",
                    "p_type": False,
                    "p_color": False
                },
                "Tyre": {
                    "is_picture_available": False,
                    "type": "No(s)",
                    "p_type": False,
                    "p_color": False
                },
                "Tube": {
                    "is_picture_available": False,
                    "type": "No(S)",
                    "p_type": False,
                    "p_color": False
                }
            },
            "Security": {
                "CCTV Cameras": {
                    "is_picture_available": False,
                    "type": "No(s)",
                    "p_type": False,
                    "p_color": False,
                    "is_fav": True,
                    "fav_order": 4
                },
                "Fire extinguisher": {
                    "is_picture_available": False,
                    "type": "No(s)",
                    "p_type": False,
                    "p_color": False
                }
            },
            "Kids Item": {
                "Toys": {
                    "is_picture_available": False,
                    "type": "No(s)",
                    "p_type": False,
                    "p_color": False,
                    "is_fav": True,
                    "fav_order": 5
                }
            }
        }

        Category.objects.all().delete()
        Media.objects.all().delete()
        for data in DATA.keys():
            media = Media(key=f'{data}.png',
                          file_name=f'{data}.png')
            media.save()
            c = Category(name=data,
                         image=media)
            c.save()
            for s_c in DATA[data]:
                media = Media(key=f'{s_c}.png',
                              file_name=f'{s_c}.png')
                media.save()
                SubCategory(
                    name=s_c,
                    category=c,
                    image=media,
                    unit=DATA[data][s_c]['type'],
                    is_picture_available=DATA[data][s_c]['is_picture_available'],
                    is_type_available=DATA[data][s_c]['p_type'],
                    is_color_available=DATA[data][s_c]['p_color'],
                    is_fav=DATA[data][s_c].get('is_fav', False),
                    fav_order=DATA[data][s_c].get('fav_order', 0),
                ).save()

    def add_arguments(self, parser):
        parser.add_argument('-o', '--only', nargs='+', type=int, help="Only run the particular process")
        parser.add_argument('-n', '--not', nargs="+", type=int, help="Not include the the particular process")

    def handle(self, *args, **options):
        BUILD_DATA = {
            1: self.setup_admin_user,
            2: self.setup_category_data,
        }

        if options['only']:
            print("Running for only {} \n".format(options['only']))
            for process_id in options['only']:
                print("Started '{} - {}' process".format(process_id, BUILD_DATA[process_id].__name__))
                try:
                    BUILD_DATA[process_id]()
                    print("Completed '{} - {}' process".format(process_id, BUILD_DATA[process_id].__name__))
                except Exception as e:
                    print(
                        "Error Occurred in '{} - {}' process - {}".format(process_id, BUILD_DATA[process_id].__name__,
                                                                          e))
                print("\n")
        else:
            skip_list = options['not'] if options['not'] else []
            for key, process in BUILD_DATA.items():
                if key not in skip_list:
                    print("Started '{} - {}' process....".format(key, process.__name__))
                    try:
                        process()
                        print("Completed '{} - {}' process.".format(key, process.__name__))
                    except Exception as e:
                        print("Error Occurred in '{} - {}' process - {}".format(key, process.__name__, str(e)))
                    print('\n')
        print('Completed Backend Setup')
