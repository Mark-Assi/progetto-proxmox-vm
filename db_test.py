from utils.database import create_request, get_all_requests

create_request(1, 'Bronze')

for r in get_all_requests():
    print(r)