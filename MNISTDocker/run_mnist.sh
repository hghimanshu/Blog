# docker rm veh_docker
docker run -it -d --runtime=nvidia --name=mnist_docker_container -v /home/himanshu/Himanshu/Blog/MnistDocker:/home/MnistDocker --network=host docker_containerized_mnist