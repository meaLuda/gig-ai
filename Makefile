build_image:
	docker build --tag gigai .

run_image: build_image
	docker run -d -it -p 8080:8000 gigai