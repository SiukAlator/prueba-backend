system-up:
	docker run -it -p 80:80 scraper-system

system-ini:
	make system-install
	make system-up

system-reset:
	make system-down
	make system-up

system-down:
	docker rm -f scraper-system

system-install:
	docker build -t scraper-system .
