up:
	docker-compose up
up_bg:
	docker-compose up -d
down:
	docker-compose down
build:
	docker-compose build
web:
	docker-compose exec web bash
db:
	docker-compose exec db psql --username=postgres --dbname=postgres
test:
	docker-compose -f docker-compose.test.yml up --abort-on-container-exit
test_down:
	docker-compose -f docker-compose.test.yml down
.PHONY: up up_bg down build web db test test_down
