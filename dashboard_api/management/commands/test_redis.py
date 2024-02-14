from django.core.management.base import BaseCommand
from redis import Redis


class Command(BaseCommand):
    help = "Check if connection to redis can be established."

    def handle(self, *args, **options):
        self.try_connect_to_redis()
    
    def try_connect_to_redis(self):
        self.stdout.write('Testing connection to Redis ...')

        try:
            redis_client = Redis(host="localhost", port=6379, db=0)

            test_key = "kaizntree-backend-redis-test-key"
            test_value = "      ... successful."

            redis_client.set(test_key, test_value)

            fetched_value = redis_client.get(test_key).decode('utf-8')
            redis_client.delete(test_key)

            if fetched_value == test_value:
                print(fetched_value)
            else:
                print("      ... OOPS, it looks like we have a big problem.")
            
            self.stdout.write('Redis is up and functional.')
        except Exception as e:
            print('Error connecting to Redis:', e)
